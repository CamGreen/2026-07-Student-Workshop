# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 3

*A 4-day introductory workshop (Tuesday to Friday) that teaches first-year students to map, analyse, and model wildfire risk in South Africa using real data and QGIS.*

| Day | Focus | Deliverable |
|---|---|---|
| Day 1 | GIS foundations: load, explore, style, and lay out a map | A styled fire event map with one written observation |
| Day 2 | Spatial analysis: connect fire to the landscape | A 4-panel seasonal severity map with written observations |
| Day 3 | Raster analysis: build your own risk model | A composite risk map compared to the trained model output |
| Day 4 | Capstone: same data, two client stories | Two slide decks (one per brief) with speaker notes, built individually |

Each day runs for about 6 working hours, split into two 2.5 hour sessions with a break in between.

---

## Day 3 — Building a Risk Model

### Recap: What You Did on Day 2

On Day 2 you moved from just looking at your Day 1 layers to actually combining them. In the morning you counted ignitions per bioregion, spatially joined the bioregion name onto every fire event, compared average fire size across biomes, and drilled into the largest fires by province. In the afternoon you loaded the NDVI and seasonal severity rasters, compared them against real fire locations, sampled pixels with the Identify tool, clipped a raster to one province, and built a 4-panel map comparing all four seasons.

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

3. **Reclassify severity into risk classes.** A continuous raster (one where every pixel can hold any value along a smooth range) is hard to compare across layers. Use **Raster > Reclassify by Table** to convert the severity raster into discrete classes, where 0 means lowest risk and 5 means highest risk. Map it using this table:

   | Minimum | Maximum | Value |
   |---|---|---|
   | 0 | 0.9 | 0 |
   | 1 | 1.9 | 1 |
   | 2 | 2.9 | 2 |
   | 3 | 3.9 | 3 |
   | 4 | 4.9 | 4 |
   | 5 |   | 5 |

   - Name the output `severity_reclass` — you'll need this exact name for the Raster Calculator step later.

   > **Photo 19 — Severity Reclassify Table.** See the Photo List appendix for exactly what to capture.

   > **Checkpoint:** Style the reclassified layer with 6 distinct colours (one per class, 0 to 5). You should see a clear spatial pattern — patches of class 5 should roughly line up with the areas you already know have high severity from Day 2.

4. **Reclassify NDVI too — but inverted.** NDVI doesn't map onto fire risk the same way severity does. Lush, green vegetation with high NDVI should end up as *low* fire risk, and dry, sparse vegetation with low NDVI should end up as *high* fire risk. Use **Raster > Reclassify by Table** again, but flip the direction of the scale this time so low NDVI values map to class 5 and high NDVI values map to class 1. Name the output `ndvi_reclass` — you'll need this exact name for the Raster Calculator step later.

   > **Watch out:** It's very easy to reclassify NDVI the same direction as severity out of habit. Before you move on, check a pixel you know is thick forest — it should land in class 1 or 2, not class 5.

   > **Think about it:** What is NDVI actually measuring, physically? It's derived from how much red and near-infrared light vegetation reflects, which relates to chlorophyll and leaf structure — essentially, how alive and water-filled the plant material is. Why would drier, less vigorous vegetation be more dangerous in a fire?

   > **Photo 20 — NDVI Reclass Inverted.** See the Photo List appendix for exactly what to capture.

Before lunch, pause and think about what you now have: two separate reclassified risk layers (severity running 0–5, NDVI running 1–5), one from severity and one from NDVI. They won't agree everywhere.

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

   > **Checkpoint:** Your composite raster's values should range roughly from 0 to 5, but now as decimals (since you're blending two integer classes), and the red ramp should show hot spots where both severity and dryness were already high. If your output is all one flat colour, check that your reclassified layers actually have variation in them.

   > **Photo 22 — Composite Risk Map Red Ramp.** See the Photo List appendix for exactly what to capture.

2. **Compare your model to the real one.** Overlay your composite risk raster against the trained model's own severity raster output from Day 2. Use layer transparency, or the Map Swipe Tool (found on the toolbar, or under View > Panels), to look at where they agree and where they sharply disagree.

   > **Think about it:** The trained model behind that severity raster used more than 170 input variables — soil moisture, historical weather, fuel type, terrain, and much more. You built your version from just 2. Where does your simple model hold up surprisingly well, and where does it clearly miss something the full model captured? What does that tell you about why professional fire risk pipelines are so much more complex than what you built today?

3. **Extension for fast finishers.** If you finish early, try adding a third variable to your composite formula. A slope layer from the static grid (the fixed set of terrain and climate layers used to train the model) is a natural choice, since steeper terrain lets fire spread faster; some of you might instead try the model's Fire Weather Index (FWI) output — a measure of how flammable the weather conditions are — as a third variable. Either way, you'll need to reclassify the new layer to the same 1–5 scale first, then rework your weighted formula in Raster Calculator so the three weights still add up to 1.

   > **Hint:** If severity keeps the largest weight, you might try something like 0.5 severity, 0.3 NDVI, 0.2 slope — but there's no single correct split. Be ready to justify whatever weights you choose.

4. **Risk summary for one district municipality.** District municipalities are one of South Africa's mid-level administrative regions, between a local municipality and a province. Load `District_Municipal_Boundary.gpkg` from your data folder — it covers the whole country, so use **Select by Attribute** (look for the field holding each municipality's name) to pick out just one. Work out what proportion of its area falls into each of your 5 composite risk classes, using **Raster > Zonal Statistics** (or a related zonal tool that reports class counts) against your selected municipality, or a careful visual estimate if you're short on time. Either way, produce a simple summary table: risk class 1 through 5, and the percentage of the municipality's area in each.

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

---

Previous: [Day 2](Day_2.md) · Next: [Day 4](Day_4.md) · Reference: [Appendices](Appendices.md)
