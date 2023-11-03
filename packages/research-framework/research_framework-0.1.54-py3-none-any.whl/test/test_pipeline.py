from typing import Any
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.container.model.global_config import GlobalConfig
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.flyweight.flyweight import FlyWeight
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.pipeline.model.pipeline_model import PipelineModel, FilterModel, InputFilterModel, MetricModel
from research_framework.pipeline.pipeline import FitPredictPipeline
from research_framework.storage.local_storage import LocalStorage

import pytest
import pandas as pd
from rich import print



# Container.global_config = GlobalConfig(
#     overwrite=True
# )

test_pipeline = PipelineModel(
    name='pipeline para tests',
    train_input= 
        InputFilterModel(
            clazz='CSVPlugin',
            name='texts_depression_2018.csv',
            params={
                "filepath_or_buffer":"test/data/texts_depression_2018.csv",
                "sep": ",",
                "index_col": 0,
            },
        )
    ,
    test_input =
        InputFilterModel(
            clazz='CSVPlugin',
            name='texts_depression_2022.csv',
            params={
                "filepath_or_buffer":"test/data/texts_depression_2022.csv",
                "sep": ",",
                "index_col": 0,
            }
        )
    ,
    filters= [
        FilterModel(
            clazz="FilterRowsByNwords",
            params={
                "upper_cut": 100,
                "lower_cut": 10,
                "df_headers": ["id", "text", "label"]
            }
        ),
        FilterModel(
            clazz="Tf",
            params={
                "lowercase":True
            }
        ),
        FilterModel(
            clazz="MaTruncatedSVD",
            params={
                "n_components":1024
            } 
        ),
        FilterModel(
            clazz="DoomyPredictor",
            params={
                "n_epoch": 3,
                "batch_size": 500,
                "emb_d": 1024
            }
        )
    ],
    metrics = [
        MetricModel(
            clazz="F1"
        )
    ]
)

@pytest.fixture
def simple_pipeline():
    # pp = pprint.PrettyPrinter(indent=4)
    print("\n* Container content: ")
    print(Container.BINDINGS)
    Container.storage = LocalStorage()
    Container.fly = FlyWeight()
    pipeline = FitPredictPipeline(test_pipeline)
    pipeline.start()
    return pipeline


def aux_delete_pipeline_generated_items(pipeline):
    print("- Train data:")
    for item in test_pipeline.train_input.items:
        try:
            print(f'{item.name} : {item.hash_code} deleted? {Container.fly.unset_item(item.hash_code)}')
        except Exception as ex:
            print(ex)
    print("- Test data:")
    for item in test_pipeline.test_input.items:
        try:
            print(f'{item.name} : {item.hash_code} deleted? {Container.fly.unset_item(item.hash_code)}')
        except Exception as ex:
            print(ex)
            
    print("- Trained models:")
    filters = []
    for plugin_filter in pipeline.pipeline.filters:
        if not plugin_filter.item is None:
            try:
                print(f'{plugin_filter.item.name} : {plugin_filter.item.hash_code} deleted? {Container.fly.unset_item(plugin_filter.item.hash_code)}')
            except Exception as ex:
                print(ex)
        plugin_filter.item = None
        filters.append(plugin_filter)
        
    pipeline.pipeline.filters = filters
    test_pipeline.test_input.items = []
    test_pipeline.train_input.items = []
    
@pytest.fixture
def delete_pipeline_items(simple_pipeline: FitPredictPipeline, request: type[pytest.FixtureRequest]):
    request.addfinalizer(lambda: aux_delete_pipeline_generated_items(simple_pipeline))
    return simple_pipeline

def test_stored_items_types_and_wrappers(delete_pipeline_items: Any):
    pipeline = delete_pipeline_items
    for item in test_pipeline.train_input.items:
        assert type(item) == ItemModel
        obj2 = Container.fly.get_data_from_item(item)
        assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset

    for item in test_pipeline.test_input.items:
        assert type(item) == ItemModel
        obj2 = Container.fly.get_data_from_item(item)
        assert type(obj2) == pd.DataFrame or type(obj2) == StandardDataset

    for plugin_filter in pipeline.pipeline.filters:
        if not plugin_filter.item is None:
            item = plugin_filter.item
            assert type(item) == ItemModel
            obj = Container.fly.wrap_plugin_from_cloud(item.params)
            assert issubclass(type(obj), BaseWrapper)
            obj2 = Container.fly.get_data_from_item(item)
            assert issubclass(type(obj2), BasePlugin)
            
def test_metrics(delete_pipeline_items: Any):
    pipeline = delete_pipeline_items
    for metric in pipeline.pipeline.metrics:
        print(f'- {metric.clazz} : {metric.value}')

    assert True