# Mapping Wildfire Risk in South Africa: A QGIS Student Workbook — Day 3 (Advanced Track)

*A companion track for honours-level GIS students, run alongside the standard 4-day workshop. Standard Day 3 builds a composite risk map by hand-picking two weights and arguing for them. Today you let real fire data pick those weights instead, by training a small regression model of your own. This isn't Riskscape's real severity model — that stays exactly as private as it's been all week. You're building a brand-new, fully transparent model from scratch, using only the same rasters and real fire records you've had access to since Day 1.*

*One more thing before you start: this document names the concepts and functions you need, not a script to copy. Standard Day 3 tells you which QGIS tool to open at each step but leaves the actual decisions — where the class breaks fall, what the weights should be — to you. Today works the same way, just in code. Figuring out the exact lines, and living with the consequences of your choices, is the exercise.*

---

## Before You Start

You already have everything you need from Day 2 Advanced: the `firerisk` conda environment, VS Code set up to run plain `.py` scripts against it. Add one package:

```
conda install -c conda-forge scikit-learn
```

> **Checkpoint:** From your activated `firerisk` environment, `python -c "import sklearn; print(sklearn.__version__)"` should print a version number.

---

## Morning Session: Building a Training Dataset

1. **Bring back yesterday's data.** Day 2 Advanced left you with a table of real ignition points, each carrying a sampled `severity` value, a sampled `ndvi` value, and the real `area_per_day` for that fire. That table is today's raw material — you shouldn't need to write the raster-sampling code again, just get that result back into a fresh script.

2. **Commit to a weight guess before you look at any data.** Standard Day 3 asks students to argue for a split like 60% severity, 40% NDVI, based on reasoning about which factor should matter more. Do that now, in a comment at the top of your script, with your reasoning — before you fit anything. Write it down and don't change it later. This isn't a formality: if you pick your "hand-picked" weights *after* seeing what the model learned, you'll unconsciously reverse-engineer a story that fits, and the comparison you're about to make becomes worthless.

3. **Reclassify `severity` and `ndvi` into the same 1–5 scheme standard Day 3 uses.** Same idea as QGIS's Reclassify by Table — you decide where the class breaks fall (look at the actual range of your sampled values first), and NDVI still needs to be inverted, since low NDVI means high risk. In pandas, look at what `pd.cut()` does with a `bins` argument — that's the tool for turning a continuous column into a labelled class column without writing a manual chain of comparisons.

   > **Watch out:** NDVI's direction is exactly as easy to get backwards in code as it was in the QGIS dialog. Before moving on, check a row you know has thick, healthy vegetation — it should land in class 1 or 2, not 5.

   > **Checkpoint:** `value_counts()` on your two new class columns should show all five classes represented, without one class swallowing almost everything. If one class has nearly all your points, your breaks probably don't span the actual data range.

4. **Think about where your training data comes from.** Every row in this table is a place a fire *did* happen. Think about it: does that introduce any bias into a model meant to describe fire risk everywhere, including places that have never burned? You don't need to fix this today — but you do need to be able to name it, in your own words, in your final write-up.

5. **Split into training and test sets before fitting anything.** Look up `train_test_split` from `sklearn.model_selection`. Hold back roughly a fifth of your points as a test set the model never sees during training.

   > **Real Pipeline Connection:** Production model evaluation always scores a model against data it never trained on. A model's performance on its own training data tells you almost nothing about how it'll behave on a fire it hasn't seen — this is true whether the model is a two-variable toy or Riskscape's real one.

---

## Afternoon Session: From a Guess to a Learned Weight

1. **Standardize your two features before fitting anything.** Look up `StandardScaler` from `sklearn.preprocessing`. Fit it on your training data only, then use it to transform both the training and test sets — never let information from your test set leak into how the scaler is fit.

   > **Watch out:** `severity_class` and `ndvi_class` may not have the same natural spread even though both run 1–5. Skip standardizing and whichever feature happens to vary more will look artificially more "important" once you inspect the fitted model, regardless of what's actually driving fire behaviour.

2. **Fit a `LinearRegression`** (from `sklearn.linear_model`) predicting `area_per_day` from your two standardized features, using the training set only.

3. **Turn the fitted coefficients into a weight pair.** A fitted `LinearRegression` stores what it learned in a `.coef_` attribute — one number per feature, in the order you gave them. Those two numbers aren't weights yet; they don't necessarily sum to 1, and they can be negative. Work out how to turn them into a `(w_severity, w_ndvi)` pair in the same shape as the guess you committed to in step 2 this morning — you've done this kind of normalization before, in Day 1 Advanced's frequency grid.

   > **Checkpoint:** Your two learned weights should sum to (approximately) 1. If one comes out negative, don't assume you've made a mistake — think about what a negative weight would actually mean for that variable before deciding it's a bug.

4. **Score the model honestly.** A fitted scikit-learn regression has a `.score()` method that returns R² given features and a true target — run it against your held-out test set, not the training set.

   > **Think about it:** Don't expect this number to be impressive, and that's not a failure state. You've built a model from two variables; the real severity model behind the raster you've used all week was trained on more than 170. What does a modest (or poor) R² actually tell you about how much of real fire behaviour these two variables alone can explain? Write your answer down — you'll need it for the deliverable.

5. **Build your learned-weight composite raster.** Using the two learned weights in place of the guess from step 2, recompute the same weighted-sum formula standard Day 3 uses — but now across the entire raster, not just your sample points. You'll need to apply the same class-break logic from this morning to the full severity and NDVI raster arrays (not just the sampled column), which means working with the raw pixel arrays rather than a pandas column — `numpy`'s `digitize` or `select` functions do the same job as `pd.cut`, just on an array instead of a Series. Write the result out as a new raster.

   > **Real Pipeline Connection:** This is the same move the real pipeline makes constantly — a relationship learned from a sample of points gets applied back across every pixel of the country, not just the pixels it was trained on.

6. **Compare three rasters.** Your hand-picked composite (from the guess you committed to this morning — recompute it the same way, across the full raster, for a fair comparison), your learned-weight composite, and the real trained model's severity raster from Day 2. Look at where they agree and where they diverge.

### Optional Extension: A Third Feature, or a Different Kind of Model

Standard Day 3's fast-finisher extension adds a third variable (slope or FWI) to the hand-picked composite. Do the equivalent here: sample the slope raster at your ignition points, reclassify it the same way, add it as a third feature, and refit. Does the three-way learned split resemble anything like the "0.5/0.3/0.2"-style guess standard Day 3 suggests?

If you want to push further: fit a `DecisionTreeRegressor` or `RandomForestRegressor` on the same features and compare its `.feature_importances_` to your linear model's normalized coefficients. Think about it: a tree-based model with very few features and not many training rows is a classic setup for overfitting — how would you actually tell, using only the tools you already have (training vs. test performance), whether that's happening here?

### Deliverable

A single standalone script, `day3_advanced.py`, that runs top to bottom with no errors and prints:
- Your committed weight guess from this morning, and your reasoning (as a comment, written *before* you saw the model's output).
- The model's learned weights and its test-set R².
- Confirmation that it wrote out the learned-weight composite raster.

At the bottom of the script, add a comment block covering:
- How your guessed weights compared to the learned weights, and whether that surprised you.
- What the R² tells you about how much of real fire behaviour two variables can explain.
- One sentence on the training-data bias question from step 4 of the morning session (every training row is a place that burned).

Your submission is the one `.py` file, plus the raster it produces — no separate write-up.

Submit your `.py` file and raster here: [Submission link](https://1drv.ms/f/c/6b0159811ba5073f/IgBCtMFL7V44SY7MtIISvpVrARTinpbTXgKSoQfrmMpaK4A?e=0DpxMl)

---

Previous: [Day 2 (Advanced Track)](Day_2_Advanced.md) · Continue with the standard cohort: [Day 4](Day_4.md) · Reference: [Appendices](Appendices.md)
