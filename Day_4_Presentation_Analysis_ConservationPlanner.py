"""
Last Update:
2026-07-12
Cameron Green

Day_4_Presentation_Analysis_ConservationPlanner.py
====================================================
Real analysis behind the Riskscape_ConservationPlanner_Wildfire_Risk_Briefing.pptx
deck (Brief B, the Conservation Planner): ignition counts, mean severity, and a
decade-over-decade frequency trend, per Western Cape bioregion (biome). Mirrors
the method in Day_4_Presentation_Analysis.py (the Insurer script), applied at
bioregion level instead of municipality level.

Bioregions are joined by a fresh spatial join against Data/bioregions.gpkg
(clipped to the Western Cape district boundary and dissolved by T_BIOME) rather
than trusting the pre-computed 'biome' column on fire_events_clean_WC_final.gpkg,
because that file's event_id does not reliably match fire_ignitions_WC.gpkg's
event_id (only ~340 of ~4,650 IDs overlap -- the two files were independently
extracted from a national dataset with different id ranges). A direct
point-in-polygon join against the bioregion polygons sidesteps that mismatch
and keeps both the count and the decade trend self-consistent.

Input : Data/bioregions.gpkg
        Data/District_Municipal_Boundary.gpkg   (Western Cape boundary only)
        Data/fire_ignitions_WC.gpkg
        Data/severity_rasters/severity_mean_summer.tif
Output: Day_4_Analysis_Outputs/conservation_analysis.json  (per-biome stats)
        Day_4_Analysis_Outputs/conservation_severity_wc.tif (severity clipped to WC)

Run from the `css2026` conda environment (see Day_4_Presentation_Analysis.py
for the PROJ_LIB gotcha with the other envs), plus:
    pip install rasterio rasterstats
Then run Day_4_Presentation_Maps_ConservationPlanner.py for the map PNGs.
"""
import os
import json

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.mask import mask as rio_mask
from rasterstats import zonal_stats

# =============================================================================
# PATHS
# =============================================================================
scriptDir = os.path.dirname(os.path.abspath(__file__))
dataDir = os.path.join(scriptDir, "Data")
outDir = os.path.join(scriptDir, "Day_4_Analysis_Outputs")
os.makedirs(outDir, exist_ok=True)

bioregionsPath = os.path.join(dataDir, "bioregions.gpkg")
munPath = os.path.join(dataDir, "District_Municipal_Boundary.gpkg")
ignPath = os.path.join(dataDir, "fire_ignitions_WC.gpkg")
severityPath = os.path.join(dataDir, "severity_rasters", "severity_mean_summer.tif")

outJson = os.path.join(outDir, "conservation_analysis.json")
severityClipTif = os.path.join(outDir, "conservation_severity_wc.tif")

# =============================================================================
# CONFIG
# =============================================================================
# 2026's data only runs through March, so it is excluded from the annualised
# decade rates (included in raw record-wide counts elsewhere) to avoid a
# partial year dragging the 2020s rate down artificially.
EARLY_DECADE = 2010
EARLY_YEARS = list(range(2012, 2020))   # 2012-2019 inclusive, 8 full years
LATE_DECADE = 2020
LATE_YEARS = list(range(2020, 2026))    # 2020-2025 inclusive, 6 full years


# =============================================================================
# STEP 1 — Bioregion polygons clipped to the Western Cape, dissolved to biome
# =============================================================================
def build_biome_polygons():
    bio = gpd.read_file(bioregionsPath)
    mun = gpd.read_file(munPath)
    wc = mun[mun["adm1_name"].str.contains("Western Cape")].to_crs(bio.crs)
    wc_dissolved = wc.geometry.union_all()
    clipped = gpd.clip(bio, wc_dissolved)
    biome_polys = clipped.dissolve(by="T_BIOME").reset_index()[["T_BIOME", "geometry"]]
    biome_polys["area_sqkm"] = biome_polys.geometry.area / 1e6
    return biome_polys, bio.crs


# =============================================================================
# STEP 2 — Spatial join: ignitions -> biome polygon (point-in-polygon)
# =============================================================================
def join_ignitions_to_biome(biome_polys, target_crs):
    ign = gpd.read_file(ignPath).to_crs(target_crs)
    ign["start_date"] = pd.to_datetime(ign["start_date"], format="mixed")
    ign["year"] = ign["start_date"].dt.year
    ign["decade"] = (ign["year"] // 10) * 10
    joined = gpd.sjoin(ign, biome_polys, how="inner", predicate="within")
    return ign, joined


# =============================================================================
# STEP 3 — Decade comparison (annualised rate, full-year decades only)
# =============================================================================
def decade_trend(joined):
    early = joined[joined["year"].isin(EARLY_YEARS)]
    late = joined[joined["year"].isin(LATE_YEARS)]
    early_counts = early.groupby("T_BIOME").size()
    late_counts = late.groupby("T_BIOME").size()
    return early_counts, late_counts


# =============================================================================
# STEP 4 — Zonal mean severity per biome
# =============================================================================
def clip_raster(path, geom, out_path=None):
    with rasterio.open(path) as src:
        arr, transform = rio_mask(src, [geom], crop=True, nodata=src.nodata)
        profile = src.profile
        profile.update(height=arr.shape[1], width=arr.shape[2], transform=transform)
        nodata = src.nodata
    if out_path:
        with rasterio.open(out_path, "w", **profile) as dst:
            dst.write(arr)
    return nodata


# =============================================================================
# MAIN
# =============================================================================
def main():
    biome_polys, target_crs = build_biome_polygons()
    ign, joined = join_ignitions_to_biome(biome_polys, target_crs)

    total_counts = joined.groupby("T_BIOME").size()
    early_counts, late_counts = decade_trend(joined)

    biome_polys_4326 = biome_polys.to_crs(4326)
    sev_nodata = clip_raster(severityPath, biome_polys.to_crs(rasterio.open(severityPath).crs).geometry.union_all(),
                              severityClipTif)
    sev_zonal = zonal_stats(biome_polys.to_crs(rasterio.open(severityPath).crs), severityPath,
                             stats=["mean"], nodata=sev_nodata)
    severity_by_biome = dict(zip(biome_polys["T_BIOME"], [z["mean"] for z in sev_zonal]))

    records = []
    for _, row in biome_polys.iterrows():
        name = row["T_BIOME"]
        early_n = int(early_counts.get(name, 0))
        late_n = int(late_counts.get(name, 0))
        early_rate = early_n / len(EARLY_YEARS)
        late_rate = late_n / len(LATE_YEARS)
        if early_rate > 0:
            pct_change = (late_rate - early_rate) / early_rate * 100
        else:
            pct_change = None
        records.append({
            "biome": name,
            "area_sqkm": float(row["area_sqkm"]),
            "ignition_count": int(total_counts.get(name, 0)),
            "severity_mean": severity_by_biome.get(name),
            "early_count_2012_2019": early_n,
            "late_count_2020_2025": late_n,
            "early_rate_per_year": round(early_rate, 1),
            "late_rate_per_year": round(late_rate, 1),
            "pct_change": round(pct_change, 1) if pct_change is not None else None,
        })
    records.sort(key=lambda r: r["severity_mean"] or 0, reverse=True)

    summary = {
        "n_ignitions_wc": int(len(ign)),
        "n_ignitions_matched_to_biome": int(len(joined)),
        "early_years": EARLY_YEARS,
        "late_years": LATE_YEARS,
        "note_2026_excluded_from_rates": "2026 has only Jan-Mar data and is excluded from annualised rates",
        "biomes": records,
    }
    with open(outJson, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(json.dumps(summary, indent=2, default=str))
    print(f"\nWrote: {outJson}\nWrote: {severityClipTif}")


if __name__ == "__main__":
    main()
