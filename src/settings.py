from enum import Enum
from sqlglot.dialects import postgres
import os 
from jinja2 import Environment, FileSystemLoader
templates_folder = os.path.abspath('templates')  
jinja_env = Environment(loader=FileSystemLoader('/home/mike/Documents/grimoires/dbt-random-generator/templates'))

class SQLType(str, Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"

SUPPORTED_TYPES = [SQLType.INT, SQLType.FLOAT, SQLType.STRING]
PK_TYPES = [SQLType.STRING, SQLType.INT]
# TODO: random size
SEED_SIZE = 50

DEFAULT_DIALECT = postgres
