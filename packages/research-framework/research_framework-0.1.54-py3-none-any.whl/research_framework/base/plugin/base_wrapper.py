from abc import ABC, abstractmethod

from research_framework.base.plugin.base_plugin import BasePlugin

class BaseWrapper(ABC):
    def __init__(self, plugin:BasePlugin):
        self.plugin:BasePlugin = plugin
        
    @abstractmethod
    def fit(*args, **kwargs): ...
    
    @abstractmethod
    def predict(*args, **kwargs): ...
