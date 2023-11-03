from research_framework.base.container.model.bind_model import BindModel
from research_framework.container.container import Container
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager
from research_framework.pipeline.pipeline import FitPredictPipeline, FitPredictGridSearchPipeline
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.flyweight import FlyWeight
from pydantic import BaseModel
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import PipelineModel
from research_framework.base.storage.base_storage import BaseStorage
from research_framework.storage.local_storage import LocalStorage

import json

PIPELINE = {
    "FitPredictPipeline": FitPredictPipeline,
    "FitPredictGridSearchPipeline": FitPredictGridSearchPipeline
}

class PipelineManager:
    
    @staticmethod
    def start_pipeline(project:str, pl_conf:BaseModel, log:bool=False, store:bool=True, overwrite:bool=False, storage:BaseStorage=LocalStorage()):
        Container.fly = FlyWeight()
        Container.storage = storage
        Container.global_config = GlobalConfig(
            log=log,
            overwrite=overwrite,
            store=store
        )
        
        pipeline = PIPELINE[pl_conf._clazz](pl_conf,project)
        pipeline.start()
        pipeline.log_metrics()
    
    @staticmethod
    def fill_pipline_items(config:PipelineModel):
        Container.fly = FlyWeight()
        config.train_input.item = ItemModel(
            name=config.train_input.name,
            hash_code= Container.fly.hashcode_from_name(config.train_input.name),
            clazz="SaaSPlugin",
            params={
                "drive_ref": Container.fly.hashcode_from_name(config.train_input.name),
            }
        )
        
        config.test_input.item = ItemModel(
            name=config.test_input.name,
            hash_code= Container.fly.hashcode_from_name(config.test_input.name),
            clazz="SaaSPlugin",
            params={
                "drive_ref": Container.fly.hashcode_from_name(config.test_input.name),
            }
        )
        
        train_data_hash_code = Container.fly.hashcode_from_name(config.train_input.name)
        train_data_name = config.train_input.name
        test_data_hash_code = Container.fly.hashcode_from_name(config.test_input.name)
        test_data_name = config.test_input.name
        
        for f in config.filters:
            bind: BindModel = Container.BINDINGS[f.clazz]   
            f_resume = Container.fly.hashcode_from_config(f.clazz, f.params)
            print(bind.manager == FitPredictFlyManager)
            if bind.manager == FitPredictFlyManager:
                filter_name = f'{f.clazz}{json.dumps(f.params)}[Trained]({train_data_hash_code})'
                filter_hash_code = Container.fly.append_to_hashcode(train_data_hash_code, f_resume, is_model=True)
                
                f.item = ItemModel(
                    name=filter_name,
                    hash_code= filter_hash_code,
                    clazz="SaaSPlugin",
                    params={
                        "drive_ref": filter_hash_code,
                    }
                )
            else:
                filter_name = f'{f.clazz}{json.dumps(f.params)}[-]'
                filter_hash_code = f_resume
                
                
            train_data_name = f'{train_data_name} -> {filter_name}'
            train_data_hash_code = Container.fly.append_to_hashcode(train_data_hash_code, filter_hash_code, is_model=False)
            
            config.train_input.items.append(
                ItemModel(
                    name=train_data_name,
                    hash_code=train_data_hash_code,
                    clazz='SaaSPlugin',
                    params={
                        "drive_ref": train_data_hash_code,
                    }
                )    
            )
            
            test_data_name = f'{test_data_name} -> {filter_name}'
            test_data_hash_code = Container.fly.append_to_hashcode(test_data_hash_code, filter_hash_code, is_model=False)
            
            config.test_input.items.append(
                ItemModel(
                    name=test_data_name,
                    hash_code=test_data_hash_code,
                    clazz='SaaSPlugin',
                    params={
                        "drive_ref": test_data_hash_code,
                    }
                )
            )
        
        return config