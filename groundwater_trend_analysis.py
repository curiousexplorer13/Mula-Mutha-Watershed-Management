# Mula–Mutha groundwater trend analysis
import pandas as pd, numpy as np, geopandas as gpd
from scipy.stats import kendalltau

GROUNDWATER_CSV = "ground_water_level_manual_quarterly_maharashtra_1970_2025.csv"
WATERSHED_SHP = "watershed.shp"

cols = ["Well ID","Latitude ","Longitude ","Date of Monitoring","Water Level, m bgl"]
aoi = gpd.read_file(WATERSHED_SHP)
xmin,ymin,xmax,ymax = aoi.total_bounds

parts=[]
for chunk in pd.read_csv(GROUNDWATER_CSV,usecols=cols,chunksize=250000,encoding="cp1252",low_memory=False):
    lat=pd.to_numeric(chunk["Latitude "],errors="coerce")
    lon=pd.to_numeric(chunk["Longitude "],errors="coerce")
    mask=lat.between(ymin,ymax)&lon.between(xmin,xmax)
    if mask.any():
        c=chunk.loc[mask].copy()
        c["Latitude "]=lat[mask]; c["Longitude "]=lon[mask]
        parts.append(c)

cand=pd.concat(parts,ignore_index=True)
pts=gpd.GeoDataFrame(cand,geometry=gpd.points_from_xy(cand["Longitude "],cand["Latitude "]),crs="EPSG:4326")
inside=gpd.sjoin(pts,aoi[["geometry"]],predicate="within",how="inner").drop(columns="index_right")
inside["Date"]=pd.to_datetime(inside["Date of Monitoring"],dayfirst=True,errors="coerce")
inside["WL"]=pd.to_numeric(inside["Water Level, m bgl"],errors="coerce")

period=inside[(inside["Date"]>="2010-01-01")&(inside["Date"]<="2025-12-31")].copy()
annual=period.assign(year=period["Date"].dt.year).groupby(["Well ID","year"],as_index=False)["WL"].mean()

def sen_slope(x,y):
    slopes=[(y[j]-y[i])/(x[j]-x[i]) for i in range(len(x)) for j in range(i+1,len(x))]
    return float(np.median(slopes))

results=[]
for well_id,g in annual.groupby("Well ID"):
    g=g.dropna(subset=["WL"]).sort_values("year")
    if len(g)<10: continue
    x=g["year"].to_numpy(float); y=g["WL"].to_numpy(float)
    slope=sen_slope(x,y); tau,p=kendalltau(x,y)
    results.append([well_id,len(g),slope,tau,p])

trend=pd.DataFrame(results,columns=["Well ID","n_years","Sen_slope_m_per_year","Kendall_tau","p_value"])
trend["Trend"]=np.select(
    [(trend["p_value"]<0.05)&(trend["Sen_slope_m_per_year"]>0),
     (trend["p_value"]<0.05)&(trend["Sen_slope_m_per_year"]<0)],
    ["Declining","Improving"],default="No significant trend")
trend.to_csv("groundwater_trend_results_2010_2025.csv",index=False)
