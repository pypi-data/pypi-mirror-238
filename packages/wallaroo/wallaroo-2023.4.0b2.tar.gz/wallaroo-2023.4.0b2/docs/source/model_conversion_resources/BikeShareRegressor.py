import torch
import torch.nn
import torch.onnx
from torch import nn


class BikeShareRegressor(torch.nn.Module):
    def __init__(self, input_size: int):
        super(BikeShareRegressor, self).__init__()
        assert type(input_size).__name__ == "int"
        l1 = 1
        l2 = 2
        dropout = 1.0
        output_size = 3
        self.net = nn.Sequential(
            nn.Linear(input_size, l1),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=dropout),
            nn.BatchNorm1d(l1),
            nn.Linear(l1, l2),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=dropout),
            nn.BatchNorm1d(l2),
            nn.Linear(l2, output_size),
        )

    def forward(self, x):
        return self.net(x)
