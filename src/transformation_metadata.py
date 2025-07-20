
from .column_transformations import Transformation
from .table import Column, Table
from dataclasses import dataclass
@dataclass
class TransformationMetadata:
    transformation: Transformation
    columns: list[Column]
    resulting_column: Column
    new_table: Table