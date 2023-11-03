import pytest
from typing import Any, Tuple
from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.container.container import Container
from research_framework.container.model.global_config import GlobalConfig
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.flyweight.model.item_dao import ItemDao
from research_framework.flyweight.flyweight import FlyWeight
from research_framework.storage.local_storage import LocalStorage
from test.plugins.test_plugin import TestPassThroughFilterWrapper

@pytest.fixture
def save_new_item():
    Container.fly = FlyWeight()
    Container.storage = LocalStorage()
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    data_hashcode, _, data = manager.predict("Test_HASHCODE", "Test_NAME", {})

    return  data_hashcode, data


@pytest.fixture
def save_new_item_delete_at_the_end(save_new_item:Tuple[BaseFlyManager, str], request):
    data_hashcode, _ = save_new_item
    request.addfinalizer(lambda: Container.fly.unset_item(data_hashcode))
    return save_new_item

def test_save_new_item(save_new_item_delete_at_the_end):
    data_hashcode, data = save_new_item_delete_at_the_end

    if callable(data):
        print("is callable()")
        data = data()
    
    assert data == TestPassThroughFilterWrapper().predict(None)
    assert True == Container.storage.check_if_exists(data_hashcode)
    assert data == Container.storage.download_file(data_hashcode)
    stored = ItemModel(**ItemDao.findOneByHashCode(data_hashcode))
    assert stored.hash_code == data_hashcode
    

def test_save_existing_item(save_new_item_delete_at_the_end: Tuple[BaseFlyManager, str]):
    data_hashcode, _ = save_new_item_delete_at_the_end
    
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    new_data_hashcode, _, new_data = manager.predict("Test_HASHCODE", "Test_NAME", {})
    
    assert callable(new_data)
    assert new_data_hashcode == data_hashcode    
    assert 1 == len(list(ItemDao.findByHashCode(data_hashcode)))
    
def test_save_existing_item_with_overwrite_global(save_new_item_delete_at_the_end: Tuple[BaseFlyManager, str]):
    data_hashcode, _ = save_new_item_delete_at_the_end
    
    Container.global_config = GlobalConfig(
        overwrite=True
    )   
    
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {})
    new_data_hashcode, _, new_data = manager.predict("Test_HASHCODE", "Test_NAME", {})
    
    print(Container.global_config.model_dump())
    assert not callable(new_data)
    assert new_data_hashcode == data_hashcode    
    assert 1 == len(list(ItemDao.findByHashCode(data_hashcode)))
    
    

def test_save_existing_item_with_overwrite_global_false_and_filter_overwrite(save_new_item_delete_at_the_end: Tuple[BaseFlyManager, str]):
    data_hashcode, _ = save_new_item_delete_at_the_end
    
    Container.global_config = GlobalConfig(
        overwrite=False
    )   
    
    manager = Container.get_filter_manager(TestPassThroughFilterWrapper.__name__, {}, overwrite=True)
    new_data_hashcode, _, new_data = manager.predict("Test_HASHCODE", "Test_NAME", {})
    
    print(Container.global_config.model_dump())
    assert not callable(new_data)
    assert new_data_hashcode == data_hashcode    
    assert 1 == len(list(ItemDao.findByHashCode(data_hashcode)))
    
def test_delete_existing_item(save_new_item: Tuple[BaseFlyManager, str]):
    data_hashcode, _ =  save_new_item
    
    Container.fly.unset_item(data_hashcode)
    
    assert ItemDao.findOneByHashCode(data_hashcode) == None
    assert Container.storage.check_if_exists(data_hashcode) == False
    
