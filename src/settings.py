from enum import Enum

class SQLType(str, Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"

SUPPORTED_TYPES = [SQLType.INT, SQLType.FLOAT, SQLType.STRING]
PK_TYPES = [SQLType.STRING, SQLType.INT]