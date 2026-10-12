# Absolute Values of an Array

## Problem Statement

Given an array A with N signed 16-bit integers, compute an array B such that `B[i] = |A[i]|`.

Each example processes the entire array and keeps A unchanged. B stores unsigned 16-bit magnitudes so that it can also represent `|-32768| = 32768`.

## Programs

- [abs_array_neg.asm](abs_array_neg.asm): mathematical approach using `NEG`.
- [abs_array_bits.asm](abs_array_bits.asm): invert all bits with `NOT`, then add 1 with `INC`.

Both are complete emu8086 `.COM` programs. Open either file, select **Emulate**, and step through the instructions. The results are stored in B; nothing is printed.

## Method 1: Mathematical Negation

For each element:

- If A[i] is nonnegative, copy it to B[i].
- If A[i] is negative, calculate `0 - A[i]` and store the result.

The core instructions are:

```asm
mov ax, A[si]
cmp ax, 0
jge store_result
neg ax

store_result:
mov B[si], ax
```

`CMP` sets the flags without changing AX. `JGE` uses a signed comparison to skip negation for nonnegative values. `NEG AX` computes `0 - AX`.

## Method 2: Two's Complement Negation

For negative values, invert every bit and add 1:

```asm
not ax
inc ax
```

These two instructions replace `NEG AX` in the first program. Nonnegative values still skip the conversion.

The same rule applies to an 8-bit value in AL. For example, converting -5 to +5:

```text
-5:             11111011
Invert bits:    00000100
Add 1:          00000101 = 5
```

```asm
not al
inc al
; Equivalent to NEG AL
```

Run the conversion only when the input is negative. Clearing only the sign bit is incorrect for two's complement: clearing the top bit of `11111011` gives `01111011` (123), not 5.

## Array Traversal

- `ORG 100h` sets the starting offset for a `.COM` program.
- `JMP start` skips the data declarations.
- `PUSH CS` followed by `POP DS` sets DS to the segment containing the code and arrays.
- `SI` holds the byte offset of the current element: 0, 2, 4, and so on.
- `CX` starts at N and counts the elements remaining.
- `JCXZ done` skips processing if the count is zero.
- `ADD SI, 2` selects the next 16-bit element.
- `LOOP next_element` decrements CX and repeats while CX is nonzero.
- `RET` terminates these `.COM` examples.

SI selects the element; it does not create a loop on its own.

## Expected Results

```text
A = {-5, 0, 7, -12, 3}
B = { 5, 0, 7,  12, 3}
```

Edit A and N together to try other inputs. To inspect -32768, set one input word to `-32768`: its output word is `8000h`, interpreted as unsigned 32768. It cannot be represented as a positive signed 16-bit integer. Similarly, the magnitude of -128 does not fit a signed 8-bit integer.

## Comparison

| Property | NEG | NOT followed by INC |
|---|---|---|
| Operation on a negative value | `0 - x` | Invert all bits, then add 1 |
| Instructions for negation | 1 | 2 |
| Readability | Expresses negation directly | Shows the two's complement representation |
| Array traversal | O(N) time, O(1) extra working space excluding B | O(N) time, O(1) extra working space excluding B |
| Result | Same unsigned magnitude | Same unsigned magnitude |

Both methods check the sign before converting. Instruction count alone is not a measured runtime comparison.
