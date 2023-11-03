from typing import Any
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.base.utils.method_overload import methdispatch
import pandas as pd
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.pipeline.model.pipeline_model import MetricModel

class DummyWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
    
    def predict(self, *args, **kwargs):
        return self.plugin.predict(*args, **kwargs)

    
# Este es para los plugins que transforman texto
class DataFrameInOutWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @fit.register
    def _(self, x:pd.DataFrame) -> BasePlugin:
        return self.plugin.fit(x, None)
    
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @predict.register
    def _(self, x:pd.DataFrame) -> pd.DataFrame:
        out = self.plugin.predict(x)
        if type(out) != pd.DataFrame:
            raise TypeError("Wrong return type: Plugin should retreive type pd.DataFrame")
        
        return out
    
# Este es para los plugins que transforman texto en vectores
# y para los clasificadores que trabajan directamente con textos
class DataFrameInStandardDatasetOutWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @fit.register
    def _fit(self, x:pd.DataFrame) -> BasePlugin:
        return self.plugin.fit(x, x.label.to_list())
    
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @predict.register
    def _pred(self, x:pd.DataFrame) -> StandardDataset:
        return StandardDataset(x, self.plugin.predict(x))
    
# Este es para los plugins que Transforman vectores en vectores
# y para los clasificadores que trabajan con textos
class StandardDatasetInOutWrapper(BaseWrapper):
    @methdispatch
    def fit(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
    
    @fit.register
    def _fit(self, x:StandardDataset) -> BasePlugin:
        return self.plugin.fit(x.vectors, x.df.label.to_list())
        
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
        
    @predict.register
    def _pred(self, x:StandardDataset) -> StandardDataset:
        return StandardDataset(x.df, self.plugin.predict(x.vectors))
    
    
# Este es para las métricas que a veces les llegan pd.DataFrame
# y otras StandardDataset
class MetricWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
        
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
        
    @predict.register
    def _pred(self, x:StandardDataset) -> Any:
        return self.plugin.predict(x.df.label.to_list(), x.vectors)
    

class EarlyMetricWrapper(BaseWrapper):
    def fit(self, *args, **kwargs):
        return self.plugin.fit(*args, **kwargs)
        
    @methdispatch
    def predict(self, x):
        raise TypeError(f"Wrong input type {type(x)}")
        
    @predict.register
    def _pred(self, x:StandardDataset) -> Any:
        return self.plugin.predict(x.df.label.to_list(), x.df['count'].to_list(), x.vectors)