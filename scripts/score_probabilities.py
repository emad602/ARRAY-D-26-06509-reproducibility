#!/usr/bin/env python3
"""Score a table of seven-class probabilities.

Metrics are accuracy, macro-F1 and balanced accuracy. For Derm7pt, pass the six shared
true classes with --true-classes; the model still outputs seven classes, and a
prediction of akiec counts as an error.
"""

import argparse
import csv
import json
import math
from collections import defaultdict

CLASSES = ("akiec", "bcc", "bkl", "df", "mel", "nv", "vasc")
DERM_CLASSES = ("bcc", "bkl", "df", "mel", "nv", "vasc")


def score(rows, lesion_level=False, true_classes=CLASSES):
    true_classes = tuple(true_classes)
    if (
        not true_classes
        or len(set(true_classes)) != len(true_classes)
        or any(x not in CLASSES for x in true_classes)
    ):
        raise ValueError("Invalid true class set")
    records = []
    for row in rows:
        y = row["true_class"]
        if y not in true_classes:
            raise ValueError("Unexpected true class in scored cohort: " + y)
        p = [float(row["p_" + c]) for c in CLASSES]
        if (
            any(not math.isfinite(v) or v < 0 or v > 1 for v in p)
            or abs(sum(p) - 1) > 1e-4
        ):
            raise ValueError("Invalid seven-output probabilities")
        records.append((row.get("lesion_id") or "", y, p))
    if lesion_level:
        groups = defaultdict(list)
        for lid, y, p in records:
            if not lid:
                raise ValueError("lesion_id required")
            groups[lid].append((y, p))
        records = []
        for lid, items in groups.items():
            if len({y for y, p in items}) != 1:
                raise ValueError("Inconsistent lesion labels")
            records.append(
                (
                    lid,
                    items[0][0],
                    [sum(p[k] for y, p in items) / len(items) for k in range(7)],
                )
            )
    if not records:
        raise ValueError("Empty cohort")
    tp, fp, fn, support = (defaultdict(int) for _ in range(4))
    correct = 0
    for lid, y, p in records:
        pred = CLASSES[max(range(7), key=lambda k: p[k])]
        support[y] += 1
        if y == pred:
            correct += 1
            tp[y] += 1
        else:
            fp[pred] += 1
            fn[y] += 1
    f1 = [
        2 * tp[c] / (2 * tp[c] + fp[c] + fn[c]) if 2 * tp[c] + fp[c] + fn[c] else 0.0
        for c in true_classes
    ]
    recall = [tp[c] / support[c] if support[c] else 0.0 for c in true_classes]
    return dict(
        n=len(records),
        accuracy=correct / len(records),
        macro_f1=sum(f1) / len(f1),
        balanced_accuracy=sum(recall) / len(recall),
        true_classes=list(true_classes),
        class_support={c: support[c] for c in true_classes},
    )


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("input_csv")
    a.add_argument("--lesion-level", action="store_true")
    a.add_argument("--true-classes", default=",".join(CLASSES))
    args = a.parse_args()
    with open(args.input_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(
        json.dumps(
            score(rows, args.lesion_level, args.true_classes.split(",")),
            indent=2,
            sort_keys=True,
        )
    )
