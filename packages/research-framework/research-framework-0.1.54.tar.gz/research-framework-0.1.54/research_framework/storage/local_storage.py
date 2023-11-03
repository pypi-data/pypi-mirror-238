from research_framework.base.storage.base_storage import BaseStorage
import io
import os
import json 
import pickle
import os

class LocalStorage(BaseStorage):
    def __init__(self, storage_path:str='data'):
        self.storage_path=storage_path
        
    def upload_file(self, file, file_name, direct_stream=False):
        try:
            print(f"* Saving in local path: {self.storage_path}/{file_name}")
            pickle.dump(file, open(f'{self.storage_path}/{file_name}', 'wb'))
            print("* Saved !")
            return file_name
        except Exception as ex:
            print(ex)
        return None
    
    def list_stored_files(self):
        return os.listdir(self.storage_path)
    
    def get_file_by_id(self, file_id):
        for file_n in os.listdir(self.storage_path):
            if file_n == file_id:
                return open(f'{self.storage_path}/{file_id}', 'rb')
                
                
    def check_if_exists(self, file_id):
        for file_n in os.listdir(self.storage_path):
            if file_n == file_id:
                return True
        return False
            
    def download_file(self, drive_ref=None):
        return pickle.load(self.get_file_by_id(drive_ref))
    
    def delete_file(self, file_id):
        if os.path.exists(f'{self.storage_path}/{file_id}'):
            os.remove(f'{self.storage_path}/{file_id}')
        else:
            raise FileExistsError("No existe en la carpeta")
    