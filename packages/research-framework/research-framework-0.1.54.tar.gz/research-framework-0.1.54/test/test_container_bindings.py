import pytest
from typing import Any, Tuple
from research_framework.flyweight.flyweight import FlyWeight
from research_framework.plugins.wrappers import DummyWrapper

from test.plugins.test_plugin import TestPassThroughFilterWrapper, TestFitPredictFilterWrapper
from research_framework.flyweight.flyweight_manager import FitPredictFlyManager, PassThroughFlyManager
from research_framework.container.container import Container

def test_get_PassTroughFlyManager_filter_manager():
    manager1 = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    
    assert type(manager1) == PassThroughFlyManager
    assert type(manager1.wrapper) == DummyWrapper
    assert type(manager1.wrapper.plugin) == TestPassThroughFilterWrapper

def test_get_FitPredictFlyManager_filter_manager(): 
    manager2 = Container.get_filter_manager(TestFitPredictFilterWrapper.__name__, {})
    
    assert type(manager2) == FitPredictFlyManager
    assert type(manager2.wrapper) == DummyWrapper
    assert type(manager2.wrapper.plugin) == TestFitPredictFilterWrapper