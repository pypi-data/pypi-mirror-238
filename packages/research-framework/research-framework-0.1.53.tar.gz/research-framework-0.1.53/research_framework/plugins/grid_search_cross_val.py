from typing import List
from sklearn.model_selection import ShuffleSplit, StratifiedShuffleSplit, StratifiedKFold
from research_framework.base.plugin.base_plugin import BaseFilterPlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container

from rich import print
from research_framework.base.utils.grid_seach import generate_combis
from research_framework.dataset.standard_dataset import StandardDataset
from research_framework.pipeline.model.pipeline_model import MetricModel

import json
import numpy as np
import pandas as pd
from tqdm import tqdm

@Container.bind()
class CrossValGridSearch(BaseFilterPlugin):
    split_algorithms={
        "ShuffleSplit":ShuffleSplit,
        "StratifiedShuffleSplit":StratifiedShuffleSplit,
        "StratifiedKFold":StratifiedKFold
    }
    def __init__(self, split_alg='ShuffleSplit', n_splits=3, test_size=0.3, random_state=43, scorers=[MetricModel(clazz='F1')], refit=True, filters=[]):
        self.n_splits = n_splits
        self.test_size = test_size
        self.random_state = random_state
        self.filters = filters
        self.scorers = scorers
        self.refit = refit
        self.alg = CrossValGridSearch.split_algorithms[split_alg]
        self.best_pipeline:List[BaseWrapper] = []
        self.best_config:str = None

    def get_params(self, _: bool = True) -> dict:
        return json.loads(self.best_config)
    
    def fit(self, x):
        if callable(x) and x.__name__ == "<lambda>":
            x = x()

        print("\n--------------------[CrossValGridSearch]-----------------------\n")
        print(self.filters)
        print("\n---------------------------------------------------------------\n")
        cv = self.alg(
            n_splits=self.n_splits, 
            test_size=self.test_size, 
            random_state=self.random_state
        )

        pbar = tqdm(generate_combis(self.filters), position=0)
        pbar.set_description(f'Processing combinations...')

        combi_dict = {}
        results = {}
        for combi in pbar:
            combi_str = json.dumps(combi)
            combi_dict[combi_str] = combi
            
            for train, test in cv.split(x):
                if type(x) == pd.DataFrame:
                    x_train = x.iloc[train]
                    x_test = x.iloc[test]
                elif type(x) == StandardDataset:
                    x_train = StandardDataset(*x[train])
                    x_test = StandardDataset(*x[test])
                else:
                    x_train = x[train]
                    x_test = x[test]

                
                for clazz, params in combi.items():
                    wrapper:BaseWrapper = Container.get_wrapper(clazz, params)
                    wrapper.fit(x_train)
                    
                    x_train = wrapper.predict(x_train)
                    x_test = wrapper.predict(x_test)
                    
                for metric in self.scorers:
                    m_wrapper = Container.get_metric(metric.clazz)
                    result = results.get(combi_str, [])
                    result.append(m_wrapper.predict(x_test))
                    results[combi_str] = result
        
        print("- Results:")
        print(results)
        print("- Results Means: ")
        results_means = dict(map(lambda x: (x[0], np.mean(x[1])), results.items()))
        print(results_means)
        print("- Max values: ")
        config, value = max(results_means.items(), key=lambda x: x[1])
        print(f'Max Combination –> {config}')
        print(f'Max value       –> {value}')
        
        print("\n-------------------------------------------\n")
        print("- Refit of best model: ")
        self.best_config = config
        for clazz, params in combi_dict[config].items():
            wrapper:BaseWrapper = Container.get_wrapper(clazz, params)
            wrapper.fit(x)
            
            self.best_pipeline.append(wrapper)
            
            x = wrapper.predict(x)
            
                                    
    
    def predict(self, x): 
        if callable(x) and x.__name__ == "<lambda>":
            x = x()
        
        for wrapper in self.best_pipeline:
            x = wrapper.predict(x)
        
        return x