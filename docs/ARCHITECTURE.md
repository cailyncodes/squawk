# Squawk Compiler Architecture

## Overview

Squawk is a low-level programming language that bridges functional and imperative paradigms. Users write pure functional code, and the compiler automatically transforms it into efficient state-modifying machine code.

## Compilation Pipeline

The Squawk compiler follows a multi-stage pipeline:

```
Source Code → Lexer → Tokens → Parser → AST → State Transformer → Imperative IR → Code Generator → Assembly
```

### 1. Lexer (`src/lexer.py`)

**Purpose**: Converts source code text into a stream of tokens.

**Key Features**:
- Tokenizes keywords, operators, identifiers, and literals
- Handles comments (lines starting with `#`)
- Tracks line and column numbers for error reporting
- Supports multi-character operators (`==`, `!=`, `<=`, `>=`, `->`)

**Example**:
```
Input:  "fn add(x: Int) -> Int = x + 1"
Output: [FN, IDENTIFIER("add"), LPAREN, IDENTIFIER("x"), COLON, INT_TYPE, ...]
```

### 2. Parser (`src/parser.py`)

**Purpose**: Builds an Abstract Syntax Tree (AST) from tokens.

**Key Features**:
- Recursive descent parser
- Operator precedence handling
- Support for expressions: literals, variables, binary ops, if-then-else, function calls, let bindings
- Function definitions with typed parameters

**AST Nodes** (`src/ast_nodes.py`):
- `IntLiteral`, `BoolLiteral`: Constant values
- `Variable`: Variable references
- `BinaryExpr`: Binary operations (+, -, *, /, ==, <, etc.)
- `IfExpr`: Conditional expressions
- `CallExpr`: Function calls
- `LetExpr`: Local bindings
- `FunctionDef`: Function definitions
- `Program`: Top-level program

**Example AST**:
```python
FunctionDef(
    name="factorial",
    parameters=[Parameter("n", Type.INT)],
    return_type=Type.INT,
    body=IfExpr(
        condition=BinaryExpr(BinaryOp.LESS_EQUAL, Variable("n"), IntLiteral(1)),
        then_expr=IntLiteral(1),
        else_expr=BinaryExpr(BinaryOp.MULTIPLY, Variable("n"), CallExpr("factorial", [BinaryExpr(...)]))
    )
)
```

### 3. State Transformer (`src/state_transformer.py`)

**Purpose**: This is the innovative core of Squawk. It converts functional AST into imperative intermediate representation (IR).

**Key Innovation**: Automatic transformation from pure functional code to efficient state-based code.

**Transformation Strategy**:
1. **Expression Evaluation**: Each expression is evaluated into a temporary variable
2. **Control Flow**: If-expressions become conditional jumps with labels
3. **Function Calls**: Direct calls with evaluated arguments
4. **Let Bindings**: Become assignments to named variables

**Example Transformation**:

Functional (Input):
```squawk
if n <= 1 then 1
else n * factorial(n - 1)
```

Imperative (Output):
```
mov t2, n
mov t3, 1
leq t1, t2, t3          # evaluate condition
jmpif t1, then0         # conditional jump
jmp else1
then0:
    mov t0, 1           # then branch
    jmp end_if2
else1:
    mov t4, n
    mov t7, n
    mov t8, 1
    sub t6, t7, t8
    call t5 = factorial(t6)  # recursive call
    mul t0, t4, t5
end_if2:
    ret t0
```

**Benefits**:
- Explicit control flow (jumps, labels)
- Explicit state (temporaries, assignments)
- Easy to optimize (register allocation, dead code elimination)
- Direct mapping to machine code

### 4. Code Generator (`src/codegen.py`)

**Purpose**: Generates assembly-like code from imperative IR.

**Output Format**:
- Function declarations
- Three-address code instructions
- Labels for control flow
- Explicit return statements

**Instruction Set**:
- `mov dest, src`: Move/assign value
- `add/sub/mul/div dest, left, right`: Arithmetic operations
- `eq/neq/lt/gt/leq/geq dest, left, right`: Comparison operations
- `jmp label`: Unconditional jump
- `jmpif cond, true_label`: Conditional jump
- `call dest = func(args)`: Function call
- `ret value`: Return from function

## Type System

Currently supports two primitive types:
- `Int`: 64-bit signed integer
- `Bool`: Boolean value (true/false)

Type checking is minimal in this bare-bones implementation.

## Language Features

### Function Definitions
```squawk
fn name(param1: Type1, param2: Type2) -> ReturnType = expression
```

### Expressions
- **Literals**: `42`, `true`, `false`
- **Variables**: `x`, `myVar`
- **Binary Operations**: `a + b`, `x * y`, `n == 0`
- **Conditionals**: `if cond then expr1 else expr2`
- **Function Calls**: `factorial(5)`
- **Let Bindings**: `let x = 10 in x + 5`

### Operator Precedence
1. Primary expressions (literals, variables, parentheses)
2. Multiplicative (`*`, `/`)
3. Additive (`+`, `-`)
4. Comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`)

## Design Philosophy

### Why Functional User Code?

1. **Easier to Reason About**: Pure functions have no side effects
2. **Composable**: Functions can be easily combined
3. **Testable**: Same input always produces same output
4. **Mathematical**: Aligns with formal verification

### Why State-Modifying Machine Code?

1. **Performance**: Imperative code maps directly to hardware
2. **Efficiency**: Minimal memory allocations, optimal register usage
3. **Control**: Direct access to low-level operations
4. **Compatibility**: Easy to interface with existing systems

### The Innovation: Automatic Transformation

Most languages force you to choose:
- Write functional code (slower runtime)
- Write imperative code (harder to reason about)

Squawk gives you both:
- Write in functional style (easy)
- Compile to imperative code (fast)
- Compiler handles the transformation automatically

## Future Enhancements

This is a bare-bones implementation. Potential improvements:

1. **Type System**:
   - Type inference
   - Polymorphic types
   - User-defined types (structs, unions)
   - Array/list types

2. **Optimizations**:
   - Tail call optimization
   - Register allocation
   - Dead code elimination
   - Constant folding
   - Function inlining

3. **Language Features**:
   - Pattern matching
   - Higher-order functions
   - Lambda expressions
   - Module system

4. **Backend**:
   - Real assembly generation (x86-64, ARM)
   - LLVM IR output
   - Bytecode interpreter
   - JIT compilation

5. **Tools**:
   - REPL (Read-Eval-Print Loop)
   - Debugger
   - IDE support
   - Package manager

## References

- **Functional Programming**: Haskell, OCaml, F#
- **State Transformation**: ANF (Administrative Normal Form), CPS (Continuation-Passing Style)
- **Low-level Languages**: C, Rust, Assembly
- **Compiler Design**: "Engineering a Compiler" by Cooper & Torczon
