import logging
from torch.utils.data import Dataset
import torch
class BasicDataset(Dataset):
    def __init__(self, texts, tokenizer):
        self.tokenizer = tokenizer
        self.texts = texts
        self.labels = []
        self.n_examples = len(self.texts)
         
    
    def __len__(self):
        return self.n_examples
    
    def __getitem__(self, item):
        try:
            return self.texts[item]
        except Exception as ex:
                print("----------------------")
                logging.info(self.texts[item])
                raise Exception
        
    
    
class BasicCollator(object):
    def __init__(self, use_tokenizer):
        self.use_tokenizer = use_tokenizer
 
    def __call__(self, sequences):
        inputs = self.use_tokenizer(text=sequences, return_tensors="pt", padding=True, truncation=True)
        return inputs