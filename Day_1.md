# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 1

*A 4-day introductory workshop (Tuesday to Friday) that teaches first-year students to map, analyse, and model wildfire risk in South Africa using real data and QGIS.*

| Day | Focus | Deliverable |
|---|---|---|
| Day 1 | GIS foundations: load, explore, style, and lay out a map | A styled fire event map with one written observation |
| Day 2 | Spatial analysis: connect fire to the landscape | A 4-panel seasonal severity map with written observations |
| Day 3 | Raster analysis: build your own risk model | A composite risk map compared to the trained model output |
| Day 4 | Capstone: same data, two client stories | Two slide decks (one per brief) with speaker notes, built individually |

Each day runs for about 6 working hours, split into two 2.5 hour sessions with a break in between.

---

## Day 1 — What is GIS, and Where Does South Africa Burn?

Welcome to your first day of GIS — the software you met in Getting Ready that stores and displays information tied to real places on a map. Today you are going to open QGIS for the first time, load some real South African fire data, and start asking questions of it.

### Morning Session

1. **Explore the empty interface (about 20 minutes).** Open QGIS but do not load any data yet. Before you have anything on screen, spend some time just clicking around so the layout makes sense later. Try to find each of these on your own:
   - The **map canvas** — the big blank area in the middle where your data will eventually appear.
   - The **Layers panel** — usually down the left side, this is where every dataset you load will be listed.
   - The **Browser panel** — often stacked with the Layers panel, this lets you browse folders and files on your computer without leaving QGIS.
   - The main **toolbars** across the top — hover over a few icons and read their tooltips. You do not need to know what they all do yet.
   - The **status bar** along the bottom — this is where QGIS quietly tells you useful things, like your mouse position and the current scale.
   - Try dragging a panel to a new spot, or closing one and getting it back (look in the **View** menu for a list of panels).

   > **Think about it:** A blank GIS program looks a bit like a blank spreadsheet — all structure, no content. What do you expect to change once real data is loaded?

   > **Photo 3 — QGIS Blank Interface.** See the [Photo List appendix](Appendices.md#photo-3) for exactly what to capture.

2. **Load the South Africa boundary layer.** Use the Layer menu to add the boundary layer as a vector layer (points, lines, or polygons, as introduced in Getting Ready). Once it is loaded:
   - Right-click the layer in the Layers panel and look for an option to zoom to it, so the whole country fills your map canvas.
   - Right-click the layer again and open its **Properties**. Find the **Symbology** tab, which controls how a layer is drawn.
   - Change the fill to transparent and give the boundary a black border.

   > **Hint:** Spend a minute hunting for the transparency setting yourself before reading on — it lives inside the Symbology tab, usually attached to the fill colour or opacity control for the symbol layer. Once you find it, set the fill to fully transparent and pick black for the stroke/border colour.

   > **Photo 4 — SA Boundary Transparent.** See the [Photo List appendix](Appendices.md#photo-4) for exactly what to capture.

   > **Checkpoint:** You should see the outline of South Africa as an empty shape with a solid black border, and nothing filled in. If the whole country is solid black or solid grey, go back into Symbology and check you changed the fill, not the border.

3. **Load the fire event polygons layer.** This one is an immediately striking layer — each polygon is a single fire event. Add it the same way you added the boundary layer, then just look around for a few minutes:
   - Zoom into the Western Cape, around Cape Town.
   - Zoom into KwaZulu-Natal.
   - Compare how dense or sparse the fires look in each region.

   No analysis yet — just get a feel for the data by looking.

   > **Photo 5 — Fire Polygons Overview.** See the [Photo List appendix](Appendices.md#photo-5) for exactly what to capture.

   > **Think about it:** Without doing any calculations, does one region look like it has more fires, bigger fires, or both? Keep that impression in mind — you'll test it properly later today.

   > **Watch out:** If you zoom in and see nothing, check that the fire layer is above the boundary layer in the Layers panel. Layers drawn lower in the list can be hidden underneath layers above them.

4. **Attribute table deep dive.** Every layer has an attribute table — a spreadsheet-like table with one row per feature (in this case, per fire). Open it by right-clicking the fire polygons layer and looking for the Attribute Table option. Find these three columns:
   - **area_km2** — the size of the fire, in square kilometres.
   - **days_burned** — how many days the fire was active.
   - **start_date** — the date the fire started.

   Sort the table by **area_km2** in descending order (largest first) by clicking the column header — you may need to click it twice to get the direction you want.

   > **Hint:** Look for a small arrow that appears next to the column name once you click it — that arrow tells you which direction you're sorted in.

   > **Photo 6 — Attribute Table Sorted.** See the [Photo List appendix](Appendices.md#photo-6) for exactly what to capture.

   Answer this for yourself: what is the single largest fire in the dataset, when did it start, and how many days did it burn?

   > **Checkpoint:** You should be able to state one area_km2 value, one start_date, and one days_burned value, all from the same row. If your top row looks suspiciously small, double check you sorted descending and not ascending.

5. **A first look at coordinate systems.** A coordinate reference system (CRS) is the system a layer uses to describe where things are on Earth's curved surface using flat map coordinates. Look at the bottom right of your status bar and move your mouse slowly across the map canvas — you'll see a pair of numbers updating live. Those are your current coordinates.
   - If your project is in **EPSG:4326**, a geographic CRS, those numbers will be in degrees of latitude and longitude, and they'll look like small decimal numbers.
   - A projected CRS instead measures in a real-world linear unit like metres, and the numbers will look like large whole numbers in the hundreds of thousands or millions.

   You don't need to change anything yet — just note which kind your project is currently using, and watch how differently the numbers behave.

   > **Photo 7 — Status Bar Coordinates.** See the [Photo List appendix](Appendices.md#photo-7) for exactly what to capture.

   > **Think about it:** Degrees are great for describing where something is on the whole globe, but not so great for measuring how big it is. Why might that matter for a dataset where one of the key columns is area_km2?

### Afternoon Session

1. **Graduated symbology on the fire polygons.** Graduated symbology colours or sizes features in classes based on a numeric value, rather than giving every feature the same look. Open the Properties of your fire polygons layer, go back to Symbology, and switch the drawing style from "single symbol" to **graduated**.
   - Set the value to classify by to **area_km2**.
   - Set the number of classes to **5**.
   - Choose a colour ramp that runs from white through to dark red.
   - Apply the changes and look at your map.

   > **Photo 8 — Graduated Symbology Dialog.** See the [Photo List appendix](Appendices.md#photo-8) for exactly what to capture.

   > **Photo 9 — Fire Map Graduated.** See the [Photo List appendix](Appendices.md#photo-9) for exactly what to capture.

   > **Think about it:** White-to-dark-red is a sequential palette — it moves in one direction, from "low" to "high." A diverging palette instead has two colours moving away from a neutral midpoint (for example blue to white to red). Why does a sequential palette make more sense here than a diverging one, given that area_km2 has no natural "zero point" worth splitting the data around?

2. **Load the ignition points layer** — the point marking roughly where each fire started, as described in Getting Ready. Add this layer, then style it as small orange dots (Symbology tab again, this time on a point layer).
   - Toggle the checkbox next to the fire polygons layer on and off a few times, with the ignition points layer showing the whole time.
   - Watch how each polygon relates to a point roughly inside or near it.

   > **Photo 10 — Ignition Points Orange.** See the [Photo List appendix](Appendices.md#photo-10) for exactly what to capture.

   > **Think about it:** The relationship here is one ignition point leads to one fire polygon. Does every polygon seem to have a point near it? What might it mean if you find one that doesn't?

3. **Load the bioregions layer.** This layer shows South Africa's biomes, the ecological zones you met in Getting Ready (think Fynbos or Savanna). Add the layer, then switch its symbology to **categorized**, using the field that stores the biome name.
   - Give each biome its own border colour.
   - Set the fill to transparent so you can still see the fires and boundary underneath.

   > **Hint:** Look for the field dropdown near the top of the Symbology tab, and a button to automatically generate one colour per category once the field is chosen.

   > **Photo 11 — Bioregions Categorized.** See the [Photo List appendix](Appendices.md#photo-11) for exactly what to capture.

   > **Think about it:** Zoom into the Fynbos biome in the Western Cape, then zoom into a Savanna region. Just by looking at fire size and shape, does it seem like these two biomes burn differently? Note down what you actually observe, not what you'd expect — you'll come back to this question with real analysis later in the course.

   > **Watch out:** If the whole bioregions layer suddenly renders as one flat colour, check that you set the symbology to categorized and not single symbol, and that you clicked the button to classify/generate the categories.

4. **Build your first map layout.** Open a new print layout from scratch — this is the part of QGIS dedicated to turning your map canvas into a printable or exportable map. Give it a name when prompted, then add:
   - A **title** (a text label at the top, something like "South African Fire Events by Size").
   - A **legend**.
   - A **north arrow**.
   - A **scale bar**.

   Arrange them so nothing overlaps and the map itself is the largest element on the page. When you're happy with it, export the layout as a PNG image.

   > **Photo 12 — Print Layout Elements.** See the [Photo List appendix](Appendices.md#photo-12) for exactly what to capture.

   > **Checkpoint:** Your exported PNG should clearly show the fire polygons shaded by size, a legend explaining the colour classes, a north arrow, a scale bar, and a title — all in one image. If your legend is showing layers you don't want (like a layer you loaded but hid), go back and check which layers are ticked visible in your Layers panel before exporting.

   > **Watch out:** A layout is separate from your map canvas — closing the layout window does not lose your work, but forgetting to save your QGIS project before closing QGIS entirely will.

### Deliverable

A styled map of South African fire events by size, with bioregions shown as context, exported as a PNG from your print layout. On the map itself (or as a text box added to the layout), include one short written annotation describing something you noticed today — for example, about fire density in a particular region, the size of the single largest fire, or a first impression of Fynbos versus Savanna.

Submit your exported PNG here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge

If someone from the Riskscape team has provided a rainfall seasonality zones (RSZ) layer, load it into your project and add it to your map. Think about where it fits in your layer order and what symbology would let you see it without hiding the fires or bioregions underneath it.

---

Previous: [Before Day 1](README.md) · Next: [Day 2](Day_2.md) · Reference: [Appendices](Appendices.md)
