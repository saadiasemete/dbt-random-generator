from networkx import Graph
from .column import Column
from .table import Table
from .randomness import generate_seed
from random import randint

class Relmap(Graph):

    def connect_table_and_column(self, table: Table, column: Column):
        if not self.has_node(table):
            self.add_node(table)
        if not self.has_node(column):
            self.add_node(column)
        self.add_edge(table, column, label='consists_of')
        self.add_edge(column, table, label='makes_up')
    
    def connect_table_and_many_columns(self, table: Table, columns: list[Column]):
        for column in columns: 
            self.connect_table_and_column(table, column)
    

    def __init__(self, 
                 number_of_seeds:int=1,
                 pk_n_min:int=1,
                 pk_n_max:int=1,
                 fields_n_min:int=2,
                 fields_n_max:int=5
                 ):
        super()
        for _ in number_of_seeds:
            seed_and_columns = generate_seed(
                pk_n=randint(pk_n_min, pk_n_max),
                fields_n_min=fields_n_min,
                fields_n_max=fields_n_max
            )
            self.connect_table_and_many_columns(
                **seed_and_columns
            )

    
    
