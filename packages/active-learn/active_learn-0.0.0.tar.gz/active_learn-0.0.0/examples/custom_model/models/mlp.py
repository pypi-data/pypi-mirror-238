import numpy as np
from torch import nn


# mlp model class
class MLP(nn.Module):
    def __init__(self, dim, embSize=128, useNonLin=True):
        super().__init__()
        self.embSize = embSize
        self.dim = int(np.prod(dim))
        self.lm1 = nn.Linear(self.dim, embSize)
        self.lm2 = nn.Linear(embSize, embSize)
        self.linear = nn.Linear(embSize, 10, bias=False)
        self.useNonLin = useNonLin

    def get_embedding_dim(self):
        return self.embSize

    def get_outputs_and_embeddings(self, x):
        x = x.view(-1, self.dim)
        if self.useNonLin:
            emb = nn.functional.relu(self.lm1(x))
        else:
            emb = self.lm1(x)
        out = self.linear(emb)
        return out, emb

    def forward(self, x):
        out, _ = self.get_outputs_and_embeddings(x)
        return out
