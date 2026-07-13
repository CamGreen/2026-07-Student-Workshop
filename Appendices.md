# Appendices — Mapping Wildfire Risk in South Africa: A QGIS Student Workbook

Shared reference material for all days: a cheat sheet, a troubleshooting guide, a glossary, a pointer to keep learning after the workshop, how to get in touch afterwards, and (for the Riskscape team) the full photo list.

## Appendix: One-Page QGIS Cheat Sheet

A quick reference for every tool you have used in this workshop. If you forget where something lives, check here before asking.

| Tool | Where to find it |
|---|---|
| Add a layer | Layer menu > Add Layer |
| Open an attribute table | Right-click the layer in the Layers panel > Open Attribute Table |
| Style a layer | Right-click the layer > Properties, then the Symbology tab |
| Build a final map | Print Layout tool (toolbar icon, or Project menu) |
| Raster Calculator | Raster menu > Raster Calculator |
| Zonal Statistics | Raster menu > Zonal Statistics |
| Reclassify by Table | Raster menu > Reclassify by Table |
| Count Points in Polygon | Vector menu > Analysis > Count Points in Polygon |
| Join Attributes by Location | Vector menu > Analysis > Join Attributes by Location |
| Basic Statistics for Fields | Vector menu > Analysis > Basic Statistics for Fields |
| Identify a feature | Identify tool (toolbar icon, looks like an "i" in a circle) |
| Select features | Select by Attribute or Select by Location (both found via the Select toolbar or Vector-related menus) |
| DBSCAN Clustering *(Advanced Track)* | Processing Toolbox > search "DBSCAN" |
| Minimum Bounding Geometry *(Advanced Track)* | Processing Toolbox > search "Minimum Bounding Geometry" |
| Create Grid *(Advanced Track)* | Processing Toolbox > search "Create Grid" |
| Join Attributes by Location (Summary) *(Advanced Track)* | Processing Toolbox > search "Join Attributes by Location (Summary)" |
| Reproject Layer *(Advanced Track)* | Processing Toolbox > search "Reproject Layer", or right-click a layer > Export > Save Features As |
| Anaconda Prompt (miniconda3) *(Advanced Track)* | Start Menu > Anaconda Prompt (miniconda3) — use this to create/activate conda environments and install packages |
| Select a Jupyter kernel in VS Code *(Advanced Track)* | Top-right corner of an open `.ipynb` file > Select Kernel > choose your conda environment |

> **Hint:** Most of these dialogs remember your last settings, so double-check every field before you click Run, especially the output file location.

## Appendix: Troubleshooting

Every beginner hits these snags. Work through the matching fix before you ask for help.

- **A layer will not show up on the map.**
  - Check the little checkbox next to the layer's name in the Layers panel. If it is unticked, the layer is loaded but hidden.
  - If it is ticked and still invisible, right-click the layer and choose Zoom to Layer. Your map might just be looking at the wrong part of the world.

- **A layer looks like it is in the wrong place (shifted, tiny, or off in the ocean somewhere).**
  - This is almost always a CRS problem. A CRS (coordinate reference system) is the mathematical system that says how coordinates map onto the real world.
  - Right-click the layer > Properties and check its CRS. Everything in this workshop should be EPSG:4326.

- **The print layout is blank.**
  - A print layout only shows what you explicitly put into it. If you have not added a map item to the layout yet, it will look empty even though your project has data.

- **The Raster Calculator refuses to run, or gives an error.**
  - Check that the layer names in your expression match the actual layer names exactly, including the `@1` band suffix.
  - Check that your output file location is valid, for example, a folder that exists and that you have permission to write to.

- **Files are not found when opening a project.**
  - Never move or rename anything inside the data folder. QGIS projects store links to files by their original location, and renaming or moving files breaks those links.
  - Keep the folder structure exactly as it was given to you.

> **Watch out:** If you have already moved or renamed a file and broken a link, do not panic. Put the file back with its original name in its original folder, and the link should repair itself the next time you open the project.

## Appendix: Glossary of Terms

- **GIS (Geographic Information System):** software that lets you store, view, and analyze data that has a location attached to it.
- **Vector data:** spatial data made of points, lines, or polygons (shapes), each with attributes attached, like a fire station represented as a point with a name and address.
- **Raster data:** spatial data made of a grid of cells or pixels, where each cell holds a value, like a satellite image or an elevation surface.
- **Attribute table:** the spreadsheet-like table attached to a vector layer, where each row is a feature and each column is a piece of information about it.
- **CRS (coordinate reference system) and EPSG code:** the system that defines how coordinates on your data line up with real locations on Earth. An EPSG code, like EPSG:4326, is just a short ID number for one specific CRS.
- **Resolution (pixel size):** how much real-world ground one pixel of a raster covers, for example a 30-meter resolution raster has each pixel representing a 30 by 30 meter square on the ground.
- **NDVI (Normalized Difference Vegetation Index):** a value calculated from satellite bands that tells you how green and healthy vegetation is in a given spot.
- **Zonal statistics:** a way of summarizing raster values that fall inside each polygon of a vector layer, for example, the average elevation within each suburb boundary.
- **Choropleth map:** a map where areas (like regions or polygons) are shaded different colors based on the value of an attribute, like population density.
- **Composite index:** a single score built by combining several different variables together, used to compare areas using more than one factor at once.
- **Ignition point:** the specific location where a fire is believed to have started.
- **Bioregion or biome:** a large area classified by its characteristic climate, plants, and animals, such as a desert or a temperate forest.
- **District municipality:** one of South Africa's mid-level administrative regions, sitting between a local municipality and a province.
- **Static grid:** the fixed set of terrain and climate layers (such as slope) used as inputs when Riskscape trains its fire severity model, as opposed to layers that change season to season.
- **Fire Weather Index (FWI):** a measure of how favourable weather conditions (temperature, wind, humidity, and recent rainfall) are for a fire to start and spread, used by the trained model as one of its inputs.
- **DBSCAN:** a computer method for grouping nearby fire detections into a single fire event, based on how close in space and time the detections are to each other.
- **VIIRS (Visible Infrared Imaging Radiometer Suite):** the satellite instrument that detects heat from fires, which is one of the main sources of fire detection data used in this workshop.
- **Convex hull *(Advanced Track):*** the smallest shape with no indentations that still contains every point in a group — like stretching a rubber band around a scatter of pins.
- **Concave hull *(Advanced Track):*** a tighter-fitting outline than a convex hull, able to follow indentations in a scatter of points rather than smoothing straight past them. Riskscape's real fire polygons use this; the advanced track uses convex hulls as a simpler stand-in.
- **Equal-area CRS *(Advanced Track):*** a coordinate reference system chosen specifically so that area calculations come out correct in real-world units. Geographic CRSs like EPSG:4326 do not have this property, and common projected CRSs like Web Mercator distort area badly at South Africa's latitude.
- **Data leakage *(Advanced Track):*** a modelling mistake where information that's only available *because* the outcome already happened gets used as an input for predicting that same outcome, making a model look better than it will ever perform on new, real data.
- **One-hot encoding *(Advanced Track):*** representing a category (like a bioregion name) as a set of numeric columns, one per possible category, each holding a 1 or 0. Requires a fixed, agreed list of categories to stay consistent across different batches of data.
- **Fire frequency (vs. severity) *(Advanced Track):*** two different questions asked of the same fire data — frequency asks how *often* a fire starts in a given area, severity asks how *bad* a fire is once it starts. Riskscape models them separately.
- **Virtual environment *(Advanced Track):*** a named, isolated set of Python packages, created with tools like Miniconda, that can't be broken by (or break) anything else installed on the same machine. Lets a workshop's exact setup be recreated reliably on any laptop.
- **GeoDataFrame *(Advanced Track):*** a pandas DataFrame (a spreadsheet-like table in Python) with an extra `geometry` column attached, provided by the `geopandas` library, so the same filtering, sorting, and grouping you'd do on a plain table also carries spatial operations like joins and area calculations.
- **Pearson correlation coefficient *(Advanced Track):*** a single number between -1 and 1 that measures how strongly two variables move together — close to 1 means they rise together, close to -1 means one rises as the other falls, and close to 0 means little to no relationship.
- **Fuel continuity *(Advanced Track):*** whether flammable vegetation forms one continuous patch or a fragmented mosaic across a landscape, which affects how fast a fire can spread once it starts. One of many inputs to Riskscape's real severity model.
- **Train/test split *(Advanced Track):*** holding back a portion of your data (never shown to the model while it's learning) so you can honestly check afterwards how well it performs on data it hasn't seen. Scoring a model only on the data it trained on tends to make it look better than it really is.
- **Feature standardization *(Advanced Track):*** rescaling each input variable so they're on a comparable footing before fitting a model — without it, a variable that happens to vary more will look more "important" in the fitted model regardless of what's actually driving the outcome.
- **R² (coefficient of determination) *(Advanced Track):*** a score, typically between 0 and 1, for how much of the variation in a target variable a model's predictions account for. A low R² isn't necessarily a broken model — it can just mean the model's inputs don't explain much of what's going on.
- **Overfitting *(Advanced Track):*** when a model learns patterns specific to its training data (including noise) rather than a genuine underlying relationship, so it performs well on training data but poorly on new data. More of a risk with complex models (like decision trees) and few training examples.

## National Geographic Society & The Nature Conservancy Community Conservation, Data Visualization, and Mapping Externship

If this week has you interested in doing more GIS and conservation-mapping work, here's a real opportunity to build on it:

**[Community Conservation, Data Visualization, and Mapping Externship](https://www.extern.com/national-geographic-society-the-nature-conservancy-externships/community-conservation-data-visualization-and-mapping-externship)** — run jointly by the National Geographic Society and The Nature Conservancy. It's an 8-week, part-time (about 10 hours/week), fully remote program where you research a conservation issue in your own community and turn it into a map-driven story, with hands-on training in Esri's mapping and GIS tools. No prior GIS or conservation experience is required, it's open worldwide to ages 18–25, and it comes with a $500 completion stipend. You finish with an Esri StoryMap portfolio piece you can point to in future applications.

<p float="left">
  <img src="Images/Externship%20Flyer%201.png" alt="Externship flyer 1 — Applications Open" width="45%" />
  <img src="Images/Externship%20Flyer%202.png" alt="Externship flyer 2 — What you'll do in this remote externship" width="45%" />
</p>

## Get in Touch

If anything from this week sparks a question later — about GIS, about this dataset, about where to go next — feel free to reach out.

<img src="Images/businessCard.png" alt="Cameron Green — business card" width="60%" />

Connect on LinkedIn: [linkedin.com/in/cameronlgreen](https://www.linkedin.com/in/cameronlgreen/)

Email: [cameron.green@riskscape.pro](mailto:cameron.green@riskscape.pro)

## Photo List

### Getting Ready

1. QGIS Empty Launch — QGIS open for the first time, showing the empty map canvas with no layers loaded

   <a id="photo-1"></a>

   ![Photo 1 — QGIS Empty Launch](Images/Photo%201.png)

2. New Empty Project Saved — A newly created, blank QGIS project saved to the Desktop, with no layers loaded yet

   <a id="photo-2"></a>

   ![Photo 2 — New Empty Project Saved](Images/Photo%202.png)

### Day 1

3. QGIS Blank Interface — the empty QGIS window with the Layers panel, Browser panel, map canvas, and status bar all labelled

   <a id="photo-3"></a>

   ![Photo 3 — QGIS Blank Interface](Images/Photo%203.png)

4. SA Boundary Transparent — the South Africa boundary showing as a transparent shape with a black outline, filling the map canvas

   <a id="photo-4"></a>

   ![Photo 4 — SA Boundary Transparent](Images/Photo%204.png)

5. Fire Polygons Overview — the fire event polygons loaded over the South Africa boundary, zoomed to show the whole country

   <a id="photo-5"></a>

   ![Photo 5 — Fire Polygons Overview](Images/Photo%205.png)

6. Attribute Table Sorted — the attribute table sorted by area_km2 descending, with the top row highlighted

   <a id="photo-6"></a>

   ![Photo 6 — Attribute Table Sorted](Images/Photo%206.png)

7. Status Bar Coordinates — the bottom-right corner of QGIS showing live coordinates as the mouse moves over the map

   <a id="photo-7"></a>

   ![Photo 7 — Status Bar Coordinates](Images/Photo%207.png)

8. Graduated Symbology Dialog — the Symbology tab set to graduated, area_km2 selected as the field, 5 classes, and a white-to-dark-red colour ramp chosen

   <a id="photo-8"></a>

   ![Photo 8 — Graduated Symbology Dialog](Images/Photo%208.png)

9. Fire Map Graduated — the finished map with fires shaded from pale to dark red by size

   <a id="photo-9"></a>

   ![Photo 9 — Fire Map Graduated](Images/Photo%209.png)

10. Ignition Points Orange — the ignition points shown as small orange dots over the fire polygons

    <a id="photo-10"></a>

    ![Photo 10 — Ignition Points Orange](Images/Photo%2010.png)

11. Bioregions Categorized — the bioregions layer shown with transparent fill and a distinct border colour for each biome, fire polygons visible underneath

    <a id="photo-11"></a>

    ![Photo 11 — Bioregions Categorized](Images/Photo%2011.png)

12. Print Layout Elements — the print layout with title, legend, north arrow, and scale bar all placed around the map

    <a id="photo-12"></a>

    ![Photo 12 — Print Layout Elements](Images/Photo%2012.png)

### Day 2

13. Count Points in Polygon Dialog — the Count Points in Polygon dialog with the points and polygons layers selected

    <a id="photo-13"></a>

    ![Photo 13 — Count Points in Polygon Dialog](Images/Photo%2013.png)

14. Fire Events with Biome Column — the fire events attribute table showing the new biome name column after the join

    <a id="photo-14"></a>

    ![Photo 14 — Fire Events with Biome Column](Images/Photo%2014.png)

15. NDVI Green Ramp Styled — the NDVI summer raster displayed with your chosen green colour ramp

    <a id="photo-15"></a>

    ![Photo 15 — NDVI Green Ramp Styled](Images/Photo%2015.png)

16. Severity Raster with Fire Overlay — the reversed RdYlGn severity raster with fire event polygons drawn on top

    <a id="photo-16"></a>

    ![Photo 16 — Severity Raster with Fire Overlay](Images/Photo%2016.png)

### Day 3

18. Zonal Statistics Dialog — the Zonal Statistics dialog with the summer severity raster and bioregion layer selected and mean/max ticked

    <a id="photo-18"></a>

    ![Photo 18 — Zonal Statistics Dialog](Images/Photo%2018.png)

19. Severity Reclassify Table — the Reclassify by Table dialog showing six class ranges mapped to values 0 through 5

    <a id="photo-19"></a>

    ![Photo 19 — Severity Reclassify Table](Images/Photo%2019.png)

20. NDVI Reclass Inverted — the inverted NDVI reclassification, showing sparse/dry areas symbolized as high risk classes

    <a id="photo-20"></a>

    ![Photo 20 — NDVI Reclass Inverted](Images/Photo%2020.png)

21. Raster Calculator Formula — the Raster Calculator dialog with the weighted formula typed in and the two reclassified layers listed

    <a id="photo-21"></a>

    ![Photo 21 — Raster Calculator Formula](Images/Photo%2021.png)

22. Composite Risk Map Red Ramp — the finished composite risk raster styled with a red colour ramp across the province

    <a id="photo-22"></a>

    ![Photo 22 — Composite Risk Map Red Ramp](Images/Photo%2022.png)

### Day 4

No photos tagged in this section.

### Appendices

No photos were tagged in this section.

---

Back to: [Before Day 1](README.md) · [Day 1](Day_1.md) · [Day 1 (Advanced Track)](Day_1_Advanced.md) · [Day 2](Day_2.md) · [Day 2 (Advanced Track)](Day_2_Advanced.md) · [Day 3](Day_3.md) · [Day 3 (Advanced Track)](Day_3_Advanced.md) · [Day 4](Day_4.md)
