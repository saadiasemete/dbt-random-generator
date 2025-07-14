from .column import Column 
from .table import Table
from .utils import randstr
import random 

def generate_seed_schema(cls, pk_n: int=1, fields_n_min: int=2, fields_n_max: int=5):
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