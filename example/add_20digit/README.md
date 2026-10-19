# 20-digit Integer Addition

## Problem Statement

Write C and Assembly programs to add two **unsigned decimal integers with up to 20 digits** using five 16-bit words per number. Use predefined values; keyboard input is not required. The Assembly program runs in emu8086.

The largest input is `99999999999999999999`, which needs 67 bits. The sum needs at most 68 bits, so five 16-bit words (80 bits) can hold both inputs and the complete result.

Both programs use:

```text
A = 12345678901234567890
B = 98765432109876543210
C = 111111111011111111100
```

## Code

- [C program](add_20digit.c): adds corresponding 16-bit words using a 32-bit temporary and an explicit carry.
- [Assembly program for emu8086](add_20digit.asm): adds the low words with `ADD`, then uses `ADC` for the remaining four words.

These are binary integers split into words, not strings of ASCII digits. In both programs, the **least significant word comes first**:

| Word index | Byte offset | A (hex) | B (hex) | C (hex) |
|---|---|---|---|---|
| 0 | 0 | 0AD2 | 7EEA | 89BC |
| 1 | 2 | EB1F | E526 | D045 |
| 2 | 4 | A98C | 4D38 | F6C5 |
| 3 | 6 | AB54 | 5AA5 | 05F9 |
| 4 | 8 | 0000 | 0005 | 0006 |

The value represented by words `w[0]` through `w[4]` is `w[0] + w[1]*2^16 + w[2]*2^32 + w[3]*2^48 + w[4]*2^64`.

## Running the C Program

Compile with GCC:

```sh
gcc -std=c11 -Wall -Wextra add_20digit.c -o add_20digit
```

Run `./add_20digit` on Linux/macOS or `.\add_20digit.exe` in PowerShell. No input is required.

Expected output:

```text
Sum (16-bit words, low first): 89BC D045 F6C5 05F9 0006
```

The cast to `uint32_t` before addition keeps the intermediate sum wide enough, including on a C implementation with 16-bit `int`. Casting the result to `uint16_t` keeps the low 16 bits; shifting right by 16 extracts the carry.

## Running the Assembly Program

Open `add_20digit.asm` in emu8086, select **Emulate**, and step through the instructions. Inspect the five words of `c` in memory before `INT 20h`. The program stores the result and does not print output.

- `DW` defines 16-bit words. Each number occupies 10 bytes.
- `[a + si]` addresses a word at byte offset SI, so the offsets are 0, 2, 4, 6, and 8.
- The first `ADD` produces the carry flag `CF`; each subsequent `ADC` adds both words and that carry.
- `MOV`, `INC`, and `LOOP` preserve `CF`. Do not use `ADD SI, 2` or `CMP` between word additions, because they overwrite the carry flag.
- The low word is handled before the loop; `CX = 4` processes the remaining four words.
- DOS initializes DS to the program segment for a `.COM` program, so this example does not need `PUSH CS / POP DS`.
- For inputs within the stated range, the sum fits in five words; no sixth word is needed.

## Expected Results

| A (decimal) | B (decimal) | C (decimal) | C words (hex, low first) |
|---|---|---|---|
| 12345678901234567890 | 98765432109876543210 | 111111111011111111100 | 89BC D045 F6C5 05F9 0006 |
| 0 | 0 | 0 | 0000 0000 0000 0000 0000 |
| 65535 | 1 | 65536 | 0000 0001 0000 0000 0000 |
| 18446744073709551615 | 1 | 18446744073709551616 | 0000 0000 0000 0000 0001 |
| 99999999999999999999 | 99999999999999999999 | 199999999999999999998 | FFFE C61F BC5A D78E 000A |

To try another case, convert each input into five 16-bit words and update the initializers in both files. Plain decimal digits inside quotes would create ASCII data and cannot be used by this binary addition loop.
