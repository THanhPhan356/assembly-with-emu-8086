# DIV: Unsigned Integer Division

`DIV` has one explicit operand: the divisor, held in a register or memory. The operand size determines the implicit dividend and result registers.

| Divisor size | Example | Dividend | Quotient | Remainder |
|---|---|---|---|---|
| 1 byte (8 bits) | `div bl` | `AX` | `AL` | `AH` |
| 2 bytes (16 bits) | `div bx` | `DX:AX` | `AX` | `DX` |

`div al, 3` is invalid: it has two operands. `div 3` is also invalid: an immediate constant cannot be the divisor. Load 3 into a register first.

## Byte Divisor

```asm
mov ax, 7
mov bl, 3
div bl           ; AL = 2, AH = 1: 7 = 2 * 3 + 1
```

When loading a small unsigned value into `AL`, clear `AH` before division so that the full `AX` contains the intended dividend:

```asm
mov al, ARR[si]
mov ah, 0
mov bl, 3
div bl
cmp ah, 0        ; A zero remainder means the value is divisible by 3.
```

After division, `AL` no longer contains the original number. Reload it from the array before calculating a sum, minimum, or maximum. Use `CMP` to test the remainder; division does not provide usable comparison flags.

## Word Divisor

```asm
mov dx, 0
mov ax, 1000
mov bx, 3
div bx           ; AX = 333, DX = 1
```

`DX:AX` combines two registers into one 32-bit unsigned value: `DX * 65536 + AX`. Set `DX = 0` when the dividend fits in `AX`; for a genuinely larger dividend, load its high word into `DX` instead.

The divisor must not be zero. The quotient must fit in `AL` (0-255) or `AX` (0-65535), respectively; otherwise a divide error occurs. Signed division uses `IDIV`, which is outside this lesson.

## Reading the Debugger

The highlighted instruction is the **next** instruction to execute. With `AX = 1` and `BL = 3`, the state changes only after stepping over `DIV BL`:

| State | AH (left, H) | AL (right, L) |
|---|---:|---:|
| Before division | 0 | 1 |
| After division | 1 (remainder) | 0 (quotient) |

See the [group A statistics example](../example/group_a_statistics/README.md) for a complete use of `DIV BL`.
