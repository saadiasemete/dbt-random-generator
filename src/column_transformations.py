import sqlglot.expressions as exp
from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence
from .settings import SQLType
from enum import Enum

F = TypeVar('F', bound=exp.Func)

class ConstPolicy(str, Enum):
    "do we accept a constant instead of column here?"
    ALLOWED = "allowed"
    REQUIRED = "required"
    FORBIDDEN = "forbidden"

@dataclass
class ArgTypeConfig:
    "If types is None, inherits types from the main_type property in the Transformation"
    types: list[SQLType] | None
    constant: ConstPolicy


class Transformation(Generic[F]):
    fn: type[F]
    main_type: SQLType
    main_type_bounds = Sequence[SQLType]
    # (min, max) or (min, 0) if maximum number of arguments is undefined
    arity: tuple[int, int]
    arguments: Sequence[ArgTypeConfig]
    # if "None", returns main_type
    returns: SQLType | None = None

    @property
    def name(self) -> str:
        return self.fn.sql_name()

    @property
    def arg_types(self) -> dict[str, bool]:
        return self.fn.arg_types

    @property
    def is_var_len_args(self) -> bool:
        return self.fn.is_var_len_args

class tr_Least(Transformation[exp.Least]):

    arity = (2, 2)
    main_type_bounds = [SQLType.INT, SQLType.FLOAT]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
    ]

class tr_Greatest(Transformation[exp.Greatest]):

    arity = (2, 2)
    main_type_bounds = [SQLType.INT, SQLType.FLOAT]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
    ]

class tr_Concat(Transformation[exp.Concat]):

    arity = (2, 0)
    main_type_bounds = [SQLType.STRING]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
        ArgTypeConfig(types=[list[None]], constant=ConstPolicy.ALLOWED),
    ]

class tr_Length(Transformation[exp.Length]):
    arity = (1,1)
    main_type_bounds = [SQLType.STRING]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
    ]


