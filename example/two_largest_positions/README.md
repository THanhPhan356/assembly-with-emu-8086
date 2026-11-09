# Positions of the Two Largest Signed 16-bit Elements

## Problem statement

Write an assembly program to find the positions of the two largest values in an array A of length N, whose elements are signed 16-bit integers.

## Conventions

- Positions are zero-based element indices, not byte offsets.
- Select two different positions. Their values may be equal.
- When values tie, choose the earliest available position.
- The two-pass versions leave both positions at -1 (FFFFh) when N is less than 2. The one-pass v2 versions require N >= 2.
- N is the actual array length. COM data and code must fit in one segment; EXE data and code must each fit in their own 64 KiB segment.

## Simple two-pass algorithm

1. Initialize max1 and pos1 from the first element. Scan the rest of the array and update them whenever a larger signed value is found.
2. Scan the array again, skipping pos1. Initialize max2 and pos2 from the first remaining element, then update them whenever a larger signed value is found.

Both passes use the same basic pattern: check the index, compare, update if needed, and increment the index. The array is unchanged. Time complexity is O(N), with O(1) extra space.

Initializing the second maximum from an actual element also handles an array containing only -32768. Initializing a maximum to zero would fail for an all-negative array.

## Variables

| Name | Meaning |
|---|---|
| A | Array of signed words (-32768 through 32767) |
| N | Number of elements |
| max1, max2 | Values at the two selected positions |
| pos1, pos2 | Resulting element indices |
| SI | Current element index |
| BX | Byte offset, equal to 2 * SI |
| AX | Current array value |

JLE performs the signed value comparison. JAE checks the unsigned array index.

## Run in emu8086

1. Open [two_largest_positions.asm](two_largest_positions.asm).
2. Compile and emulate the COM program.
3. Run to the final RET and inspect pos1, pos2, max1, and max2 in memory. These variables contain the results; the program does not print them.

For the supplied array:

```text
A = [-7, 12, 5, 12, -2]
pos1 = 1, max1 = 12
pos2 = 3, max2 = 12
```

## DOS EXE versions

| Algorithm | COM source | EXE source |
|---|---|---|
| Two passes; results in memory; handles N < 2 | [two_largest_positions.asm](two_largest_positions.asm) | [two_largest_positions_exe.asm](two_largest_positions_exe.asm) |
| One pass; maxima in AX/DX; requires N >= 2 | [two_largest_positions_v2.asm](two_largest_positions_v2.asm) | [two_largest_positions_v2_exe.asm](two_largest_positions_v2_exe.asm) |

Open an EXE source in emu8086, select **Compile**, save the output as `.exe`, then select **Emulate**. Both EXE sources use `.MODEL SMALL`, `.STACK 100h`, `.DATA`, `.CODE`, `MAIN PROC` and `END MAIN`. They initialize DS with `mov ax, @DATA` / `mov ds, ax` and exit with `INT 21h / AH=4Ch` instead of `RET`.

Stop at `done`, **before** `mov ah, 4Ch`, to inspect the results. In v2, AX and DX are the two maximum values; selecting the DOS exit function changes AH. In both versions, `pos1 = 1` and `pos2 = 3` for the supplied array. The programs do not print the results.

## Automated machine-code check

The test assembles the same instructions with FASM after adapting only the assembler syntax, then executes the resulting 16-bit machine code with Unicorn. It checks both positions, both values, and that the input array is unchanged, including empty, single-element, all-negative, duplicate-maximum, and signed-limit cases.

With Python, FASM, and the Unicorn Python package available:

```text
python verify_two_largest_positions.py
python verify_two_largest_positions_exe.py
```

The EXE check runs both MZ programs with DOS-style PSP startup, relocation and stack setup. It verifies positions, maxima, unchanged input, DS initialization, balanced stack and DOS termination: 63 two-pass cases and 60 one-pass cases. The one-pass check skips arrays shorter than two elements, matching its documented precondition.

Set the FASM environment variable if the assembler is not on PATH. These checks are not runs inside the emu8086 GUI.
