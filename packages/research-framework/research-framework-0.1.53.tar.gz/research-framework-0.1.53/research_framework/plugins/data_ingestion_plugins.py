from research_framework.container.container import Container
from research_framework.base.plugin.base_plugin import BaseFilterPlugin, InputTextFilterPlugin
import pandas as pd

from research_framework.flyweight.flyweight_manager import InputFlyManager

@Container.bind(InputFlyManager)
class SaaSPlugin(BaseFilterPlugin):
    def __init__(self, drive_ref=""):
        self.drive_ref = drive_ref

    def fit(self, *args, **kwargs):
        return self

    def predict(self, _):
        obj = Container.storage.download_file(self.drive_ref)
        return obj

    
@Container.bind(InputFlyManager)
class CSVPlugin(InputTextFilterPlugin):
    def __init__(self, translate_cols=None, validate_cols=["label", "text"],filepath_or_buffer="", sep=',', index_col=False):
        self.filepath_or_buffer = filepath_or_buffer
        self.sep = sep
        self.index_col = index_col
        self.validate_cols = validate_cols
        self.translate_cols = translate_cols
        
    def fit(self, *args, **kwargs):
        return self

    def predict(self, _) -> pd.DataFrame:
        obj:pd.DataFrame = pd.read_csv(filepath_or_buffer=self.filepath_or_buffer, sep=self.sep, index_col=self.index_col)
        if set(self.validate_cols).issubset(obj.columns.to_list()):
            return obj
        else:
            raise Exception(f'Not all values in {self.validate_cols} found in df cols {obj.columns.to_list}')

        

