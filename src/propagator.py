from .table import Table, Column
from .column_transformations import Transformation
from .settings import SQLType
from .utils import randstr
from .relmap import Relmap
import random 

from .transformation_metadata import TransformationMetadata



def select_transformation(related_columns_classified: dict[SQLType, list[Column]], 
                          type_: SQLType, 
                          lower_col_number:int=1, 
                          upper_col_number:int|None=None) -> tuple[Transformation, int]:
    
    if upper_col_number is None: 
        upper_col_number = len(related_columns_classified[type_])
    affected_columns_nummber = random.randint(lower_col_number, upper_col_number)

    potential_transformations = []
    min_arity = 999
    max_arity = -1

    for t in Transformation.__subclasses__():
        if type_ in t.main_type_bounds:
            if t.arity[0] > affected_columns_nummber or t.arity[1] != 0 and t.arity[1] < affected_columns_nummber:
                min_arity = min(min_arity, t.arity[0])
                max_arity = max(max_arity, t.arity[1])
            else:
                potential_transformations.append(t)
    
    if len(potential_transformations) == 0:
        return select_transformation(related_columns_classified, type_, min_arity, max_arity)
    else:
        return random.choice(potential_transformations), affected_columns_nummber

def classify_columns(related_columns: list[Column]) -> dict[SQLType, list[Column]]:
    related_columns_classified: dict[SQLType, list[Column]] = dict()
    for column in related_columns:
        if not column.is_pk:
            related_columns_classified.setdefault(column.type, []).append(column)
    return related_columns_classified


def create_transformations(graph: Relmap, related_columns: list[Column], new_table: Table) -> list[TransformationMetadata]:
    transformation_number_coeff = 2
    transformation_number = random.randint(1, round(transformation_number_coeff*len(related_columns)))
    transformations: list[TransformationMetadata] = []

    related_columns_classified = classify_columns(related_columns)

    for _ in range(transformation_number):
        
        transformation, affected_columns_nummber = select_transformation(
            related_columns_classified,
            random.choice([type_ for type_ in related_columns_classified])
            )
        transformations.append(
            TransformationMetadata(
                transformation=transformation,
                columns=random.choices(related_columns, k=affected_columns_nummber),
                resulting_column=Column(
                    name=randstr(),
                    type=transformation.return_type,
                    table_name=new_table.name
                ),
                new_table=new_table
            )
        )
    return transformations
    
    # 
        


def propagate(graph: Relmap):
    # TODO: allow multiple seeds
    seed = graph.get_all_tables('seed')[0]
    related_columns: list[Column] = [col for col, col_meta in graph[seed].items() if col_meta.get('label') == 'makes_up']
    new_table = Table(
        randstr(),
        'model',
    )
    
    transformations = create_transformations(graph, related_columns, new_table)

    for transformation_metadata in transformations:
        graph.apply_transformation(transformation_metadata)





