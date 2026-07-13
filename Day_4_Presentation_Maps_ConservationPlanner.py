"""
Last Update:
2026-07-12
Cameron Green

Day_4_Presentation_Maps_ConservationPlanner.py
================================================
Renders the three client-facing maps used in Riskscape_ConservationPlanner_
Wildfire_Risk_Briefing.pptx (Brief B), reading the outputs of
Day_4_Presentation_Analysis_ConservationPlanner.py. Same plain matplotlib/
geopandas approach (no QGIS UI chrome) and equal-area CRS as the Insurer maps
script, applied to bioregion polygons instead of municipal boundaries.

Input : Day_4_Analysis_Outputs/conservation_analysis.json
        Day_4_Analysis_Outputs/conservation_severity_wc.tif
        Data/bioregions.gpkg
        Data/District_Municipal_Boundary.gpkg
Output: Day_4_Analysis_Outputs/conservation_map1_ignition_count.png
        Day_4_Analysis_Outputs/conservation_map2_severity.png
        Day_4_Analysis_Outputs/conservation_map3_decade_trend.png

Run Day_4_Presentation_Analysis_ConservationPlanner.py first. Needs the
`css2026` conda environment plus:
    pip install rasterio rasterstats matplotlib-scalebar
"""
import os
import json

import numpy as np
import geopandas as gpd
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm, TwoSlopeNorm
from matplotlib_scalebar.scalebar import ScaleBar

# =============================================================================
# PATHS
# =============================================================================
scriptDir = os.path.dirname(os.path.abspath(__file__))
dataDir = os.path.join(scriptDir, "Data")
outDir = os.path.join(scriptDir, "Day_4_Analysis_Outputs")

analysisJson = os.path.join(outDir, "conservation_analysis.json")
bioregionsPath = os.path.join(dataDir, "bioregions.gpkg")
munPath = os.path.join(dataDir, "District_Municipal_Boundary.gpkg")

# =============================================================================
# BRAND / STYLE — matches the Insurer deck
# =============================================================================
RED = "#AA1D13"
CHARCOAL = "#262626"
BLUE = "#2A5C8A"

cmap_red = LinearSegmentedColormap.from_list(
    "riskscape_red", ["#F7F4EF", "#E8B4AE", "#C24A3B", RED, "#5C0F09"]
)
cmap_diverging = LinearSegmentedColormap.from_list(
    "riskscape_diverging", [BLUE, "#CFE0EC", "#F7F4EF", "#E8B4AE", RED]
)
plt.rcParams["font.family"] = "Segoe UI"

# Small-sample biomes (fewer than 30 ignitions on record) get an asterisk in
# their label so a reader doesn't over-read a dramatic-looking swing.
SMALL_SAMPLE_THRESHOLD = 30

LABEL_OFFSETS = {"Grassland": (145000, 95000), "Succulent Karoo": (137596, -124138)}


# =============================================================================
# HELPERS
# =============================================================================
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


def label_biomes(ax, biome_polys, text_fn, dark_fn=None):
    for _, row in biome_polys.iterrows():
        name = row["T_BIOME"]
        c = row.geometry.representative_point()
        dx, dy = LABEL_OFFSETS.get(name, (0, 0))
        tx, ty = c.x + dx, c.y + dy
        # A moved label is no longer sitting on its own polygon fill, so it must
        # never use the white-text "dark background" style regardless of value.
        dark = (dark_fn(row) if dark_fn else False) and not (dx or dy)
        kwargs = dict(ha="center", va="center", fontsize=9.5, fontweight="bold", linespacing=1.35)
        if dark:
            ax.annotate(text_fn(row), xy=(tx, ty), color="white", **kwargs)
        else:
            ax.annotate(text_fn(row), xy=(tx, ty), color=CHARCOAL,
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=CHARCOAL, lw=0.6, alpha=0.9), **kwargs)
        if dx or dy:
            ax.plot([c.x, tx], [c.y, ty], color=CHARCOAL, lw=0.8)


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


# =============================================================================
# MAP 1 — Ignition count per biome (log-scaled color, Fynbos dwarfs the rest)
# =============================================================================
def render_map1(biome_polys, xlim, ylim, out_path):
    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    norm = LogNorm(vmin=max(biome_polys["ignition_count"].min(), 1), vmax=biome_polys["ignition_count"].max())
    biome_polys.plot(column="ignition_count", cmap=cmap_red, norm=norm,
                      linewidth=1.1, edgecolor="white", ax=ax, legend=False)
    biome_polys.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.1)

    label_biomes(
        ax, biome_polys,
        text_fn=lambda row: f"{row['T_BIOME']}\n{row['ignition_count']:,} fires"
        + ("*" if row["ignition_count"] < SMALL_SAMPLE_THRESHOLD else ""),
        dark_fn=lambda row: row["ignition_count"] > 500,
    )

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)

    sm = plt.cm.ScalarMappable(cmap=cmap_red, norm=norm)
    add_colorbar(fig, sm, "Ignition count, 2012–2026 (log scale)")

    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


# =============================================================================
# MAP 2 — Mean severity per biome (zonal statistics)
# =============================================================================
def render_map2(biome_polys, xlim, ylim, out_path):
    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    biome_polys.plot(column="severity_mean", cmap=cmap_red, linewidth=1.1, edgecolor="white", ax=ax, legend=False)
    biome_polys.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.1)

    median_sev = biome_polys["severity_mean"].median()
    label_biomes(
        ax, biome_polys,
        text_fn=lambda row: f"{row['T_BIOME']}\n{row['severity_mean']:.2f} mean severity",
        dark_fn=lambda row: row["severity_mean"] > median_sev,
    )

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)

    sm = plt.cm.ScalarMappable(cmap=cmap_red, norm=plt.Normalize(
        vmin=biome_polys["severity_mean"].min(), vmax=biome_polys["severity_mean"].max()))
    add_colorbar(fig, sm, "Mean modelled severity (summer), zonal average per biome")

    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


# =============================================================================
# MAP 3 — Decade-over-decade frequency trend (diverging)
# =============================================================================
def render_map3(biome_polys, xlim, ylim, out_path):
    fig, ax = plt.subplots(figsize=(9.5, 8), dpi=220)
    vals = biome_polys["pct_change"].fillna(0)
    vmax = max(abs(vals.min()), abs(vals.max()))
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    biome_polys.plot(column="pct_change", cmap=cmap_diverging, norm=norm,
                      linewidth=1.1, edgecolor="white", ax=ax, legend=False)
    biome_polys.boundary.plot(ax=ax, color=CHARCOAL, linewidth=1.1)

    def fmt_pct(row):
        sample_flag = "*" if row["ignition_count"] < SMALL_SAMPLE_THRESHOLD else ""
        sign = "+" if row["pct_change"] >= 0 else ""
        return f"{row['T_BIOME']}\n{sign}{row['pct_change']:.0f}%{sample_flag}"

    label_biomes(ax, biome_polys, text_fn=fmt_pct, dark_fn=lambda row: False)

    style_axes(ax, xlim, ylim)
    north_arrow(ax)
    add_scalebar(ax)

    sm = plt.cm.ScalarMappable(cmap=cmap_diverging, norm=norm)
    add_colorbar(fig, sm, "Change in annual ignition rate, 2020–2025 vs. 2012–2019")

    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.15, facecolor="white")
    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================
def main():
    with open(analysisJson) as f:
        summary = json.load(f)
    biome_stats = {b["biome"]: b for b in summary["biomes"]}

    target_crs = gpd.read_file(bioregionsPath, rows=1).crs
    biome_polys = build_biome_polygons(target_crs)
    biome_polys["ignition_count"] = biome_polys["T_BIOME"].map(lambda n: biome_stats[n]["ignition_count"])
    biome_polys["severity_mean"] = biome_polys["T_BIOME"].map(lambda n: biome_stats[n]["severity_mean"])
    biome_polys["pct_change"] = biome_polys["T_BIOME"].map(lambda n: biome_stats[n]["pct_change"])

    minx, miny, maxx, maxy = biome_polys.total_bounds
    pad_x = (maxx - minx) * 0.06
    pad_y = (maxy - miny) * 0.06
    xlim = (minx - pad_x, maxx + pad_x)
    ylim = (miny - pad_y, maxy + pad_y)

    render_map1(biome_polys, xlim, ylim, os.path.join(outDir, "conservation_map1_ignition_count.png"))
    render_map2(biome_polys, xlim, ylim, os.path.join(outDir, "conservation_map2_severity.png"))
    render_map3(biome_polys, xlim, ylim, os.path.join(outDir, "conservation_map3_decade_trend.png"))

    print(f"Maps written to: {outDir}")


if __name__ == "__main__":
    main()
