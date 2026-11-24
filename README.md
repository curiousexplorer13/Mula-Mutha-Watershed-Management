# Mula–Mutha Watershed Management Project

This repository contains processed data, final report figures, and selected scripts for the CE 766 Watershed Management project on the Mula–Mutha watershed, Maharashtra.

## Repository contents

- `Data/Processed/` — analysed tables used for the reported results.
- `Figures/` — final Figure 1 and Figure 2, in PNG and PDF formats.
- `Scripts/groundwater_trend_analysis.py` — recalculates Sen's slope and Kendall's tau from the processed annual groundwater-level table.
- `Scripts/intervention_sensitivity.py` — recalculates the illustrative 0%, 1% and 2% rainfall-capture scenarios.
- `Scripts/plot_figure_2.py` — regenerates the rainfall–ET and intervention-sensitivity figure.
- `Documentation/` — notes on processing, data sources and limitations.

## Study area and periods

The study area is the Mula–Mutha watershed, Maharashtra (approximately 2,621.4 km²). The analyses cover LULC in 2010–11 and 2022–23, groundwater levels in 2010–2025, and annual rainfall and actual ET in 2010–2024.

## Main methods

1. **LULC:** NRSC/ISRO Bhuvan 1:250,000 LULC classes for 2010–11 and 2022–23 were compared over a common analysis footprint. The rasters were harmonised to a 55 m grid in WGS 84 / UTM zone 43N (EPSG:32643) using nearest-neighbour resampling. Class area and area change were summarised.
2. **Groundwater:** Quarterly manual groundwater observations were aggregated to annual well means. For 31 wells with at least 10 annual observations, Sen's slope and Kendall's tau were calculated. A p-value below 0.05 was used to identify significant trends. Positive slope in metres below ground level indicates increasing depth and therefore a declining groundwater level.
3. **Rainfall:** IMD daily 0.25° gridded rainfall was summed to annual totals and averaged spatially over the watershed using latitude weighting.
4. **Actual ET:** MODIS MOD16A2GF.061 500 m, 8-day ET was aggregated to annual totals after applying the product scale factor.
5. **Intervention screening:** Potential captured volume was estimated for assumed capture fractions of 0%, 1% and 2% of mean annual rainfall. This is a sensitivity calculation, not a calibrated intervention or groundwater-recharge model.

## Run the scripts

Install dependencies:

```bash
pip install -r requirements.txt
```

From the repository root:

```bash
python Scripts/groundwater_trend_analysis.py
python Scripts/intervention_sensitivity.py
python Scripts/plot_figure_2.py
```

The scripts write recalculated outputs into `Data/Processed/` and `Figures/`. The supplied final report figures are retained separately as the submission versions.

## Main findings represented in the figures

- Groundwater trends: 2 wells showed significant declining trends, 5 showed improving trends, and 24 showed no statistically significant trend.
- Mean annual rainfall (2010–2024): approximately 1,950.3 mm/year.
- Mean annual actual ET (2010–2024): approximately 675.7 mm/year.
- Illustrative 1% and 2% rainfall-capture scenarios: approximately 51.1 and 102.3 MCM/year, respectively.

## Data sources

- NRSC/ISRO Bhuvan: LULC 1:250,000, 2010–11 and 2022–23 — https://bhuvan.nrsc.gov.in/
- IMD daily gridded rainfall, 0.25°; see Pai et al. (2014), *MAUSAM*, 65(1), 1–18. DOI: https://doi.org/10.54302/mausam.v65i1.851
- NASA LP DAAC, MODIS MOD16A2GF.061 — https://doi.org/10.5067/MODIS/MOD16A2GF.061
- National Water Data Portal / Maharashtra Ground Water Department, manual groundwater-level dataset — https://nwdp.nwic.gov.in/
- Watershed boundary: NIH-DHAARA.

## Important limitations and interpretation

- The rainfall-minus-ET difference is a climatic surplus, **not groundwater recharge**. Runoff, lateral flows and changes in soil/water storage were not quantified, so the total water balance was not closed.
- The 1% and 2% scenarios are assumed capture fractions. They are not measured intervention efficiencies, recharge volumes or predicted groundwater-level rises.
- Intervention locations were not optimised or field-validated. Soil infiltration, slope, geology, streamflow and groundwater-abstraction data are needed for site-level decisions.
- Two-date LULC comparison does not establish causation between land-cover change and groundwater trends.
- IMD rainfall is much coarser in spatial resolution than the LULC and MODIS ET products.

## Licensing and redistribution

The original Bhuvan LULC GeoTIFFs are **not included** in this repository. Their accompanying terms identify a single-user licence and restrictions on hosting/redistribution. Obtain the data directly from the provider and follow its licence. Only derived summary tables and final visual outputs are included here. The full raw quarterly groundwater source download and original IMD/MODIS source files are also not included; users should obtain them from their respective providers.

## Reproducibility note

The included scripts reproduce the groundwater trend statistics from the supplied annual well-mean table, the intervention sensitivity table from annual rainfall, and Figure 2 from the processed climate/scenario tables. Figure 1 and the LULC summary tables are supplied as final derived outputs; the original licensed LULC rasters are not redistributed here.
