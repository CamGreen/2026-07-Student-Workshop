# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 2 (Advanced Track)

*A companion track for honours-level GIS students, run alongside the standard 4-day workshop. Same data, same deliverable-per-day philosophy — but where Day 1 Advanced stayed entirely inside QGIS's own tools, today you step outside it. You'll set up a real, isolated Python environment with Miniconda, write code in VS Code, and analyse the same fire, bioregion, NDVI, and severity data using the same kind of standalone Python that Riskscape's actual pipeline is built from.*

---

## Before You Start: Setting Up Your Python Environment

Professional geospatial and data science work is almost never done by clicking through a GUI one dataset at a time — it's scripted, versioned, and re-runnable. Two pieces of software make that practical: **Miniconda**, which gives you an isolated, self-contained set of Python packages that can't be broken by (or break) anything else on your laptop, and **VS Code**, a proper code editor with debugging built in.

1. **Install Miniconda3.** Your instructor will provide the installer the same way QGIS was provided — by USB stick, shared drive, or download link. Run it and accept the defaults. When it asks about adding Miniconda to your PATH, you can leave that unticked — you'll launch everything from the **Anaconda Prompt (miniconda3)** entry in your Start Menu instead, which avoids a common Windows conflict where multiple Python installs fight over the PATH.

   > **Checkpoint:** Open **Anaconda Prompt (miniconda3)** from the Start Menu and run `conda --version`. You should see a version number printed, not an error.

2. **Create a dedicated virtual environment for this workshop.** A virtual environment is just a named, isolated set of packages — creating one for this workshop means nothing you install here can conflict with anything else on your machine, now or later.

   ```
   conda create -n firerisk python=3.11
   conda activate firerisk
   ```

   > **Checkpoint:** Your prompt should now start with `(firerisk)`. That prefix tells you which environment is currently active — get in the habit of checking it before running any code.

3. **Install the geospatial packages.**

   ```
   conda install -c conda-forge geopandas rasterio matplotlib
   ```

   > **Watch out:** `geopandas` and `rasterio` both wrap C libraries (GDAL, among others) that are notoriously fiddly to install correctly on Windows with plain `pip`. Installing from the `conda-forge` channel, as above, handles that dependency chain properly. This step also needs an internet connection and can take several minutes — do it well before your session starts, not live in front of the room.

4. **Set up VS Code.**
   - Open VS Code and install the **Python** extension from the Extensions panel (the icon with four squares on the left sidebar).
   - Use **File > Open Folder** to open your workshop folder.
   - Create a new file called `day2_advanced.py` — a plain Python script, not a notebook. You'll write it top to bottom and run the whole thing at once, the same way the real pipeline scripts you've heard about all week are run.
   - Open the Command Palette (**Ctrl+Shift+P**), run **Python: Select Interpreter**, and choose your `firerisk` conda environment from the list.

   > **Hint:** If `firerisk` doesn't show up in the interpreter list, close and fully reopen VS Code — it usually only refreshes the list of available environments on startup.

   > **Checkpoint:** Put this at the top of `day2_advanced.py` and run it (the ▷ **Run Python File** button in the top-right corner, or `python day2_advanced.py` in the integrated terminal):
   > ```python
   > import geopandas as gpd
   > import rasterio
   > print(gpd.__version__, rasterio.__version__)
   > ```
   > You should see two version numbers printed, not an import error. If you get `ModuleNotFoundError`, double-check the interpreter selected for this file is actually `firerisk`, not your system's default Python.

---

## Morning Session: Scripting the Vector Analysis

Everything you did in the standard Day 2 morning session — filter to one biome, run a tool, note the number, repeat — is exactly the kind of repetitive work Riskscape's real pipeline never does by hand. When new fire data lands, the same statistics get recomputed for every bioregion, every province, every season, automatically, by a script. Today you write small pieces of that script yourself.

1. **Load the data as GeoDataFrames.**

   ```python
   import geopandas as gpd

   fires = gpd.read_file("../Data/fire_events_clean.gpkg")
   bioregions = gpd.read_file("../Data/bioregions.gpkg")
   print(fires.head())
   ```

   A GeoDataFrame is just a pandas DataFrame with an extra `geometry` column attached — everything you already know about filtering, sorting, and grouping a table still applies here, plus spatial operations like joins and area calculations.

2. **Check your CRSs match before joining anything.** Don't assume every layer in the data folder shares one CRS just because it's supposed to — check it:

   ```python
   print(fires.crs)
   print(bioregions.crs)
   ```

   `bioregions.gpkg` isn't guaranteed to come through in the same CRS as the fire layers. If the two don't match, reproject before doing anything spatial with them together:

   ```python
   if bioregions.crs != fires.crs:
       bioregions = bioregions.to_crs(fires.crs)
   ```

   > **Watch out:** A CRS mismatch here doesn't raise an error. `sjoin` just quietly returns zero matches, because the two layers' coordinates no longer land on the same part of the map — everything runs, nothing crashes, and your `T_BIOME` column comes back entirely empty. Always check and reproject explicitly rather than assume.

3. **Do this morning's spatial join in code.** This mirrors the "Join Attributes by Location" step from the standard Day 2 morning session — attaching each fire event's bioregion name based on where it sits on the map, not a shared ID.

   ```python
   fires_with_biome = gpd.sjoin(
       fires, bioregions[["T_BIOME", "geometry"]],
       how="left", predicate="intersects"
   )
   ```

   > **Watch out:** Exactly like the QGIS dialog, `sjoin` can produce more than one output row for a single fire if its polygon overlaps two bioregions. Check `len(fires_with_biome)` against `len(fires)` — if it's grown, you have fires touching more than one bioregion to think about.

   > **Checkpoint:** `fire_events_clean.gpkg` already ships with its own pre-built `biome` column from the real pipeline. Compare `fires_with_biome["T_BIOME"]` against `fires_with_biome["biome"]` for a handful of rows as an independent check that your join worked — if they disagree, this is worth digging into before moving on.

4. **Per-biome stats, two ways.** First, write it as an explicit loop, so you can see exactly what's happening:

   ```python
   for biome in fires_with_biome["T_BIOME"].dropna().unique():
       subset = fires_with_biome[fires_with_biome["T_BIOME"] == biome]
       print(biome, len(subset), subset["area_km2"].mean())
   ```

   Then write the same thing the way you'd actually do it in real code:

   ```python
   biome_stats = fires_with_biome.groupby("T_BIOME")["area_km2"].agg(["count", "mean"])
   print(biome_stats)
   ```

   > **Real Pipeline Connection:** Production code almost always looks like the second version. The loop is how you reason through *what* you want; `groupby` is how you'd actually write it once you know. Both compute the same numbers — confirm that for yourself by checking one biome's mean matches in both versions, and against what you found by hand in this morning's standard session.

5. **Automate the fire-density extension challenge.** This morning's extension asked you to compute fires per 100 km² by hand, biome by biome. Fold it into the same script.

   - Just as in Day 1 Advanced's CRS exercise, `.area` in a geographic CRS (like EPSG:4326, which `bioregions` is now in after step 2's reprojection) gives you square *degrees*, not square kilometres. Reproject to an equal-area CRS first:
     ```python
     bioregions_albers = bioregions.to_crs("ESRI:102022")  # Africa Albers Equal Area Conic
     bioregions["area_km2"] = bioregions_albers.area / 1_000_000
     ```
   - Join your per-biome fire counts from step 3 onto `bioregions`, then compute `density = (fire_count / area_km2) * 100`.
   - Sort by density, descending, and print it.

   > **Think about it:** Does the ranking change once you divide by area, compared to your raw fire-count ranking? If it does, which ranking would you actually show a client trying to decide where fire risk is highest — raw counts, or counts per unit area? There's a real argument for either, depending on the question being asked.

---

## Afternoon Session: From Manual Sampling to a Real Correlation

This morning you scripted vector work. This afternoon you script the raster sampling you did by hand — clicking 10 pixels with the Identify tool — and turn it into something with real statistical weight: every ignition point instead of 10, and an actual correlation coefficient instead of an eyeball check.

1. **Sample the severity and NDVI rasters at every ignition point.** `rasterio`'s `.sample()` method takes a raster and a list of coordinates and returns the pixel value at each one — no loop-and-click required.

   ```python
   import rasterio

   ignitions = gpd.read_file("../Data/fire_ignitions.gpkg")
   coords = [(geom.x, geom.y) for geom in ignitions.geometry]

   with rasterio.open("../Data/severity_rasters/severity_mean_summer.tif") as src:
       ignitions["severity"] = [v[0] for v in src.sample(coords)]

   with rasterio.open("../Data/ndvi_rasters/ndvi_summer.tif") as src:
       ignitions["ndvi"] = [v[0] for v in src.sample(coords)]
   ```

   > **Watch out:** `.sample()` expects coordinates in the raster's own CRS. Everything in this workshop is EPSG:4326, so you're fine here — but this exact assumption (my points and my raster are definitely in the same CRS) is one of the most common silent-failure points in real spatial pipelines. It's worth checking explicitly rather than assuming, even when you're fairly sure.

   > **Real Pipeline Connection:** This is genuinely how every one of the 170+ input variables in the real severity model gets attached to every fire event — sampling a raster value at a point location, at national scale, thousands of times over. You just wrote a small, honest version of that step.

2. **Bring in the target variable.** `fire_events_clean.gpkg` already carries `area_per_day` — the same burned-area-per-day severity proxy Day 1 Advanced built by hand as `burn_rate`. Join it on using `event_id`, the shared key between ignitions and fire events:

   ```python
   merged = ignitions.merge(fires[["event_id", "area_per_day"]], on="event_id")
   ```

   > **Watch out:** `fire_ignitions.gpkg` already has its own `area_per_day` column (a different, per-ignition-point value). Merging without addressing that gives you `area_per_day_x` and `area_per_day_y` instead of the single column the rest of this exercise expects — check `merged.columns` after this step, and if you see the `_x`/`_y` suffixes, drop `ignitions`' own copy of the column before merging.

3. **Write your own correlation coefficient — no library, just the formula — then check it against the real thing.** Implement Pearson's r yourself for a pair of columns:

   ```
   r = ( n*Σ(xy) - Σx*Σy ) / sqrt( (n*Σ(x²) - (Σx)²) * (n*Σ(y²) - (Σy)²) )
   ```

   Compute it twice: once for (`severity`, `area_per_day`), once for (`ndvi`, `area_per_day`). Then compare both results against the one-line version:

   ```python
   print(merged[["severity", "ndvi", "area_per_day"]].corr())
   ```

   > **Checkpoint:** Your hand-rolled values should match pandas' `.corr()` output to a few decimal places. If they don't, you have a bug in your formula, not a surprising real-world result — and either way, both numbers must land between -1 and 1.

   > **Real Pipeline Connection / Think about it:** This is a hand-rolled version of the very first thing a data scientist does before training any model on a candidate variable — checking whether it's even related to the thing you're trying to predict. Which of severity or NDVI correlates more strongly with `area_per_day`? Does that match what you'd have guessed from yesterday's overlay-and-eyeball comparison, or did putting a real number on it change your answer?

4. **Optional extension: a fuel continuity proxy, scripted.** The real severity model includes a measure of *fuel continuity* — whether flammable vegetation forms one continuous patch or a fragmented mosaic — which affects how fast a fire can spread. You have a rough stand-in for this already: the slope raster's local variability. Install one more package first:

   ```
   conda install -c conda-forge rasterstats
   ```

   Then compute the standard deviation of slope within each bioregion polygon:

   ```python
   from rasterstats import zonal_stats

   stats = zonal_stats(bioregions, "../Data/output_SRTMGL3_slope.tif", stats=["std", "mean"])
   ```

   A bioregion with a high standard deviation of slope has more varied, "chopped-up" terrain than one with a flat, uniform slope — a crude but genuine terrain-fragmentation signal.

   > **Real Pipeline Connection:** This is a simplified stand-in for a real feature in Riskscape's production model. The real fuel continuity measure comes from land-cover classes rather than terrain roughness, but the underlying idea — how "patchy" is the landscape at this location — is the same one.

### Deliverable

A single standalone script, `day2_advanced.py`, that runs top to bottom with no errors and prints:
- The per-biome stats (both the loop and the `groupby` version).
- The fire density table, ranked by density descending.
- Both correlation results — your hand-rolled Pearson r and pandas' `.corr()` — for severity and for NDVI against `area_per_day`.

At the bottom of the script, add a comment block with two or three sentences: which of severity or NDVI correlates more strongly with actual fire behaviour, and one thing that surprised you about moving from a GUI to a script. Your submission is the one `.py` file — no separate notebook or write-up.

Submit your `.py` file here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge: Build Your Own NDVI From Raw Bands

NDVI isn't handed down from nowhere — it's calculated from two satellite bands, red and near-infrared, as `(NIR - Red) / (NIR + Red)`. This extension needs the raw red and near-infrared band rasters, which aren't currently part of the workshop data folder — flag it with your instructor if you'd like to attempt this one, since it depends on sourcing that extra pair of rasters first.

If they're available:

```python
import numpy as np

with rasterio.open("red_band.tif") as src:
    red = src.read(1).astype(float)
with rasterio.open("nir_band.tif") as src:
    nir = src.read(1).astype(float)

with np.errstate(divide="ignore", invalid="ignore"):
    ndvi = (nir - red) / (nir + red)
```

Compare your result pixel-for-pixel against the provided `ndvi_summer.tif`. They should match closely — small differences are expected, since the provided raster is a multi-year seasonal average rather than a single date's imagery.

---

Previous: [Day 1 (Advanced Track)](Day_1_Advanced.md) · Continue with the advanced cohort: [Day 3 (Advanced Track)](Day_3_Advanced.md) · Reference: [Appendices](Appendices.md)
