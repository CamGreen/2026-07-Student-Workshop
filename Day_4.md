# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 4

*A 4-day introductory workshop (Tuesday to Friday) that teaches first-year students to map, analyse, and model wildfire risk in South Africa using real data and QGIS.*

| Day | Focus | Deliverable |
|---|---|---|
| Day 1 | GIS foundations: load, explore, style, and lay out a map | A styled fire event map with one written observation |
| Day 2 | Spatial analysis: connect fire to the landscape | A 4-panel seasonal severity map with written observations |
| Day 3 | Raster analysis: build your own risk model | A composite risk map compared to the trained model output |
| Day 4 | Capstone: same data, two client stories | Two slide decks (one per brief) with speaker notes, built individually |

Each day runs for about 6 working hours, split into two 2.5 hour sessions with a break in between.

---

## Day 4 — Presenting to Two Clients

### Recap: What You Did on Day 3

On Day 3 you built your own small risk model. You ran zonal statistics on the severity raster per bioregion, reclassified both the severity raster and the NDVI raster into 1–5 risk classes (inverting NDVI's direction so dry vegetation reads as high risk), and blended the two together with a weighted Raster Calculator formula into a single composite risk raster. You then compared your result against the trained model's own severity output and summarised risk classes for one district municipality.

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

---

Previous: [Day 3](Day_3.md) · Reference: [Appendices](Appendices.md)
