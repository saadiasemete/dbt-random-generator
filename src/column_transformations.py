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
    _returns: SQLType | None = None
    # if True, main_type could be of Const type
    allows_const: bool

    @property 
    def return_type(self) -> SQLType:
        if self._returns is None:
            return self.main_type
        else:
            return self._returns 

    @property
    def name(self) -> str:
        return self.fn.sql_name()

    @property
    def arg_types(self) -> dict[str, bool]:
        return self.fn.arg_types

    @property
    def is_var_len_args(self) -> bool:
        return self.fn.is_var_len_args
    
    def build_expr(self, args: list, alias: str) -> exp.Func:
        if issubclass(self.fn, exp.Func):
            if hasattr(self.fn, "arg_types") and "expressions" in self.fn.arg_types:
                return self.fn(expressions=args).as_(alias)
            elif "this" in self.arg_types:
                return self.fn(this=args[0]).as_(alias)
        raise ValueError(f"Don't know how to handle {self.fn}")
    
    

class tr_Least(Transformation[exp.Least]):

    fn = exp.Least
    arity = (2, 2)
    main_type_bounds = [SQLType.INT, SQLType.FLOAT]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
    ]
    allows_const = True

class tr_Greatest(Transformation[exp.Greatest]):

    fn = exp.Greatest
    arity = (2, 2)
    main_type_bounds = [SQLType.INT, SQLType.FLOAT]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
    ]
    allows_const = True

class tr_Concat(Transformation[exp.Concat]):

    fn = exp.Concat
    arity = (2, 0)
    main_type_bounds = [SQLType.STRING]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
        ArgTypeConfig(types=[list[None]], constant=ConstPolicy.ALLOWED),
    ]
    allows_const = True

class tr_Length(Transformation[exp.Length]):

    fn = exp.Length
    arity = (1,1)
    main_type_bounds = [SQLType.STRING]
    arguments = [
        ArgTypeConfig(types=None, constant=ConstPolicy.ALLOWED),
    ]
    allows_const = True


