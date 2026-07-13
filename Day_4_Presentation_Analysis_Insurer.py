"""
Last Update:
2026-07-12
Cameron Green

Day_4_Presentation_Analysis.py
===============================
Real analysis behind the Riskscape_Insurer_Wildfire_Risk_Briefing.pptx deck
(Brief A, the Insurer): ignition counts, mean severity, and a composite risk
index per Western Cape district municipality. Reclassification + weighted
blend follows the same method already used in Day_3_Advanced_Memo.py, applied
here at municipality level for a client-facing deliverable rather than a
per-pixel teaching exercise.

Input : Data/District_Municipal_Boundary.gpkg
        Data/fire_ignitions_WC.gpkg
        Data/fire_events_clean_WC_final.gpkg
        Data/severity_rasters/severity_mean_summer.tif
        Data/ndvi_rasters/ndvi_summer.tif
Output: Day_4_Analysis_Outputs/insurer_analysis.json   (per-district stats + tiers)
        Day_4_Analysis_Outputs/severity_wc.tif         (severity clipped to the WC districts)
        Day_4_Analysis_Outputs/composite_risk_wc.tif   (composite risk raster, WC extent)

Run from the `css2026` conda environment -- the base anaconda install and the
`Cameron_Fire_Data_Prep` env both hit a PROJ_LIB conflict with a PostGIS-bundled
proj.db (wrong DATABASE.LAYOUT.VERSION) that breaks every geopandas CRS read.
Also needs, on top of `css2026`'s defaults:
    pip install rasterio rasterstats
Then run Day_4_Presentation_Maps.py to turn these outputs into the three PNGs
used in the deck.
"""
import os
import json

import numpy as np
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

munPath = os.path.join(dataDir, "District_Municipal_Boundary.gpkg")
ignPath = os.path.join(dataDir, "fire_ignitions_WC.gpkg")
firesPath = os.path.join(dataDir, "fire_events_clean_WC_final.gpkg")
severityPath = os.path.join(dataDir, "severity_rasters", "severity_mean_summer.tif")
ndviPath = os.path.join(dataDir, "ndvi_rasters", "ndvi_summer.tif")

outJson = os.path.join(outDir, "insurer_analysis.json")
severityClipTif = os.path.join(outDir, "severity_wc.tif")
compositeTif = os.path.join(outDir, "composite_risk_wc.tif")

# =============================================================================
# CONFIG
# =============================================================================
# Same hand-picked weighting as Day_3_Advanced_Memo.py's handPickedWeights --
# severity already blends fuel/weather/terrain via the production model, so it
# outweighs a single vegetation-dryness proxy on its own.
SEVERITY_WEIGHT = 0.6
NDVI_WEIGHT = 0.4
N_CLASSES = 5


# =============================================================================
# STEP 1 — Ignition count per municipality (spatial join, point-in-polygon)
# =============================================================================
def count_ignitions_per_municipality(wc, ign_path):
    ign = gpd.read_file(ign_path)
    joined = gpd.sjoin(ign, wc[["adm2_name", "geometry"]], how="inner", predicate="within")
    counts = joined.groupby("adm2_name").size().reindex(wc["adm2_name"]).fillna(0).astype(int)
    return ign, counts


# =============================================================================
# STEP 2 — Clip severity + NDVI rasters to the Western Cape municipal extent
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
    return arr[0], transform, nodata, profile


# =============================================================================
# STEP 3 — Quantile reclassification into 1-5 classes (WC-local edges, same
#          method as Day_3_Advanced_Memo.py's reclassify_with_edges)
# =============================================================================
def quantile_edges(values, n_classes=N_CLASSES):
    qs = np.linspace(0, 1, n_classes + 1)
    edges = np.quantile(values, qs)
    edges[0] -= 1e-6
    edges[-1] += 1e-6
    return edges


def reclassify(arr, edges, nodata, invert=False):
    n_classes = len(edges) - 1
    classes = np.digitize(arr, edges[1:-1], right=True) + 1
    classes = np.clip(classes, 1, n_classes).astype(float)
    if invert:
        classes = (n_classes + 1) - classes
    classes[arr == nodata] = np.nan
    return classes


# =============================================================================
# STEP 4 — Rank + tier assignment (terciles across the 6 WC districts)
# =============================================================================
def assign_tiers(wc):
    wc = wc.sort_values("composite_mean", ascending=False).reset_index(drop=True)
    n = len(wc)
    tiers = []
    for i in range(n):
        frac = i / n
        if frac < 1 / 3:
            tiers.append("Highest")
        elif frac < 2 / 3:
            tiers.append("Standard-plus")
        else:
            tiers.append("Standard")
    wc["tier"] = tiers
    return wc


# =============================================================================
# MAIN
# =============================================================================
def main():
    mun = gpd.read_file(munPath)
    wc = mun[mun["adm1_name"].str.contains("Western Cape")].reset_index(drop=True)
    wc_dissolved = wc.geometry.union_all()

    fires = gpd.read_file(firesPath)
    ign, counts = count_ignitions_per_municipality(wc, ignPath)
    wc["ignition_count"] = wc["adm2_name"].map(counts)

    sev_arr, sev_transform, sev_nodata, sev_profile = clip_raster(severityPath, wc_dissolved, severityClipTif)
    ndvi_arr, ndvi_transform, ndvi_nodata, ndvi_profile = clip_raster(ndviPath, wc_dissolved)

    sev_valid = sev_arr[sev_arr != sev_nodata]
    ndvi_valid = ndvi_arr[ndvi_arr != ndvi_nodata]

    sev_edges = quantile_edges(sev_valid)
    ndvi_edges = quantile_edges(ndvi_valid)

    sev_class = reclassify(sev_arr, sev_edges, sev_nodata, invert=False)
    ndvi_class = reclassify(ndvi_arr, ndvi_edges, ndvi_nodata, invert=True)  # low ndvi (dry) -> high risk

    composite = SEVERITY_WEIGHT * sev_class + NDVI_WEIGHT * ndvi_class
    composite_nodata = -9999.0
    composite_filled = np.where(np.isnan(composite), composite_nodata, composite)

    comp_profile = sev_profile.copy()
    comp_profile.update(dtype="float32", count=1, nodata=composite_nodata)
    with rasterio.open(compositeTif, "w", **comp_profile) as dst:
        dst.write(composite_filled.astype("float32"), 1)

    # Zonal stats: mean severity, mean composite risk per municipality
    sev_zonal = zonal_stats(wc, severityPath, stats=["mean"], nodata=sev_nodata)
    wc["severity_mean"] = [z["mean"] for z in sev_zonal]

    comp_zonal = zonal_stats(wc, compositeTif, stats=["mean"], nodata=composite_nodata)
    wc["composite_mean"] = [z["mean"] for z in comp_zonal]

    wc = assign_tiers(wc)

    summary = {
        "n_fire_events_wc": int(len(fires)),
        "n_ignitions_wc": int(len(ign)),
        "record_start": str(fires["start_date"].min()),
        "record_end": str(fires["start_date"].max()),
        "severity_weight": SEVERITY_WEIGHT,
        "ndvi_weight": NDVI_WEIGHT,
        "sev_edges": sev_edges.tolist(),
        "ndvi_edges": ndvi_edges.tolist(),
        "municipalities": wc[
            ["adm2_name", "area_sqkm", "ignition_count", "severity_mean", "composite_mean", "tier"]
        ].to_dict(orient="records"),
    }
    with open(outJson, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(json.dumps(summary, indent=2, default=str))
    print(f"\nWrote: {outJson}\nWrote: {severityClipTif}\nWrote: {compositeTif}")


if __name__ == "__main__":
    main()
