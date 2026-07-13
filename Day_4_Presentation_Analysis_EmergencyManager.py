"""
Last Update:
2026-07-12
Cameron Green

Day_4_Presentation_Analysis_EmergencyManager.py
=================================================
Real analysis behind the Riskscape_EmergencyManager_Wildfire_Risk_Briefing.pptx
deck (Brief C, the Emergency Manager): the 50 largest fire events on record by
area, what vegetation they're associated with, and how they check against the
composite risk index already built for the Insurer brief (Day_4_Presentation_
Analysis.py) -- deliberately reusing that raster rather than recomputing it,
since it's the same real layer serving a different question (the point Day 4
itself makes explicit: "the same composite risk raster you built yesterday").

Input : Data/fire_events_clean_WC_final.gpkg
        Data/District_Municipal_Boundary.gpkg          (Western Cape boundary only, for the NDVI clip)
        Data/ndvi_rasters/ndvi_summer.tif
        Day_4_Analysis_Outputs/composite_risk_wc.tif  (from Day_4_Presentation_Analysis.py --
                                                         run that script first)
Output: Day_4_Analysis_Outputs/emergency_analysis.json   (top-50 fire table + biome/risk summary)
        Day_4_Analysis_Outputs/emergency_top50.gpkg      (top-50 fire polygons, for mapping)
        Day_4_Analysis_Outputs/emergency_ndvi_wc.tif     (NDVI clipped to the Western Cape, for Map 2)

Run from the `css2026` conda environment, plus:
    pip install rasterio rasterstats
Then run Day_4_Presentation_Maps_EmergencyManager.py for the map PNGs.
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

firesPath = os.path.join(dataDir, "fire_events_clean_WC_final.gpkg")
munPath = os.path.join(dataDir, "District_Municipal_Boundary.gpkg")
ndviPath = os.path.join(dataDir, "ndvi_rasters", "ndvi_summer.tif")
compositeTif = os.path.join(outDir, "composite_risk_wc.tif")

outJson = os.path.join(outDir, "emergency_analysis.json")
top50Gpkg = os.path.join(outDir, "emergency_top50.gpkg")
ndviClipTif = os.path.join(outDir, "emergency_ndvi_wc.tif")


def clip_ndvi_to_wc():
    mun = gpd.read_file(munPath)
    with rasterio.open(ndviPath) as src:
        wc = mun[mun["adm1_name"].str.contains("Western Cape")].to_crs(src.crs)
        wc_dissolved = wc.geometry.union_all()
        arr, transform = rio_mask(src, [wc_dissolved], crop=True, nodata=src.nodata)
        profile = src.profile
        profile.update(height=arr.shape[1], width=arr.shape[2], transform=transform)
    with rasterio.open(ndviClipTif, "w", **profile) as dst:
        dst.write(arr)

N_TOP = 50
# Composite risk classes are 1-5 (see Day_4_Presentation_Analysis.py); treat a
# mean composite score at or above this as "high risk" for the agreement check.
HIGH_RISK_THRESHOLD = 3.0


def main():
    fires = gpd.read_file(firesPath)
    top50 = fires.sort_values("area_km2", ascending=False).head(N_TOP).reset_index(drop=True)

    if not os.path.exists(compositeTif):
        raise FileNotFoundError(
            f"{compositeTif} not found -- run Day_4_Presentation_Analysis.py (the Insurer "
            "script) first, since this brief deliberately reuses its composite risk raster."
        )

    with rasterio.open(compositeTif) as src:
        composite_nodata = src.nodata
    zonal = zonal_stats(top50, compositeTif, stats=["mean"], nodata=composite_nodata)
    top50["composite_risk_mean"] = [z["mean"] for z in zonal]
    top50["high_risk_agreement"] = top50["composite_risk_mean"] >= HIGH_RISK_THRESHOLD

    top50.to_file(top50Gpkg, driver="GPKG")
    clip_ndvi_to_wc()

    biome_counts = top50["biome"].value_counts().to_dict()
    n_agree = int(top50["high_risk_agreement"].sum())

    records = []
    for _, row in top50.head(10).iterrows():
        records.append({
            "event_id": int(row["event_id"]),
            "start_date": str(row["start_date"]),
            "area_km2": round(float(row["area_km2"]), 1),
            "days_burned": int(row["days_burned"]),
            "biome": row["biome"],
            "composite_risk_mean": round(float(row["composite_risk_mean"]), 2)
                if row["composite_risk_mean"] is not None else None,
            "high_risk_agreement": bool(row["high_risk_agreement"]),
        })

    summary = {
        "n_total_fire_events_wc": int(len(fires)),
        "n_top": N_TOP,
        "smallest_in_top50_km2": round(float(top50["area_km2"].min()), 1),
        "largest_km2": round(float(top50["area_km2"].max()), 1),
        "biome_counts_in_top50": biome_counts,
        "high_risk_threshold": HIGH_RISK_THRESHOLD,
        "n_agree_high_risk": n_agree,
        "n_disagree_low_risk": N_TOP - n_agree,
        "top10_table": records,
    }
    with open(outJson, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(json.dumps(summary, indent=2, default=str))
    print(f"\nWrote: {outJson}\nWrote: {top50Gpkg}\nWrote: {ndviClipTif}")


if __name__ == "__main__":
    main()
