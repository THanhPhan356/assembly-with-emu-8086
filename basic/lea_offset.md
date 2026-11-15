# LEA and OFFSET: Addresses Versus Values

An address tells you **where** data is stored. Reading that address gives you the **value** stored there. In 8086 real mode, a segment and an offset identify a memory location:

`physical address = segment * 16 + offset`

An offset alone is not a complete physical address.

## A Fixed Variable

Assume the program declares a word named `VALUE` and initializes DS to its data segment:

```asm
VALUE DW 1234h
```

Consider these instructions independently, using emu8086/MASM-style syntax:

| Instruction | What AX receives |
|---|---|
| `mov ax, VALUE` | The stored word: 1234h |
| `mov ax, [VALUE]` | The stored word: 1234h |
| `mov ax, OFFSET VALUE` | The offset of VALUE |
| `lea ax, VALUE` | The offset of VALUE |

If VALUE happens to be at offset 0020h, the first two instructions give AX = 1234h; the last two give AX = 0020h. The actual offset depends on the assembled program.

## OFFSET Is an Assembler Operator

`OFFSET VALUE` asks the assembler/linker to resolve the offset of a label. It is not a CPU instruction. In `mov ax, OFFSET VALUE`, the CPU executes MOV with an immediate offset value.

Use OFFSET when loading the address of a known variable, array, string, or procedure.

OFFSET does not evaluate live CPU registers. Do not use `OFFSET [bx+si]` to calculate an address from the current BX and SI.

## LEA Is a CPU Instruction

LEA means **Load Effective Address**. It calculates an offset from a legal memory-address expression without reading memory at that address.

```asm
mov bx, 1000h
mov si, 0006h
lea ax, [bx+si+2]    ; AX = 1008h; no data is read from memory.
```

LEA does not change BX, SI, segment registers, or flags. Its destination on 8086 is a 16-bit general-purpose register.

For a fixed label, `lea si, ARRAY` and `mov si, OFFSET ARRAY` produce the same offset. LEA is useful when the address also depends on current register values.

## Calculating an Address Versus Reading It

Assume DS:1008h contains the word 5678h:

| Operation | Result |
|---|---|
| `lea ax, [bx+si+2]`, with BX = 1000h and SI = 6 | AX = 1008h |
| `mov ax, [bx+si+2]`, with the same registers | AX = 5678h |

LEA also works with BP-based expressions. `lea ax, [bp+4]` calculates BP + 4; `mov ax, [bp+4]` reads a word from SS:BP + 4.

## 8086 Addressing Limits

- Use BX or BP as a base and SI or DI as an index, optionally with a displacement.
- BX, BP, SI, and DI can also be used individually.
- Pairs such as BX + SI or BP + DI are legal; AX, SP, BX + BP, and SI + DI are not legal address expressions on 8086.
- Scaled indexes such as `[bx+si*2]` are not available on 8086.
- LEA and OFFSET do not initialize DS or SS. A later memory access still needs the correct segment.
- These are learning fragments, not complete programs. A DOS EXE must initialize DS before accessing its data.

Self-check: with BX = 0200h and SI = 4, LEA of [BX + SI + 2] gives 0206h, regardless of the contents of memory there.

Next: [Three Basic Ways to Use the Stack](stack.md).
