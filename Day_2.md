# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 2

*A 4-day introductory workshop (Tuesday to Friday) that teaches first-year students to map, analyse, and model wildfire risk in South Africa using real data and QGIS.*

| Day | Focus | Deliverable |
|---|---|---|
| Day 1 | GIS foundations: load, explore, style, and lay out a map | A styled fire event map with one written observation |
| Day 2 | Spatial analysis: connect fire to the landscape | A 4-panel seasonal severity map with written observations |
| Day 3 | Raster analysis: build your own risk model | A composite risk map compared to the trained model output |
| Day 4 | Capstone: same data, two client stories | Two slide decks (one per brief) with speaker notes, built individually |

Each day runs for about 6 working hours, split into two 2.5 hour sessions with a break in between.

---

## Day 2 — What Drives Fire?

### Recap: What You Did on Day 1

Yesterday you got the QGIS interface under your belt and loaded your first real data. You added the South Africa boundary, the fire event polygons, the ignition points, and the bioregions into your own project; styled the fire polygons with graduated symbology by `area_km2`; and built your first print layout, exporting a styled map of fire events by size with bioregions shown as context.

Today you start asking that data real questions: which biomes burn most, how big are those fires, and what do the underlying maps of vegetation and predicted severity actually tell you about why fire happens where it does. You already know your way around QGIS menus and panels, so this section names the tools you need and trusts you to work out the dialog boxes yourself.

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

---

Previous: [Day 1](Day_1.md) · Next: [Day 3](Day_3.md) · Reference: [Appendices](Appendices.md)
