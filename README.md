# Squawk

A low-level programming language with an emphasis on functional user code and an innovative model for converting to state-modifying machine code.

## Overview

Squawk is designed to bridge the gap between pure functional programming and efficient low-level machine code. Users write in a functional style, and the compiler automatically transforms these expressions into optimized state-modifying instructions.

## Key Features

- **Functional User Code**: Write pure, composable functions without worrying about state management
- **Automatic State Transformation**: Innovative compiler transforms functional code into efficient imperative machine code
- **Low-Level Control**: Direct access to memory and registers when needed
- **Type Safety**: Static type system prevents common errors

## Language Design

### Functional Layer (User-Facing)
- Pure functions and expressions
- Immutable data structures
- Pattern matching
- Function composition

### Imperative Layer (Generated)
- Efficient register allocation
- Minimal memory allocations
- Optimized state mutations
- Direct hardware access

## Quick Start

```squawk
# Define a pure function
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)

# The compiler automatically converts this to efficient
# iterative code with register-based state management
```

## Building

```bash
python3 src/squawk.py <input-file.sq>
```

## Examples

See the `examples/` directory for sample programs demonstrating Squawk's features.

## Architecture

1. **Lexer**: Tokenizes source code
2. **Parser**: Builds Abstract Syntax Tree (AST)
3. **Functional IR**: Intermediate representation preserving functional semantics
4. **State Transformer**: Converts functional IR to imperative IR
5. **Code Generator**: Produces target machine code

## Status

This is a bare-bones implementation demonstrating the core concepts of the language.