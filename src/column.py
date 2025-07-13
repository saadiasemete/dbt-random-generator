from .settings import PK_TYPES, SUPPORTED_TYPES
from .utils import randstr
import random

class Column:
    def __init__(self, name: str, type: str, table_name: str, is_pk: bool=False, **kwargs):
        self.name = name 
        self.type = type 
        self.table_name = table_name
        self.full_name = '.'.join([table_name, name])
        self.is_pk = is_pk 
    
    def __repr__(self):
        return self.full_name
    
    def __hash__(self):
        return hash(self.full_name)
    
    @classmethod 
    def generate_field(cls, table_name: str, is_pk: bool=False):
        types = PK_TYPES if is_pk else SUPPORTED_TYPES
        return cls(
            name=randstr(),
            type=random.choice(types),
            table_name=table_name,
            is_pk=is_pk,
        )