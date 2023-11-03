from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.base.flyweight.base_flyweight import BaseFlyweight

from typing import Dict, Any, Optional
from rich import print
import json

class FitPredictFlyManager(BaseFlyManager):
    def __init__(self, clazz:str, params:Dict[str, Any], wrapper: BaseWrapper, fly: BaseFlyweight, store:bool, overwrite:bool):
        self.clazz:str = clazz
        self.params:Dict[str, Any] = params
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.hashcode:Optional[str] = None
        self.filter_name:Optional[str] = None
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, data_hashcode:str, data:Any):
        filter_hashcode = self.fly.hashcode_from_config(self.clazz, self.params)
        trained_filter_name = f'{self.clazz}{json.dumps(self.params)}[Trained]({data_hashcode})'
        trained_filter_hashcode = self.fly.append_to_hashcode(data_hashcode, filter_hashcode, is_model=True)
        filter_trained_item = self.fly.get_item(trained_filter_hashcode)
        
        print("---------------------[Filter Training]----------------------------")
        print(f"Trained_filter_name -> {trained_filter_name}")
        print(f'Data_hash_code -> {data_hashcode}')
        print(f'Trained_filter_hashcode -> {trained_filter_hashcode}')
        print(filter_trained_item)
        print("-------------------------------------------------")
        if filter_trained_item is None or self.overwrite:
            #Esto significa que no tenemos el modelo entrenado guardado.
            if callable(data):
                data = data()

            self.wrapper.fit(data)
            
            if self.store:
                if filter_trained_item is None:
                    if not self.fly.set_item(
                        trained_filter_name,
                        trained_filter_hashcode,
                        self.wrapper.plugin
                    ):
                        raise Exception("Couldn't save item")
                else:
                    if not self.fly.set_item(
                        trained_filter_name,
                        trained_filter_hashcode,
                        self.wrapper.plugin,
                        self.overwrite
                    ):
                        raise Exception("Couldn't save item")
            
            self.hashcode = trained_filter_hashcode
            self.filter_name = trained_filter_name
            
        else:
            self.wrapper = lambda : self.fly.wrap_plugin_from_cloud(filter_trained_item.params)
            self.hashcode = trained_filter_hashcode
            self.filter_name = trained_filter_name
                
    def predict(self, data_hashcode:str, data_name:str, data:Any):
        if self.hashcode is None:
            raise Exception("Model not trained, call fit() before calling predict()!")
        else:
            data_name = f'{data_name} -> {self.filter_name}'
            
            data_hashcode = self.fly.append_to_hashcode(data_hashcode, self.hashcode, is_model=False)
            data_item = self.fly.get_item(data_hashcode)
            print("-------------------------------------------------")
            print(f"Data_name -> {data_name}")
            print(f'Hash_code -> {data_hashcode}')
            print(data_item)
            print("-------------------------------------------------")
            if data_item is None or self.overwrite:
                # Esto significa que aun no hemos generado los nuevos datos
                if callable(data):
                    data = data()
                    
                if callable(self.wrapper) and self.wrapper.__name__ == "<lambda>":
                    self.wrapper = self.wrapper()
                
                data = self.wrapper.predict(data)
                
                if self.store:
                    if data_item is None:
                        if not self.fly.set_item(
                            data_name,
                            data_hashcode,
                            data
                        ):
                            raise Exception("Couldn't save item")
                    else:
                        if not self.fly.set_item(
                            data_name,
                            data_hashcode,
                            data,
                            self.overwrite                    
                        ):
                            raise Exception("Couldn't save item")
                
            else:
                data = lambda : self.fly.get_data_from_item(data_item)
            
            return data_hashcode, data_name, data
                
class PassThroughFlyManager(BaseFlyManager):
    def __init__(self, clazz:str, params:Dict[str, Any], wrapper: BaseWrapper, fly: BaseFlyweight, store:bool, overwrite:bool, *args, **kwargs):
        self.clazz:str = clazz
        self.params:Dict[str, Any] = params
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.hashcode:Optional[str] = None
        self.filter_name:Optional[str] = f'{self.clazz}{json.dumps(self.params)}[-]'
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, *args, **kwargs): ...
        
    def predict(self, data_hashcode:str, data_name:str, data):
        data_name = f'{data_name} -> {self.filter_name}'
        filter_hashcode = self.fly.hashcode_from_config(self.clazz, self.params)
        data_hashcode = self.fly.append_to_hashcode(data_hashcode, filter_hashcode, is_model=False)
        print("-------------------------------------------------")
        print(f"Data_name -> {data_name}")
        print(f'Hash_code -> {data_hashcode}')
        data_item = self.fly.get_item(data_hashcode)
        print(data_item)
        print("-------------------------------------------------")
        if data_item is None or self.overwrite:
            # Esto significa que aun no hemos generado los nuevos datos
            if callable(data):
                data = data()
            
            data = self.wrapper.predict(data)
            
            if self.store:
                if data_item is None:
                    if not self.fly.set_item(
                        data_name,
                        data_hashcode,
                        data                    
                    ):
                        raise Exception("Couldn't save item")
                else:
                    if not self.fly.set_item(
                        data_name,
                        data_hashcode,
                        data,
                        self.overwrite                    
                    ):
                        raise Exception("Couldn't save item")
                    
        else:
            data = lambda : self.fly.get_data_from_item(data_item)
        
        return data_hashcode, data_name, data
    
class InputFlyManager(BaseFlyManager):
    def __init__(self, clazz:str, params:Dict[str, Any], wrapper: BaseWrapper, fly: BaseFlyweight, store:bool, overwrite:bool, *args, **kwargs):
        self.clazz:str = clazz
        self.params:Dict[str, Any] = params
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.store:bool = store
        self.overwrite:bool = overwrite
        
    def fit(self, *args, **kwargs): ...
    
    
    def predict(self, data_name:str, *args, **kwargs):
        data_hashcode = self.fly.hashcode_from_name(data_name)
        
        data_item = self.fly.get_item(data_hashcode)
        
        if data_item is None or self.overwrite:
            data = self.wrapper.predict(None)
            
            if self.store:
                
                if data_item is None:
                    if not self.fly.set_item(
                        data_name,
                        data_hashcode,
                        data                    
                    ):
                        raise Exception("Couldn't save item")
                else:
                    if not self.fly.set_item(
                        data_name,
                        data_hashcode,
                        data,
                        self.overwrite                    
                    ):
                        raise Exception("Couldn't save item")
            
        else:
            data = lambda: self.wrapper.predict(None)
        
        return data_hashcode, data_name, data
        
class DummyFlyManager(BaseFlyManager):
    def __init__(self, clazz:str, params:Dict[str, Any], wrapper: BaseWrapper, fly: BaseFlyweight, *args, **kwargs):
        self.clazz:str = clazz
        self.params:Dict[str, Any] = params
        self.wrapper: BaseWrapper = wrapper
        self.fly: BaseFlyweight = fly
        self.hashcode = None
        self.filter_name = None

    def fit(self, data_hashcode:str, data):
        self.wrapper.fit(data)
        self.filter_name = f'{self.wrapper.plugin.get_params()}[Trained]({data_hashcode})'
        self.hashcode = self.fly.hashcode_from_name(self.filter_name)
        
        print("-------------------------------------------------")
        print(f"data_hashcode -> {data_hashcode}")
        print(f'filter_name -> {self.filter_name}')
        print(f'hash_code -> {self.hashcode}')
        print("-------------------------------------------------")
    
    def predict(self, data_hashcode: str, data_name: str, data):
        data = self.wrapper.predict(data)
        data_name = f'{data_name} -> {self.filter_name}'
        data_hashcode = self.fly.append_to_hashcode(data_hashcode, self.hashcode, is_model=False)
        
        print("-------------------------------------------------")
        print(f"data_hashcode -> {data_hashcode}")
        print(f'data_name -> {data_name}')
        print(f'filter_name -> {self.filter_name}')
        print("-------------------------------------------------")
        
        return data_hashcode, data_name, data
      
class OutputFlyManager(BaseFlyManager):
    def __init__(self, clazz:str, wrapper:BaseWrapper):
        self.clazz:str = clazz
        self.wrapper: BaseWrapper = wrapper
        
    def fit(self, *args, **kwargs): ...
    
    def predict(self, data):
        if callable(data):
            data = data()
            
        return self.wrapper.predict(data)

 