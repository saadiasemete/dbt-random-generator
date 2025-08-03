from dataclasses import dataclass
from .settings import SQLType
from typing import Any
from sqlglot import exp

@dataclass
class Constant:
    """
    thing is, id(1) == id(1)
    but id(Constant(SQLType.INT, 1)) != id(Constant(SQLType.INT, 1))
    """

    type: SQLType
    value: Any

    def __hash__(self):
        return id(self)
    
    def to_sqlglot_literal(self):
        if self.type in (SQLType.FLOAT, SQLType.INT):
            return exp.Literal.number(self.value)
        elif self.type in (SQLType.STRING,):
            return exp.Literal.string(self.value)
        else:
            raise TypeError(f"Unsupported constant type: {self.type}")
