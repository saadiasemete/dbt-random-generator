from networkx import Graph
from .column import Column
from .table import Table

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
    
    
