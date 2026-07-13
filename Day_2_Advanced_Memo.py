"""
Last Update:
2026-07-07
Cameron Green

day2_advanced_memo.py
======================
ANSWER MEMO for Day 2 (Advanced Track). 

Rebuilds the standard Day 2 vector/raster analysis (biome joins, per-biome
statistics, fire density, raster sampling, severity/NDVI correlation) as a
standalone Python script, in the same shape as the production fire-risk
pipeline scripts referenced throughout this workshop.

Input : Data/fire_events_clean.gpkg
        Data/bioregions.gpkg
        Data/fire_ignitions.gpkg
        Data/severity_rasters/severity_mean_summer.tif
        Data/ndvi_rasters/ndvi_summer.tif
        Data/output_SRTMGL3_slope.tif        (optional fragmentation extension)
Output: per-biome fire statistics, a fire-density ranking, and the severity/NDVI
        correlation against area_per_day — printed to the console and logged.

Run from a Python environment with geopandas + rasterio installed (the
`firerisk` conda environment set up in Day_2_Advanced.md).
"""

import os
import time
import datetime
import logging

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

# =============================================================================
# LOGGING SETUP
# =============================================================================
_script_name = "day2_advanced_memo"
_log_path = f"{_script_name}_{datetime.date.today():%Y-%m-%d}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(_log_path, mode="a", encoding="utf-8"),
    ],
)
log = logging.getLogger()

# =============================================================================
# PATHS
# =============================================================================
dataDir        = r"C:\Users\cameron.green\OneDrive - Riskscape\Documents\2026\Students Week 202607\Data"
fireEventsPath = os.path.join(dataDir, "fire_events_clean.gpkg")
bioregionsPath = os.path.join(dataDir, "bioregions.gpkg")
ignitionsPath  = os.path.join(dataDir, "fire_ignitions.gpkg")
severityTif    = os.path.join(dataDir, "severity_rasters", "severity_mean_summer.tif")
ndviTif        = os.path.join(dataDir, "ndvi_rasters", "ndvi_summer.tif")
slopeTif       = os.path.join(dataDir, "output_SRTMGL3_slope.tif")

# =============================================================================
# CONFIG
# =============================================================================
# SA Albers equal-area — used wherever a true area figure is needed (the same
# projection family the real pipeline uses for area/buffer work, for the same reason:
# EPSG:4326's $area is in square degrees, not a real-world unit).
saAlbers = ("+proj=aea +lat_1=-24 +lat_2=-33 +lat_0=-29 +lon_0=25 "
            "+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs")


# =============================================================================
# STEP 1 — Load layers and fix the bioregions CRS
# =============================================================================
def load_layers():
    fires = gpd.read_file(fireEventsPath)
    bioregions = gpd.read_file(bioregionsPath)
    ignitions = gpd.read_file(ignitionsPath)
    log.info(f"Loaded fires={len(fires):,}  bioregions={len(bioregions):,}  "
             f"ignitions={len(ignitions):,}")

    # Watch out: don't assume every layer shares one CRS just because the workshop docs
    # say so. bioregions.gpkg has come through in a projected Albers CRS in past runs of
    # this workshop, not EPSG:4326 like the fire layers. A mismatch here doesn't raise an
    # error — sjoin just quietly returns zero matches, because the two layers' coordinates
    # no longer land on the same part of the map. Always reproject explicitly.
    log.info(f"  fires CRS:      {fires.crs}")
    log.info(f"  bioregions CRS: {bioregions.crs}")
    if bioregions.crs != fires.crs:
        bioregions = bioregions.to_crs(fires.crs)
        log.info(f"  Reprojected bioregions to match fires: {bioregions.crs}")

    return fires, bioregions, ignitions


# =============================================================================
# STEP 2 — Spatial join: attach bioregion name to each fire event
# =============================================================================
def join_biome(fires, bioregions):
    joined = gpd.sjoin(
        fires, bioregions[["T_BIOME", "geometry"]],
        how="left", predicate="intersects"
    )
    log.info(f"Spatial join: {len(fires):,} fires -> {len(joined):,} rows")

    dupes = joined.index.duplicated().sum()
    if dupes:
        log.info(f"  {dupes:,} fire(s) matched more than one bioregion; keeping first match")
        joined = joined[~joined.index.duplicated(keep="first")]

    # Checkpoint: fire_events_clean.gpkg already ships with its own pre-built 'biome'
    # column from the real pipeline. Use it as an independent check on the join above.
    biome_norm = joined["biome"].str.strip().str.lower()
    t_biome_norm = joined["T_BIOME"].str.strip().str.lower()
    mismatch = (biome_norm != t_biome_norm).sum()
    log.info(f"  Mismatches vs. pre-built 'biome' column: {mismatch:,} / {len(joined):,}")

    return joined


# =============================================================================
# STEP 3 — Per-biome fire-size statistics
# =============================================================================
def biome_statistics(fires_with_biome):
    stats = (
        fires_with_biome.groupby("T_BIOME")["area_km2"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
    )
    log.info("Per-biome fire size (count, mean area_km2):")
    for biome, row in stats.iterrows():
        log.info(f"  {biome:30s} count={int(row['count']):>6,}  mean_area_km2={row['mean']:.2f}")
    return stats


# =============================================================================
# STEP 4 — Fire density per biome (fires per 100 km^2)
# =============================================================================
def fire_density(fires_with_biome, bioregions):
    # bioregions.gpkg has one row per vegetation polygon, not one row per biome — the
    # same biome name repeats across many scattered patches. Aggregate area by biome
    # name before dividing, or the density figure is wrong for any biome with more than
    # one polygon.
    bioregions_albers = bioregions.to_crs(saAlbers)
    biome_area = (bioregions_albers.area / 1_000_000).groupby(bioregions["T_BIOME"]).sum()
    fire_counts = fires_with_biome.groupby("T_BIOME").size()

    density = (fire_counts / biome_area * 100).sort_values(ascending=False)
    density.name = "fires_per_100km2"
    log.info("Fire density per biome (fires per 100 km^2), descending:")
    for biome, value in density.items():
        log.info(f"  {biome:30s} {value:.3f}")
    return density


# =============================================================================
# STEP 5 — Sample severity + NDVI at every ignition point
# =============================================================================
def sample_raster(path, coords):
    with rasterio.open(path) as src:
        nodata = src.nodata
        values = np.array([v[0] for v in src.sample(coords)], dtype=float)
    if nodata is not None:
        values[values == nodata] = np.nan
    return values


def sample_ignition_rasters(ignitions):
    coords = [(geom.x, geom.y) for geom in ignitions.geometry]
    ignitions = ignitions.copy()
    ignitions["severity"] = sample_raster(severityTif, coords)
    ignitions["ndvi"] = sample_raster(ndviTif, coords)
    log.info(f"Sampled severity + NDVI at {len(ignitions):,} ignition points")
    log.info(f"  severity: min={ignitions['severity'].min():.3f}  "
             f"max={ignitions['severity'].max():.3f}  mean={ignitions['severity'].mean():.3f}")
    log.info(f"  ndvi:     min={ignitions['ndvi'].min():.3f}  "
             f"max={ignitions['ndvi'].max():.3f}  mean={ignitions['ndvi'].mean():.3f}")
    return ignitions


# =============================================================================
# STEP 6 — Correlate severity / NDVI against area_per_day
# =============================================================================
def pearson_r(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    sum_x, sum_y = x.sum(), y.sum()
    sum_xy = (x * y).sum()
    sum_x2, sum_y2 = (x ** 2).sum(), (y ** 2).sum()
    numerator = n * sum_xy - sum_x * sum_y
    denominator = np.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
    return numerator / denominator


def correlate_with_severity_and_ndvi(ignitions, fires):
    # Watch out: fire_ignitions.gpkg already carries its own area_per_day field (a
    # per-ignition-point value), separate from the one on fire_events_clean.gpkg.
    # Merging without dropping it first silently produces area_per_day_x/_y instead of
    # the column this step actually wants.
    ignitions = ignitions.drop(columns=["area_per_day"], errors="ignore")
    merged = ignitions.merge(fires[["event_id", "area_per_day"]], on="event_id")
    merged_clean = merged.dropna(subset=["severity", "ndvi", "area_per_day"])
    log.info(f"Merged: {len(merged):,} rows -> {len(merged_clean):,} after dropping nulls")

    r_severity = pearson_r(merged_clean["severity"], merged_clean["area_per_day"])
    r_ndvi = pearson_r(merged_clean["ndvi"], merged_clean["area_per_day"])
    log.info(f"  hand-rolled r (severity vs area_per_day): {r_severity:.4f}")
    log.info(f"  hand-rolled r (ndvi vs area_per_day):     {r_ndvi:.4f}")

    check = merged_clean[["severity", "ndvi", "area_per_day"]].corr()
    log.info("  pandas .corr() check:\n" + check.to_string())

    return {"r_severity": r_severity, "r_ndvi": r_ndvi, "corr_matrix": check}


# =============================================================================
# OPTIONAL EXTENSION — fuel continuity / fragmentation proxy
# =============================================================================
def fragmentation_extension(bioregions):
    try:
        from rasterstats import zonal_stats
    except ImportError:
        log.info("Skipping fragmentation extension: 'rasterstats' not installed "
                 "(conda install -c conda-forge rasterstats)")
        return None

    stats = zonal_stats(bioregions, slopeTif, stats=["std", "mean"])
    df = pd.DataFrame(stats)
    df["T_BIOME"] = bioregions["T_BIOME"].values
    result = df.groupby("T_BIOME")[["std", "mean"]].mean().sort_values("std", ascending=False)
    log.info("Slope fragmentation proxy per biome (std, mean), descending:\n" + result.to_string())
    return result


# =============================================================================
# MAIN
# =============================================================================
def main():
    t0 = time.time()
    log.info("=" * 65)
    log.info(f"Script  : {_script_name}")
    log.info("Step    : Day 2 (Advanced) answer memo")
    log.info(f"Log file: {_log_path}")
    log.info("=" * 65)

    fires, bioregions, ignitions = load_layers()

    log.info("-" * 65)
    log.info("Morning session: vector analysis")
    log.info("-" * 65)
    fires_with_biome = join_biome(fires, bioregions)
    biome_statistics(fires_with_biome)
    fire_density(fires_with_biome, bioregions)

    log.info("-" * 65)
    log.info("Afternoon session: raster sampling + correlation")
    log.info("-" * 65)
    ignitions_sampled = sample_ignition_rasters(ignitions)
    correlate_with_severity_and_ndvi(ignitions_sampled, fires)

    log.info("-" * 65)
    log.info("Optional extension: fragmentation proxy")
    log.info("-" * 65)
    fragmentation_extension(bioregions)

    # Extension challenge (NDVI from raw bands) is not runnable against the current
    # data folder — it needs raw red/NIR band rasters that aren't part of the workshop
    # package. If they're sourced, the pattern is:
    #
    #   with rasterio.open("red_band.tif") as src:
    #       red = src.read(1).astype(float)
    #   with rasterio.open("nir_band.tif") as src:
    #       nir = src.read(1).astype(float)
    #   with np.errstate(divide="ignore", invalid="ignore"):
    #       ndvi = (nir - red) / (nir + red)

    log.info("=" * 65)
    log.info(f"Done — total elapsed: {(time.time() - t0) / 60:.1f} min")
    log.info("=" * 65)


if __name__ == "__main__":
    main()
