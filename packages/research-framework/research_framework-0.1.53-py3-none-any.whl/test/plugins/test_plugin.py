from research_framework.container.container import Container
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.flyweight.flyweight_manager import PassThroughFlyManager, FitPredictFlyManager, DummyFlyManager
from research_framework.plugins.wrappers import DataFrameInOutWrapper, StandardDatasetInOutWrapper, DataFrameInStandardDatasetOutWrapper

import pandas as pd


@Container.bind(PassThroughFlyManager)
class TestPassThroughFilterWrapper(BasePlugin):

    def fit(self, *args, **kwargs): ...

    def predict(self, _):
        return "Data generated"



@Container.bind(FitPredictFlyManager)
class TestFitPredictFilterWrapper(BasePlugin):

    def fit(self, *args, **kwargs):
        return "Model Trained"

    def predict(self, _):
        return "Data generated"


@Container.bind(DummyFlyManager, DataFrameInOutWrapper)
class DummyDataFrameInOutWrapper(BasePlugin):
    def fit(self, x, y):
        return self
    
    def predict(self, x):
        return x
    
@Container.bind(DummyFlyManager, DataFrameInOutWrapper)
class DummyDataFrameInOutWrapperOutWrongType(BasePlugin):
    def fit(self, x, y):
        return self
    
    def predict(self, x):
        return StandardDataset(pd.DataFrame({'label': [1]}), None)
    
@Container.bind(DummyFlyManager, StandardDatasetInOutWrapper)
class DummyStandardDatasetInOutWrapper(BasePlugin):
    def fit(self, x, y):
        return x
    
    def predict(self, x):
        return x
    
@Container.bind(DummyFlyManager, StandardDatasetInOutWrapper)
class DummyStandardDatasetInOutWrapperOutWrongType(BasePlugin):
    def fit(self, x, y):
        return x
    
    def predict(self, x):
        return pd.DataFrame({'label': [1]})