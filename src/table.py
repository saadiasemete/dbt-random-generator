from .column import Column
from .utils import randstr
import networkx as nx 
import random

class Table:


    def __init__(self, name: str, kind: str, columns: list[Column], **kwargs):
        self.name = name 
        self.kind = kind
        self.columns = columns
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(self.name)

    def represent_as_graph(self):

        result_subgraph = rs = nx.Graph()
        rs.add_node(self)
        for column in self.columns:
            rs.add_node(column)
            rs.add_edge(self, column, label='consists_of')
            rs.add_edge(column, self, label='makes_up')
        return rs


    @classmethod 
    def generate_seed(cls, pk_n: int=1, fields_n_min: int=2, fields_n_max: int=5):
        fields_n = random.randint(fields_n_min, fields_n_max)
        table_name = randstr()
        columns = list()
        for _ in range(pk_n):
            columns.append(Column.generate_field(table_name, is_pk=True))
        for _ in range(fields_n):
            columns.append(Column.generate_field(table_name, is_pk=False))
        return cls(
            name=table_name,
            kind='seed',
            columns=columns,
        )
        