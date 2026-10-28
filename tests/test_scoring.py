"""Tests for score_probabilities.py on synthetic data."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from score_probabilities import CLASSES, DERM_CLASSES, score


def rec(lid, y, p):
    return dict(
        lesion_id=lid, true_class=y, **{"p_" + c: p[i] for i, c in enumerate(CLASSES)}
    )


def onehot(y):
    return [float(x == y) for x in CLASSES]


def test_derm():
    rows = [rec("a", "mel", onehot("akiec")), rec("b", "bcc", onehot("bcc"))]
    a = score(rows, true_classes=DERM_CLASSES)
    assert (
        a["n"] == 2
        and a["accuracy"] == 0.5
        and a["macro_f1"] == 1 / 6
        and a["balanced_accuracy"] == 1 / 6
    )
    assert score(rows)["macro_f1"] == 1 / 7


def test_lesion():
    assert (
        score(
            [
                rec("x", "bcc", [0.8, 0.2, 0, 0, 0, 0, 0]),
                rec("x", "bcc", [0.1, 0.9, 0, 0, 0, 0, 0]),
            ],
            lesion_level=True,
        )["accuracy"]
        == 1.0
    )


def test_rejection():
    try:
        score([rec("x", "akiec", onehot("akiec"))], true_classes=DERM_CLASSES)
    except ValueError:
        pass
    else:
        raise AssertionError("Unmapped label not rejected")


if __name__ == "__main__":
    test_derm()
    test_lesion()
    test_rejection()
    print("PASS scoring six true/seven outputs and lesion aggregation")
