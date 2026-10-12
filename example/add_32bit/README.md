# 32-bit Integer Addition

## Problem Statement

Write C and Assembly programs to add two **unsigned 32-bit integers**. The Assembly program runs in emu8086. Store the lower 32 bits of the sum and extract the 33rd bit as a carry if the addition exceeds the 32-bit range.

Each input must be between `0` and `4294967295`. Both programs perform the same calculation. The C program reads decimal inputs from the keyboard; the Assembly program uses predefined values.

## Code

- [C program](add_32bit.c): uses `uint32_t`, calculates `sum = a + b`, and detects carry with `carry = (sum < a)`.
- [Assembly program for emu8086](add_32bit.asm): splits each input into two 16-bit words, adds the low words with `ADD`, and adds the high words plus carry with `ADC`.

## Running the C Program

Compile with GCC:

```sh
gcc -std=c11 -Wall -Wextra add_32bit.c -o add_32bit
```

Run `./add_32bit` on Linux/macOS or `.\add_32bit.exe` in PowerShell. Enter two valid decimal integers within the range specified above.

Example input:

```text
4294967295 1
```

Output, after the input prompt:

```text
32-bit sum = 0
Carry bit = 1
```

## Running the Assembly Program

Open `add_32bit.asm` in emu8086, select **Emulate**, and step through the instructions to inspect registers and memory. The program stores its results in variables and does not print them.

Each input is declared with the **low word first, followed by the high word**:

```asm
a dw 0FFFFh, 0FFFFh   ; FFFFFFFFh
b dw 0001h, 0000h     ; 00000001h
```

- `[a]` reads the low word; `[a + 2]` reads the high word, because each word occupies 2 bytes.
- `ADD` produces the carry flag `CF`; `ADC` includes `CF` in the next addition.
- `MOV` preserves `CF`. Do not replace `mov cx, 0` with `xor cx, cx`, because `XOR` clears the carry flag.
- The 32-bit sum is held in `DX:AX` and stored in `sum`. The final carry is held in `CX` and stored in `carry`.

For the values above, `sum = 00000000h` and `carry = 1`. The full result is `100000000h` (4294967296).

## Expected Results

| A (decimal) | B (decimal) | 32-bit Sum (decimal) | Carry |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 10 | 20 | 30 | 0 |
| 65535 | 1 | 65536 | 0 |
| 4294967295 | 1 | 0 | 1 |
| 4294967295 | 4294967295 | 4294967294 | 1 |

In the Assembly program, change the two words of `a` and `b` to try other inputs.
