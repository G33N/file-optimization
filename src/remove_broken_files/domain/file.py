from dataclasses import dataclass
import uuid


@dataclass
class File:
    
    def __init__ (self, path:str, id= uuid.uuid4(), source:str = None, source_id:str = None):
        self.id = id
        self.path = path
        self.source = source
        self.source_id = source_id



