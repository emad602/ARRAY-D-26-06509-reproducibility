"""Check that the fusion step returns valid probabilities (synthetic input, needs torch)."""

from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fusion import residual_fusion_architecture, apply_frozen_fusion


def run():
    p = np.ones((3, 7), dtype=np.float64) / 7
    models = [residual_fusion_architecture() for _ in range(3)]
    out = apply_frozen_fusion(p, p, models, 0.8378957941821958)
    assert out.shape == (3, 7)
    assert np.allclose(out.sum(axis=1), 1, atol=1e-8)
    assert np.isfinite(out).all()


if __name__ == "__main__":
    run()
    print("PASS: frozen fusion reference smoke test")
