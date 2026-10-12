# Converting a While Loop to Assembly

## Problem Statement

Convert the following pseudocode into an emu8086 program:

```c
i = 0;
while (i < n) {
    b[i] = abs(a[i]);
    i++;
}
```

This example uses signed 8-bit elements in A (`DB`). B stores unsigned 8-bit magnitudes. Each element occupies one byte, so SI serves as both the array index and the byte offset.

## Code

[while_abs_array.asm](while_abs_array.asm)

The file is a complete `.COM` program. Open it in emu8086, select **Emulate**, and step through the instructions. Inspect B in memory; the program does not print output.

## Translation

| Pseudocode | Assembly | Purpose |
|---|---|---|
| `i = 0` | `mov si, 0` | Initialize the index |
| `while (i < n)` | `cmp si, N` / `jae end_while` | Exit before the body when i >= N |
| Read `a[i]` | `mov al, A[si]` | Load the current byte |
| Calculate `abs(a[i])` | `cmp al, 0` / `jge result` / `neg al` | Negate only negative values |
| Store `b[i]` | `mov B[si], al` | Store the magnitude |
| `i++` | `inc si` | Move to the next byte |
| Repeat | `jmp while_loop` | Return to the condition |

`JAE` uses an unsigned comparison for the array index. `JGE` uses a signed comparison for the value in AL. The condition is checked before every iteration, so a zero count skips the body.

## Memory Addressing

- `A[si]` and `[A + si]` address the same byte.
- `mov al, A + si` is not the correct syntax for loading an array element.
- `mov B[si], A[si]` is not allowed: MOV cannot copy directly between two memory operands. Use AL.
- Labels cannot contain spaces: use `end_while:`.
- `PUSH CS` / `POP DS` initializes DS for the arrays in this `.COM` program.
- SI does not repeat instructions by itself; the jump back to `while_loop` creates the loop.

For 16-bit elements (`DW`), use AX to load values and advance the byte offset by 2. Keep the logical element index separate from that offset when comparing against N. See the [16-bit absolute-value examples](../abs_array/README.md).

## Expected Results

```text
A = {-5, 0, 7, -12, 3}
B = { 5, 0, 7,  12, 3}
```

Edit A and N together to try other inputs. The magnitude of -128 is 128 (`80h`), which fits unsigned B but not a signed 8-bit value.
