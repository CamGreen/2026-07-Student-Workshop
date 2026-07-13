# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook

## Cover

A 4-day introductory workshop (Tuesday to Friday) that teaches first-year students to map, analyse, and model wildfire risk in South Africa using real data and QGIS.


<div style="page-break-after: always;"></div>

## Note to the Instructor (remove before printing for students)

- Students build their own QGIS project from scratch each day, loading and styling layers themselves rather than opening a pre-built project file. This is deliberate: the loading, styling, and layer-ordering steps are part of what they're meant to practise.
- Distribute the full data folder for your chosen province (Western Cape recommended) to every student before Day 1 begins. Students will add layers into their own projects directly from this folder, so if it goes missing or gets restructured, layers will fail to load.
- Tell students to copy the folder to their Desktop and leave the internal file and folder names exactly as given. Renaming or moving individual files inside the folder is the single most common cause of "broken layer" problems on Day 1 morning.
- The Day 1 extension challenge (rainfall seasonality zones) and the Day 3 extension challenge (a slope layer derived from the static grid — the fixed set of terrain and climate layers behind the trained model — and/or a Fire Weather Index (FWI) severity raster) both need extra data layers that are not part of the core package described below. Only add those layers to the folder if you want students to be able to attempt those specific extensions.

## Table of Contents

- [Before Day 1 — Getting Ready](#before-day-1-getting-ready)
  - [What is GIS?](#what-is-gis)
  - [Installing QGIS](#installing-qgis)
  - [Getting Your Data Folder](#getting-your-data-folder)
  - [What's in Your Data Folder](#whats-in-your-data-folder)
  - [You Are Ready for Day 1 When...](#you-are-ready-for-day-1-when)
- [Day 1 — What is GIS, and Where Does South Africa Burn?](#day-1-what-is-gis-and-where-does-south-africa-burn)
  - [Morning Session](#morning-session)
  - [Afternoon Session](#afternoon-session)
  - [Deliverable](#deliverable)
  - [Extension Challenge](#extension-challenge)
- [Day 2 — What Drives Fire?](#day-2-what-drives-fire)
  - [Morning Session](#morning-session-1)
  - [Afternoon Session](#afternoon-session-1)
  - [Deliverable](#deliverable-1)
  - [Extension Challenge](#extension-challenge-1)
- [Day 3 — Building a Risk Model](#day-3-building-a-risk-model)
  - [Morning Session](#morning-session-2)
  - [Afternoon Session](#afternoon-session-2)
  - [Deliverable](#deliverable-2)
  - [Extension Challenge](#extension-challenge-2)
- [Day 4 — Presenting to Two Clients](#day-4-presenting-to-two-clients)
  - [The Brief](#the-brief)
  - [Choose Your Two Clients](#choose-your-two-clients)
  - [Tools You Already Know](#tools-you-already-know)
  - [Morning Session: Your First Brief](#morning-session-your-first-brief)
  - [Afternoon Session: Your Second Brief](#afternoon-session-your-second-brief)
  - [Deliverable](#deliverable-3)
  - [Extension Challenge](#extension-challenge-3)
- [Appendices](#appendices)
  - [Appendix: One-Page QGIS Cheat Sheet](#appendix-one-page-qgis-cheat-sheet)
  - [Appendix: Troubleshooting](#appendix-troubleshooting)
  - [Appendix: Glossary of Terms](#appendix-glossary-of-terms)
- [Photo List (For the Instructor)](#photo-list-for-the-instructor)

<div style="page-break-after: always;"></div>

## Before Day 1 — Getting Ready

Welcome. Over the next few days you're going to work with real wildfire data from South Africa, the same data used by Riskscape, a risk analytics company, to build an actual fire severity model that is used today. Every day, a NASA satellite instrument called VIIRS scans the country and detects heat signatures from fires. A clustering algorithm stitches together the detections that belong to the same fire into a single "fire event," and this has been happening since 2012. Riskscape combines thousands of these fire events with climate and terrain data and trains a machine learning model that predicts, for every 500 metre patch of the country, how severe a fire is likely to be in each season.

You're going to start at the end of that pipeline, by exploring the finished model's output, and then work backwards to understand where the numbers actually came from. By Day 3, you'll build a small version of that model yourself. None of this requires any GIS or programming experience. That's exactly what this first section is for: getting your computer ready so you can dive straight into the real work on Day 1.

Here's the shape of the whole workshop:

| Day | Focus | Deliverable |
|---|---|---|
| Day 1 | GIS foundations: load, explore, style, and lay out a map | A styled fire event map with one written observation |
| Day 2 | Spatial analysis: connect fire to the landscape | A 4-panel seasonal severity map with written observations |
| Day 3 | Raster analysis: build your own risk model | A composite risk map compared to the trained model output |
| Day 4 | Capstone: same data, two client stories | Two slide decks (one per brief) with speaker notes, built individually |

Each day runs for about 6 working hours, split into two 2.5 hour sessions with a break in between.

### What is GIS?

A geographic information system, or GIS, is just software that stores and displays information tied to real places on a map, rather than in a plain spreadsheet or document. Underneath, almost all mapped data comes in one of two basic forms: vector data, which is points, lines, and shapes (like a dot for a city or an outline for a country), and raster data, which is a grid of pixels, each holding a value (like a satellite image or a temperature map). Don't worry about memorising that distinction right now. You'll meet vector data properly on Day 1 and raster data on Day 2.

### Installing QGIS

QGIS is the free, open-source GIS software you'll use for the whole workshop. Your instructor will give you the installer on a USB flash stick, so you won't need to download anything yourself. Follow these steps before Day 1 so you're not installing software while everyone else is already working.

1. Plug in the USB flash stick your instructor gives you and copy the QGIS installer onto your Desktop.
2. The installer is the **Long Term Release**, sometimes shortened to **LTR**. This is the most stable version of QGIS, which matters more than having the latest features for a workshop like this — don't swap it out for a different version even if you find one online.
3. Run the installer once it's copied over, and accept all the default options as you click through it. There's no need to change any settings.
4. Once installation finishes, open QGIS from your Start menu or Applications folder.
5. Confirm that QGIS launches successfully to an empty map window, with menus across the top and panels down the sides but no data loaded yet.

> **Photo 1 — QGIS Empty Launch.** See the Photo List appendix for exactly what to capture.

> **Checkpoint:** You know the install worked if QGIS opens to a blank map canvas within a few seconds, with no error messages. You don't need to click anything else yet, just confirm it opens.

> **Hint:** If QGIS won't open or crashes immediately, restarting your computer fixes the problem more often than you'd expect. If it still won't open after that, flag it with your instructor before Day 1 rather than on the morning itself.

### Getting Your Data Folder

Your instructor will give you the workshop data folder before Day 1, by USB stick, a shared drive, or a download link, whichever has been arranged for your class.

1. Copy the **entire folder** onto your Desktop. Don't just copy individual files out of it.
2. Don't rename the folder, and don't rename or move any files inside it. You'll be loading layers into QGIS directly from this folder, by file path, throughout the workshop.
3. Open QGIS and create a new, empty project. Save it somewhere sensible (your Desktop is fine) so you can find it again — you'll build each day's project yourself from this blank starting point.

> **Photo 2 — New Empty Project Saved.** See the Photo List appendix for exactly what to capture.

### What's in Your Data Folder

Here's a plain-language guide to what you'll find inside, so the file names mean something before you even open them:

- **sa_boundary.gpkg** — the outline of the whole of South Africa. You'll use this just for context, so you always know where in the country you're looking.
- **province_boundary.gpkg** — the outline of the one province this workshop focuses on, the Western Cape, already cut out from the national boundary for you.
- **fire_events_clean.gpkg** — the star of the show. Every polygon (a mapped shape with an outline, used to represent an area) in this file is one real wildfire, going all the way back to 2012. Each one carries information in columns including `area_km2` (how big the fire was, in square kilometres), `days_burned` (how many days it burned for), and `start_date` (when it began).
- **fire_ignitions.gpkg** — one point per fire event, marking roughly where that fire is believed to have started.
- **bioregions.gpkg** — the Western Cape divided up into ecological zones called bioregions or biomes (think Fynbos or Savanna), taken from South Africa's national vegetation map. This tells you what kind of landscape and vegetation each fire happened in.
- **severity_rasters/severity_mean_summer.tif**, **severity_mean_autumn.tif**, **severity_mean_winter.tif**, **severity_mean_spring.tif** — the actual output of Riskscape's trained fire severity model, one file per season, inside the `severity_rasters` subfolder. Each is a raster (a grid of pixels), and each pixel is a prediction of how many square kilometres are likely to burn per day at that spot.
- **ndvi_rasters/ndvi_summer.tif** (and the autumn/winter/spring equivalents) — a vegetation greenness index called NDVI (Normalised Difference Vegetation Index), built from satellite imagery and averaged over many years, inside the `ndvi_rasters` subfolder. High values mean lush, green vegetation; low values mean dry or sparse vegetation. This is one of the clues the model uses to predict fire severity.
- **District_Municipal_Boundary.gpkg** — South Africa's district municipalities (the mid-level administrative regions between a local municipality and a province, introduced in Day 3). The municipality name is in the `adm2_name` field.

Every layer in your folder already uses the same coordinate system (a shared way of describing locations on Earth, called EPSG:4326), so everything lines up correctly on the map with no extra work from you.

> **Watch out:** It's tempting to peek inside the folder and start dragging in whatever files look interesting. Resist that urge for now — each day's instructions tell you exactly which layers to load and in what order, so your layers, colours, and labels stay comparable to everyone else's in the room.

### You Are Ready for Day 1 When...

- QGIS is installed on your laptop and you've confirmed it opens to an empty map window.
- Your workshop data folder is copied, unchanged, onto your Desktop.
- You've created and saved a blank QGIS project of your own, ready to build on.
- You've got a rough idea of what a fire event, a bioregion, and a raster grid are, even if the details are still fuzzy. That's exactly where Day 1 picks up.

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

   > **Photo 3 — QGIS Blank Interface.** See the Photo List appendix for exactly what to capture.

2. **Load the South Africa boundary layer.** Use the Layer menu to add the boundary layer as a vector layer (points, lines, or polygons, as introduced in Getting Ready). Once it is loaded:
   - Right-click the layer in the Layers panel and look for an option to zoom to it, so the whole country fills your map canvas.
   - Right-click the layer again and open its **Properties**. Find the **Symbology** tab, which controls how a layer is drawn.
   - Change the fill to transparent and give the boundary a black border.

   > **Hint:** Spend a minute hunting for the transparency setting yourself before reading on — it lives inside the Symbology tab, usually attached to the fill colour or opacity control for the symbol layer. Once you find it, set the fill to fully transparent and pick black for the stroke/border colour.

   > **Photo 4 — SA Boundary Transparent.** See the Photo List appendix for exactly what to capture.

   > **Checkpoint:** You should see the outline of South Africa as an empty shape with a solid black border, and nothing filled in. If the whole country is solid black or solid grey, go back into Symbology and check you changed the fill, not the border.

3. **Load the fire event polygons layer.** This one is an immediately striking layer — each polygon is a single fire event. Add it the same way you added the boundary layer, then just look around for a few minutes:
   - Zoom into the Western Cape, around Cape Town.
   - Zoom into KwaZulu-Natal.
   - Compare how dense or sparse the fires look in each region.

   No analysis yet — just get a feel for the data by looking.

   > **Photo 5 — Fire Polygons Overview.** See the Photo List appendix for exactly what to capture.

   > **Think about it:** Without doing any calculations, does one region look like it has more fires, bigger fires, or both? Keep that impression in mind — you'll test it properly later today.

   > **Watch out:** If you zoom in and see nothing, check that the fire layer is above the boundary layer in the Layers panel. Layers drawn lower in the list can be hidden underneath layers above them.

4. **Attribute table deep dive.** Every layer has an attribute table — a spreadsheet-like table with one row per feature (in this case, per fire). Open it by right-clicking the fire polygons layer and looking for the Attribute Table option. Find these three columns:
   - **area_km2** — the size of the fire, in square kilometres.
   - **days_burned** — how many days the fire was active.
   - **start_date** — the date the fire started.

   Sort the table by **area_km2** in descending order (largest first) by clicking the column header — you may need to click it twice to get the direction you want.

   > **Hint:** Look for a small arrow that appears next to the column name once you click it — that arrow tells you which direction you're sorted in.

   > **Photo 6 — Attribute Table Sorted.** See the Photo List appendix for exactly what to capture.

   Answer this for yourself: what is the single largest fire in the dataset, when did it start, and how many days did it burn?

   > **Checkpoint:** You should be able to state one area_km2 value, one start_date, and one days_burned value, all from the same row. If your top row looks suspiciously small, double check you sorted descending and not ascending.

5. **A first look at coordinate systems.** A coordinate reference system (CRS) is the system a layer uses to describe where things are on Earth's curved surface using flat map coordinates. Look at the bottom right of your status bar and move your mouse slowly across the map canvas — you'll see a pair of numbers updating live. Those are your current coordinates.
   - If your project is in **EPSG:4326**, a geographic CRS, those numbers will be in degrees of latitude and longitude, and they'll look like small decimal numbers.
   - A projected CRS instead measures in a real-world linear unit like metres, and the numbers will look like large whole numbers in the hundreds of thousands or millions.

   You don't need to change anything yet — just note which kind your project is currently using, and watch how differently the numbers behave.

   > **Photo 7 — Status Bar Coordinates.** See the Photo List appendix for exactly what to capture.

   > **Think about it:** Degrees are great for describing where something is on the whole globe, but not so great for measuring how big it is. Why might that matter for a dataset where one of the key columns is area_km2?

### Afternoon Session

1. **Graduated symbology on the fire polygons.** Graduated symbology colours or sizes features in classes based on a numeric value, rather than giving every feature the same look. Open the Properties of your fire polygons layer, go back to Symbology, and switch the drawing style from "single symbol" to **graduated**.
   - Set the value to classify by to **area_km2**.
   - Set the number of classes to **5**.
   - Choose a colour ramp that runs from white through to dark red.
   - Apply the changes and look at your map.

   > **Photo 8 — Graduated Symbology Dialog.** See the Photo List appendix for exactly what to capture.

   > **Photo 9 — Fire Map Graduated.** See the Photo List appendix for exactly what to capture.

   > **Think about it:** White-to-dark-red is a sequential palette — it moves in one direction, from "low" to "high." A diverging palette instead has two colours moving away from a neutral midpoint (for example blue to white to red). Why does a sequential palette make more sense here than a diverging one, given that area_km2 has no natural "zero point" worth splitting the data around?

2. **Load the ignition points layer** — the point marking roughly where each fire started, as described in Getting Ready. Add this layer, then style it as small orange dots (Symbology tab again, this time on a point layer).
   - Toggle the checkbox next to the fire polygons layer on and off a few times, with the ignition points layer showing the whole time.
   - Watch how each polygon relates to a point roughly inside or near it.

   > **Photo 10 — Ignition Points Orange.** See the Photo List appendix for exactly what to capture.

   > **Think about it:** The relationship here is one ignition point leads to one fire polygon. Does every polygon seem to have a point near it? What might it mean if you find one that doesn't?

3. **Load the bioregions layer.** This layer shows South Africa's biomes, the ecological zones you met in Getting Ready (think Fynbos or Savanna). Add the layer, then switch its symbology to **categorized**, using the field that stores the biome name.
   - Give each biome its own border colour.
   - Set the fill to transparent so you can still see the fires and boundary underneath.

   > **Hint:** Look for the field dropdown near the top of the Symbology tab, and a button to automatically generate one colour per category once the field is chosen.

   > **Photo 11 — Bioregions Categorized.** See the Photo List appendix for exactly what to capture.

   > **Think about it:** Zoom into the Fynbos biome in the Western Cape, then zoom into a Savanna region. Just by looking at fire size and shape, does it seem like these two biomes burn differently? Note down what you actually observe, not what you'd expect — you'll come back to this question with real analysis later in the course.

   > **Watch out:** If the whole bioregions layer suddenly renders as one flat colour, check that you set the symbology to categorized and not single symbol, and that you clicked the button to classify/generate the categories.

4. **Build your first map layout.** Open a new print layout from scratch — this is the part of QGIS dedicated to turning your map canvas into a printable or exportable map. Give it a name when prompted, then add:
   - A **title** (a text label at the top, something like "South African Fire Events by Size").
   - A **legend**.
   - A **north arrow**.
   - A **scale bar**.

   Arrange them so nothing overlaps and the map itself is the largest element on the page. When you're happy with it, export the layout as a PNG image.

   > **Photo 12 — Print Layout Elements.** See the Photo List appendix for exactly what to capture.

   > **Checkpoint:** Your exported PNG should clearly show the fire polygons shaded by size, a legend explaining the colour classes, a north arrow, a scale bar, and a title — all in one image. If your legend is showing layers you don't want (like a layer you loaded but hid), go back and check which layers are ticked visible in your Layers panel before exporting.

   > **Watch out:** A layout is separate from your map canvas — closing the layout window does not lose your work, but forgetting to save your QGIS project before closing QGIS entirely will.

### Deliverable

A styled map of South African fire events by size, with bioregions shown as context, exported as a PNG from your print layout. On the map itself (or as a text box added to the layout), include one short written annotation describing something you noticed today — for example, about fire density in a particular region, the size of the single largest fire, or a first impression of Fynbos versus Savanna.

Submit your exported PNG here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge

If your instructor has provided a rainfall seasonality zones (RSZ) layer, load it into your project and add it to your map. Think about where it fits in your layer order and what symbology would let you see it without hiding the fires or bioregions underneath it.

<div style="page-break-after: always;"></div>

## Day 2 — What Drives Fire?

Yesterday you got the data loaded and the interface under your belt. Today you start asking it real questions: which biomes burn most, how big are those fires, and what do the underlying maps of vegetation and predicted severity actually tell you about why fire happens where it does. You already know your way around QGIS menus and panels, so this section names the tools you need and trusts you to work out the dialog boxes yourself.

### Morning Session

Your ignition points, fire event polygons, and bioregion (biome) polygons from Day 1 are the stars of the morning. You're going to combine them to find patterns, not just look at them side by side.

1. **Count how many ignitions fall in each bioregion.**
   - Use **Vector > Analysis > Count Points in Polygon**. This tool takes a points layer and a polygons layer and adds a new field to a copy of the polygons recording how many points fall inside each one — exactly what you need to compare ignition counts across biomes.
   - Work out which layer goes in which slot in the dialog, run it, and open the resulting attribute table.
   - Sort the new count field from highest to lowest to find your answer.

   > **Photo 13 — Count Points in Polygon Dialog.** See the Photo List appendix for exactly what to capture.

> **Think about it:** Is the biome with the most ignition points necessarily the one most "at risk" from fire? What else would you need to know before you'd make that claim?

2. **Attach the bioregion name to every fire event.**
   - Right now your fire event polygons don't know which biome they're in. You need a **spatial join** — a way of combining two attribute tables based on where features sit on the map, rather than a shared ID field.
   - Look in the Vector menu (or search the Processing Toolbox) for a tool called **Join Attributes by Location**. Join the fire events layer to the bioregion polygons so each fire event picks up the bioregion's name field.
   - Once it's run, open the joined layer's attribute table. You should now see a new column carrying the biome name for every fire event.
   - Sort by that new column, then try the attribute table's filter option to isolate just one biome at a time. Discuss with a neighbour: does anything about the pattern surprise you?

> **Watch out:** Join Attributes by Location can produce more than one output row per fire event if a fire polygon happens to overlap two bioregions at once. Check your output feature count against your original fire event count — if it's gone up, look at the join dialog's options for handling multiple matches.

> **Photo 14 — Fire Events with Biome Column.** See the Photo List appendix for exactly what to capture.

3. **Compare average fire size across biomes.**
   - Use **Vector > Analysis > Basic Statistics for Fields** on the `area_km2` field.
   - This tool doesn't split results by category on its own, so you'll need to isolate one biome at a time — select or filter the fire events belonging to a single biome, run the tool on that selection, note the mean, then repeat for the next biome.
   - Build yourself a small table as you go, for example: *fires in Fynbos average __ km², fires in Savanna average __ km²*. Fill in your own numbers.

> **Checkpoint:** Your table should have one row per biome and the means should be plausible fire sizes (tens to low hundreds of km², not thousands). If a mean looks wildly too large, check whether your selection actually isolated one biome or accidentally kept the whole layer selected.

4. **Find the large fires, and see where they land.**
   - Use **select by attribute** to select every fire event where `area_km2` is greater than 100. Look in the Vector menu's selection tools, or use the toolbar button, if you need a reminder of where it lives.
   - Now use **select by location** to narrow that down further to fires intersecting a specific province — most select-by-location dialogs let you combine with your current selection rather than starting over, so look for that option.
   - Repeat for a couple of different provinces and tally up how many large fires each one contains.

> **Hint:** If your select-by-location result comes back empty, double check which layer you set as the one "to select from" versus the one you're comparing "by comparing to" — it's an easy pair to swap by accident.

### Afternoon Session

This afternoon you move from vector data back to raster data, the pixel grids you met in Getting Ready. A raster's **resolution** is the size of each pixel on the ground (for example, a 250 m resolution raster has one value for every 250 x 250 m square of land). What that number *means* depends entirely on what the raster represents, which is exactly what you're about to explore.

1. **Load and understand the NDVI summer raster.**
   - NDVI, introduced in Getting Ready, typically ranges from about -1 to 1 at each pixel.
   - Load the NDVI summer raster and open its Properties to apply a green colour ramp under the raster's symbology settings. There's no single correct shade or ramp direction to use here — pick something that reads clearly to you, and be ready to explain your choice.

   > **Photo 15 — NDVI Green Ramp Styled.** See the Photo List appendix for exactly what to capture.

> **Think about it:** What do you think a very high NDVI pixel represents on the ground? What about a very low one? Consider water bodies, bare soil, and dense forest — they can all produce surprisingly similar-looking NDVI values in some ranges.

2. **Load the severity raster and compare it against real fires.**
   - The severity raster, the trained model output introduced in Getting Ready, estimates how destructive a fire would be at each pixel.
   - Style it with a reversed RdYlGn colour ramp (red-yellow-green, flipped so red means high severity rather than low). Again, the exact shades and number of colour classes are your call — just make sure the direction (red = high danger) is unambiguous to someone else reading your map.
   - Overlay your fire event polygons on top of the severity raster (check they're above it in the Layers panel).
   - Look at where the actual fires sit relative to the severity colours. Does the model's "high severity" red generally line up with where fires actually burned?

   > **Photo 16 — Severity Raster with Fire Overlay.** See the Photo List appendix for exactly what to capture.

> **Watch out:** A reversed colour ramp is easy to leave un-reversed by accident. If your map shows green where you expected red, check the "invert colour ramp" option in the raster's symbology tab rather than manually reassigning colours.

3. **Sample the raster with the Identify tool.**
   - Use the Identify tool to click on 10 different pixels scattered across your study area — try to pick a genuine mix, not just points you already suspect are interesting.
   - For each click, note the severity value QGIS reports, and note (by eye, checking against the fire polygons layer) whether a real fire actually occurred there.
   - Jot this down as a simple 10-row list or table: point number, severity value, fire occurred (yes/no).

> **Checkpoint:** Across your 10 points, do the "yes" (fire occurred) points tend to cluster at the higher severity values? A handful of mismatches is normal and worth discussing — a model is a prediction, not a certainty.

4. **Clip the severity raster to a single province.**
   - Working with a national raster is slow and often unnecessary when you only care about one region. Look in the Raster menu, under the extraction tools, for a clip-by-extent option.
   - Clip the national severity raster down to just one province of your choice. This is called **spatial subsetting** — cutting a dataset down to the area you actually need, which produces a smaller, faster file to work with.

> **Hint:** You'll need something to define the clip extent from — think about what layer in your project already outlines the province boundary, and whether the clip tool lets you use a layer's extent directly instead of typing coordinates by hand.

5. **Compare all four seasons.**
   - Load the remaining three seasonal severity rasters (autumn, winter, spring) alongside the summer one you already have.
   - Style all four consistently — same colour ramp, same value range — so they're actually comparable to each other rather than each looking dangerous in its own way.
   - Compare the Western Cape and Limpopo across the four rasters. Which season looks most severe in each province?

> **Think about it:** If the two provinces peak in different seasons, what does that tell you about their climates? Think about when each region gets its rainfall, and when its vegetation would be driest.

### Deliverable

Produce a single 4-panel map for one province, showing that province's summer, autumn, winter, and spring severity rasters side by side, each styled with the same colour ramp so they're genuinely comparable. Use QGIS's layout tools (check the Project menu for a print layout option) to arrange the four small maps together with clear labels for each season.

Underneath or alongside the map, write one paragraph of your own observations about the seasonal pattern you found — which season is worst for your chosen province, whether that matches what you'd expect from its climate, and anything that surprised you.

Submit your exported PNG here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge

Try computing **fire density** — fires per 100 km² — for each bioregion, by hand.

- You already have an ignition (or fire event) count per bioregion from task 1 this morning.
- You'll need each bioregion's own area in km². If that's not already a field in your bioregion layer, think about how the field calculator's `$area` expression could get you there, and what unit conversion you'd need to go from square metres to km².
- Density = (fire count ÷ bioregion area in km²) × 100.
- Once you have a density value per biome, compare it to your raw counts from this morning — does the biome with the *most* fires still look the most fire-prone once you account for how big it is?

<div style="page-break-after: always;"></div>

## Day 3 — Building a Risk Model

Today you move from describing the landscape to actually modelling risk. You'll take the raster layers you've been building since Day 1 and turn them into a single map that says, in effect, "this is how risky this pixel is." This is the analytical heart of the workbook, so expect it to take real thinking, not just clicking.

A **composite index** is what you get when you combine two or more different measurements into a single score, usually by weighting each one and adding them together. That's exactly what you're building today: one number per pixel that blends fire severity and vegetation dryness into an overall risk rating.

### Morning Session

1. **Zonal statistics on fire severity.** For each bioregion polygon, you need the mean and max predicted severity from yesterday's summer severity raster. Use **Raster > Zonal Statistics** to do this — it calculates statistics (like mean, max, standard deviation) for a raster within the boundary of each polygon in a vector layer, and writes the results as new columns in that layer's attribute table.
   - Run it once, check the new columns appeared, and sort the attribute table to find out which bioregion has the highest mean severity and which has the highest max severity. They might not be the same bioregion — think about why.
   - Build a small ranking table (bioregion, mean severity, max severity) so you can compare it to something in a moment.

   > **Hint:** Think about which raster actually answers this question, and which statistics you'll need ticked before you run the tool.

   > **Photo 18 — Zonal Statistics Dialog.** See the Photo List appendix for exactly what to capture.

   > **Checkpoint:** Open the bioregion attribute table — you should see new columns holding a mean and a max value for every polygon, with no blank or zero rows. If a bioregion shows zero everywhere, double-check the raster actually overlaps that polygon.

2. Now pull up your ignition-count ranking of bioregions from yesterday and put it side by side with today's severity ranking.

   > **Think about it:** Does the bioregion with the most fire ignitions also have the highest predicted severity? If not, what might that mean — are ignitions and severity actually measuring different things? One could be about how often fires start, the other about how bad they get once they do.

3. **Reclassify severity into risk classes.** A continuous raster (one where every pixel can hold any value along a smooth range, like severity from 0 to 1) is hard to compare across layers. Use **Raster > Reclassify by Table** to convert the severity raster into 5 discrete classes, where 1 means lowest risk and 5 means highest risk.
   - You decide where the class breaks fall — look at the raster's value range first (its min and max) so your five classes actually span the data sensibly, rather than being evenly split on a scale the data doesn't use.
   - Name the output `severity_reclass` — you'll need this exact name for the Raster Calculator step later.

   > **Hint:** Check the raster's minimum and maximum values first (right-click the layer, look for information about its properties) before you decide where each class boundary should sit.

   > **Photo 19 — Severity Reclassify Table.** See the Photo List appendix for exactly what to capture.

   > **Checkpoint:** Style the reclassified layer with 5 distinct colours (one per class). You should see a clear spatial pattern — patches of class 5 should roughly line up with the areas you already know have high severity from Day 2.

4. **Reclassify NDVI too — but inverted.** NDVI doesn't map onto fire risk the same way severity does. Lush, green vegetation with high NDVI should end up as *low* fire risk, and dry, sparse vegetation with low NDVI should end up as *high* fire risk. Use **Raster > Reclassify by Table** again, but flip the direction of the scale this time so low NDVI values map to class 5 and high NDVI values map to class 1. Name the output `ndvi_reclass` — you'll need this exact name for the Raster Calculator step later.

   > **Watch out:** It's very easy to reclassify NDVI the same direction as severity out of habit. Before you move on, check a pixel you know is thick forest — it should land in class 1 or 2, not class 5.

   > **Think about it:** What is NDVI actually measuring, physically? It's derived from how much red and near-infrared light vegetation reflects, which relates to chlorophyll and leaf structure — essentially, how alive and water-filled the plant material is. Why would drier, less vigorous vegetation be more dangerous in a fire?

   > **Photo 20 — NDVI Reclass Inverted.** See the Photo List appendix for exactly what to capture.

Before lunch, pause and think about what you now have: two separate 1–5 risk layers, one from severity and one from NDVI. They won't agree everywhere.

> **Think about it:** If you had to combine these two into one score, would you treat them as equally important? A fire scientist would probably argue that predicted severity — because it already reflects fuel, weather, and terrain together — should count for more than vegetation dryness alone. A 60/40 split (severity weighted more heavily) is a reasonable starting position. Do you agree, and would you ever change that split for a different landscape?

### Afternoon Session

1. **Build your composite risk raster.** Open **Raster > Raster Calculator** and combine your two reclassified layers using this pattern, plugging in the two weights you settled on earlier — they should sum to 1 (for example 0.6 and 0.4 if you agreed with the reasoning above, or your own split):

   ```
   ("severity_reclass@1" * <severity_weight>) + ("ndvi_reclass@1" * <ndvi_weight>)
   ```

   - The `@1` refers to band 1 of each raster — reclassified rasters normally only have one band, but the calculator still needs you to specify it.
   - Save the output with a clear name, such as `composite_risk`, and apply a red colour ramp so higher values read as "hotter."

   > **Watch out:** Raster Calculator will refuse to combine layers that don't share the same extent and pixel size. If you get an error, check the properties of both reclassified rasters — this is one of the most common snags in raster work, and it's worth knowing how to spot it rather than just re-running the tool.

   > **Photo 21 — Raster Calculator Formula.** See the Photo List appendix for exactly what to capture.

   > **Checkpoint:** Your composite raster's values should range roughly from 1 to 5, but now as decimals (since you're blending two integer classes), and the red ramp should show hot spots where both severity and dryness were already high. If your output is all one flat colour, check that your reclassified layers actually have variation in them.

   > **Photo 22 — Composite Risk Map Red Ramp.** See the Photo List appendix for exactly what to capture.

2. **Compare your model to the real one.** Overlay your composite risk raster against the trained model's own severity raster output from Day 2. Use layer transparency, or the Map Swipe Tool (found on the toolbar, or under View > Panels), to look at where they agree and where they sharply disagree.

   > **Think about it:** The trained model behind that severity raster used more than 170 input variables — soil moisture, historical weather, fuel type, terrain, and much more. You built your version from just 2. Where does your simple model hold up surprisingly well, and where does it clearly miss something the full model captured? What does that tell you about why professional fire risk pipelines are so much more complex than what you built today?

3. **Extension for fast finishers.** If you finish early, try adding a third variable to your composite formula. A slope layer from the static grid (the fixed set of terrain and climate layers used to train the model) is a natural choice, since steeper terrain lets fire spread faster; some of you might instead try the model's Fire Weather Index (FWI) output — a measure of how flammable the weather conditions are — as a third variable. Either way, you'll need to reclassify the new layer to the same 1–5 scale first, then rework your weighted formula in Raster Calculator so the three weights still add up to 1.

   > **Hint:** If severity keeps the largest weight, you might try something like 0.5 severity, 0.3 NDVI, 0.2 slope — but there's no single correct split. Be ready to justify whatever weights you choose.

4. **Risk summary for one district municipality.** Pick one district municipality (one of South Africa's mid-level administrative regions, between a local municipality and a province) and work out what proportion of its area falls into each of your 5 composite risk classes. You can do this properly with **Raster > Zonal Statistics** (or a related zonal tool that reports class counts) against the municipality boundary, or make a careful visual estimate if you're short on time. Either way, produce a simple summary table: risk class 1 through 5, and the percentage of the municipality's area in each.

   > **Checkpoint:** Your percentages across all 5 classes should add up to roughly 100%. If they don't, you're probably missing pixels outside the raster's extent or double-counting overlapping zones.

### Deliverable

By the end of today, be ready to show:

- Your finished composite risk map for one province, styled with a red colour ramp.
- A side-by-side (or overlaid/swiped) comparison of your composite map against the trained model's severity raster.
- Your risk class summary table for the one district municipality you chose.
- A short written explanation (a few sentences is enough) of what your model captures well and what it misses compared to the full trained model.

Submit your map, table, and written explanation here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge

Add a third variable to your composite risk model — either the slope layer from the static grid or the trained model's Fire Weather Index (FWI) output — and rebuild your weighted Raster Calculator formula so all three weights sum to 1. Be ready to explain why you chose the weights you did.

<div style="page-break-after: always;"></div>

## Day 4 — Presenting to Two Clients

### The Brief

You've spent three days building up a GIS skillset: loading and exploring wildfire data, styling and analyzing it, and combining rasters and vectors into risk indicators. Today you put all of it to work — twice.

Here's the setup: you work for a small geospatial consultancy, and two different clients have each asked for a short visual analysis to support a decision. Same underlying data both times — the same fires, the same bioregions, the same composite risk raster you built yesterday — but two different questions, from two different people, who care about different things. Your job today is to prove to yourself that "the data" doesn't hand you one answer; the story you tell depends on who's asking.

This section will not tell you which tools to use for which map. That's the job today. You've done zonal statistics, reclassification, raster calculators, joins, and print layouts before — figuring out which combination answers each brief, and in what order, is the actual skill being assessed.

Today is individual work — no pairs, no groups. Everyone picks their own two briefs, builds two atlases, and puts together two decks.

> **Think about it:** Before you open QGIS, sketch on paper (or in your head) what each of your three maps needs to show and roughly how you'll get there. Ten minutes of planning will save you an hour of backtracking — for each brief.

### Choose Your Two Clients

Pick TWO of the three briefs below — one for your morning session, one for your afternoon session. Read all three before deciding.

**Brief A — The Insurer**
*"Which municipalities in the Western Cape should be charged the highest wildfire premiums?"*

- Map 1: Fire frequency, shown as a choropleth (a map where areas are shaded by value, like population density) of ignition counts by municipality.
- Map 2: Seasonal severity raster with fire event points overlaid.
- Map 3: A composite risk index, with municipality boundaries drawn on top.

**Brief B — The Conservation Planner**
*"Which bioregions are burning most severely, and is fire frequency changing over time?"*

- Map 1: Ignition count per bioregion, shown as a choropleth built from a zonal count.
- Map 2: Mean severity per bioregion, from zonal statistics.
- Map 3: An early-period versus late-period comparison, splitting fire events by the decade of `start_date`.

**Brief C — The Emergency Manager**
*"Where are the largest fire events, and what landscape features are they associated with?"*

- Map 1: The top 50 largest fires by area, styled and labelled.
- Map 2: Those same fires overlaid on NDVI and bioregions.
- Map 3: A composite risk map highlighting those areas.

> **Watch out:** It's tempting to pick two briefs that end up needing almost the same maps in a different colour. For today's exercise to actually teach you something, pay attention going in to whether your two chosen briefs genuinely ask different questions of the data — not just the same map with a different title.

> **Think about it:** Before building anything, write one sentence per brief: who is asking, and what do they actually need to know to make a decision? Keep both sentences somewhere visible — you'll come back to them at the end of the day.

### Tools You Already Know

A memory jog, not a manual. Somewhere in this workshop you've used all of these — today is about deciding which ones apply, and when:

- Styling and symbology (graduated, categorized symbology)
- Labelling
- Print Layout (multi-map atlases, legends, titles, scale bars)
- Attribute joins
- Zonal Statistics
- Reclassify
- Raster Calculator
- Selection and export by expression or attribute
- Layer ordering and grouping

### Morning Session: Your First Brief

1. Confirm your first brief and identify the three maps you need to produce.
2. Work out, layer by layer, what already exists in your project and what you still need to build or derive.
3. Build each intermediate layer or raster in whatever order makes sense for your brief.
4. Style each map so that it stands alone but also reads as part of one consistent set.
5. Assemble your three maps — either as one combined Print Layout or as three separate exports, whichever will drop more cleanly into slides — with enough labelling (titles, legends, a scale bar, north arrow) that someone outside the room could understand them without you talking.

> **Checkpoint:** Before you call it done, look at your atlas as if you were the client and had never seen the data before. Could you answer the brief's question just by looking at the three maps? If you have to explain something out loud that isn't on the page, add it to the page.

Then build your deck for this brief: a short PowerPoint (6 to 8 slides) you would present if you were standing in front of this client — a title/brief slide, one slide per map, and a slide with your direct answer to the client's question. Write real speaker notes on every slide — the actual words you'd say out loud, not a repeat of the slide's bullet points.

> **Think about it:** A good speaker note doesn't just restate the slide's text — it's what makes the slide land when spoken out loud. If you read your notes back and they just repeat the bullet points, rewrite them.

### Afternoon Session: Your Second Brief

Repeat the same process for your second brief — new maps, new deck.

Before you start building, look back at what you produced this morning:

- Which layers or rasters can you carry over untouched?
- Which ones need to be re-derived or re-styled because the question changed, even though the underlying data didn't?

> **Real Pipeline Connection:** This is exactly the situation Riskscape's own team is in constantly — one severity model, one set of fire records, feeding completely different products depending on who's asking: an insurer pricing premiums, a conservation planner tracking bioregion health, an emergency manager triaging response. The data doesn't change. The question does.

Build this second brief's atlas and deck the same way you did the first — but this time, on your closing slide, use your speaker notes to answer:

- What surprised you most about the data, across both briefs?
- What would you do differently if you had another day?
- What data do you wish you had that was not given to you?
- If you were either client, would you trust this analysis, and why or why not?
- Looking at your two decks side by side: what actually changed between them because the audience and question changed, and what stayed the same because the underlying data didn't? What does that tell you about who "owns" a dataset's story?

### Deliverable

Two short PowerPoint decks, built on your own — one per brief — each with its own 3-map atlas worked into the slides and full speaker notes on every slide, as if you were about to present each one to its client. Your second deck's closing slide should include the side-by-side reflection above.

Submit both `.pptx` files here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

### Extension Challenge

Pick the one brief you didn't build. Without fully building it, sketch out (in a short written note, or as an extra slide) how your morning or afternoon deck would need to change to answer it instead — which maps would carry over, which would need to be rebuilt from scratch, and why.

<div style="page-break-after: always;"></div>

## Appendices

### Appendix: One-Page QGIS Cheat Sheet

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

> **Hint:** Most of these dialogs remember your last settings, so double-check every field before you click Run, especially the output file location.

### Appendix: Troubleshooting

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

### Appendix: Glossary of Terms

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

## Photo List (For the Instructor)

### Getting Ready

1. QGIS Empty Launch — QGIS open for the first time, showing the empty map canvas with no layers loaded
2. New Empty Project Saved — A newly created, blank QGIS project saved to the Desktop, with no layers loaded yet

### Day 1

3. QGIS Blank Interface — the empty QGIS window with the Layers panel, Browser panel, map canvas, and status bar all labelled
4. SA Boundary Transparent — the South Africa boundary showing as a transparent shape with a black outline, filling the map canvas
5. Fire Polygons Overview — the fire event polygons loaded over the South Africa boundary, zoomed to show the whole country
6. Attribute Table Sorted — the attribute table sorted by area_km2 descending, with the top row highlighted
7. Status Bar Coordinates — the bottom-right corner of QGIS showing live coordinates as the mouse moves over the map
8. Graduated Symbology Dialog — the Symbology tab set to graduated, area_km2 selected as the field, 5 classes, and a white-to-dark-red colour ramp chosen
9. Fire Map Graduated — the finished map with fires shaded from pale to dark red by size
10. Ignition Points Orange — the ignition points shown as small orange dots over the fire polygons
11. Bioregions Categorized — the bioregions layer shown with transparent fill and a distinct border colour for each biome, fire polygons visible underneath
12. Print Layout Elements — the print layout with title, legend, north arrow, and scale bar all placed around the map

### Day 2

13. Count Points in Polygon Dialog — the Count Points in Polygon dialog with the points and polygons layers selected
14. Fire Events with Biome Column — the fire events attribute table showing the new biome name column after the join
15. NDVI Green Ramp Styled — the NDVI summer raster displayed with your chosen green colour ramp
16. Severity Raster with Fire Overlay — the reversed RdYlGn severity raster with fire event polygons drawn on top

### Day 3

18. Zonal Statistics Dialog — the Zonal Statistics dialog with the summer severity raster and bioregion layer selected and mean/max ticked
19. Severity Reclassify Table — the Reclassify by Table dialog showing five class ranges mapped to values 1 through 5
20. NDVI Reclass Inverted — the inverted NDVI reclassification, showing sparse/dry areas symbolized as high risk classes
21. Raster Calculator Formula — the Raster Calculator dialog with the weighted formula typed in and the two reclassified layers listed
22. Composite Risk Map Red Ramp — the finished composite risk raster styled with a red colour ramp across the province

### Day 4

No photos tagged in this section.

### Appendices

No photos were tagged in this section.