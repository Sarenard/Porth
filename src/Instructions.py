from enum import auto, IntEnum

class I(IntEnum):
    PUSHINT = auto()
    ADD = auto()
    PRINT = auto()
    DUP = auto()
    DROP = auto()
    SWAP = auto()
    OVER = auto()
    MUL = auto()
    IF = auto()
    SUB = auto()
    EQUAL = auto()
    INPUT = auto()
    DUP2 = auto()
    MACRO = auto()
    MACROWORD = auto()
    INCLUDE = auto()
    BIGGER = auto()
    NAND = auto()
    ROTATE = auto()
    TRUE = auto()
    FALSE = auto()
    WHILE = auto()
    DIV = auto()
    PUSHSTRING = auto()

class Type(IntEnum):
    INT = auto()
    BOOL = auto()
    STRING = auto()