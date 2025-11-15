# Squawk Examples

This directory contains example programs written in Squawk.

## Running Examples

To compile an example:
```bash
python3 src/squawk.py examples/<filename>.sq
```

## Example Programs

### factorial.sq
Classic factorial function using recursion.

**Functional Code**:
```squawk
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)
```

**Generated Assembly** (excerpt):
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

### fibonacci.sq
Fibonacci sequence using double recursion.

Shows how the compiler handles multiple recursive calls in a single expression.

### sum.sq
Simple recursive sum from n down to 0.

### power.sq
Power function (base^exp) using recursion with multiple parameters.

### max.sq
Maximum of two numbers using comparison operators.

Demonstrates simple if-then-else without recursion.

## Understanding the Output

The compiler generates assembly-like code with:

1. **Temporaries**: Variables like `t0`, `t1`, `t2` are compiler-generated temps
2. **Labels**: `then0`, `else1`, `end_if2` mark jump targets
3. **Instructions**:
   - `mov`: Assignment
   - `add/sub/mul/div`: Arithmetic
   - `eq/neq/lt/gt/leq/geq`: Comparisons
   - `jmp`: Unconditional jump
   - `jmpif`: Conditional jump
   - `call`: Function call
   - `ret`: Return

## Key Observations

Notice how:
- Pure functional recursion becomes explicit loops with jumps
- Expression evaluation is broken into steps with temporaries
- Control flow becomes explicit with labels and jumps
- All state is made explicit through assignments

This demonstrates Squawk's core innovation: automatic transformation from functional to imperative code.
