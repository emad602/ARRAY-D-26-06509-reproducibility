# Split and cohort identifier lists

These files contain identifiers only: no diagnoses, labels, predictions, image paths, image hashes or patient information. The identifiers are those of the original datasets, which remain the property of their providers and must be obtained from them under their terms.

| File | Rows | Columns | Content |
|---|---|---|---|
| `ham_development_folds.csv` | 8,513 | `image_id`, `lesion_id`, `fold` | The five lesion-disjoint folds (0–4) used for the out-of-fold analysis. Each lesion is in one fold. |
| `ham_fixed_test.csv` | 1,502 | `image_id`, `lesion_id` | The fixed HAM10000 test images (1,121 lesions), disjoint from the development set. This set had been evaluated with earlier systems; see the manuscript. |
| `bcn20000_images.csv` | 11,977 | `cohort_row_index`, `external_image_id`, `external_lesion_id` | The BCN20000 images used (3,453 lesions), in the order used for inference. |

The Derm7pt cohort (1,011 cases, 987 after the six-class mapping) is defined by the diagnosis mapping in Supplementary Table S3 of the manuscript, applied to the public Derm7pt metadata. No Derm7pt list is distributed here.

The BCN20000 list describes an evaluation cohort. It is not a training or test split; BCN20000 was used for evaluation only.

`tests/test_splits.py` checks these files against the counts in the paper.

| File | SHA-256 |
|---|---|
| `ham_development_folds.csv` | f562853debb13e0fad038cba8b7826118f8239e984a49b34ca8c9f8268dd179c |
| `ham_fixed_test.csv` | eb7ea31c4f4266a72aacc251563bd0a0c63c459580e5b046fde909744698aaba |
| `bcn20000_images.csv` | ff4aa970eafad588515b66660ed66fecf4e013e19546af65e997bca0aabbda5f |

## Sources

- HAM10000: Tschandl P, Rosendahl C, Kittler H. The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions. Scientific Data 2018;5:180161. https://doi.org/10.1038/sdata.2018.161
- Derm7pt: Kawahara J, Daneshvar S, Argenziano G, Hamarneh G. Seven-point checklist and skin lesion classification using multitask multimodal neural nets. IEEE Journal of Biomedical and Health Informatics 2019;23:538–546. https://doi.org/10.1109/JBHI.2018.2824327
- BCN20000: Hernandez-Perez C, Combalia M, Podlipnik S, et al. BCN20000: Dermoscopic Lesions in the Wild. Scientific Data 2024;11:641. https://doi.org/10.1038/s41597-024-03387-w
