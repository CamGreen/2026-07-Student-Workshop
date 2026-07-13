"""
Last Update:
2026-07-12
Cameron Green

Day_4_Presentation_Maps.py
===========================
Renders the three client-facing maps used in Riskscape_Insurer_Wildfire_Risk_
Briefing.pptx (Brief A, the Insurer), reading the outputs of
Day_4_Presentation_Analysis.py. Plain matplotlib/geopandas exports -- no QGIS
UI chrome -- reprojected to the equal-area CRS already used by
Data/bioregions.gpkg so the scale bar is geometrically accurate rather than a
degrees-to-metres approximation.

Input : Day_4_Analysis_Outputs/insurer_analysis.json
        Day_4_Analysis_Outputs/severity_wc.tif
        Day_4_Analysis_Outputs/composite_risk_wc.tif
        Data/District_Municipal_Boundary.gpkg
        Data/fire_events_clean_WC_final.gpkg
        Data/bioregions.gpkg               (source of the target equal-area CRS)
Output: Day_4_Analysis_Outputs/map1_ignition_count.png
        Day_4_Analysis_Outputs/map2_severity_fires.png
        Day_4_Analysis_Outputs/map3_composite_risk.png

Run Day_4_Presentation_Analysis.py first. Needs the `css2026` conda
environment plus:
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

analysisJson = os.path.join(outDir, "insurer_analysis.json")
severityClipTif = os.path.join(outDir, "severity_wc.tif")
compositeTif = os.path.join(outDir, "composite_risk_wc.tif")

munPath = os.path.join(dataDir, "District_Municipal_Boundary.gpkg")
firesPath = os.path.join(dataDir, "fire_events_clean_WC_final.gpkg")
bioregionsPath = os.path.join(dataDir, "bioregions.gpkg")

# =============================================================================
# BRAND / STYLE — matches Riskscape_Insurer_Wildfire_Risk_Briefing.pptx
# =============================================================================
RED = "#AA1D13"
CHARCOAL = "#262626"

cmap_red = LinearSegmentedColormap.from_list(
    "riskscape_red", ["#F7F4EF", "#E8B4AE", "#C24A3B", RED, "#5C0F09"]
)
plt.rcParams["font.family"] = "Segoe UI"

# Manual nudge so the small City of Cape Town label doesn't collide with
# West Coast / Overberg -- its polygon is too thin for a centred label.
LABEL_OFFSETS = {"City of Cape Town": (-95000, -85000)}


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
        bounds = rasterio.transform.array_bounds(height, width, transform)  # left, bottom, right, top
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


def add_scalebar(ax):
    ax.add_artist(ScaleBar(1, units="m", dimension="si-length", location="lower right",
                            box_alpha=0.75, color=CHARCOAL, box_color="white",
                            font_properties={"size": 10}))


def label_municipalities(ax, wc, text_fn, dark_fn=None):
    for _, row in wc.iterrows():
        name = row["adm2_name"]
        c = row.geometry.representative_point()
        dx, dy = LABEL_OFFSETS.get(name, (0, 0))
        tx, ty = c.x + dx, c.y + dy
        dark = dark_fn(row) if dark_fn else False
        kwargs = dict(ha="center", va="center", fontsize=10, fontweight="bold", linespacing=1.4)
        if dark:
            ax.annotate(text_fn(row), xy=(tx, ty), color="white", **kwargs)
        else:
            ax.annotate(text_fn(row), xy=(tx, ty), color=CHARCOAL,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=CHARCOAL, lw=0.6, alpha=0.88), **kwargs)
        if dx or dy:
            ax.plot([c.x, tx], [c.y, ty], color=CHARCOAL, lw=0.8)


def add_colorbar(fig, mappable, label):
    cax = fig.add_axes([0.14, 0.06, 0.3, 0.02])
    cb = fig.colorbar(mappable, cax=cax, orientation="horizontal")
    cb.set_label(label, fontsize=9.5, color=CHARCOAL)
    cb.ax.tick_params(labelsize=8, colors=CHARCOAL)


# =============================================================================
# MAP 1 — Ignition count choropleth
# =============================================================================
def render_map1(wc, xlim, ylim, out_path):
    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    wc.plot(column="ignition_count", cmap=cmap_red, linewidth=1.1, edgecolor="white", ax=ax, legend=False)
    wc.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.1)

    median_count = wc["ignition_count"].median()
    label_municipalities(
        ax, wc,
        text_fn=lambda row: f"{row['adm2_name']}\n{row['ignition_count']:,} fires",
        dark_fn=lambda row: row["ignition_count"] > median_count and row["adm2_name"] not in LABEL_OFFSETS,
    )

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)

    sm = plt.cm.ScalarMappable(cmap=cmap_red, norm=plt.Normalize(
        vmin=wc["ignition_count"].min(), vmax=wc["ignition_count"].max()))
    add_colorbar(fig, sm, "Ignition count (2012–2026)")

    fig.savefig(out_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# =============================================================================
# MAP 2 — Severity raster with fire events overlaid
# =============================================================================
def render_map2(wc, fires_wc, target_crs, xlim, ylim, out_path):
    sev_arr, sev_nodata, sev_bounds = reproject_to_target(severityClipTif, target_crs)
    sev_masked = np.ma.masked_equal(sev_arr, sev_nodata)

    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    im = ax.imshow(sev_masked, extent=(sev_bounds[0], sev_bounds[2], sev_bounds[1], sev_bounds[3]),
                   cmap=cmap_red, vmin=np.nanpercentile(sev_masked.compressed(), 2),
                   vmax=np.nanpercentile(sev_masked.compressed(), 98))
    fires_wc.boundary.plot(ax=ax, color=CHARCOAL, linewidth=0.35, alpha=0.75)
    wc.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.1)

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)
    add_colorbar(fig, im, "Modelled severity (summer) — higher = more km²/day")

    fig.savefig(out_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# =============================================================================
# MAP 3 — Composite risk with municipality boundaries + tier labels
# =============================================================================
def render_map3(wc, target_crs, xlim, ylim, out_path):
    comp_arr, comp_nodata, comp_bounds = reproject_to_target(compositeTif, target_crs)
    comp_masked = np.ma.masked_equal(comp_arr, comp_nodata)

    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    im = ax.imshow(comp_masked, extent=(comp_bounds[0], comp_bounds[2], comp_bounds[1], comp_bounds[3]), cmap=cmap_red)
    wc.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.4)

    tier_label = {"Highest": "HIGHEST TIER", "Standard-plus": "STANDARD-PLUS", "Standard": "STANDARD"}
    label_municipalities(
        ax, wc,
        text_fn=lambda row: f"{row['adm2_name']}\n{tier_label[row['tier']]}",
    )

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)
    add_colorbar(fig, im, "Composite risk index (1–5, severity + vegetation dryness)")

    fig.savefig(out_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================
def main():
    with open(analysisJson) as f:
        summary = json.load(f)
    mun_stats = {m["adm2_name"]: m for m in summary["municipalities"]}

    # Same equal-area CRS already established in this project (bioregions.gpkg)
    # so distances/areas -- and the scale bar -- are geometrically accurate.
    target_crs = gpd.read_file(bioregionsPath, rows=1).crs

    mun = gpd.read_file(munPath)
    wc_4326 = mun[mun["adm1_name"].str.contains("Western Cape")].copy()
    wc_4326["ignition_count"] = wc_4326["adm2_name"].map(lambda n: mun_stats[n]["ignition_count"])
    wc_4326["severity_mean"] = wc_4326["adm2_name"].map(lambda n: mun_stats[n]["severity_mean"])
    wc_4326["composite_mean"] = wc_4326["adm2_name"].map(lambda n: mun_stats[n]["composite_mean"])
    wc_4326["tier"] = wc_4326["adm2_name"].map(lambda n: mun_stats[n]["tier"])
    wc = wc_4326.to_crs(target_crs)

    fires = gpd.read_file(firesPath)
    wc_dissolved_4326 = wc_4326.geometry.union_all()
    fires_wc = fires[fires.intersects(wc_dissolved_4326)].to_crs(target_crs)

    minx, miny, maxx, maxy = wc.total_bounds
    pad_x = (maxx - minx) * 0.06
    pad_y = (maxy - miny) * 0.06
    xlim = (minx - pad_x, maxx + pad_x)
    ylim = (miny - pad_y, maxy + pad_y)

    render_map1(wc, xlim, ylim, os.path.join(outDir, "map1_ignition_count.png"))
    render_map2(wc, fires_wc, target_crs, xlim, ylim, os.path.join(outDir, "map2_severity_fires.png"))
    render_map3(wc, target_crs, xlim, ylim, os.path.join(outDir, "map3_composite_risk.png"))

    print(f"Maps written to: {outDir}")


if __name__ == "__main__":
    main()
