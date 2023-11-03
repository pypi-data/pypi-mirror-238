from pydantic import BaseModel, ConfigDict
from typing import Optional, Type

from research_framework.base.flyweight.base_flyweight_manager import BaseFlyManager
from research_framework.base.plugin.base_plugin import BasePlugin
from research_framework.base.plugin.base_wrapper import BaseWrapper

from research_framework.flyweight.flyweight_manager import DummyFlyManager
from research_framework.plugins.wrappers import DummyWrapper

class BindModel(BaseModel):
    manager: Optional[Type[BaseFlyManager]] = DummyFlyManager
    wrapper: Optional[Type[BaseWrapper]] = DummyWrapper
    plugin: Type[BasePlugin]
    
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        populate_by_name = True
    )