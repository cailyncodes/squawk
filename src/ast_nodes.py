"""
Squawk AST (Abstract Syntax Tree) - Defines the structure of parsed programs
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto


class BinaryOp(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()


class Type(Enum):
    INT = auto()
    BOOL = auto()


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass


@dataclass
class IntLiteral(ASTNode):
    value: int


@dataclass
class BoolLiteral(ASTNode):
    value: bool


@dataclass
class Variable(ASTNode):
    name: str


@dataclass
class BinaryExpr(ASTNode):
    op: BinaryOp
    left: ASTNode
    right: ASTNode


@dataclass
class IfExpr(ASTNode):
    condition: ASTNode
    then_expr: ASTNode
    else_expr: ASTNode


@dataclass
class CallExpr(ASTNode):
    function: str
    args: List[ASTNode]


@dataclass
class LetExpr(ASTNode):
    name: str
    value: ASTNode
    body: ASTNode


@dataclass
class Parameter:
    name: str
    type: Type


@dataclass
class FunctionDef(ASTNode):
    name: str
    parameters: List[Parameter]
    return_type: Type
    body: ASTNode


@dataclass
class Program(ASTNode):
    functions: List[FunctionDef]
