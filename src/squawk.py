#!/usr/bin/env python3
"""
Squawk Compiler - Main driver for the Squawk programming language
"""

import sys
from lexer import Lexer
from parser import Parser
from state_transformer import StateTransformer
from codegen import CodeGenerator


def compile_squawk(source_code: str) -> str:
    """
    Compile Squawk source code to assembly-like output
    
    Pipeline:
    1. Lexer: Source code -> Tokens
    2. Parser: Tokens -> AST
    3. State Transformer: AST -> Imperative IR
    4. Code Generator: Imperative IR -> Assembly
    """
    
    # Lexical analysis
    print("=== LEXER ===", file=sys.stderr)
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    print(f"Generated {len(tokens)} tokens", file=sys.stderr)
    
    # Parsing
    print("\n=== PARSER ===", file=sys.stderr)
    parser = Parser(tokens)
    ast = parser.parse_program()
    print(f"Parsed {len(ast.functions)} function(s)", file=sys.stderr)
    
    # State transformation (Functional -> Imperative)
    print("\n=== STATE TRANSFORMER ===", file=sys.stderr)
    transformer = StateTransformer()
    imperative_ir = transformer.transform_program(ast)
    print(f"Transformed to imperative IR with {len(imperative_ir.functions)} function(s)", file=sys.stderr)
    
    # Code generation
    print("\n=== CODE GENERATOR ===", file=sys.stderr)
    codegen = CodeGenerator()
    output = codegen.generate_program(imperative_ir)
    print(f"Generated {len(output.splitlines())} lines of code", file=sys.stderr)
    
    return output


def main():
    if len(sys.argv) != 2:
        print("Usage: squawk.py <source-file>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  python3 src/squawk.py examples/factorial.sq", file=sys.stderr)
        sys.exit(1)
    
    source_file = sys.argv[1]
    
    try:
        with open(source_file, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        output = compile_squawk(source_code)
        print("\n=== OUTPUT ===\n", file=sys.stderr)
        print(output)
    except SyntaxError as e:
        print(f"\nCompilation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nCompilation failed with error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
