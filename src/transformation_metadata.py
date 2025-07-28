
from .column_transformations import Transformation
from .table import Table
from .column import Column 
from .constant import Constant
from dataclasses import dataclass
@dataclass
class TransformationMetadata:
    transformation: Transformation
    args: list[Column|Constant]
    resulting_column: Column
    new_table: Table