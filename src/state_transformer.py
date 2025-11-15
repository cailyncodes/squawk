"""
Squawk State Transformer - Converts functional IR to imperative IR
This is the innovative core of Squawk: automatic transformation from pure
functional code to efficient state-modifying code.
"""

from typing import List
from functional_ir import *
from imperative_ir import *
import ast_nodes


class StateTransformer:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.instructions: List[ImpInstruction] = []
    
    def fresh_temp(self) -> str:
        """Generate a fresh temporary variable name"""
        name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return name
    
    def fresh_label(self, prefix: str = "L") -> str:
        """Generate a fresh label name"""
        name = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return name
    
    def convert_binop(self, op: ast_nodes.BinaryOp) -> ImpOp:
        """Convert AST binary operation to imperative operation"""
        mapping = {
            ast_nodes.BinaryOp.ADD: ImpOp.ADD,
            ast_nodes.BinaryOp.SUBTRACT: ImpOp.SUB,
            ast_nodes.BinaryOp.MULTIPLY: ImpOp.MUL,
            ast_nodes.BinaryOp.DIVIDE: ImpOp.DIV,
            ast_nodes.BinaryOp.EQUAL: ImpOp.EQ,
            ast_nodes.BinaryOp.NOT_EQUAL: ImpOp.NEQ,
            ast_nodes.BinaryOp.LESS_THAN: ImpOp.LT,
            ast_nodes.BinaryOp.GREATER_THAN: ImpOp.GT,
            ast_nodes.BinaryOp.LESS_EQUAL: ImpOp.LEQ,
            ast_nodes.BinaryOp.GREATER_EQUAL: ImpOp.GEQ,
        }
        return mapping[op]
    
    def transform_expr(self, expr: ast_nodes.ASTNode, dest: str) -> None:
        """Transform an expression and store result in dest"""
        
        if isinstance(expr, ast_nodes.IntLiteral):
            self.instructions.append(ImpAssign(dest, ImpIntLiteral(expr.value)))
        
        elif isinstance(expr, ast_nodes.BoolLiteral):
            self.instructions.append(ImpAssign(dest, ImpBoolLiteral(expr.value)))
        
        elif isinstance(expr, ast_nodes.Variable):
            self.instructions.append(ImpAssign(dest, ImpVar(expr.name)))
        
        elif isinstance(expr, ast_nodes.BinaryExpr):
            # Evaluate left operand
            left_temp = self.fresh_temp()
            self.transform_expr(expr.left, left_temp)
            
            # Evaluate right operand
            right_temp = self.fresh_temp()
            self.transform_expr(expr.right, right_temp)
            
            # Perform operation
            op = self.convert_binop(expr.op)
            self.instructions.append(
                ImpBinaryOp(dest, op, ImpVar(left_temp), ImpVar(right_temp))
            )
        
        elif isinstance(expr, ast_nodes.IfExpr):
            # Evaluate condition
            cond_temp = self.fresh_temp()
            self.transform_expr(expr.condition, cond_temp)
            
            # Create labels
            then_label = self.fresh_label("then")
            else_label = self.fresh_label("else")
            end_label = self.fresh_label("end_if")
            
            # Conditional jump
            self.instructions.append(
                ImpCondJump(ImpVar(cond_temp), then_label, else_label)
            )
            
            # Then branch
            self.instructions.append(ImpLabel(then_label))
            self.transform_expr(expr.then_expr, dest)
            self.instructions.append(ImpJump(end_label))
            
            # Else branch
            self.instructions.append(ImpLabel(else_label))
            self.transform_expr(expr.else_expr, dest)
            
            # End
            self.instructions.append(ImpLabel(end_label))
        
        elif isinstance(expr, ast_nodes.CallExpr):
            # Evaluate arguments
            arg_temps = []
            for arg in expr.args:
                arg_temp = self.fresh_temp()
                self.transform_expr(arg, arg_temp)
                arg_temps.append(ImpVar(arg_temp))
            
            # Make call
            self.instructions.append(ImpCall(dest, expr.function, arg_temps))
        
        elif isinstance(expr, ast_nodes.LetExpr):
            # Evaluate the value
            value_temp = self.fresh_temp()
            self.transform_expr(expr.value, value_temp)
            
            # Bind to name (simulate with assignment)
            self.instructions.append(ImpAssign(expr.name, ImpVar(value_temp)))
            
            # Evaluate body
            self.transform_expr(expr.body, dest)
        
        else:
            raise Exception(f"Unknown expression type: {type(expr)}")
    
    def transform_function(self, func: ast_nodes.FunctionDef) -> ImpFunction:
        """Transform a functional function definition to imperative form"""
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
        
        # Extract parameter names
        params = [p.name for p in func.parameters]
        
        # Transform body
        result_temp = self.fresh_temp()
        self.transform_expr(func.body, result_temp)
        
        # Add return
        self.instructions.append(ImpReturn(ImpVar(result_temp)))
        
        return ImpFunction(func.name, params, self.instructions)
    
    def transform_program(self, program: ast_nodes.Program) -> ImpProgram:
        """Transform an entire program"""
        functions = []
        for func in program.functions:
            functions.append(self.transform_function(func))
        
        return ImpProgram(functions)
