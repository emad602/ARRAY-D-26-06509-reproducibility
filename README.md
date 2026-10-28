# Prediction-frozen external validation of CNN–Transformer fusion: code and aggregate results

Materials accompanying the manuscript *Prediction-Frozen External Validation of CNN–Transformer Fusion Reveals Class-Dependent Generalization Degradation in Dermoscopy*.

The study evaluates a frozen ensemble of five ConvNeXt-S and five DINOv2 ViT-B/14 models with residual-MLP fusion on HAM10000 (lesion-disjoint five-fold out-of-fold), Derm7pt and BCN20000.

## Contents

| Folder | What it contains |
|---|---|
| `src/` | Model definitions and the fusion/temperature calculation (`fusion.py`), and the ScNet comparator (`scnet.py`). No trained weights. |
| `scripts/` | `score_probabilities.py`: accuracy, macro-F1 and balanced accuracy from a table of probabilities. |
| `tests/` | Tests on synthetic data, and checks of the BCN20000 lesion-level table and of the identifier lists in `splits/`. |
| `protocols/` | Analysis protocols and decision rules. See `protocols/README.md`. |
| `splits/` | Identifier lists: HAM10000 fold assignment and fixed test set, and the BCN20000 evaluation images. No labels. See `splits/README.md`. |
| `tables/` | Aggregate results (no case-level data). |

## Running the tests

Python 3.11 or newer. The first three commands need no extra packages.

```
python tests/test_scoring.py
python tests/test_bcn_table.py
python tests/test_splits.py
python tests/test_fusion.py      # needs torch, see requirements.txt
```

## Scoring your own predictions

Provide a CSV with the columns `lesion_id`, `true_class` and `p_akiec, p_bcc, p_bkl, p_df, p_mel, p_nv, p_vasc`.

```
# seven true classes (HAM10000, BCN20000)
python scripts/score_probabilities.py predictions.csv
python scripts/score_probabilities.py predictions.csv --lesion-level

# Derm7pt: six shared true classes, seven model outputs
python scripts/score_probabilities.py predictions.csv --true-classes bcc,bkl,df,mel,nv,vasc
```

In seven-class scoring, classes with no true samples receive zero recall and remain included in the macro averages.

For Derm7pt, a predicted akiec counts as an error and probabilities are not renormalized. With `--lesion-level`, probabilities are averaged over the images of each lesion before the argmax; the script stops if the images of one lesion have different labels.

## What is not included

- Dermoscopic images, diagnosis labels, case-level predictions and trained weights. The files in `splits/` contain identifiers only.
- A complete pipeline from images to probabilities. The tests check the scoring rules, the BCN20000 lesion-level table and the identifier lists; they do not rerun the models, the calibration fit or the bootstrap analyses. The confidence intervals in the paper come from separate analyses.
- No Derm7pt case list is distributed. The Derm7pt cohort is defined by the diagnosis mapping in Supplementary Table S3 of the manuscript.
- The exact DINOv2 source revision and pretrained weights used in the experiments.

## Notes for interpretation

- ScNet is our own reimplementation, trained under a study-specific recipe. It is not the original authors' code.
- BCN20000 had been evaluated with an earlier model before the final system was frozen. BCN20000 results are secondary and retrospective.
- `tables/accuracy_decomposition_by_class.csv` gives point estimates. The confidence intervals are in the paper.
- Latencies are model-execution times on one A100 GPU, without preprocessing or data transfer. MACs are operation counts, not time.

## Data and licence

The MIT licence (`LICENSE`) covers author-owned software in this repository; it does not override any third-party rights or licenses. HAM10000, Derm7pt, BCN20000 and pretrained models must be obtained from their respective providers.
