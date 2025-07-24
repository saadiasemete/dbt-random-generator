from .settings import PK_TYPES, SUPPORTED_TYPES
from .utils import randstr
import random
from typing import TYPE_CHECKING
from sqlglot import exp

if TYPE_CHECKING:
    from .table import Table

class Column:
    def __init__(self, name: str, type: str, table: 'Table', is_pk: bool=False, **kwargs):
        self.name = name 
        self.type = type 
        self.table = table
        self.table_name = table.name
        self.full_name = '.'.join([self.table_name, name])
        self.is_pk = is_pk 
    
    def __repr__(self):
        return self.full_name
    
    def __hash__(self):
        return hash(self.full_name)
    
    def to_sqlglot_column(self, alias:str|None=None):
        if alias is None: 
            alias = self.table.name
        return exp.Column(
            this=exp.Identifier(this=self.name),
            table=exp.Identifier(this=alias)
        )
    
    @classmethod 
    def generate_field(cls, table: 'Table', is_pk: bool=False):
        types = PK_TYPES if is_pk else SUPPORTED_TYPES
        return cls(
            name=randstr(),
            type=random.choice(types),
            table=table,
            is_pk=is_pk,
        )