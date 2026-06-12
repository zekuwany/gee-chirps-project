# Rainfall Climatology Analysis with Google Earth Engine

## Overview

This project demonstrates **cloud-based geospatial analysis** by computing long-term monthly rainfall climatology using the [CHIRPS](https://www.chc.ucsb.edu/data/chirps) (Climate Hazards Group InfraRed Precipitation with Station data) daily precipitation dataset via the Google Earth Engine Python API.

The analysis computes the **average number of rainy days per month** over a 42-year period (1981–2023) for a custom area of interest, producing publication-quality raster maps that reveal seasonal precipitation patterns.

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

## Medium posts
- [Analyzing 42 Years of Rainfall Data Using Google Earth Engine](https://medium.com/@linh-ktran/analyzing-chirps-rainfall-data-using-google-earth-engine-bb4901ca29b7)

## References

- Funk, C., et al. (2015). The climate hazards infrared precipitation with stations — a new environmental record for monitoring extremes. *Scientific Data*, 2, 150066.
- [Google Earth Engine Documentation](https://developers.google.com/earth-engine)
- [CHIRPS Data Portal](https://www.chc.ucsb.edu/data/chirps)

---

<p align="center">
  <i>Built with Google Earth Engine & Python</i>
</p>
