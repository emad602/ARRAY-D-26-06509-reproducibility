#!/usr/bin/env python3
"""Check the BCN20000 lesion-level table (tables/bcn_lesion_level_metrics.csv)."""

import csv
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "tables" / "bcn_lesion_level_metrics.csv"
with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 5, "Five distinct systems are required"
assert {r["system"] for r in rows} == {
    "5C_ConvNeXt",
    "5D_DINOv2",
    "Simple_average",
    "Deployment",
    "ScNet",
}
assert all(int(r["n_lesions"]) == 3453 for r in rows)
by_name = {r["system"]: r for r in rows}
assert abs(float(by_name["Deployment"]["accuracy"]) - 0.6875181002027223) < 1e-12
assert abs(float(by_name["Deployment"]["macro_f1"]) - 0.5453748376663041) < 1e-12
assert (
    abs(float(by_name["Deployment"]["balanced_accuracy"]) - 0.5479494459762783) < 1e-12
)
print("PASS: BCN lesion-level table")
