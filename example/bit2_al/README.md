# Exercise 3: Test, Set, Clear, and Toggle Bit 2 of AL

## Problem Statement

AL contains 8 bits, numbered 0 through 7. Bit 0 is the LSB; bit 7 is the MSB. Write a program to test, set, clear, and toggle bit 2 of AL while leaving the other bits unchanged.

## emu8086 Code

[bit2_al.asm](bit2_al.asm)

The mask for bit 2 is `00000100b` (`04h`). The mask for clearing bit 2 is `11111011b` (`FBh`).

| Operation | Instruction | Effect |
|---|---|---|
| Test | `test al, 00000100b` | AL is unchanged; ZF = 1 if bit 2 is 0, ZF = 0 if bit 2 is 1 |
| Set | `or al, 00000100b` | Set bit 2 to 1 |
| Clear | `and al, 11111011b` | Set bit 2 to 0 |
| Toggle | `xor al, 00000100b` | Change bit 2 from 0 to 1 or from 1 to 0 |

## Running the Program and Expected Results

Open the file in emu8086, select **Emulate**, and step through each instruction. Inspect `ZF` immediately after `TEST`, because subsequent instructions change the flags.

Starting with `AL = 00001000b`:

- After `TEST`: AL remains `00001000b`, ZF = 1.
- After `OR`: AL = `00001100b`.
- After `AND`: AL = `00001000b`.
- After `XOR`: AL = `00001100b`.

The operations run sequentially on the same AL value. The program does not print output.
