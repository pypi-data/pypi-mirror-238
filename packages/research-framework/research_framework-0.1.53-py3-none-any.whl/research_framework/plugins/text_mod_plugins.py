from research_framework.container.container import Container
from research_framework.base.plugin.base_plugin import TextModificationFilterPlugin
from research_framework.flyweight.flyweight_manager import PassThroughFlyManager
from research_framework.plugins.wrappers import DataFrameInOutWrapper
from tqdm import tqdm

import pandas as pd


@Container.bind(PassThroughFlyManager, DataFrameInOutWrapper)
class FilterRowsByNwords(TextModificationFilterPlugin):
    def __init__(self, df_headers=["id", "text", "label"], upper_cut=100, lower_cut=10):
        self.evr = None
        self.upper_cut=upper_cut
        self.lower_cut=lower_cut
        self.df_headers=df_headers
        
    def fit(self, *args, **kwargs):
        return self
    
    def transform(self, x):
        return self.predict(x)
    
    def predict(self, x:pd.DataFrame):
        aux = {}
        x.reset_index()
        pbar = tqdm(x.itertuples())
        pbar.set_description(f"FilterRowsByNwords - {self.get_params(deep=False)}")
        for sentence in pbar:
            try:
                if len(str(sentence.text)) > self.lower_cut\
                and (len(str(sentence.text)) < self.upper_cut or self.upper_cut < 0):
                    for k,v in sentence._asdict().items():
                        inner = aux.get(k, [])
                        inner.append(v)
                        aux[k] = inner
            except Exception as ex:
                print(sentence.text)
                raise ex

        return pd.DataFrame(aux)
        