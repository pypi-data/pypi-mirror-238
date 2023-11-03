from research_framework.container.container import Container
from research_framework.base.plugin.base_plugin import VectorModFilterPlugin
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager
from research_framework.plugins.wrappers import StandardDatasetInOutWrapper

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MaxAbsScaler

@Container.bind(FitPredictFlyManager, StandardDatasetInOutWrapper)
class MaTruncatedSVD(VectorModFilterPlugin):
    def __init__(self, n_components=3, n_iter=7, random_state=42):
        self.n_components=n_components
        self.n_iter=n_iter
        self.random_state=random_state
        
    def fit(self, x, *args, **kwargs):
        self.scaler = MaxAbsScaler().fit(x)
        self.pca = TruncatedSVD(self.n_components, n_iter=self.n_iter, random_state=self.random_state).fit(self.scaler.transform(x))
        return self
        
    def predict(self, x):
        x = self.pca.transform(self.scaler.transform(x))
        return x
    
    def transform(self, x):
        return self.predict(x)
    