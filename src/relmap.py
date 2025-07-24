from networkx import Graph
from .column import Column
from .constant import Constant
from .table import Table
from .randomness import generate_seed
from .column_transformations import Transformation
from random import randint
from .transformation_metadata import TransformationMetadata
from .utils import randstr

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
    
    def get_all_tables(self, kind:str|None=None) -> list[Table]:
        return [i for i in self.nodes if isinstance(i, Table) and (kind is None or i.kind == kind)]

    def get_model_columns(self, model:Table) -> list[Column]:
        columns: list[Column] = []
        for node in self.nodes: 
            if isinstance(node, Column) and self.has_edge(model, node) and self.edges[(model,node)]['label'] == 'makes_up':
                columns.append(node)
        return columns
    
    def get_creating_transformation(self, column: Column) -> Transformation:
        print([i for i, j in self[column].items() if j['label'] == 'makes'])
        return [i for i, j in self[column].items() if j['label'] == 'makes'][0]

    
    def get_transformation_arguments(self, transformation: Transformation) -> list[Column|Constant]:
        return [i for i, j in self[transformation].items() if j['label'] == 'argument']


    def apply_transformation(self, transformation_metadata: TransformationMetadata):

        transformation_instance = transformation_metadata.transformation()
        resulting_column = transformation_metadata.resulting_column

        self.add_node(transformation_instance)
        for column in transformation_metadata.columns:
            # old col <-> transformation
            self.add_edge(column, transformation_instance, label='goes_to')
            self.add_edge(transformation_instance, column, label='argument')
        
        self.add_node(resulting_column)
        # new_col <-> transformation
        self.add_edge(resulting_column, transformation_instance, label='made_of')
        self.add_edge(transformation_instance, resulting_column, label='makes')
        # new_col <-> new_table
        self.connect_table_and_column(transformation_metadata.new_table, resulting_column)
    
    def generate_random_seeds(self, 
                 number_of_seeds:int=1,
                 pk_n_min:int=1,
                 pk_n_max:int=1,
                 fields_n_min:int=2,
                 fields_n_max:int=5):
        for _ in range(number_of_seeds):
            seed_and_columns = generate_seed(
                pk_n=randint(pk_n_min, pk_n_max),
                fields_n_min=fields_n_min,
                fields_n_max=fields_n_max
            )
            self.connect_table_and_many_columns(
                **seed_and_columns
            )

    
    
