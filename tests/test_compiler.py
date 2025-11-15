"""
Test suite for Squawk compiler
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import Lexer, TokenType
from parser import Parser
from state_transformer import StateTransformer
from codegen import CodeGenerator
import ast_nodes


def test_lexer_basic():
    """Test basic lexer functionality"""
    source = "fn add(x: Int, y: Int) -> Int = x + y"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.FN
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].value == "add"
    print("✓ Lexer basic test passed")


def test_lexer_literals():
    """Test lexer with literals"""
    source = "42 true false"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 42
    assert tokens[1].type == TokenType.TRUE
    assert tokens[2].type == TokenType.FALSE
    print("✓ Lexer literals test passed")


def test_parser_simple_function():
    """Test parsing simple function"""
    source = "fn identity(x: Int) -> Int = x"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse_program()
    
    assert len(program.functions) == 1
    func = program.functions[0]
    assert func.name == "identity"
    assert len(func.parameters) == 1
    assert func.parameters[0].name == "x"
    assert isinstance(func.body, ast_nodes.Variable)
    print("✓ Parser simple function test passed")


def test_parser_binary_expr():
    """Test parsing binary expressions"""
    source = "fn add(a: Int, b: Int) -> Int = a + b"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse_program()
    
    func = program.functions[0]
    assert isinstance(func.body, ast_nodes.BinaryExpr)
    assert func.body.op == ast_nodes.BinaryOp.ADD
    print("✓ Parser binary expression test passed")


def test_parser_if_expr():
    """Test parsing if expressions"""
    source = "fn max(a: Int, b: Int) -> Int = if a > b then a else b"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse_program()
    
    func = program.functions[0]
    assert isinstance(func.body, ast_nodes.IfExpr)
    assert isinstance(func.body.condition, ast_nodes.BinaryExpr)
    print("✓ Parser if expression test passed")


def test_state_transformer():
    """Test state transformer"""
    source = "fn simple(x: Int) -> Int = x + 1"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse_program()
    
    transformer = StateTransformer()
    imp_program = transformer.transform_program(program)
    
    assert len(imp_program.functions) == 1
    func = imp_program.functions[0]
    assert func.name == "simple"
    assert len(func.params) == 1
    assert len(func.instructions) > 0
    print("✓ State transformer test passed")


def test_codegen():
    """Test code generation"""
    source = "fn identity(x: Int) -> Int = x"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse_program()
    transformer = StateTransformer()
    imp_program = transformer.transform_program(program)
    
    codegen = CodeGenerator()
    output = codegen.generate_program(imp_program)
    
    assert "function identity" in output
    assert "ret" in output
    print("✓ Code generator test passed")


def test_full_pipeline():
    """Test complete compilation pipeline"""
    source = """
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)
"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse_program()
    transformer = StateTransformer()
    imp_program = transformer.transform_program(program)
    codegen = CodeGenerator()
    output = codegen.generate_program(imp_program)
    
    assert "function factorial" in output
    assert "call" in output  # recursive call
    assert "ret" in output
    print("✓ Full pipeline test passed")


def run_tests():
    """Run all tests"""
    print("Running Squawk compiler tests...\n")
    
    test_lexer_basic()
    test_lexer_literals()
    test_parser_simple_function()
    test_parser_binary_expr()
    test_parser_if_expr()
    test_state_transformer()
    test_codegen()
    test_full_pipeline()
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    run_tests()
