"""
Squawk Code Generator - Generates assembly-like code from imperative IR
"""

from imperative_ir import *
from typing import TextIO


class CodeGenerator:
    def __init__(self):
        self.output = []
    
    def emit(self, line: str):
        """Emit a line of code"""
        self.output.append(line)
    
    def generate_value(self, value: ImpValue) -> str:
        """Generate code for a value"""
        if isinstance(value, ImpIntLiteral):
            return str(value.value)
        elif isinstance(value, ImpBoolLiteral):
            return "1" if value.value else "0"
        elif isinstance(value, ImpVar):
            return value.name
        else:
            raise Exception(f"Unknown value type: {type(value)}")
    
    def generate_op(self, op: ImpOp) -> str:
        """Generate operation mnemonic"""
        mapping = {
            ImpOp.ADD: "add",
            ImpOp.SUB: "sub",
            ImpOp.MUL: "mul",
            ImpOp.DIV: "div",
            ImpOp.EQ: "eq",
            ImpOp.NEQ: "neq",
            ImpOp.LT: "lt",
            ImpOp.GT: "gt",
            ImpOp.LEQ: "leq",
            ImpOp.GEQ: "geq",
        }
        return mapping[op]
    
    def generate_instruction(self, instr: ImpInstruction):
        """Generate code for an instruction"""
        if isinstance(instr, ImpAssign):
            value_str = self.generate_value(instr.value)
            self.emit(f"    mov {instr.dest}, {value_str}")
        
        elif isinstance(instr, ImpBinaryOp):
            op_str = self.generate_op(instr.op)
            left_str = self.generate_value(instr.left)
            right_str = self.generate_value(instr.right)
            self.emit(f"    {op_str} {instr.dest}, {left_str}, {right_str}")
        
        elif isinstance(instr, ImpLabel):
            self.emit(f"{instr.name}:")
        
        elif isinstance(instr, ImpJump):
            self.emit(f"    jmp {instr.target}")
        
        elif isinstance(instr, ImpCondJump):
            cond_str = self.generate_value(instr.condition)
            self.emit(f"    jmpif {cond_str}, {instr.true_target}")
            self.emit(f"    jmp {instr.false_target}")
        
        elif isinstance(instr, ImpCall):
            args_str = ", ".join(self.generate_value(arg) for arg in instr.args)
            if instr.dest:
                self.emit(f"    call {instr.dest} = {instr.function}({args_str})")
            else:
                self.emit(f"    call {instr.function}({args_str})")
        
        elif isinstance(instr, ImpReturn):
            value_str = self.generate_value(instr.value)
            self.emit(f"    ret {value_str}")
        
        else:
            raise Exception(f"Unknown instruction type: {type(instr)}")
    
    def generate_function(self, func: ImpFunction):
        """Generate code for a function"""
        params_str = ", ".join(func.params)
        self.emit(f"\nfunction {func.name}({params_str}):")
        
        for instr in func.instructions:
            self.generate_instruction(instr)
    
    def generate_program(self, program: ImpProgram) -> str:
        """Generate code for entire program"""
        self.output = []
        self.emit("; Squawk Compiler Output")
        self.emit("; Generated from functional code")
        
        for func in program.functions:
            self.generate_function(func)
        
        return "\n".join(self.output)
