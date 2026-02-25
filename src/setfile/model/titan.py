import torch.nn as nn
import torch

class TiTAN_MAG(nn.Module):
    def __init__(self, embed_dim=768, num_heads=8, num_layers=4, num_classes=11):
        super().__init__()

        # Memory-as-Gate
        self.memory_gate = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.GELU(),
            nn.Linear(embed_dim, embed_dim),
            nn.Sigmoid()
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        self.classifier = nn.Sequential(
            nn.Linear(embed_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        # x = [B, D] from DataLoader, needs to be [B, T, D] for transformer
        x = x.unsqueeze(1) # Add sequence length dimension (T=1)

        # token-wise surprise
        mean_token = x.mean(dim=1, keepdim=True)     # [B, 1, D]
        surprise = torch.abs(x - mean_token)        # [B, 1, D]

        # memory gate
        gate = self.memory_gate(surprise)           # [B, 1, D]

        # apply MAG
        x = x * gate

        # transformer
        x = self.transformer(x)                     # [B, 1, D]

        # pool tokens
        x = x.mean(dim=1)                           # [B, D]

        return self.classifier(x)
