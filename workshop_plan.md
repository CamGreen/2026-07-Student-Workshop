# QGIS Wildfire Risk Workshop — 4-Day Student Project Plan (Tuesday–Friday)

## Context

This workshop is built around a real South African fire risk modelling system developed at Riskscape. The system ingests NASA VIIRS satellite fire detections, processes them into fire event polygons, attaches climate and terrain variables, and runs a trained deep neural network (compiled as a Julia executable) to produce seasonal fire severity rasters at 500 m resolution across South Africa.

The data students will use comes directly from this pipeline:

- **Fire event polygons** — cleaned, final fire events going back to 2012, derived from VIIRS Suomi-NPP Collection 2 satellite detections clustered by an adaptive DBSCAN algorithm. Each polygon has attributes including area (km²), duration (days), and ignition location.
- **Ignition points** — the estimated point of origin for each fire event.
- **Bioregion shapefile** — the SANBI 2024 National Vegetation Map (NVM2024), classifying South Africa into ecological bioregions.
- **Seasonal NDVI rasters** — summer, autumn, winter, and spring normalised difference vegetation index derived from MODIS satellite imagery at 250 m resolution, averaged across 2012–2025.
- **Seasonal severity rasters** — the output of the trained fire severity model: predicted burned area per day (km²/day) for each season at 500 m resolution across South Africa.
- **Static grid** — a 500 m point grid covering South Africa with terrain variables (elevation, slope, aspect), rainfall seasonality zones, and bioregion attributes.

Students follow the same pipeline used to build this product, but in reverse — starting with the final model outputs and peeling back through the data to understand where the numbers came from. By the end they build their own simplified fire risk map and present it as a deliverable to a simulated insurance client.

---

## Overall Arc: "From Raw Data to Insurance Product"

Each day has a clear deliverable so students leave with something real they produced themselves.

| Day | Theme | Deliverable |
|-----|-------|-------------|
| 1 | GIS foundations — load, explore, style, layout | Styled fire event map with one written observation |
| 2 | Spatial analysis — connect fire to landscape | 4-panel seasonal severity map with written observations |
| 3 | Raster analysis — build your own risk model | Composite risk map compared to the trained model output |
| 4 | Capstone — same data, two client stories | Two slide decks (one per brief) with speaker notes, built individually |

**Assumed schedule:** ~6 working hours per day, two sessions of ~2.5 hours with a break between them.

---

## Day 1 — "What is GIS, and Where Does South Africa Burn?"

**Theme:** Foundations. Get data on screen, make it look good, ask basic questions.

### Morning Session: QGIS Orientation (2.5h)

1. **Interface tour** — panels, toolbars, map canvas, layer list. Spend 20 minutes clicking around with nothing loaded so students understand the layout before data appears.

2. **Load the SA boundary** — students load their first layer, zoom to it, and change the fill to transparent with a black border.

3. **Load fire event polygons** — immediately striking visual. Students spend time just exploring: zoom into the Cape, zoom into KZN, compare density. No analysis yet — just looking.

4. **Attribute table deep-dive** — introduce columns: `area_km2`, `days_burned`, `start_date`. Sort by area descending.
   - *Question to answer: What is the single largest fire in the dataset? When did it start? How many days did it burn?*

5. **Coordinate systems** — brief and practical only. Show the visual difference between EPSG:4326 (geographic, degrees) and a projected CRS (metres). Don't go deep — just enough that students understand why the choice matters and aren't confused later.

### Afternoon Session: Styling and First Map (2.5h)

1. **Graduated symbology** — style fire polygons by `area_km2`, 5 classes, white to dark red. Discuss: what does colour choice communicate? Try a sequential vs diverging palette and compare.

2. **Load ignition points** — style as small orange dots. Toggle between points and polygons. Discuss the relationship: one ignition point leads to one fire polygon.

3. **Load bioregion shapefile** — categorised by biome name, transparent fill, coloured borders. Visual question: *"Does the Fynbos biome burn differently to the Savanna biome? Can you tell just by looking?"*

4. **First map layout** — open print composer from scratch. Add: title, legend, north arrow, scale bar. Export as PNG.

### Day 1 Deliverable

A styled map of South African fire events by size with bioregions as context. Student adds one written annotation on the map describing something they noticed.

---

## Day 2 — "What Drives Fire?"

**Theme:** Spatial analysis — connecting fire occurrence to the landscape and terrain it burns through.

### Morning Session: Spatial Joins and Statistics (2.5h)

1. **Count points in polygon** — use QGIS's built-in tool (*Vector → Analysis → Count Points in Polygon*) to count how many ignition points fall in each bioregion. Students discover which biome has the most ignitions.

2. **Join attributes by location** — attach bioregion name to each fire event polygon. The fire events attribute table now has a biome column. Sort, filter, discuss.

3. **Basic statistics by category** — use *Vector → Analysis → Basic Statistics for Fields*. Compare mean `area_km2` per biome.
   - *Students produce a small table: "Fires in Fynbos average X km², fires in Savanna average Y km²."*

4. **Selection tools** — select by attribute (`area_km2 > 100`), select by location (fires intersecting a specific province). How many large fires are in each province?

### Afternoon Session: Terrain and Vegetation Context (2.5h)

1. **Load the NDVI summer raster** — introduce rasters properly: pixels, resolution, what the values mean. Apply a green colour ramp. Question: *"What does high NDVI mean physically? What does low NDVI mean?"*

2. **Load the severity raster** — apply RdYlGn colour ramp (reversed, so red = high severity). Overlay fire polygons on top. Students compare: *"Does the model predict high severity where fires actually burned?"*

3. **Raster value inspection** — use the *Identify* tool to click on pixels and read values. Students sample 10 random points, note the severity value, and record whether a real fire occurred there.

4. **Clip raster by extent** — clip the national severity raster to a single province to create a smaller working file. Introduces the concept of spatial subsetting.

5. **Load all 4 seasonal severity rasters** — students compare summer vs winter. Which season is most severe in the Western Cape? In Limpopo? Why might that differ?

### Day 2 Deliverable

A 4-panel seasonal severity map (summer / autumn / winter / spring) for one province. One paragraph of written observations about seasonal patterns.

---

## Day 3 — "Building a Risk Model"

**Theme:** Students build their own simplified fire risk map using the raster calculator — the most analytically demanding day.

### Morning Session: Raster Analysis Tools (2.5h)

1. **Zonal statistics** — for each bioregion polygon, compute mean and max severity from the summer raster (*Raster → Zonal Statistics*). Students get a table showing which bioregion has the highest predicted fire severity. Compare to yesterday's ignition count — do the two measures agree?

2. **Reclassify rasters** — reclassify the severity raster into 5 risk classes (1 = lowest, 5 = highest) using *Raster → Reclassify by Table*. This converts a continuous variable into a categorical risk score.

3. **Reclassify NDVI** — invert it: high NDVI (lush, green) = lower fire risk; low NDVI (dry, sparse) = higher risk. Reclassify to a 1–5 scale. Discuss: *"Why does drier vegetation mean higher fire risk? What is it actually representing?"*

4. **Introduce composite index concept** — *"You now have two risk layers. How do you combine them into one map? Should they be weighted equally?"* Discuss: severity is probably more important than NDVI — perhaps 60/40.

### Afternoon Session: Build Their Own Risk Map (2.5h)

1. **Raster calculator** — combine the two reclassified rasters with a weighted formula:
   ```
   ("severity_reclass@1" * 0.6) + ("ndvi_reclass@1" * 0.4)
   ```
   Students produce their first composite risk raster. Apply a red colour ramp.

2. **Compare to the model output** — overlay their composite risk map against the trained model's severity raster. Are they similar? Where do they disagree? Discussion: the trained model used 170+ input variables; students used 2. This is a moment to appreciate why the full pipeline exists.

3. **Extension (fast finishers):** add a slope layer from the static grid as a third term. Steeper terrain = faster fire spread. Students modify their raster calculator formula to include it.

4. **Risk summary for a specific area** — pick one district municipality. What proportion of its area falls into each risk class? Use *Zonal Statistics* or estimate visually. Students produce a simple summary table.

### Day 3 Deliverable

A composite risk map for one province. A side-by-side comparison of their model and the trained model output. A written explanation of what their model captures and what it misses.

---

## Day 4 (Half Day) — "Presenting to the Client"

**Theme:** Capstone. Students synthesise everything into a professional map atlas and package it as a slide deck. Individual work — no pairs or groups.

### Morning: Final Product (2–2.5h)

Students choose one of three client briefs and produce a 3-map atlas to answer it. All required data has already been loaded in previous days.

---

**Brief A — The Insurer**

*"Which municipalities in the Western Cape should we charge the highest wildfire premiums? Show us the evidence."*

- Map 1: Fire frequency (ignition density heatmap) by municipality
- Map 2: Seasonal severity raster with fire event overlay
- Map 3: Composite risk index with municipality boundaries

---

**Brief B — The Conservation Planner**

*"Which bioregions are burning most severely, and is fire frequency changing over time?"*

- Map 1: Ignition count per bioregion (choropleth from zonal count)
- Map 2: Mean severity per bioregion (from zonal statistics)
- Map 3: Early period vs late period comparison (split fire events by `start_date` decade)

---

**Brief C — The Emergency Manager**

*"Where are the largest fire events, and what landscape features are they associated with?"*

- Map 1: Top 50 largest fires by area, styled and labelled
- Map 2: Those fires overlaid on NDVI and slope
- Map 3: Composite risk map highlighting those areas

---

### Build Your Presentation (1h)

No live presenting — each student builds their own short PowerPoint deck (6–8 slides) with full speaker notes on every slide, as if presenting to the client. Closing slide covers the debrief questions as personal reflection:

- *"What surprised you most about the data?"*
- *"What would you do differently if you had another day?"*
- *"What data do you wish you had that we didn't give you?"*
- *"If you were the client, would you trust this analysis? Why or why not?"*

---

## Data Package for Students

Pre-clip all layers to one province (Western Cape recommended — dramatic fire patterns, manageable size, good seasonal contrast). Students should open one `.qgz` project file and have everything appear without troubleshooting file paths.

| File | Source in pipeline |
|------|--------------------|
| `sa_boundary.gpkg` | Any SA admin boundary |
| `province_boundary.gpkg` | Clipped to chosen province |
| `fire_events_clean.gpkg` | Output of `07_remove_manual_sites.py` |
| `fire_ignitions.gpkg` | Ignition points from `04_dissolve_events.py` |
| `bioregions.shp` | Sanbi NVM2024 shapefile |
| `severity_mean_summer.tif` | Output of `4_build_severity_rasters.py` |
| `severity_mean_autumn.tif` | Output of `4_build_severity_rasters.py` |
| `severity_mean_winter.tif` | Output of `4_build_severity_rasters.py` |
| `severity_mean_spring.tif` | Output of `4_build_severity_rasters.py` |
| `ndvi_summer.tif` | Output of `5_build_ndvi_rasters.py` |

All rasters should be pre-projected to EPSG:4326 to avoid CRS mismatch errors.

---

## Skills Progression

| Day | New concepts introduced |
|-----|-------------------------|
| 1 | Interface navigation, vector data, attribute tables, graduated/categorised symbology, map layouts |
| 2 | Spatial joins, statistics by category, raster data, seasonal comparison, clipping |
| 3 | Zonal statistics, reclassification, raster calculator, composite index design |
| 4 | Independent analysis, professional cartography, presenting spatial evidence |

---

## Workshop Delivery Notes

**Pre-load a `.qgz` project file for each day** with the correct layers already present and default styles applied. Students spend time learning, not troubleshooting missing files.

**Progression of independence across the days:**
- Day 1: Follow step-by-step instructions exactly
- Day 2: Instructions given, students choose their own styling and colours
- Day 3: Goal given, method suggested, students figure out the steps
- Day 4: Goal only — students plan their own approach

**Checkpoint every 45–60 minutes:** stop the class, show one student's screen on the projector, ask others to compare. Normalises that every map looks different.

**Extension tasks for fast finishers** on each day so no one sits idle:
- Day 1: Add rainfall seasonality zones (RSZ) to the map
- Day 2: Try computing fire density (fires per 100 km²) per bioregion manually
- Day 3: Add a third variable (slope or FWI severity) to the composite risk model
- Day 4: Add a data table or chart to the print layout alongside the maps

**One-page QGIS cheat sheet** with screenshots: where the Layer menu is, how to open an attribute table, where the raster calculator lives, how to open print composer. Saves answering the same question repeatedly.
