from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .column import Column 
    from .table import Table
import random 
from .settings import SQLType, SUPPORTED_TYPES

def generate_random_letter():
    A = 65 
    Z = 90
    a = 97
    z = 122
    return chr(random.choice([random.randint(A, Z), random.randint(a, z)]))

def randstr(len: int=16) -> str:
    return ''.join(generate_random_letter() for _ in range(len))

def generate_field_name_type(types: list[SQLType]=SUPPORTED_TYPES):
    return {
        'name': randstr(),
        'type': random.choice(types),
    }

def random_piece_of_data(type_: SQLType):
    match type_:
        case SQLType.STRING:
            return randstr()
        case SQLType.INT:
            return random.randint(-127, 128)
        case SQLType.FLOAT:
            return random_piece_of_data(SQLType.INT)*random.random()
        case _:
            raise NotImplementedError(type_)

