from dataclasses import dataclass
import uuid


@dataclass
class Image:
    
    def __init__ (self, path:str, filename= uuid.uuid4(), format=None, resourceKey=None, driver='local'):
        self.filename = filename
        self.path = path
        self.format = format
        self.resourceKey = resourceKey
        self.driver = driver

