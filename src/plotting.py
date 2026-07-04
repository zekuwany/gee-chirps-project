"""Plotting functions for CHIRPS rainfall analysis.

All figures use a white background by default.
"""

import calendar

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap

# ---------------------------------------------------------------------------
# Global style: white background for all plots
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "text.color": "black",
    "axes.labelcolor": "black",
    "axes.edgecolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
})

# Shared color palette matching GEE visualization
RAINY_DAYS_PALETTE = ["#ffffcc", "#7eccba", "#41b7c4", "#2c80b8", "#253494", "#662A00"]


def plot_monthly_rasters(tif_files, month_labels, title, output_path=None):
    """Create a multi-panel plot of monthly rainy day rasters from GeoTIFF files."""
    import rasterio

    cmap = ListedColormap(RAINY_DAYS_PALETTE)
    bounds = [0, 1, 2, 3, 4, 5, 6]
    norm = BoundaryNorm(bounds, cmap.N)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.98)

    for idx, (tif_file, month_label) in enumerate(zip(tif_files, month_labels)):
        ax = axes[idx // 3, idx % 3]
        with rasterio.open(tif_file) as src:
            data = src.read(1)
            data = np.where(data < 0, np.nan, data)
            ax.imshow(
                data,
                cmap=cmap,
                norm=norm,
                extent=[src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top],
            )
        ax.set_title(month_label, fontsize=12, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_annual_trend(years, values, mk_result, start_year, end_year, output_path=None):
    """Bar chart of annual rainy days with Sen's slope trend line."""
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(years, values, color="steelblue", alpha=0.7, label="Annual rainy days")
    ax.plot(
        years,
        mk_result.intercept + mk_result.slope * (years - years[0]),
        "r--",
        linewidth=2,
        label=f"Sen's slope: {mk_result.slope:.2f} days/year",
    )

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Total Rainy Days", fontsize=12)
    ax.set_title(
        f"Annual Rainy Day Trend ({start_year}–{end_year}) — {mk_result.trend} (p={mk_result.p:.4f})",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_monthly_trends(monthly_trends, output_path=None):
    """Bar chart of monthly Sen's slopes with significance markers."""
    fig, ax = plt.subplots(figsize=(10, 5))

    labels = [t["month"] for t in monthly_trends]
    slopes = [t["slope"] for t in monthly_trends]
    colors = ["#d73027" if s > 0 else "#4575b4" for s in slopes]
    edge_colors = ["black" if t["p_value"] < 0.05 else "none" for t in monthly_trends]

    ax.bar(labels, slopes, color=colors, edgecolor=edge_colors, linewidth=2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Sen's Slope (days/year)", fontsize=12)
    ax.set_title(
        "Monthly Rainy Day Trends (black border = significant at α=0.05)",
        fontsize=13,
        fontweight="bold",
    )
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_seasonal_distributions(monthly_distributions, start_year, end_year, output_path=None):
    """3×4 grid of monthly rainy day histograms with fitted normal curves."""
    from scipy import stats

    fig, axes = plt.subplots(3, 4, figsize=(16, 10))
    fig.suptitle(
        "Seasonal Forecast: Monthly Rainy Day Probability Distributions\n"
        f"Based on {end_year - start_year + 1} Years of Historical Data",
        fontsize=14,
        fontweight="bold",
    )

    for m in range(1, 13):
        ax = axes[(m - 1) // 4, (m - 1) % 4]
        data = monthly_distributions[m]
        mu, sigma = stats.norm.fit(data)

        ax.hist(data, bins=10, density=True, alpha=0.6, color="steelblue", edgecolor="white")
        x = np.linspace(data.min() - 1, data.max() + 1, 100)
        ax.plot(x, stats.norm.pdf(x, mu, sigma), "r-", linewidth=2)

        p50 = np.median(data)
        ax.axvline(p50, color="orange", linestyle="--", linewidth=1.5, label=f"Median: {p50:.1f}")
        ax.set_title(calendar.month_name[m], fontsize=11, fontweight="bold")
        ax.set_xlabel("Rainy Days")
        ax.legend(fontsize=8)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_threshold_stacked_bar(threshold_monthly_means, output_path=None):
    """Stacked bar chart of monthly rainy days by intensity category."""
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(12)
    width = 0.6
    bottom = np.zeros(12)

    colors_map = {"light": "#7eccba", "moderate": "#2c80b8", "heavy": "#662A00"}
    labels_map = {
        "light": "Light (0–5 mm)",
        "moderate": "Moderate (5–20 mm)",
        "heavy": "Heavy (>20 mm)",
    }

    for name in ["light", "moderate", "heavy"]:
        values = np.array(threshold_monthly_means[name])
        ax.bar(
            x, values, width, bottom=bottom,
            label=labels_map[name], color=colors_map[name],
            edgecolor="white", linewidth=0.5,
        )
        bottom += values

    ax.set_xticks(x)
    ax.set_xticklabels([calendar.month_abbr[i + 1] for i in range(12)])
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Average Days per Month", fontsize=12)
    ax.set_title(
        "Monthly Rainy Days by Intensity Category (1985–2024 Climatology)",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_dataset_comparison(chirps_monthly, era5_monthly, gpm_monthly, output_path=None):
    """Side-by-side bar chart and scatter correlation of three precipitation datasets."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    x = np.arange(12)
    width = 0.25

    ax1.bar(x - width, chirps_monthly, width, label="CHIRPS", color="#2c80b8", alpha=0.8)
    ax1.bar(x, era5_monthly, width, label="ERA5-Land", color="#d73027", alpha=0.8)
    ax1.bar(x + width, gpm_monthly, width, label="GPM IMERG", color="#4daf4a", alpha=0.8)

    ax1.set_xticks(x)
    ax1.set_xticklabels([calendar.month_abbr[i + 1] for i in range(12)])
    ax1.set_xlabel("Month", fontsize=12)
    ax1.set_ylabel("Mean Daily Precipitation (mm/day)", fontsize=12)
    ax1.set_title(
        "Monthly Precipitation Climatology\nDataset Comparison (2001–2023)",
        fontsize=13,
        fontweight="bold",
    )
    ax1.legend(fontsize=11)
    ax1.grid(axis="y", alpha=0.3)

    # Scatter
    ax2.scatter(chirps_monthly, era5_monthly, s=80, c="#d73027", label="ERA5 vs CHIRPS", zorder=5)
    ax2.scatter(chirps_monthly, gpm_monthly, s=80, c="#4daf4a", marker="^", label="GPM vs CHIRPS", zorder=5)

    max_val = max(max(chirps_monthly), max(era5_monthly), max(gpm_monthly))
    ax2.plot([0, max_val], [0, max_val], "k--", alpha=0.5, label="1:1 line")

    r_era5 = np.corrcoef(chirps_monthly, era5_monthly)[0, 1]
    r_gpm = np.corrcoef(chirps_monthly, gpm_monthly)[0, 1]

    ax2.set_xlabel("CHIRPS (mm/day)", fontsize=12)
    ax2.set_ylabel("Other Dataset (mm/day)", fontsize=12)
    ax2.set_title(
        f"Dataset Correlation\nERA5 r={r_era5:.3f}, GPM r={r_gpm:.3f}",
        fontsize=13,
        fontweight="bold",
    )
    ax2.legend(fontsize=11)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.show()

    return r_era5, r_gpm

