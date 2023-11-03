from abc import ABC, abstractmethod
from typing import Any, Dict
from research_framework.base.plugin.base_wrapper import BaseWrapper

class BaseFlyweight(ABC):
    
    @staticmethod
    @abstractmethod
    def hashcode_from_name(name): ...
        
    @staticmethod
    @abstractmethod
    def hashcode_from_config(clazz, params):...
    
    @staticmethod
    @abstractmethod
    def append_to_hashcode(hashcode, hashcode2, is_model=False): ...
    @abstractmethod
    def wrap_plugin_from_cloud(self, cloud_params:Dict[str, Any]) -> BaseWrapper:...
    @abstractmethod
    def get_data_from_item(self, item):...
    @abstractmethod
    def get_item(self, hash_code):...
    @abstractmethod
    def set_item(self, name:str, hashcode:str, data:Any):...
    @abstractmethod                
    def unset_item(self, hashcode:str):...