# Sort Signed 16-bit Integers in Ascending Order

## Problem Statement

Given a positive integer N and an array ARR of N signed 16-bit integers, write a complete 8086 assembly program using the DOS EXE template.

Requirements:

1. Declare N and ARR in the data segment.
2. Sort ARR in ascending (nondecreasing) order using two nested loops and comparisons followed by swaps.
3. Store the result directly in ARR.
4. Run the program in emu8086 and inspect the array in memory.

The program should handle a single element, duplicate values, negative values, and an already sorted array.

Example:

- Input: N = 6, ARR = [7, -3, 12, 0, -8, 7].
- Expected result: ARR = [-8, -3, 0, 7, 7, 12].

## Solution

[sort_signed_words_exe.asm](sort_signed_words_exe.asm) contains the complete DOS EXE program.

This is a direct exchange sort. For each position i, compare ARR[i] with every later element ARR[j]. Whenever ARR[i] is larger, swap the two values immediately. After the inner loop, position i contains the minimum of the remaining elements.

The algorithm uses O(N^2) comparisons and O(1) extra storage. It is not stable: swapping distant elements can change the relative order of equal elements.

## Register Roles

| Register | Role |
|---|---|
| SI | Byte offset of the current outer-loop element |
| DI | Byte offset of the inner-loop element |
| AX | Current value of ARR[SI] |
| BX | Value of ARR[DI] |
| CX | Remaining outer-loop passes |
| DX | Exclusive byte-offset limit, 2*N |

## How the Program Works

1. Initialize DS with the address of the data segment.
2. Return immediately to DOS when N is at most one. Otherwise, set CX to N-1, DX to 2*N, and SI to zero.
3. At outer_loop, load ARR[SI] into AX and set DI to SI+2.
4. At inner_loop, stop the scan when DI reaches DX. Otherwise, load ARR[DI] into BX.
5. Compare AX and BX. JLE skips the swap when AX is less than or equal to BX, using a signed comparison.
6. If a swap is needed, XCHG exchanges AX and BX, then two MOV instructions write both values back into ARR.
7. Advance DI by two bytes and continue the inner loop.
8. When the inner loop finishes, advance SI by two bytes. LOOP decrements CX and starts the next outer pass while CX is nonzero.
9. Exit through INT 21h, function 4Ch.

For the first pass of the sample, AX starts at 7, becomes -3, then becomes -8. The first position therefore contains -8 at the end of that pass.

## Details to Notice

- Each DW element occupies two bytes, so SI and DI advance by 2.
- ARR[SI] is equivalent to [ARR+SI]. The offsets are measured in bytes, not element counts.
- SHL DX, 1 doubles N to obtain the byte limit. For N=6, valid element offsets are 0, 2, 4, 6, 8, and 10; 12 is the stopping boundary.
- JLE is appropriate for signed values. JB would interpret the operands as unsigned.
- XCHG AX, BX exchanges the register values; the array changes only after the two stores.
- Only the outer loop uses LOOP, so the inner loop does not consume the CX counter.
- .STACK 100h reserves 256 bytes. This sorting loop needs no explicit PUSH or POP instructions.

## Run in emu8086

Open the source, compile it as an EXE, and select Emulate. Step to sort_done and inspect the signed words in ARR.

The program changes the array in memory and does not print it. The exit instructions overwrite AX; the sorted result remains in ARR.

When changing the input, update N to match the number of DW elements. Keep 1 <= N <= 32767 and ensure the data segment fits within 64 KiB, so the byte limit and array addresses do not wrap.

## COM Version

[sort_signed_words.asm](sort_signed_words.asm) contains the complete COM template: `ORG 100h`, a jump over the data, DS set to CS, and a near RET that exits through the PSP. Code, data, and the DOS-provided stack share one segment.

Open this source in emu8086 and compile as COM. Inspect ARR at sort_done; the sample becomes `[-8, -3, 0, 7, 7, 12]`. The COM version uses the same signed exchange sort. Keep N equal to the declared number of words, and keep the code, array, and DOS stack within the shared 64 KiB segment without overlap. This is a stricter size limit than a separate EXE data segment.

[verify_com_templates.py](../verify_com_templates.py) checks the COM machine code, results, memory bounds, segment setup, stack balance, and DOS exit with FASM and Unicorn.

## Verification

[verify_sort_signed_words.py](verify_sort_signed_words.py) assembles the source's instruction sequence with Keystone and runs it in 16-bit Unicorn. It checks the resulting array, unchanged N, DOS termination, and unchanged memory surrounding the array.

Run with Python after making keystone-engine and unicorn available:

```text
python verify_sort_signed_words.py
```

The check substitutes explicit data addresses for the assembler's EXE directives. It verifies instruction execution, including DS initialization, but does not compile the native emu8086 EXE template.
