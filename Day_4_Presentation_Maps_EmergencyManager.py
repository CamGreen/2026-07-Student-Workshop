"""
Last Update:
2026-07-12
Cameron Green

Day_4_Presentation_Maps_EmergencyManager.py
=============================================
Renders the three client-facing maps used in Riskscape_EmergencyManager_
Wildfire_Risk_Briefing.pptx (Brief C), reading the outputs of
Day_4_Presentation_Analysis_EmergencyManager.py. Same plain matplotlib/
geopandas approach (no QGIS UI chrome) and equal-area CRS as the other two
briefs' maps scripts.

Input : Day_4_Analysis_Outputs/emergency_analysis.json
        Day_4_Analysis_Outputs/emergency_top50.gpkg
        Day_4_Analysis_Outputs/emergency_ndvi_wc.tif
        Day_4_Analysis_Outputs/composite_risk_wc.tif   (from Day_4_Presentation_Analysis.py)
        Data/bioregions.gpkg
        Data/District_Municipal_Boundary.gpkg
Output: Day_4_Analysis_Outputs/emergency_map1_top50_fires.png
        Day_4_Analysis_Outputs/emergency_map2_ndvi_bioregions.png
        Day_4_Analysis_Outputs/emergency_map3_composite_risk.png

Run Day_4_Presentation_Analysis_EmergencyManager.py first (which itself
depends on Day_4_Presentation_Analysis.py having already run). Needs the
`css2026` conda environment plus:
    pip install rasterio rasterstats matplotlib-scalebar
"""
import os
import json

import numpy as np
import geopandas as gpd
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib_scalebar.scalebar import ScaleBar

# =============================================================================
# PATHS
# =============================================================================
scriptDir = os.path.dirname(os.path.abspath(__file__))
dataDir = os.path.join(scriptDir, "Data")
outDir = os.path.join(scriptDir, "Day_4_Analysis_Outputs")

analysisJson = os.path.join(outDir, "emergency_analysis.json")
top50Gpkg = os.path.join(outDir, "emergency_top50.gpkg")
ndviClipTif = os.path.join(outDir, "emergency_ndvi_wc.tif")
compositeTif = os.path.join(outDir, "composite_risk_wc.tif")
bioregionsPath = os.path.join(dataDir, "bioregions.gpkg")
munPath = os.path.join(dataDir, "District_Municipal_Boundary.gpkg")

# =============================================================================
# BRAND / STYLE — matches the other two decks
# =============================================================================
RED = "#AA1D13"
CHARCOAL = "#262626"
GOLD = "#C9971F"

cmap_red = LinearSegmentedColormap.from_list(
    "riskscape_red", ["#F7F4EF", "#E8B4AE", "#C24A3B", RED, "#5C0F09"]
)
# NDVI is conventionally shown as a green ramp -- the one deliberate deviation
# from the brand red, same convention the workshop's own NDVI screenshots use.
cmap_ndvi = LinearSegmentedColormap.from_list(
    "ndvi_green", ["#F7F4EF", "#D9E8C4", "#9CC177", "#5B8F3A", "#2E5D1E"]
)
plt.rcParams["font.family"] = "Segoe UI"

N_LABEL = 8  # only label the N largest fires -- labelling all 50 would be unreadable

# Rank #3 and #4 sit only ~27km apart in the same mountain range -- nudge #4
# clear so the two label boxes don't collide.
FIRE_LABEL_OFFSETS = {121334: (85000, -75000)}


# =============================================================================
# HELPERS
# =============================================================================
def reproject_to_target(src_path, target_crs):
    with rasterio.open(src_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, target_crs, src.width, src.height, *src.bounds)
        dst_arr = np.full((height, width), src.nodata, dtype="float32")
        reproject(
            source=rasterio.band(src, 1), destination=dst_arr,
            src_transform=src.transform, src_crs=src.crs,
            dst_transform=transform, dst_crs=target_crs,
            resampling=Resampling.bilinear, src_nodata=src.nodata, dst_nodata=src.nodata,
        )
        bounds = rasterio.transform.array_bounds(height, width, transform)
        return dst_arr, src.nodata, bounds


def style_axes(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_aspect("equal")


def north_arrow(ax, x=0.94, y=0.90):
    ax.annotate("N", xy=(x, y), xycoords="axes fraction", ha="center", va="center",
                fontsize=15, fontweight="bold", color=CHARCOAL)
    ax.annotate("", xy=(x, y + 0.055), xytext=(x, y - 0.045), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color=CHARCOAL, lw=1.8))


def add_scalebar(ax, location="lower right"):
    ax.add_artist(ScaleBar(1, units="m", dimension="si-length", location=location,
                            box_alpha=0.75, color=CHARCOAL, box_color="white",
                            font_properties={"size": 10}))


def add_colorbar(fig, mappable, label):
    cax = fig.add_axes([0.14, 0.06, 0.3, 0.02])
    cb = fig.colorbar(mappable, cax=cax, orientation="horizontal")
    cb.set_label(label, fontsize=9.5, color=CHARCOAL)
    cb.ax.tick_params(labelsize=8, colors=CHARCOAL)


def build_biome_polygons(target_crs):
    bio = gpd.read_file(bioregionsPath)
    mun = gpd.read_file(munPath)
    wc = mun[mun["adm1_name"].str.contains("Western Cape")].to_crs(bio.crs)
    wc_dissolved = wc.geometry.union_all()
    clipped = gpd.clip(bio, wc_dissolved)
    biome_polys = clipped.dissolve(by="T_BIOME").reset_index()[["T_BIOME", "geometry"]]
    return biome_polys.to_crs(target_crs)


def label_top_fires(ax, top50, n=N_LABEL):
    ranked = top50.sort_values("area_km2", ascending=False).reset_index(drop=True)
    for i, row in ranked.head(n).iterrows():
        c = row.geometry.representative_point()
        dx, dy = FIRE_LABEL_OFFSETS.get(int(row["event_id"]), (0, 0))
        tx, ty = c.x + dx, c.y + dy
        ax.annotate(f"#{i + 1}  {row['area_km2']:.0f} km²", xy=(tx, ty),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=8.5, fontweight="bold", color=CHARCOAL,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=CHARCOAL, lw=0.5, alpha=0.85))
        if dx or dy:
            ax.plot([c.x, tx], [c.y, ty], color=CHARCOAL, lw=0.8)


# =============================================================================
# MAP 1 — Top 50 largest fires, styled and labelled
# =============================================================================
def render_map1(top50, biome_polys, xlim, ylim, out_path):
    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    biome_polys.plot(ax=ax, color="#F0EDE7", edgecolor="white", linewidth=0.8)
    biome_polys.boundary.plot(ax=ax, color="#B9B4AC", linewidth=0.8)

    top50.plot(column="area_km2", cmap=cmap_red, linewidth=0.6, edgecolor=CHARCOAL, ax=ax, legend=False)
    label_top_fires(ax, top50)

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)

    sm = plt.cm.ScalarMappable(cmap=cmap_red, norm=plt.Normalize(
        vmin=top50["area_km2"].min(), vmax=top50["area_km2"].max()))
    add_colorbar(fig, sm, "Fire size, km² (50 largest events on record, 2012–2026)")

    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.3, facecolor="white")
    plt.close(fig)


# =============================================================================
# MAP 2 — Same fires over NDVI + bioregions
# =============================================================================
def render_map2(top50, biome_polys, target_crs, xlim, ylim, out_path):
    ndvi_arr, ndvi_nodata, ndvi_bounds = reproject_to_target(ndviClipTif, target_crs)
    ndvi_masked = np.ma.masked_equal(ndvi_arr, ndvi_nodata)

    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    im = ax.imshow(ndvi_masked, extent=(ndvi_bounds[0], ndvi_bounds[2], ndvi_bounds[1], ndvi_bounds[3]),
                   cmap=cmap_ndvi, vmin=np.nanpercentile(ndvi_masked.compressed(), 2),
                   vmax=np.nanpercentile(ndvi_masked.compressed(), 98))
    biome_polys.boundary.plot(ax=ax, color=CHARCOAL, linewidth=0.7, linestyle=(0, (4, 3)), alpha=0.8)
    top50.boundary.plot(ax=ax, color=RED, linewidth=1.1)

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)
    add_colorbar(fig, im, "NDVI (summer) — darker green = lusher; fire outlines in red")

    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.3, facecolor="white")
    plt.close(fig)


# =============================================================================
# MAP 3 — Composite risk with the top-50 fires highlighted by agreement
# =============================================================================
def render_map3(top50, target_crs, xlim, ylim, out_path):
    comp_arr, comp_nodata, comp_bounds = reproject_to_target(compositeTif, target_crs)
    comp_masked = np.ma.masked_equal(comp_arr, comp_nodata)

    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    im = ax.imshow(comp_masked, extent=(comp_bounds[0], comp_bounds[2], comp_bounds[1], comp_bounds[3]),
                   cmap=cmap_red)

    agree = top50[top50["high_risk_agreement"]]
    disagree = top50[~top50["high_risk_agreement"]]
    disagree.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.3)
    agree.boundary.plot(ax=ax, color=GOLD, linewidth=1.6)

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax, location="lower left")
    add_colorbar(fig, im, "Composite risk index (1–5)")

    # Small legend explaining the two outline colours
    legend_ax = fig.add_axes([0.62, 0.10, 0.32, 0.09])
    legend_ax.axis("off")
    legend_ax.plot([0, 1], [1, 1], color=GOLD, lw=2.2)
    legend_ax.text(1.15, 1, "Falls in a high-risk zone (17 of 50)", va="center", fontsize=9.5, color=CHARCOAL)
    legend_ax.plot([0, 1], [0, 0], color=CHARCOAL, lw=2.2)
    legend_ax.text(1.15, 0, "Falls in a lower-risk zone (33 of 50)", va="center", fontsize=9.5, color=CHARCOAL)
    legend_ax.set_xlim(0, 4.2)
    legend_ax.set_ylim(-0.6, 1.6)

    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.3, facecolor="white")
    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================
def main():
    with open(analysisJson) as f:
        summary = json.load(f)

    target_crs = gpd.read_file(bioregionsPath, rows=1).crs
    top50 = gpd.read_file(top50Gpkg).to_crs(target_crs)
    biome_polys = build_biome_polygons(target_crs)

    minx, miny, maxx, maxy = biome_polys.total_bounds
    pad_x = (maxx - minx) * 0.06
    pad_y = (maxy - miny) * 0.06
    xlim = (minx - pad_x, maxx + pad_x)
    ylim = (miny - pad_y, maxy + pad_y)

    render_map1(top50, biome_polys, xlim, ylim, os.path.join(outDir, "emergency_map1_top50_fires.png"))
    render_map2(top50, biome_polys, target_crs, xlim, ylim, os.path.join(outDir, "emergency_map2_ndvi_bioregions.png"))
    render_map3(top50, target_crs, xlim, ylim, os.path.join(outDir, "emergency_map3_composite_risk.png"))

    print(f"Maps written to: {outDir}")


if __name__ == "__main__":
    main()
