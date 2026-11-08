# Jumps: Signed and Unsigned Comparisons

Remember the letters:

- **A / B = Above / Below = unsigned.**
- **G / L = Greater / Less = signed.**
- **E = Equal.**

## Comparing Two Values

After `cmp ax, bx`, choose a jump according to how the operands should be interpreted:

| Condition | Signed | Unsigned |
|---|---|---|
| AX > BX | JG | JA |
| AX >= BX | JGE | JAE |
| AX < BX | JL | JB |
| AX <= BX | JLE | JBE |
| AX == BX | JE / JZ | JE / JZ |
| AX != BX | JNE / JNZ | JNE / JNZ |

`JMP` jumps unconditionally and does not inspect flags.

`CMP` sets flags as if it calculated AX - BX, without changing either operand. It does not decide whether the values are signed; the conditional jump selects the interpretation. Keep the jump immediately after `CMP` while learning, so another instruction does not change the flags first.

`JE` and `JZ` are aliases that test ZF = 1. `JNE` and `JNZ` are aliases that test ZF = 0. Equality works for both signed and unsigned values because the bit patterns are either identical or different.

## Example: JL Versus JB

```asm
mov ax, 0FFFFh
mov bx, 1
cmp ax, bx
```

Consider each jump independently, immediately after that comparison:

| Jump | Interpretation of AX | Comparison | Taken? |
|---|---|---|---|
| JL label | -1 (signed) | -1 < 1 | Yes |
| JB label | 65535 (unsigned) | 65535 < 1 | No |

`JB` is not a special jump for negative numbers. It always uses the unsigned interpretation. Use `JL` when comparing signed values, including negative values.

For 16-bit operands, when both values are in 0-32767, signed and unsigned ordering agree. When the high bit is set, they can differ: the same 16 bits represent either 32768-65535 unsigned or -32768 to -1 signed.

## Runnable Demo

Open [jumps_demo.asm](jumps_demo.asm) in emu8086, choose **Compile**, then **Emulate**, then **Run**. Each result is selected by an actual `JL` or `JB` instruction; the messages are not hard-coded outcomes.

The program reloads the operands for each case and compares them again after printing, because DOS output may change flags. The print helper preserves the operand registers.

Expected output:

```text
AX = FFFFh (-1 signed / 65535 unsigned), BX = 1
  JL (signed less):    TAKEN
  JB (unsigned below): NOT TAKEN

AX = 2, BX = 3
  JL (signed less):    TAKEN
  JB (unsigned below): TAKEN

AX = 3, BX = 2
  JL (signed less):    NOT TAKEN
  JB (unsigned below): NOT TAKEN

AX = 3, BX = 3
  JL (signed less):    NOT TAKEN
  JB (unsigned below): NOT TAKEN
```

When stepping through the demo, watch AX and BX at each `CMP`, then check whether execution enters the `signed_less` or `unsigned_below` label.

The source assembles with the bundled FASM. Direct execution in the emu8086 application has not been verified.
