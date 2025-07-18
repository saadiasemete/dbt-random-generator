from dataclasses import dataclass
from .settings import SQLType
from typing import Any

@dataclass
class Constant:
    """
    thing is, id(1) == id(1)
    but id(Constant(SQLType.INT, 1)) != id(Constant(SQLType.INT, 1))
    """

    type_: SQLType
    value: Any
