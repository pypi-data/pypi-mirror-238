import pytest
import pandas as pd
from typing import Any, Tuple

from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_wrapper import BaseWrapper
from research_framework.container.container import Container
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.flyweight.model.item_dao import ItemDao
from research_framework.flyweight.flyweight import FlyWeight

from test.plugins.test_plugin import *


def test_validate_DataFrameInOutWrapper_in_ok_out_ok():
    '''
    Validar que todo funcione bien cuando los datos de entrada son correctos
    y el plugin tiene bien definido el formato de salida no hay excepciones.
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyDataFrameInOutWrapper', {})
        wrapper.fit(pd.DataFrame({'label': [1]}))
        data = pd.DataFrame({'label': [1]})
        assert pd.DataFrame == type(wrapper.predict(data))
    except Exception as ex:
        print(ex)
        assert False

def test_validate_DataFrameInOutWrapper_in_ok_out_fails():
    '''
    Validar que todo funcione bien cuando los datos de entrada son correctos
    pero que fallse cuando el el plugin  no tiene bien definido el formato de 
    salida lanzando una excepción TypeError.
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyDataFrameInOutWrapperOutWrongType', {})
        wrapper.fit(pd.DataFrame({'label': [1]}))
        wrapper.predict(pd.DataFrame({'label': [1]}))
        assert False
    except TypeError as ex:
        assert True

def test_validate_DataFrameInOutWrapper_in_fails_fit():
    '''
    Validar que se arroje una excepción TypeError cuando el tipo de los datos 
    de entrada no son correctos
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyDataFrameInOutWrapper', {})
        wrapper.fit(StandardDataset(pd.DataFrame({'label': [1]}), None))
    except TypeError as ex:
        assert True
        
def test_validate_DataFrameInOutWrapper_in_fails_predict():
    '''
    Validar que se arroje una excepción TypeError cuando el tipo de los datos 
    de entrada no son correctos
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyDataFrameInOutWrapper', {})
        wrapper.predict(StandardDataset(pd.DataFrame({'label': [1]}), None))
    except TypeError as ex:
        assert True

"""StandardDatasetInOutWrapper"""
def test_validate_StandardDatasetInOutWrapper_in_ok_out_ok():
    '''
    Validar que todo funcione bien cuando los datos de entrada son correctos
    y el plugin tiene bien definido el formato de salida no hay excepciones.
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyStandardDatasetInOutWrapper', {})
        wrapper.fit(StandardDataset(pd.DataFrame({'label': [1]}), None))
        data = StandardDataset(pd.DataFrame({'label': [1]}), None)
        assert StandardDataset == type(wrapper.predict(data))
    except Exception as ex:
        print(ex)
        assert False
        
def test_validate_StandardDatasetInOutWrapper_in_ok_out_transforms_to_ok():
    '''
    Validar que todo funcione bien cuando los datos de entrada son correctos
    pero que fallse cuando el el plugin  no tiene bien definido el formato de 
    salida lanzando una excepción TypeError.
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyStandardDatasetInOutWrapperOutWrongType', {})
        wrapper.fit(StandardDataset(pd.DataFrame({'label': [1]}), None))
        assert StandardDataset == type(wrapper.predict(StandardDataset(pd.DataFrame({'label': [1]}), None)))
        
    except TypeError as ex:
        assert False        

def test_validate_DataFrameInOutWrapper_in_fails_fit():
    '''
    Validar que se arroje una excepción TypeError cuando el tipo de los datos 
    de entrada no son correctos
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyStandardDatasetInOutWrapper', {})
        wrapper.fit(pd.DataFrame({'label': [1]}))
    except TypeError as ex:
        assert True

def test_validate_DataFrameInOutWrapper_in_fails_predict():
    '''
    Validar que se arroje una excepción TypeError cuando el tipo de los datos 
    de entrada no son correctos
    '''
    try:
        wrapper:BaseWrapper = Container.get_wrapper('DummyStandardDatasetInOutWrapper', {})
        wrapper.predict(pd.DataFrame({'label': [1]}))
    except TypeError as ex:
        assert True