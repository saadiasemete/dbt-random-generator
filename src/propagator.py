from .table import Table, Column
from .column_transformations import Transformation
from .settings import SQLType
from .randomness import randstr, random_piece_of_data
from .constant import Constant
from .relmap import Relmap
from copy import deepcopy
import random

from .transformation_metadata import TransformationMetadata


def classify_columns(related_columns: list[Column]) -> dict[SQLType, list[Column]]:
    related_columns_classified: dict[SQLType, list[Column]] = dict()
    for column in related_columns:
        if not column.is_pk:
            related_columns_classified.setdefault(
                column.type, []).append(column)
    return related_columns_classified


def select_transformation(related_columns_classified: dict[SQLType, list[Column]],
                          type_: SQLType,
                          lower_col_number: int = 1,
                          upper_col_number: int | None = None) -> tuple[Transformation|None, int]:
    # meaning it isn't the first attempt, and it found no candidates

    if upper_col_number in (None, -1, 0):
        upper_col_number = len(related_columns_classified[type_])
    if lower_col_number > upper_col_number:
        print(lower_col_number, upper_col_number)
        return (None, 0)
    elif lower_col_number == upper_col_number:
        affected_columns_number = lower_col_number
    else:
        affected_columns_number = random.randint(
            lower_col_number, upper_col_number)

    potential_transformations = []
    min_arity = 999
    max_arity = -1

    for t in Transformation.__subclasses__():
        if type_ in t.main_type_bounds:
            if (not t.allows_const and t.arity[0] > affected_columns_number):
                min_arity = min(min_arity, t.arity[0])
            elif (t.arity[1] != 0 and t.arity[1] < affected_columns_number):
                max_arity = max(max_arity, t.arity[1])
            else:
                assert not (not t.allows_const and t.arity[0] > affected_columns_number)
                assert not (t.arity[1] != 0 and t.arity[1] < affected_columns_number)
                potential_transformations.append(t)

    if len(potential_transformations) == 0:
        return select_transformation(related_columns_classified, type_, min_arity, max_arity)
    else:
        return random.choice(potential_transformations), affected_columns_number


def select_type_and_transformations(related_columns_classified: dict[SQLType, list[Column]],
                                    new_table: Table,
                                    exclude_types: list[SQLType] | None = None
                                    ):
    if exclude_types is None:
        exclude_types = []
    print(exclude_types)
    available_types = set([type_ for type_ in related_columns_classified]).difference(set(exclude_types))
    if not available_types:
        raise Exception("Unable to select type and transformation")
    main_type = random.choice([type_ for type_ in related_columns_classified])

    transformation, affected_columns_number = select_transformation(
        related_columns_classified,
        main_type
    )
    # select_transformation returns (None, 0) if it was unable to find a transformation
    if not transformation:
        exclude_types.append(main_type)
        return select_type_and_transformations(related_columns_classified, new_table, exclude_types)
    # we're gonna possibly add constants to it, but it's not a fact that we'd need them otherwise
    population = deepcopy(related_columns_classified[main_type])
    # if the number of arguments is less than the nuber of columns, use constants
    affected_columns_number = max(transformation.arity[0], affected_columns_number)
    # TODO: add logic to make constants even when there's no necessity
    print(
        {
            'transformation': transformation,
            'arity': transformation.arity,
            'population': population,
            'affected': affected_columns_number
        }
    )
    while len(population) < affected_columns_number or False:
        population.append(
            Constant(main_type, random_piece_of_data(main_type)))

    assert len(population) >= affected_columns_number
    assert len(population) >= transformation.arity[0]
    
    return TransformationMetadata(
        transformation=transformation,
        args=random.sample(population, k=affected_columns_number),
        resulting_column=Column(
            name=randstr(),
            type=transformation.return_type,
            table=new_table
        ),
        new_table=new_table
    )
    

def create_transformations(graph: Relmap, related_columns: list[Column], new_table: Table) -> list[TransformationMetadata]:
    transformation_number_coeff = 1
    transformation_number = random.randint(
        1, round(transformation_number_coeff*len(related_columns)))
    transformations: list[TransformationMetadata] = []

    related_columns_classified = classify_columns(related_columns)
    for _ in range(transformation_number):
        transformations.append(select_type_and_transformations(
            related_columns_classified,
            new_table,
        ))
        print('selected successfully')
    return transformations

    #


def propagate(graph: Relmap, staging:bool=True):
    if staging:
        kind = 'seed'
    else:
        kind = 'model'
    models = graph.get_all_tables(kind)
    # TODO: allow multiple 
    model = models[0]
    related_columns: list[Column] = [
        col for col, col_meta in graph[model].items() if col_meta.get('label') == 'makes_up']
    new_table = Table(
        randstr(),
        'model',
    )

    transformations = create_transformations(graph, related_columns, new_table)
    
    for transformation_metadata in transformations:
        graph.apply_transformation(transformation_metadata)
