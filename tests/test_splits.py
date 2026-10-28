"""Check the identifier lists in splits/ against the counts reported in the paper."""

import csv
from collections import Counter, defaultdict
from pathlib import Path

SPLITS = Path(__file__).resolve().parents[1] / "splits"


def read(name):
    with (SPLITS / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_ham_development():
    rows = read("ham_development_folds.csv")
    assert len(rows) == 8513
    assert len({r["image_id"] for r in rows}) == 8513
    assert len({r["lesion_id"] for r in rows}) == 6349
    folds_per_lesion = defaultdict(set)
    for r in rows:
        folds_per_lesion[r["lesion_id"]].add(r["fold"])
    assert all(len(v) == 1 for v in folds_per_lesion.values())
    sizes = Counter(r["fold"] for r in rows)
    assert [sizes[str(k)] for k in range(5)] == [1712, 1724, 1704, 1658, 1715]


def test_ham_fixed_test():
    dev = read("ham_development_folds.csv")
    test = read("ham_fixed_test.csv")
    assert len(test) == 1502
    assert len({r["lesion_id"] for r in test}) == 1121
    assert not {r["image_id"] for r in dev} & {r["image_id"] for r in test}
    assert not {r["lesion_id"] for r in dev} & {r["lesion_id"] for r in test}
    assert len(dev) + len(test) == 10015


def test_bcn20000():
    rows = read("bcn20000_images.csv")
    assert len(rows) == 11977
    assert len({r["external_image_id"] for r in rows}) == 11977
    assert len({r["external_lesion_id"] for r in rows}) == 3453


if __name__ == "__main__":
    test_ham_development()
    test_ham_fixed_test()
    test_bcn20000()
    print("PASS: split and cohort identifier lists")
