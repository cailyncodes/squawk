"""
Squawk Functional IR - Intermediate representation preserving functional semantics
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto


class IRType(Enum):
    INT = auto()
    BOOL = auto()


class IRBinaryOp(Enum):
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
class IRNode:
    """Base class for all IR nodes"""
    pass


@dataclass
class IRIntLiteral(IRNode):
    value: int


@dataclass
class IRBoolLiteral(IRNode):
    value: bool


@dataclass
class IRVar(IRNode):
    name: str


@dataclass
class IRBinaryOp(IRNode):
    op: IRBinaryOp
    left: IRNode
    right: IRNode


@dataclass
class IRIf(IRNode):
    condition: IRNode
    then_branch: IRNode
    else_branch: IRNode


@dataclass
class IRCall(IRNode):
    function: str
    args: List[IRNode]


@dataclass
class IRLet(IRNode):
    name: str
    value: IRNode
    body: IRNode


@dataclass
class IRFunction:
    name: str
    params: List[tuple[str, IRType]]
    return_type: IRType
    body: IRNode


@dataclass
class IRProgram:
    functions: List[IRFunction]
