from atpbar import atpbar

from research_framework.base.plugin.base_plugin import TextRepresentationFilterPlugin
from research_framework.container.container import Container
from research_framework.dataset.basic_dataset import BasicCollator, BasicDataset
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager, PassThroughFlyManager
from research_framework.plugins.wrappers import DataFrameInStandardDatasetOutWrapper

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from transformers import AutoTokenizer
from transformers import AutoModel
from torch.utils.data import DataLoader

from typing import Dict, Any

import torch
import pandas as pd
import numpy as np



@Container.bind(FitPredictFlyManager, DataFrameInStandardDatasetOutWrapper)
class Tf(TextRepresentationFilterPlugin):
    def __init__(self, lowercase=True):
        self.lowercase = lowercase
        self.model = CountVectorizer(lowercase=self.lowercase)


    def set_params(self, **params):
        aux = super().set_params(**params)
        self.model = CountVectorizer(lowercase=self.lowercase)
        return aux

    def fit(self, x:pd.DataFrame, y=None):
        self.model.fit(x.text)
        return self
        
    def transform(self, x:pd.DataFrame):
        return self.predict(x)

    def predict(self, x:pd.DataFrame) -> Any:
        return self.model.transform(x.text)

    


@Container.bind(FitPredictFlyManager, DataFrameInStandardDatasetOutWrapper)
class TfIdf(TextRepresentationFilterPlugin):
    def __init__(self, lowercase=True):
        self.lowercase = lowercase
        self.model = TfidfVectorizer(lowercase=self.lowercase)

    def set_params(self, **params):
        aux = super().set_params(**params)
        self.model = TfidfVectorizer(lowercase=self.lowercase)
        return aux
    
    def fit(self, x:pd.DataFrame, y=None):
        self.model.fit(x.text)
        return self
        
    def transform(self, x:pd.DataFrame):
        return self.predict(x)

    def predict(self, x:pd.DataFrame) -> Any:
        return self.model.transform(x.text)
    
    
@Container.bind(PassThroughFlyManager, DataFrameInStandardDatasetOutWrapper)
class RoBERTa(TextRepresentationFilterPlugin):
    def __init__(self, batch_size=10):
        self.batch_size = batch_size
        self.model = AutoModel.from_pretrained('sentence-transformers/stsb-roberta-large')
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/stsb-roberta-large', use_fast=True)
        self.collator = BasicCollator(self.tokenizer)
        
    def mean_pooling(self, model_output, attention_mask):
        import torch
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def set_params(self, **params):
        aux = super().set_params(**params)
        return aux

    def fit(self, x:pd.DataFrame, y=None):
        return self
        
    def transform(self, x:pd.DataFrame):
        return self.predict(x)

    def predict(self, x:pd.DataFrame) -> Any:
        dataset = BasicDataset(x.text.to_numpy(), self.tokenizer)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, collate_fn=self.collator, num_workers=4)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.model.to(device)
        with torch.no_grad():
            result = []
            for batch in atpbar(dataloader):
                batch = {k: v.to(device) for k, v in batch.items()}                                                                                                                                                                                                                                 
                m_out = self.model(**batch)
                sentence_embeddings = self.mean_pooling(m_out, batch['attention_mask'])
                result.append(sentence_embeddings.cpu())
       
            return np.concatenate(result, axis=0)
