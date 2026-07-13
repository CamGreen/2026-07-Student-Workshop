"""
Last Update:
2026-07-07
Cameron Green

day3_advanced_memo.py
======================
ANSWER MEMO for Day 3 (Advanced Track). Instructor reference only — not for
distribution to students.

Standard Day 3 hand-picks two weights (e.g. 0.6 severity / 0.4 NDVI) and blends
reclassified severity + NDVI into a composite risk raster. This script trains a
small, fully transparent scikit-learn LinearRegression on real fire outcomes to
derive a data-driven weight pair instead, and compares it against a hand-picked
guess -- without ever touching or approximating Riskscape's real trained model.
The target is always real fire behaviour (area_per_day), never the severity
raster's own values, so this stays a model of fire outcomes, not a surrogate of
the production model.

Input : Data/fire_events_clean.gpkg
        Data/fire_ignitions.gpkg
        Data/severity_rasters/severity_mean_summer.tif
        Data/ndvi_rasters/ndvi_summer.tif
        Data/output_SRTMGL3_slope.tif        (optional 3-feature extension)
Output: hand-picked vs. learned weights, test-set R^2, and a learned-weight
        composite risk raster written alongside the input rasters.

Run from the `firerisk` conda environment set up in Day_2_Advanced.md, plus:
    conda install -c conda-forge scikit-learn
"""

import os
import time
import datetime
import logging

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# =============================================================================
# LOGGING SETUP
# =============================================================================
_script_name = "day3_advanced_memo"
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
dataDir          = "../Data"
fireEventsPath   = os.path.join(dataDir, "fire_events_clean.gpkg")
ignitionsPath    = os.path.join(dataDir, "fire_ignitions.gpkg")
severityTif      = os.path.join(dataDir, "severity_rasters", "severity_mean_summer.tif")
ndviTif          = os.path.join(dataDir, "ndvi_rasters", "ndvi_summer.tif")
slopeTif         = os.path.join(dataDir, "output_SRTMGL3_slope.tif")
outputCompositeHandPicked = "composite_risk_handpicked.tif"
outputCompositeLearned    = "composite_risk_learned.tif"

# =============================================================================
# CONFIG
# =============================================================================
# The hand-picked guess a standard-track student might reasonably defend:
# severity already blends fuel/weather/terrain (via the real model), so it should
# outweigh a single vegetation-dryness proxy on its own.
handPickedWeights = {"severity": 0.6, "ndvi": 0.4}

nClasses = 5              # same 1-5 scheme as standard Day 3's Reclassify by Table
testFraction = 0.2
randomState = 42          # fixed so the train/test split is reproducible
enableThirdFeatureExtension = False
enableTreeModelExtension = False


# =============================================================================
# STEP 1 — Rebuild yesterday's training table (severity, ndvi, area_per_day)
# =============================================================================
def sample_raster(path, coords):
    with rasterio.open(path) as src:
        nodata = src.nodata
        values = np.array([v[0] for v in src.sample(coords)], dtype=float)
    if nodata is not None:
        values[values == nodata] = np.nan
    return values


def load_training_table():
    fires = gpd.read_file(fireEventsPath)
    ignitions = gpd.read_file(ignitionsPath)

    coords = [(geom.x, geom.y) for geom in ignitions.geometry]
    ignitions["severity"] = sample_raster(severityTif, coords)
    ignitions["ndvi"] = sample_raster(ndviTif, coords)

    # Watch out: fire_ignitions.gpkg already has its own area_per_day column,
    # distinct from the one on fire_events_clean.gpkg -- drop it before merging
    # or pandas silently produces area_per_day_x / area_per_day_y instead.
    ignitions = ignitions.drop(columns=["area_per_day"], errors="ignore")
    merged = ignitions.merge(fires[["event_id", "area_per_day"]], on="event_id")
    merged = merged.dropna(subset=["severity", "ndvi", "area_per_day"])

    log.info(f"Training table: {len(merged):,} ignition points with severity, "
             f"ndvi, and area_per_day")

    # Every row here is a place a fire DID happen -- worth naming explicitly as a
    # sampling bias before it's forgotten further down the pipeline.
    log.info("Note: training data is drawn only from places fires occurred -- "
             "no negative (no-fire) examples are represented.")
    return merged, fires


# =============================================================================
# STEP 2 — Reclassify severity / ndvi into the same 1-5 scheme as standard Day 3
# =============================================================================
def reclassify_with_edges(series, n_classes=nClasses, invert=False):
    """Quantile-based reclassification. Returns (class_labels, bin_edges) so the
    same edges can be reused when reclassifying the full raster later -- using
    fresh quantiles on the raster would silently redefine what each class means."""
    labels = list(range(1, n_classes + 1))
    if invert:
        labels = labels[::-1]
    classes, edges = pd.qcut(series, q=n_classes, labels=labels, retbins=True, duplicates="drop")
    return classes.astype(int), edges


def build_features(df):
    df = df.copy()
    df["severity_class"], severity_edges = reclassify_with_edges(df["severity"], invert=False)
    df["ndvi_class"], ndvi_edges = reclassify_with_edges(df["ndvi"], invert=True)  # low ndvi -> high risk

    log.info("severity_class distribution:\n" + df["severity_class"].value_counts().sort_index().to_string())
    log.info("ndvi_class distribution:\n" + df["ndvi_class"].value_counts().sort_index().to_string())

    return df, severity_edges, ndvi_edges


# =============================================================================
# STEP 3 — Train/test split, standardize, fit
# =============================================================================
def fit_learned_weights(df):
    X = df[["severity_class", "ndvi_class"]].astype(float)
    y = df["area_per_day"].astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=testFraction, random_state=randomState
    )

    scaler = StandardScaler().fit(X_train)          # fit on train only -- no test leakage
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression().fit(X_train_scaled, y_train)
    r2 = model.score(X_test_scaled, y_test)

    raw_coefs = model.coef_       # order: [severity_class, ndvi_class]
    coef_sum = raw_coefs.sum()
    if coef_sum == 0:
        log.info("Coefficients summed to zero -- falling back to equal weights")
        learned_weights = {"severity": 0.5, "ndvi": 0.5}
    else:
        learned = raw_coefs / coef_sum
        learned_weights = {"severity": float(learned[0]), "ndvi": float(learned[1])}

    log.info(f"Raw coefficients (severity, ndvi): {raw_coefs}")
    log.info(f"Learned weights (normalized to sum to 1): {learned_weights}")
    log.info(f"Test-set R^2: {r2:.4f}")

    if any(w < 0 for w in learned_weights.values()):
        log.info("Note: a learned weight is negative -- this means that feature "
                 "moved opposite to area_per_day in this sample. Worth discussing, "
                 "not assuming it's a bug.")

    return model, scaler, learned_weights, r2


# =============================================================================
# STEP 4 — Apply weights across the full raster
# =============================================================================
def reclassify_array(array, edges, invert=False):
    n_classes = len(edges) - 1
    classes = np.digitize(array, edges[1:-1], right=True) + 1
    classes = np.clip(classes, 1, n_classes)
    if invert:
        classes = (n_classes + 1) - classes
    return classes.astype(float)


def build_composite_raster(weights, severity_edges, ndvi_edges, out_path):
    with rasterio.open(severityTif) as sSrc:
        severityArr = sSrc.read(1).astype(float)
        profile = sSrc.profile
        severityNodata = sSrc.nodata

    with rasterio.open(ndviTif) as nSrc:
        ndviArr = nSrc.read(1).astype(float)

    severityClass = reclassify_array(severityArr, severity_edges, invert=False)
    ndviClass = reclassify_array(ndviArr, ndvi_edges, invert=True)

    composite = weights["severity"] * severityClass + weights["ndvi"] * ndviClass

    if severityNodata is not None:
        composite[severityArr == severityNodata] = severityNodata

    profile.update(dtype="float32", count=1, nodata=severityNodata)
    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(composite.astype("float32"), 1)

    log.info(f"Wrote composite raster ({weights}) -> {out_path}")


# =============================================================================
# OPTIONAL EXTENSION — third feature (slope) + tree-based model comparison
# =============================================================================
def add_slope_feature(df):
    ignitions = gpd.read_file(ignitionsPath)
    coords = [(geom.x, geom.y) for geom in ignitions.geometry]
    slope_values = sample_raster(slopeTif, coords)
    ignitions = ignitions[["event_id"]].copy()
    ignitions["slope"] = slope_values
    merged = df.merge(ignitions, on="event_id", how="left").dropna(subset=["slope"])
    merged["slope_class"], _ = reclassify_with_edges(merged["slope"], invert=False)
    log.info(f"Added slope feature to {len(merged):,} rows")
    return merged


def compare_tree_model(df):
    X = df[["severity_class", "ndvi_class"]].astype(float)
    y = df["area_per_day"].astype(float)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=testFraction, random_state=randomState
    )
    tree = RandomForestRegressor(n_estimators=200, random_state=randomState).fit(X_train, y_train)
    train_score = tree.score(X_train, y_train)
    test_score = tree.score(X_test, y_test)
    log.info(f"RandomForest train R^2={train_score:.4f}  test R^2={test_score:.4f}")
    if train_score - test_score > 0.2:
        log.info("Large train/test gap -- classic overfitting signature with this "
                 "few features and rows.")
    log.info(f"Feature importances (severity, ndvi): {tree.feature_importances_}")
    return tree


# =============================================================================
# MAIN
# =============================================================================
def main():
    t0 = time.time()
    log.info("=" * 65)
    log.info(f"Script  : {_script_name}")
    log.info("Step    : Day 3 (Advanced) answer memo")
    log.info(f"Log file: {_log_path}")
    log.info("=" * 65)

    log.info(f"Hand-picked weights (the guess a student might defend): {handPickedWeights}")

    log.info("-" * 65)
    log.info("Step 1-2: training table + reclassification")
    log.info("-" * 65)
    df, fires = load_training_table()
    df, severity_edges, ndvi_edges = build_features(df)

    log.info("-" * 65)
    log.info("Step 3: fit learned weights")
    log.info("-" * 65)
    model, scaler, learned_weights, r2 = fit_learned_weights(df)

    log.info("-" * 65)
    log.info("Step 4: build composite rasters (hand-picked vs. learned)")
    log.info("-" * 65)
    build_composite_raster(handPickedWeights, severity_edges, ndvi_edges, outputCompositeHandPicked)
    build_composite_raster(learned_weights, severity_edges, ndvi_edges, outputCompositeLearned)

    log.info("-" * 65)
    log.info("Summary")
    log.info("-" * 65)
    log.info(f"  Hand-picked : severity={handPickedWeights['severity']:.2f}  ndvi={handPickedWeights['ndvi']:.2f}")
    log.info(f"  Learned     : severity={learned_weights['severity']:.2f}  ndvi={learned_weights['ndvi']:.2f}")
    log.info(f"  Test R^2    : {r2:.4f}")

    if enableThirdFeatureExtension:
        log.info("-" * 65)
        log.info("Optional extension: third feature (slope)")
        log.info("-" * 65)
        df_slope = add_slope_feature(df)
        # Refit with severity_class + ndvi_class + slope_class using the same
        # fit_learned_weights logic, generalized to N features -- left as an
        # exercise to extend fit_learned_weights() rather than duplicating it here.

    if enableTreeModelExtension:
        log.info("-" * 65)
        log.info("Optional extension: tree-based model comparison")
        log.info("-" * 65)
        compare_tree_model(df)

    log.info("=" * 65)
    log.info(f"Done — total elapsed: {(time.time() - t0) / 60:.1f} min")
    log.info("=" * 65)


if __name__ == "__main__":
    main()
