# Squawk Language Specification

## 1. Introduction

Squawk is a low-level programming language that allows users to write functional code which is automatically transformed into efficient state-modifying machine code.

## 2. Lexical Structure

### 2.1 Keywords
```
fn if then else let in Int Bool return
```

### 2.2 Operators
```
+ - * / = == != < > <= >= ->
```

### 2.3 Delimiters
```
( ) { } , : ;
```

### 2.4 Literals
- **Integer**: `0`, `42`, `-10`
- **Boolean**: `true`, `false`

### 2.5 Identifiers
Start with letter or underscore, followed by letters, digits, or underscores.

## 3. Syntax

### 3.1 Function Definition
```
fn <name>(<param>: <type>, ...) -> <return-type> =
  <expression>
```

### 3.2 Expressions

#### Literals
```
42
true
false
```

#### Variables
```
x
myVariable
```

#### Binary Operations
```
a + b
x * y
n == 0
```

#### Conditionals
```
if condition then expr1 else expr2
```

#### Function Calls
```
factorial(5)
add(x, y)
```

#### Let Bindings
```
let x = 10 in x + 5
```

## 4. Type System

### 4.1 Primitive Types
- `Int`: 64-bit signed integer
- `Bool`: Boolean value

### 4.2 Function Types
```
Int -> Int
(Int, Int) -> Bool
```

## 5. Semantics

### 5.1 Functional Semantics
All user code is pure and referentially transparent. Functions always return the same output for the same input.

### 5.2 Compilation Model

The compiler performs the following transformations:

1. **Parsing**: Source code → AST
2. **Type Checking**: Verify type correctness
3. **Functional IR**: Generate functional intermediate representation
4. **State Transformation**: Convert to imperative IR with explicit state
5. **Optimization**: Register allocation, tail call optimization
6. **Code Generation**: Produce target code

### 5.3 State Transformation Innovation

The key innovation is automatic conversion from functional to imperative:

**Functional (User Writes):**
```
fn sum(list: List) -> Int =
  if empty(list) then 0
  else head(list) + sum(tail(list))
```

**Imperative (Compiler Generates):**
```
sum_impl:
  mov r0, 0          # accumulator = 0
  mov r1, [list]     # current = list
loop:
  cmp r1, null
  je done
  add r0, [r1]       # accumulator += current.value
  mov r1, [r1+8]     # current = current.next
  jmp loop
done:
  ret
```

## 6. Example Programs

### Factorial
```squawk
fn factorial(n: Int) -> Int =
  if n <= 1 then 1
  else n * factorial(n - 1)
```

### Fibonacci
```squawk
fn fib(n: Int) -> Int =
  if n <= 1 then n
  else fib(n - 1) + fib(n - 2)
```

### Sum
```squawk
fn sum(n: Int) -> Int =
  if n <= 0 then 0
  else n + sum(n - 1)
```
