from abc import ABC, abstractmethod
from sklearn.base import BaseEstimator


from typing import Any

import pandas as pd

class BasePlugin(ABC):
    @abstractmethod
    def fit(*args, **kwargs): ...
    
    @abstractmethod
    def predict(*args, **kwargs): ...

class BaseFilterPlugin(BasePlugin, BaseEstimator): ...

class InputTextFilterPlugin(BaseFilterPlugin):
    @abstractmethod
    def predict(self, *args, **kwargs) -> pd.DataFrame: ...

class TextModificationFilterPlugin(BaseFilterPlugin):
    @abstractmethod
    def predict(self, x:pd.DataFrame, *args, **kwargs) -> pd.DataFrame: ...

class TextRepresentationFilterPlugin(BaseFilterPlugin):
    @abstractmethod
    def fit(self, x:pd.DataFrame, *args, **kwargs): ...
    
    @abstractmethod
    def predict(self, x:pd.DataFrame, *args, **kwargs) -> Any: ...
    

class VectorModFilterPlugin(BaseFilterPlugin):
    @abstractmethod
    def fit(self, x:Any, *args, **kwargs): ...
    
    @abstractmethod
    def predict(self, x:Any, *args, **kwargs) -> Any: ...
    