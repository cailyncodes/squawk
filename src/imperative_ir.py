"""
Squawk Imperative IR - State-based intermediate representation
This is the result of transforming functional IR into imperative form
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto


class ImpType(Enum):
    INT = auto()
    BOOL = auto()


class ImpOp(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LEQ = auto()
    GEQ = auto()


@dataclass
class ImpInstruction:
    """Base class for imperative instructions"""
    pass


@dataclass
class ImpAssign(ImpInstruction):
    """Assign value to a variable (register)"""
    dest: str
    value: 'ImpValue'


@dataclass
class ImpBinaryOp(ImpInstruction):
    """Binary operation with result stored in dest"""
    dest: str
    op: ImpOp
    left: 'ImpValue'
    right: 'ImpValue'


@dataclass
class ImpLabel(ImpInstruction):
    """Label for jump targets"""
    name: str


@dataclass
class ImpJump(ImpInstruction):
    """Unconditional jump"""
    target: str


@dataclass
class ImpCondJump(ImpInstruction):
    """Conditional jump"""
    condition: 'ImpValue'
    true_target: str
    false_target: str


@dataclass
class ImpCall(ImpInstruction):
    """Function call with result"""
    dest: Optional[str]
    function: str
    args: List['ImpValue']


@dataclass
class ImpReturn(ImpInstruction):
    """Return from function"""
    value: 'ImpValue'


@dataclass
class ImpValue:
    """Base class for values in imperative IR"""
    pass


@dataclass
class ImpIntLiteral(ImpValue):
    value: int


@dataclass
class ImpBoolLiteral(ImpValue):
    value: bool


@dataclass
class ImpVar(ImpValue):
    name: str


@dataclass
class ImpFunction:
    name: str
    params: List[str]
    instructions: List[ImpInstruction]


@dataclass
class ImpProgram:
    functions: List[ImpFunction]
