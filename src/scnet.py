"""ScNet comparator: MobileNetV3-Large backbone with a two-layer classification head.

This is our own reimplementation of the published description, trained under the
study's recipe. It is not the original authors' code.
"""


def build_scnet(pretrained=False, dropout=0.5, num_classes=7):
    from torch import nn
    from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights

    class ScNet(nn.Module):
        def __init__(self):
            super().__init__()
            base = mobilenet_v3_large(
                weights=MobileNet_V3_Large_Weights.IMAGENET1K_V1 if pretrained else None
            )
            self.features = base.features
            self.pool = nn.AdaptiveAvgPool2d(1)
            self.acm = nn.Sequential(
                nn.Linear(960, 512),
                nn.BatchNorm1d(512),
                nn.ReLU(inplace=True),
                nn.Dropout(dropout),
                nn.Linear(512, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(inplace=True),
                nn.Dropout(dropout),
                nn.Linear(128, num_classes),
            )
            for mod in self.acm.modules():
                if isinstance(mod, nn.Linear):
                    nn.init.xavier_uniform_(mod.weight)
                    nn.init.zeros_(mod.bias)
                elif isinstance(mod, nn.BatchNorm1d):
                    nn.init.ones_(mod.weight)
                    nn.init.zeros_(mod.bias)

        def forward(self, x):
            return self.acm(self.pool(self.features(x)).flatten(1))

        def set_backbone_trainable(self, trainable):
            for p in self.features.parameters():
                p.requires_grad = bool(trainable)

        def training_mode(self, backbone_trainable):
            self.train()
            if not backbone_trainable:
                self.features.eval()

    return ScNet()
