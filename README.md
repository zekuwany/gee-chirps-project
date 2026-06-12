# 🌧️ Rainfall Climatology Analysis with Google Earth Engine

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/linh-ktran/gee-chirps-rainfall-analysis/blob/main/notebooks/rainfall_analysis.ipynb)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![GEE](https://img.shields.io/badge/Google%20Earth%20Engine-API-green.svg)](https://earthengine.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project demonstrates **cloud-based geospatial analysis** by computing long-term monthly rainfall climatology using the [CHIRPS](https://www.chc.ucsb.edu/data/chirps) (Climate Hazards Group InfraRed Precipitation with Station data) daily precipitation dataset via the Google Earth Engine Python API.

The analysis computes the **average number of rainy days per month** over a 42-year period (1981–2023) for a custom area of interest, producing publication-quality raster maps that reveal seasonal precipitation patterns.

<p align="center">
  <img src="plots/Avg_rainy_days_January_to_June.png" width="90%" alt="Average rainy days Jan-Jun"/>
</p>
<p align="center">
  <img src="plots/Avg_rainy_days_July_to_December.png" width="90%" alt="Average rainy days Jul-Dec"/>
</p>

## Key Skills Demonstrated

| Category | Skills |
|----------|--------|
| **Cloud Computing** | Google Earth Engine (GEE) server-side processing, large-scale raster computation |
| **Geospatial Analysis** | Remote sensing data processing, temporal aggregation, spatial clipping, multi-dataset comparison |
| **Python** | `earthengine-api`, `geemap`, `rasterio`, `matplotlib`, `numpy`, `scipy`, `pymannkendall` |
| **Data Engineering** | Processing 15,000+ daily raster images into monthly climatologies |
| **Statistical Analysis** | Mann-Kendall trend detection, Sen's slope estimation, probabilistic forecasting |
| **Visualization** | Interactive web maps (ipyleaflet), multi-panel raster plots with custom colormaps |

## Methodology

```mermaid
graph LR
    A[CHIRPS Daily Data<br/>1981-2023] --> B[Binary Rainy Day Mask<br/>precip > 0 mm/day]
    B --> C[Monthly Sum<br/>per year]
    C --> D[Multi-Year Average<br/>per month]
    D --> E[Clip to AOI]
    E --> F[Visualization<br/>& Export]
```

### Pipeline Steps

1. **Data Ingestion** — Load CHIRPS daily precipitation ImageCollection (1981–2023)
2. **Feature Engineering** — Create binary rainy day mask (precipitation > 0 mm/day)
3. **Temporal Aggregation** — Compute monthly rainy day totals for each year
4. **Climatology Computation** — Calculate multi-year mean for each calendar month
5. **Spatial Processing** — Clip results to the area of interest (shapefile)
6. **Visualization & Export** — Interactive maps and publication-ready raster plots
7. **Trend Analysis** — Mann-Kendall test with Sen's slope for long-term trend detection
8. **Seasonal Forecasting** — Probabilistic outlooks using historical distributions and terciles
9. **Multi-Threshold Analysis** — Light/moderate/heavy rain frequency classification
10. **Dataset Comparison** — Cross-validation against ERA5-Land and GPM IMERG

## Quick Start

### Prerequisites

- Python 3.9+
- A [Google Earth Engine account](https://signup.earthengine.google.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/linh-ktran/gee-chirps-rainfall-analysis.git
cd gee-chirps-rainfall-analysis

# Install dependencies
pip install -r requirements.txt

# Authenticate with Google Earth Engine (first time only)
earthengine authenticate
```

### Running the Analysis

```bash
# Option 1: Run in Jupyter
jupyter notebook notebooks/rainfall_analysis.ipynb

# Option 2: Open in Google Colab (no local setup needed)
# Click the "Open in Colab" badge above
```

## Technical Details

### Dataset

| Property | Value |
|----------|-------|
| **Dataset** | UCSB-CHG/CHIRPS/DAILY |
| **Temporal Coverage** | 1981–2023 (42 years) |
| **Spatial Resolution** | 0.05° (~5.5 km) |
| **Total Images Processed** | ~15,700 daily images |
| **Source** | Climate Hazards Center, UC Santa Barbara |

### Key Implementation Highlights

- **Server-side computation**: All heavy processing runs on Google's cloud infrastructure via GEE, enabling analysis of terabytes of data without local compute
- **Functional programming pattern**: Uses `map()` operations for efficient batch processing of ImageCollections
- **Nested temporal aggregation**: Two-level aggregation (monthly sum → multi-year mean) computed efficiently using GEE's lazy evaluation

## Results

The analysis reveals distinct seasonal patterns in rainfall frequency across the study area:
- **Winter months (Dec–Feb)**: Minimal rainy days (0–2 days/month)
- **Summer months (Jun–Aug)**: Peak rainfall frequency (4–6+ days/month)
- **Spatial gradient**: Clear north-south precipitation gradient driven by topography and atmospheric circulation

## Improvements

- [x] Add trend analysis (Mann-Kendall test) to detect changing rainfall patterns
- [x] Implement seasonal forecasting using historical patterns
- [x] Extend to multiple precipitation thresholds (light/moderate/heavy rain)
- [x] Add comparison with other precipitation datasets (ERA5, GPM)

## References

- Funk, C., et al. (2015). The climate hazards infrared precipitation with stations — a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066.
- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [CHIRPS Data Portal](https://www.chc.ucsb.edu/data/chirps)

---

<p align="center">
  <i>Built with Google Earth Engine & Python</i>
</p>
