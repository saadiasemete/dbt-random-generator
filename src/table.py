from .column import Column
from .randomness import randstr
import networkx as nx 
import random

class Table:


    def __init__(self, name: str, kind: str, **kwargs):
        self.name = name 
        self.kind = kind
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)
    
    def dbt_ref(self):

        ref_components = ["{{ ref('", self.name, "') }}",]
        return ''.join(ref_components)
    
    @classmethod
    def generate_seed(cls, pk_n: int=1, fields_n_min: int=2, fields_n_max: int=5):
        fields_n = random.randint(fields_n_min, fields_n_max)
        table_name = randstr()
        columns = list()
        seed_table = cls(name=table_name,kind='seed',)
        for _ in range(pk_n):
            columns.append(Column.generate_field(seed_table, is_pk=True))
        for _ in range(fields_n):
            columns.append(Column.generate_field(seed_table, is_pk=False))
        return {
            'table': seed_table,
            'columns': columns
        }


        