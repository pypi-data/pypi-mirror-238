from research_framework.container.container import Container
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.flyweight import FlyWeight
from research_framework.pipeline.model.pipeline_model import MetricModel, GridSearchFilterModel, PipelineModel, FilterModel, InputFilterModel
from research_framework.pipeline.pipeline import FitPredictPipeline
from research_framework.storage.local_storage import LocalStorage

from rich import print

test_pipeline = PipelineModel(
    name='pipeline para tests',
    global_config=GlobalConfig(),
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
                "upper_cut": -1,
                "lower_cut": 10,
            }
        ),
        FilterModel(
            clazz="CrossValGridSearch",
            params={
                "n_splits": 1,
                "test_size": 0.3,
                "random_state": 43,
                "refit": True,
                "scorers": [
                    MetricModel(
                        clazz='F1'
                    )
                ],
                "filters": [
                    GridSearchFilterModel(
                        clazz="Tf",
                        params={
                            "lowercase": [True]
                        }
                    ),
                    GridSearchFilterModel(
                        clazz="MaTruncatedSVD",
                        params={
                            "n_components":[1024]
                        }    
                    ),
                    GridSearchFilterModel(
                        clazz="DoomyPredictor",
                        params={
                            "n_epoch": [10],
                            "batch_size": [500],
                            "emb_d": [1024],
                        }
                    )
                ],
            }
        ),
    ],
    metrics = [
        
    ]
)

def test_simple_pipeline():
    print(Container.BINDINGS)
    
    Container.global_config = GlobalConfig(
        store = False
    )
    Container.storage = LocalStorage()
    Container.fly = FlyWeight()
    pipeline = FitPredictPipeline(test_pipeline)
    pipeline.start()