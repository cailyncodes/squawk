# Getting Started with Squawk

Welcome to Squawk! This guide will help you get started with the language.

## Installation

No installation required! Squawk is a Python-based compiler. Just clone the repository:

```bash
git clone https://github.com/cailyncodes/squawk.git
cd squawk
```

## Requirements

- Python 3.6 or higher

## Your First Squawk Program

Create a file called `hello.sq`:

```squawk
fn greet(n: Int) -> Int =
  if n > 0 then n else 1
```

Compile it:

```bash
python3 src/squawk.py hello.sq
```

You'll see the compiled assembly-like output!

## Language Basics

### Function Definition

```squawk
fn functionName(param1: Type1, param2: Type2) -> ReturnType =
  expression
```

### Types

- `Int` - 64-bit signed integer
- `Bool` - Boolean (true or false)

### Expressions

#### Literals
```squawk
42        # integer
true      # boolean
false     # boolean
```

#### Binary Operations
```squawk
x + y     # addition
x - y     # subtraction
x * y     # multiplication
x / y     # division
x == y    # equality
x != y    # inequality
x < y     # less than
x > y     # greater than
x <= y    # less or equal
x >= y    # greater or equal
```

#### Conditionals
```squawk
if condition then trueExpr else falseExpr
```

Example:
```squawk
fn max(a: Int, b: Int) -> Int =
  if a > b then a else b
```

#### Function Calls
```squawk
factorial(5)
power(2, 10)
```

#### Let Bindings
```squawk
let name = value in body
```

Example:
```squawk
fn compute(x: Int) -> Int =
  let squared = x * x in
  let doubled = squared * 2 in
  doubled + 1
```

### Comments

Lines starting with `#` are comments:
```squawk
# This is a comment
fn add(x: Int, y: Int) -> Int = x + y  # function definition
```

## Examples

The `examples/` directory contains several example programs:

### 1. Factorial (Recursion)
```squawk
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)
```

Run: `python3 src/squawk.py examples/factorial.sq`

### 2. Fibonacci (Double Recursion)
```squawk
fn fib(n: Int) -> Int =
  if n <= 1 then n
  else fib(n - 1) + fib(n - 2)
```

Run: `python3 src/squawk.py examples/fibonacci.sq`

### 3. Maximum (Simple Conditional)
```squawk
fn max(a: Int, b: Int) -> Int =
  if a > b then a else b
```

Run: `python3 src/squawk.py examples/max.sq`

## Understanding the Output

When you compile a Squawk program, you get assembly-like code:

```assembly
function factorial(n):
    mov t2, n           # load n into temp t2
    mov t3, 1           # load 1 into temp t3
    leq t1, t2, t3      # compare n <= 1
    jmpif t1, then0     # jump to then0 if true
    jmp else1           # otherwise jump to else1
then0:
    mov t0, 1           # result = 1
    jmp end_if2         # jump to end
else1:
    # ... recursive case
    call t5 = factorial(t6)  # recursive call
    mul t0, t4, t5           # multiply results
end_if2:
    ret t0              # return result
```

### Key Instructions:

- `mov dest, src` - Move/assign value
- `add/sub/mul/div dest, left, right` - Arithmetic
- `eq/neq/lt/gt/leq/geq dest, left, right` - Comparisons
- `jmp label` - Unconditional jump
- `jmpif cond, label` - Conditional jump
- `call dest = func(args)` - Function call
- `ret value` - Return from function

## What Makes Squawk Special?

### You Write Functional Code:
```squawk
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)
```

- No loops
- No mutable variables
- No explicit state
- Pure, mathematical expressions

### Compiler Generates Imperative Code:
```assembly
function factorial(n):
    mov t2, n
    leq t1, t2, 1
    jmpif t1, then0
    jmp else1
then0:
    mov t0, 1
    ...
```

- Explicit control flow (jumps)
- Mutable temporaries
- Optimizable state transformations
- Direct mapping to machine code

**This is the innovation**: You get the benefits of functional programming (easy to write, reason about, and verify) AND efficient imperative execution (direct hardware mapping, minimal overhead).

## Testing

Run the test suite:

```bash
python3 tests/test_compiler.py
```

All tests should pass!

## What's Next?

1. Try modifying the examples
2. Write your own Squawk programs
3. Examine the generated assembly
4. Read the [Architecture](docs/ARCHITECTURE.md) documentation
5. Check the [Language Specification](docs/SPECIFICATION.md)

## Tips

- Start simple - try functions with just numbers and basic operations
- All expressions must be pure - no side effects
- Every function must return a value
- Use comments (`#`) to document your code
- The compiler shows you each step - watch how your functional code becomes imperative!

## Troubleshooting

**Syntax Error?**
- Check that all `if` expressions have both `then` and `else`
- Make sure all parentheses match
- Verify all parameters have type annotations

**Unexpected Output?**
- Run with `python3 src/squawk.py yourfile.sq` to see compilation stages
- Check the examples for correct syntax

## Learn More

- [Architecture Documentation](docs/ARCHITECTURE.md) - How the compiler works
- [Language Specification](docs/SPECIFICATION.md) - Formal language definition
- [Examples](examples/) - Working example programs

Happy coding with Squawk! 🦜
