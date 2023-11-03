
from torch.utils.data import Dataset
import pandas as pd
import scipy
from typing import Any
import numpy as np

class StandardDataset(Dataset):
    def __init__(self, df:pd.DataFrame, vectors:Any):
        self.df = df
        self.vectors = vectors
        if scipy.sparse.issparse(self.vectors):
            self.vectors = self.vectors.tocsr()

    def __len__(self):
        return len(self.df.index)
    
    def __getitem__(self, index) -> Any:
        if scipy.sparse.issparse(self.vectors):
            if hasattr(index, "__len__"):
                return self.df.iloc[index], self.vectors[index, :]
            else:
                return self.df.iloc[index], self.vectors.getrow(index)
        else:
            if type(self.vectors) is list:
                self.vectors = np.array(self.vectors)
            return self.df.iloc[index], self.vectors[index]
            