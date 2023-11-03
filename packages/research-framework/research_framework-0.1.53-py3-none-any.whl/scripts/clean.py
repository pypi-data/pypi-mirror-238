from research_framework.container.container import Container
from research_framework.flyweight.model.item_dao import ItemDao
from research_framework.flyweight.model.item_model import ItemModel
from research_framework.flyweight.flyweight import FlyWeight
from rich import print

for item in ItemDao.findAll():
    i = ItemModel(**item)
    print(i)
    print(Container.storage.check_if_exists(i.hash_code))
    
    
Container.fly = FlyWeight()

Container.fly.unset_item("600c845eb1ae710f10956c9bdace4529")

