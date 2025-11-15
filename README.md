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

```bash
# Compile a Squawk program
python3 src/squawk.py examples/factorial.sq
```

```squawk
# Define a pure function
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)

# The compiler automatically converts this to efficient
# iterative code with register-based state management
```

Output:
```assembly
function factorial(n):
    mov t2, n
    mov t3, 1
    leq t1, t2, t3
    jmpif t1, then0
    jmp else1
then0:
    mov t0, 1
    jmp end_if2
else1:
    mov t4, n
    mov t7, n
    mov t8, 1
    sub t6, t7, t8
    call t5 = factorial(t6)
    mul t0, t4, t5
end_if2:
    ret t0
```

## Documentation

- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Learn the language and write your first program
- **[Language Specification](docs/SPECIFICATION.md)** - Formal syntax and semantics
- **[Architecture](docs/ARCHITECTURE.md)** - How the compiler works
- **[Examples](examples/README.md)** - Example programs with explanations

## Running

Compile a Squawk program:

```bash
python3 src/squawk.py <input-file.sq>
```

Run the test suite:

```bash
python3 tests/test_compiler.py
```

Try the examples:

```bash
python3 src/squawk.py examples/factorial.sq
python3 src/squawk.py examples/fibonacci.sq
python3 src/squawk.py examples/max.sq
```

## The Innovation

**The Problem**: Traditional languages force you to choose:
- **Functional languages**: Easy to reason about but often slower
- **Imperative languages**: Fast but harder to write correctly

**Squawk's Solution**: Write functional, compile to imperative!

Users write pure, mathematical functions. The compiler automatically transforms them into efficient state-based machine code with:
- Explicit control flow (jumps, labels)
- Optimized register allocation
- Minimal memory operations
- Direct hardware mapping

This gives you the best of both worlds: functional clarity with imperative performance.

## Architecture

The compiler pipeline:

1. **Lexer** (`src/lexer.py`): Tokenizes source code
2. **Parser** (`src/parser.py`): Builds Abstract Syntax Tree (AST)
3. **State Transformer** (`src/state_transformer.py`): Converts functional AST to imperative IR ⭐
4. **Code Generator** (`src/codegen.py`): Produces assembly-like output

The **State Transformer** is the innovative core - it automatically converts pure functional expressions into efficient imperative instructions.

## Project Status

This is a **bare-bones implementation** demonstrating the core concepts:

✅ Working compiler with full pipeline  
✅ Functional to imperative transformation  
✅ 6 example programs  
✅ 8 comprehensive tests  
✅ Complete documentation  

**Current Features**:
- Function definitions with typed parameters
- Integer and boolean types
- Recursive functions
- Conditionals (if-then-else)
- Binary operations (+, -, *, /, ==, !=, <, >, <=, >=)
- Let bindings
- Function calls

**Future Enhancements**: See [Architecture docs](docs/ARCHITECTURE.md) for potential improvements (type inference, optimizations, real code generation, etc.)

## Contributing

This is a demonstration project showing the bare bones of a functional-to-imperative language compiler. Feel free to explore, learn, and extend!

## License

Open source - use and modify as you wish.