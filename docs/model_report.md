import torch.nn as nn


class LeNet5(nn.Module):
    """
    Classic LeNet-5 (LeCun, 1998), adapted for 28x28x1 input (Fashion MNIST).
    Note: real LeNet-5 has no dropout — it predates the technique.
    `dropout` is accepted only so the constructor matches SimpleCNN's
    interface; it isn't used inside this model.
    """
    def __init__(self, num_classes=10, dropout=0.3):
        super().__init__()
        self.conv_block = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, padding=2),   # 28x28x1  -> 28x28x6
            nn.ReLU(),
            nn.AvgPool2d(2),                              # -> 14x14x6
            nn.Conv2d(6, 16, kernel_size=5),               # -> 10x10x16
            nn.ReLU(),
            nn.AvgPool2d(2),                              # -> 5x5x16
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                                  # -> 400
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, num_classes),
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.classifier(x)
        return x


class VGGMini(nn.Module):
    """
    VGG-11-style network, adapted for 28x28x1 input (Fashion MNIST).
    Keeps VGG-11's exact per-block conv-layer pattern (1, 1, 2, 2, 2) and
    channel progression (64, 128, 256, 512, 512), plus its BatchNorm + ReLU
    + MaxPool convention.

    Deviation from textbook VGG-11: real VGG-11 pools 5 times on a 224x224
    input. On 28x28, a 5th pool would shrink a 1x1 map to 0x0. Block 5 here
    keeps its two conv layers (matching real VGG-11's structure) but skips
    the trailing pool, since there's no spatial size left to reduce.
    """
    def __init__(self, num_classes=10, dropout=0.3):
        super().__init__()
        self.conv_block = nn.Sequential(
            # Block 1
            nn.Conv2d(1, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 28 -> 14

            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 14 -> 7

            # Block 3 (two conv layers, like real VGG-11)
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 7 -> 3

            # Block 4 (two conv layers)
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 3 -> 1

            # Block 5 (two conv layers, no pool — already at 1x1)
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                                  # -> 512
            nn.Linear(512 * 1 * 1, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.conv_block(x)
        x = self.classifier(x)
        return x