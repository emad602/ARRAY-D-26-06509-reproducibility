"""Model definitions and fusion arithmetic of the frozen system (Methods 2.4).

Contains the ConvNeXt-S and DINOv2 classifier heads, the residual fusion network,
and the averaging and temperature-scaling step. No trained weights are included.
"""

CLASS_ORDER = ("akiec", "bcc", "bkl", "df", "mel", "nv", "vasc")
MEAN = (0.485, 0.456, 0.406)
STD = (0.229, 0.224, 0.225)


def preprocessing():
    from torchvision import transforms as T
    from torchvision.transforms import InterpolationMode as I

    conv = T.Compose(
        [
            T.Resize(int(320 * 1.08), interpolation=I.BICUBIC, antialias=True),
            T.CenterCrop(320),
            T.ToTensor(),
            T.Normalize(MEAN, STD),
        ]
    )
    dino = T.Compose(
        [
            T.Resize(350, interpolation=I.BICUBIC, antialias=True),
            T.CenterCrop(322),
            T.ToTensor(),
            T.Normalize(MEAN, STD),
        ]
    )
    return conv, dino


def convnext_architecture():
    import torch.nn as nn
    from torchvision.models import convnext_small

    model = convnext_small(weights=None)
    f = model.classifier[2].in_features
    model.classifier[2] = nn.Sequential(nn.Dropout(0.25), nn.Linear(f, 7))
    return model


def dino_classifier(backbone):
    import torch, torch.nn as nn

    class Classifier(nn.Module):
        def __init__(self, b):
            super().__init__()
            self.backbone = b
            d = int(b.embed_dim) * 2
            self.head = nn.Sequential(
                nn.LayerNorm(d), nn.Dropout(0.25), nn.Linear(d, 7)
            )

        def forward(self, x):
            f = self.backbone.forward_features(x)
            z = torch.cat(
                [f["x_norm_clstoken"], f["x_norm_patchtokens"].mean(1)], dim=1
            )
            return self.head(z)

    return Classifier(backbone)


def residual_fusion_architecture():
    import torch.nn as nn

    class Residual(nn.Module):
        def __init__(self):
            super().__init__()
            self.norm = nn.LayerNorm(14, elementwise_affine=False)
            self.correction = nn.Sequential(
                nn.Linear(14, 64), nn.GELU(), nn.Dropout(0.15), nn.Linear(64, 7)
            )

        def forward(self, x, conv_logp):
            return conv_logp + self.correction(self.norm(x))

    return Residual()


def apply_frozen_fusion(conv_probs, dino_probs, models, temperature):
    """5-fold branch means in; 3-seed mean then frozen scalar temperature out."""
    import numpy as np, torch

    def norm(v):
        v = np.clip(np.asarray(v, dtype=np.float64), 1e-9, None)
        return v / v.sum(1, keepdims=True)

    assert len(models) == 3 and temperature > 0
    c, d = norm(conv_probs), norm(dino_probs)
    logc = torch.from_numpy(np.log(c).astype(np.float32))
    x = torch.cat([logc, torch.from_numpy(np.log(d).astype(np.float32))], dim=1)
    seed_probs = []
    with torch.no_grad():
        for m in models:
            m.eval()
            seed_probs.append(torch.softmax(m(x, logc).float(), dim=1).cpu().numpy())
    p = norm(np.mean(seed_probs, axis=0))
    logits = np.log(np.clip(p, 1e-12, None)) / temperature
    out = np.exp(logits - logits.max(axis=1, keepdims=True))
    return out / out.sum(1, keepdims=True)
