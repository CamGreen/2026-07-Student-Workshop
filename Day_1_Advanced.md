# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 1 (Advanced Track)

*A companion track for honours-level GIS students, run alongside the standard 4-day workshop. Same data, same software, same deliverable-per-day philosophy — but today you rebuild, from raw points, several of the actual techniques Riskscape's production fire risk pipeline uses, entirely inside QGIS's built-in Processing tools. No coding required.*

---

## Day 1 (Advanced) — Rebuilding the Pipeline, One Step at a Time

You already know what a fire polygon, an ignition point, and a bioregion are. What you're going to do today that the standard track doesn't is **rebuild small, honest versions of the actual algorithms** that turned raw satellite detections into the polygons you'll be handed on other days — using nothing but QGIS's Processing Toolbox — and then hold your results up against the real thing to see where a simplified method holds up and where it quietly breaks down.

> **Real Pipeline Connection:** Every fire event polygon in `fire_events_clean_WC_final.gpkg` started life as a scatter of individual satellite heat detections. Riskscape's pipeline clusters those detections into events, builds a polygon around each cluster, and only then computes `area_km2`, `days_burned`, and `start_date`. Today you do the clustering and polygon-building steps yourself, using the ignition points as a stand-in for that raw detection scatter.

### Morning Session: Clustering Points Into Fires

1. **Load your working layers.** Start a fresh project and load `fire_ignitions_WC.gpkg` and, for later comparison, `fire_events_clean_WC_final.gpkg`. Don't style the second one yet — hide it for now so you're not tempted to peek while you build your own version.

2. **Find the real date range you're working with.** Open the ignition points' attribute table and sort by `start_date` — you already know how to do this. Note the earliest and latest date. You'll need the number of years this spans later today, so write it down now (round to the nearest whole year is fine).

   > **Checkpoint:** You should have a single number, something like "13 years," derived from a real min and max in your own data, not an assumption.

3. **Cluster the ignition points with DBSCAN.** Open the Processing Toolbox and search for **DBSCAN Clustering**. This is a real density-based clustering algorithm — it groups points together when enough of them sit within a given distance of each other, and treats isolated points as noise rather than forcing them into a cluster.
   - Set the **minimum cluster size** to **3**.
   - Set the **maximum distance between clustered points (epsilon)** to **800 metres**, and run it.
   - Open the output's attribute table. A new field (something like `CLUSTER_ID`) now tells you which cluster each point belongs to — a value of `-1` means that point was treated as noise.
   - Note how many distinct cluster IDs you got (sort or use the field's unique-values list).

   > **Real Pipeline Connection:** This is genuinely the same algorithm family the production pipeline uses to turn raw VIIRS satellite detections into fire events — DBSCAN, minimum cluster size of 3 points, exactly as you just set it. The one difference: Riskscape doesn't use a single fixed distance. Each day's clustering radius is scaled by that day's average wind speed, stretching from about 800 m in calm conditions up to about 1,500 m in the windiest conditions, because a satellite's heat detections from the same fire spread further apart when wind is dragging the fire (and its smoke/heat signature) across the landscape.

4. **Re-run the clustering at the windy end of the scale.** Run **DBSCAN Clustering** again on the same points, minimum cluster size still **3**, but this time set epsilon to **1,500 metres**. Compare the new cluster count to your first run.

   > **Think about it:** Did the cluster count go up or down when you widened the radius? Did any clusters merge together that were separate before? A wider radius should, in general, produce fewer, larger clusters — if yours didn't behave that way, look again at whether you're comparing the right output layers.

   > **Watch out:** `-1` (noise) is not "cluster number negative one" in any meaningful sense — it's QGIS's way of saying "this point had too few neighbours to belong to any cluster at this radius." Don't include noise points when you count or style clusters, or your numbers will be off by however many isolated ignitions you have.

5. **Turn your clusters into polygons.** Pick whichever of your two clustering runs you'd like to carry forward (the 800 m run is a reasonable default). Open the Processing Toolbox again and find **Minimum Bounding Geometry**.
   - Set the input to your clustered points layer.
   - Set the geometry type to **convex hull**.
   - Look for a field parameter that lets you group by your cluster ID field — set it there. Leaving this blank will build one giant shape around *all* your points instead of one shape per cluster, which is not what you want.
   - Run it. You should get one polygon per cluster: your own reconstruction of fire event boundaries, built entirely from points.

   > **Real Pipeline Connection:** The production pipeline does this same "points → one shape per cluster" step, but instead of a convex hull it uses a **concave hull** (a tighter-fitting outline that can wrap around indentations, rather than the simplest shape that contains every point) with a small buffer added afterward. A convex hull will systematically read as *larger* than a concave hull for the same points, sometimes considerably so for oddly shaped fires. Keep that in mind for the comparison you're about to do — some of the size difference you see is a genuine methodology gap, not a mistake.

6. **Compare your reconstruction to the real thing.** Turn on `fire_events_clean_WC_final.gpkg` and overlay it with your convex hull polygons.
   - How does your polygon count compare to the real event count in this area?
   - Pick two or three of your polygons and visually compare their shape and size to the nearest real fire event polygon underneath.

   > **Checkpoint:** You should be able to point to at least one of your polygons and say, concretely, "mine is bigger/smaller than the real one because [convex vs. concave hull / my fixed radius vs. their wind-scaled radius / a noise point that should have joined a cluster]." A vague "they look similar" is not a checkpoint pass — find a specific difference and explain it.

---

### Afternoon Session: From Fire Size to Fire Severity, and From One Fire to a Hazard Surface

This morning you rebuilt *where* fires are. This afternoon you build two of the derived quantities the real severity and frequency models actually use — and along the way, meet one CRS decision and one data-leakage decision that Riskscape's team had to make for real.

1. **Compute a proper severity proxy, not just size.** In the standard Day 1, students style fires by raw `area_km2` — a big fire and a slow-burning fire look the same if they cover the same ground. Open the field calculator on `fire_events_clean_WC_final.gpkg` and create a new field:

   ```
   burn_rate = area_km2 / days_burned
   ```

   Style this new field with graduated symbology, 5 classes, white to dark red — the same recipe you'd use for `area_km2`, just pointed at a different field.

   > **Real Pipeline Connection:** `area_km2 / days_burned` — burned area *per day* — is exactly the target variable Riskscape's severity model is trained to predict. It's not an approximation of their method; it's their actual definition of severity, because a fire that burns 50 km² in one day is a fundamentally more dangerous, faster-moving event than one that burns the same area over three weeks, even though `area_km2` alone can't tell them apart.

   > **Watch out:** Check your data for any `days_burned` value of 0 before you run the calculation — dividing by zero will either error or silently produce a null/infinite value depending on your QGIS version, and a handful of bad rows can wreck your colour classification without you noticing.

   > **Think about it:** Find a fire that ranks near the top by `area_km2` but *not* near the top by `burn_rate`, or vice versa. What does that pair tell you about the difference between "big" and "severe"?

2. **Do the CRS exercise that actually broke Riskscape's numbers once.** Your `fire_events_clean_WC_final.gpkg` layer already has a correct `area_km2` field, computed properly by the pipeline. You're going to recompute it yourself two different ways and see how much a CRS choice matters.
   - With your layer still in its current (geographic, EPSG:4326) CRS, open the field calculator and add a field using the `$area` expression. Don't convert units yet — just look at the raw number. It should look nothing like square kilometres, because `$area` in a geographic CRS returns square *degrees*, a unit with no consistent real-world size.
   - Now make a reprojected copy of the layer: right-click → Export → Save Features As, and choose a projected, **equal-area** CRS — search the CRS picker for **Africa Albers Equal Area Conic**.
   - On this reprojected copy, add `$area` again (now in square metres — divide by 1,000,000 for km²) and compare it to the original pipeline's `area_km2` field for the same fires.

   > **Real Pipeline Connection:** Riskscape's polygon-building step deliberately does all of its area and buffer calculations in an equal-area Albers projection, for exactly the reason you just saw: a common alternative like Web Mercator inflates area by roughly a third at South Africa's latitude, and a plain geographic CRS doesn't give you a real-world area unit at all. Choosing the right CRS for a calculation — not just for display — is a genuine, recurring engineering decision in this pipeline, not a one-time setup step.

   > **Checkpoint:** Your Albers-reprojected `$area` figures should land close to the pipeline's own `area_km2` values (small differences are fine — the pipeline additionally buffers each polygon by 150 m, which will always add a bit of area). Your raw EPSG:4326 `$area` figures should look wildly wrong by comparison. If they don't, double check you actually reprojected the layer rather than just changing the project's display CRS, which doesn't touch the underlying coordinates.

3. **Build your own fire frequency / hazard surface.** So far you've looked at individual fires. Now build a surface showing *where fire happens often*, independent of any one event's size.
   - Use **Create Grid** to build a regular grid of cells (a rectangular grid, roughly 5 km × 5 km cells, is a reasonable choice) covering the extent of your Western Cape fire events layer.
   - Use **Join Attributes by Location (Summary)** to join your grid to `fire_events_clean_WC_final.gpkg`, with the **count** summary statistic, so each grid cell picks up a field recording how many fire event *polygons* overlap it.
   - In the field calculator, divide that count by the number of years you noted back in step 2 of the morning session, to get a **fires-per-cell-per-year** frequency field.
   - Style the grid with graduated symbology on your new frequency field. This is your own simplified fire hazard surface.

   > **Real Pipeline Connection:** Riskscape maintains a real fire frequency product built the same way — a regular grid (theirs runs at roughly 2 km resolution nationally) where each cell records how many fire events have touched it, divided into a rate per year. It feeds a separate model from the severity one you met in `burn_rate` above: severity asks "how bad is a fire here," frequency asks "how often does one start here." They're deliberately kept as two different questions.

   > **Think about it — this one matters.** You joined *fire event polygons*, not ignition points, to build your frequency grid. What would go wrong if, later in the week, you also wanted to build a model that *predicts* fire occurrence using "distance to nearest past ignition point" as an input variable, and you'd built your frequency grid from those same ignition points? You'd be using the same information as both an answer and a clue for finding that answer — a mistake called **data leakage**, and it's a real design decision documented in Riskscape's own frequency pipeline: they deliberately build their frequency/occurrence *target* from full burned-area polygons rather than ignition points, specifically to avoid this trap.

4. **A short reflection on categories that need to stay stable.** Look back at the bioregion layer you'd have categorised by biome name in the standard Day 1 (categorized symbology, one colour per biome). That's a purely cartographic choice — but the same idea, "one column per category," is also exactly how Riskscape's models represent bioregion and rainfall-zone as numeric inputs to a machine learning model (a technique usually called one-hot encoding).

   > **Real Pipeline Connection:** This has bitten the production pipeline before. If the *set* of bioregion categories present in one batch of data doesn't exactly match the set the trained model expects — even a difference as small as one batch encoding a category as `6.0` and another as `6` — the resulting columns silently fail to line up, and every row touching that category can end up scored as if that variable were entirely absent, with no error message. The fix is to always encode against one **fixed, agreed list** of categories, never against "whatever categories happen to be in today's data."

   > **Think about it:** Why might this kind of bug be worse than one that crashes the program outright?

5. **Assemble a comparison layout.** Build a print layout with (at minimum) two maps side by side: your DBSCAN/convex-hull fire reconstruction next to the real `fire_events_clean_WC_final.gpkg` polygons, styled identically so the comparison is fair. If you have room, add your `burn_rate` choropleth and your frequency grid as a second row. Title, legend, north arrow, scale bar — you know the drill from the standard track.

### Deliverable

A short atlas (one print layout, multiple map frames) containing: your DBSCAN-reconstructed fire polygons next to the real fire event polygons for visual comparison; your `burn_rate` severity choropleth; and your fire frequency grid. Alongside it, a written paragraph (a few sentences is plenty) covering:
- One concrete difference between your reconstructed polygons and the real ones, and which methodology choice caused it.
- Whether your Albers-reprojected area calculation matched the pipeline's own `area_km2` field, and why the geographic-CRS version didn't.
- One sentence on the data leakage question from step 3 of the afternoon session.

Submit your atlas and written paragraph here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge: The Rare-Event Problem

This one is pen-and-calculator (or field-calculator) work, not a QGIS tool — a genuine piece of applied statistics from Riskscape's occurrence-modelling side, for students who want a harder problem.

Fire ignition, looked at as "did a fire start in this grid cell on this day," is a very rare event — the true rate might be something like 1 in 15,000 cell-days. If you tried to train any model on that data directly, almost every example would be a "no," and the model would learn almost nothing. Riskscape's real fix: keep every positive (a fire that did happen) and pair it with a random sample of negatives at a fixed ratio — say, 20 negatives for every 1 positive — then correct for the fact that this sample no longer reflects the true rarity of the event.

Work through it with these two numbers:
- `tau` = the *true* occurrence rate (small — you decide a plausible value, e.g. `0.0001`).
- `ybar` = the occurrence rate *in your artificially balanced sample* (with a 20:1 negative:positive ratio, this works out to `1/21 ≈ 0.048`).

Compute the correction that has to be subtracted from a model's raw prediction before it can be trusted as a real-world probability again:

```
offset = ln[ ((1 - tau) / tau) × (ybar / (1 - ybar)) ]
```

> **Think about it:** Why does undersampling the "no fire" cases and then not correcting for it produce a model that's systematically overconfident about fire risk everywhere?

---

Previous: [Before Day 1](README.md) · Continue with the advanced cohort: [Day 2 (Advanced Track)](Day_2_Advanced.md) · Reference: [Appendices](Appendices.md)
