from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, Type

from pydantic import BaseModel
from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.pipeline.model.pipeline_model import PipelineModel
# from research_framework.flyweight.flyweight_manager import DummyFlyManager
# from research_framework.plugins.wrappers import DummyWrapper

class BaseContainer(ABC):
    
    @staticmethod
    @abstractmethod
    def start_pipeline(project:str, name:str, pl_conf:BaseModel, log:bool=False, store:bool=True, overwrite:bool=False): ...
    
    @staticmethod
    @abstractmethod
    def init_wandb_logger(project:str, name:Dict[str, Any]): ...
    
    @staticmethod
    @abstractmethod
    def send_to_logger(message:Dict[str, Any], step:Optional[int] = None): ...
    
    @staticmethod
    @abstractmethod
    def register_dao(collection): ...
    
    @staticmethod
    @abstractmethod
    def bind(manager:Optional[BaseFlyManager], wrapper:Optional[BaseWrapper]): ...
    
    @staticmethod
    @abstractmethod
    def wrap_object(model_clazz:str, object:object) -> BaseWrapper: ...
    
    @staticmethod
    @abstractmethod
    def get_wrapper(clazz:str, params:Dict[str, Any]) -> BaseWrapper: ...
        
    @staticmethod
    @abstractmethod
    def get_filter_manager(clazz:str, params:Dict[str, Any]) -> BaseFlyManager: ...
    
    @staticmethod
    @abstractmethod
    def get_model(clazz:str, params:Dict[str, Any]) -> BasePlugin: ...
    
    @staticmethod
    @abstractmethod
    def get_clazz(clazz:str) -> Type[BasePlugin]: ...
    
    @staticmethod
    @abstractmethod
    def get_metric(clazz:str) -> BaseFlyManager: ...