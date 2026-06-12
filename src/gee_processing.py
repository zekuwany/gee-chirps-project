"""Google Earth Engine helper functions for CHIRPS rainfall analysis."""

import ee


def load_chirps(start_year: int, end_year: int) -> ee.ImageCollection:
    """Load CHIRPS daily precipitation ImageCollection for a date range."""
    start_date = ee.Date.fromYMD(start_year, 1, 1)
    end_date = ee.Date.fromYMD(end_year, 12, 31)
    return ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY").filterDate(start_date, end_date)


def create_rainy_day_mask(image: ee.Image, threshold: float = 0) -> ee.Image:
    """Create a binary mask where 1 = rainy day (precip > threshold)."""
    rainy_day = image.select("precipitation").gt(threshold)
    return image.addBands(rainy_day.rename("rainy_day"))


def compute_monthly_rainy_days(
    rainy_collection: ee.ImageCollection,
    years: ee.List,
    months: ee.List,
) -> ee.ImageCollection:
    """Compute total rainy days per month per year via nested server-side mapping."""

    def yearly_monthly_sum(year):
        def monthly_sum(month):
            total = (
                rainy_collection
                .filter(ee.Filter.calendarRange(year, year, "year"))
                .filter(ee.Filter.calendarRange(month, month, "month"))
                .sum()
            )
            return total.set({
                "year": year,
                "month": month,
                "system:time_start": ee.Date.fromYMD(year, month, 1),
            })
        return months.map(monthly_sum)

    return ee.ImageCollection.fromImages(years.map(yearly_monthly_sum).flatten())


def compute_climatology(
    monthly_rainy_days: ee.ImageCollection,
    months: ee.List,
) -> ee.ImageCollection:
    """Average monthly totals across all years to produce a 12-image climatology."""

    def monthly_mean(month):
        clim = monthly_rainy_days.filter(ee.Filter.eq("month", month)).mean().round()
        return clim.set({"month": month, "system:time_start": ee.Date.fromYMD(2000, month, 1)})

    return ee.ImageCollection.fromImages(months.map(monthly_mean))


def clip_collection(collection: ee.ImageCollection, aoi) -> ee.ImageCollection:
    """Clip every image in a collection to an area of interest."""
    return collection.map(lambda img: img.clip(aoi))


def extract_monthly_values(collection: ee.ImageCollection, band_name: str, aoi) -> list:
    """Extract 12 monthly AOI-average values from a climatology collection."""
    coll_list = collection.toList(12)
    values = []
    for i in range(12):
        img = ee.Image(coll_list.get(i))
        mean_val = (
            img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=aoi.geometry(),
                scale=5566,
                maxPixels=1e9,
            )
            .get(band_name)
            .getInfo()
        )
        values.append(mean_val if mean_val else 0)
    return values


def compute_annual_rainy_days(
    rainy_collection: ee.ImageCollection,
    years: ee.List,
) -> ee.ImageCollection:
    """Compute total rainy days per year."""

    def annual_sum(year):
        total = (
            rainy_collection
            .filter(ee.Filter.calendarRange(year, year, "year"))
            .sum()
        )
        return total.set({"year": year, "system:time_start": ee.Date.fromYMD(year, 1, 1)})

    return ee.ImageCollection.fromImages(years.map(annual_sum))


def extract_annual_values(
    annual_collection: ee.ImageCollection,
    n_years: int,
    aoi,
) -> list:
    """Extract annual AOI-average rainy day values."""
    annual_list = annual_collection.toList(annual_collection.size())
    stats = []
    for i in range(n_years):
        img = ee.Image(annual_list.get(i))
        mean_val = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=aoi.geometry(),
            scale=5566,
            maxPixels=1e9,
        ).get("rainy_day")
        stats.append(mean_val)
    return ee.List(stats).getInfo()


def compute_threshold_climatology(
    chirps: ee.ImageCollection,
    thresholds: dict,
    aoi,
    days_in_month: list,
) -> dict:
    """Compute average days per month for each precipitation threshold.

    Uses a memory-efficient approach: computes the probability of a threshold day
    (mean of binary values) then multiplies by days-in-month.

    Parameters
    ----------
    chirps : ee.ImageCollection
        CHIRPS daily precipitation collection.
    thresholds : dict
        e.g. {'light': (0, 5), 'moderate': (5, 20), 'heavy': (20, None)}
    aoi : ee.FeatureCollection
        Area of interest.
    days_in_month : list of float
        Average days per calendar month (length 12).

    Returns
    -------
    dict
        {threshold_name: [12 monthly avg day values]}
    """
    results = {}

    for name, (lower, upper) in thresholds.items():
        monthly_means = []
        for m in range(1, 13):
            month_chirps = chirps.filter(ee.Filter.calendarRange(m, m, "month"))

            if upper is not None:
                prob_image = month_chirps.map(
                    lambda img, lo=lower, up=upper: img.select("precipitation")
                    .gt(lo)
                    .And(img.select("precipitation").lte(up))
                    .rename("threshold_day")
                ).mean()
            else:
                prob_image = month_chirps.map(
                    lambda img, lo=lower: img.select("precipitation")
                    .gt(lo)
                    .rename("threshold_day")
                ).mean()

            mean_prob = (
                prob_image.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=aoi.geometry(),
                    scale=5566,
                    maxPixels=1e9,
                )
                .get("threshold_day")
                .getInfo()
            )

            avg_days = (mean_prob * days_in_month[m - 1]) if mean_prob else 0
            monthly_means.append(round(avg_days, 1))

        results[name] = monthly_means

    return results

