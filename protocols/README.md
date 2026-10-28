# Analysis protocols

These versioned protocol records document the analyses and their historical decision rules. Most original analysis locks were recorded before the corresponding analysis; the compute-benchmark source-matching amendment was documented afterward, without changing any reported results. Some analyses were specified after the external labels had already been revealed, as stated in the manuscript. The JSON files were renamed for this repository without changing their bytes; their SHA-256 values match the original versions. Identifiers inside the files (for example W2, M5, 11E) are historical working labels.

| File | Content | Date in file | SHA-256 |
|---|---|---|---|
| `fusion_selection_protocol.json` | Selection of the fusion model and temperature on development data | 2026-08-23 | 4caf146ea370bcb3da5c8fed7c89a0fcf766ea368592da58ab2e159ad0763d8c |
| `input_aggregation_protocol_v1.0.json` | Averaging models before versus after fusion | 2026-10-14 | 16caa38461c0585b9f9477bb54a6b3a8acc4afccb9aab0dddb15b609c1e16855 |
| `ablation_protocol_v1.1.json` | Ablations: single models, simple averaging, linear and residual fusion | 2026-10-15 | b6925dda1aadf3ff521d9c6ad9d0610292e9078f047defcb66b75cc8b2f77cbb |
| `scnet_external_protocol_v1.0.json` | External evaluation of ScNet and the reproduction check | 2026-10-15 | 6e95c30c225443bedddbec6ef67fbe6b3729ef80874b926da8f8cdab6002c9ad |
| `class_cohort_interaction_protocol_v1.1.json` | Test of class-by-cohort interaction | 2026-10-18 | e4d323612de3f5916003e4776e846f3261e9c5d4725b8145b660f56fafc7fd7a |
| `compute_benchmark_protocol_v1.0.json` | Performance-compute comparison | 2026-10-15 | 559b8d8042d67e409344caaa93d66ddbfc5ba065e14f643c8c5326bd93e641b4 |
| `compute_benchmark_amendment_v1.1.json` | Correction to the source of the matched ScNet comparison, made after the analysis; no result changed | not dated | f8fbd10f927333b5e908431ce12ddcc54cf87083114238d184deb49416d3974a |

The analyses of 2026-10-14 and later were carried out after the Derm7pt and BCN20000 labels were known. They are post-exposure analyses (see the manuscript).
