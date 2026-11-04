# Average of Nonzero Signed Bytes

## Problem statement

Given a previously declared one-dimensional array of N signed one-byte integers, write an 8086 assembly program that computes the arithmetic mean of its nonzero elements. Store the result in AX.

The original exercise also asks for:

a. An algorithm flowchart.
b. Assembly code for emu8086.
c. A run using `N = 5` and `a DB 1,2,-3,0,4`, with the result displayed from emu8086.
d. An equivalent ARM Cortex-M4 or RISC-V assembly program, including tests.
e. An equivalent C function using this template:

```c
int count_average(char *a, int N) {
    /* Calculate c here. */
    return c;
}
```

f. An assembly implementation of that C function, including the calling sequence, tested with:

```c
char array[10] = {1, 3, 5, -1, 0, 2};
int n = 6;
int x;

x = count_average(array, n);
printf("%d", x);
```

The supplied exercise wrote `count_average(array, int N)` at the call site; the example above corrects that syntax. The original `char *` interface also needs signed-char semantics when implemented in C.

This folder currently contains the agreed 8086 `.COM` solution and its automated check. The other implementations and an actual emu8086 screen capture are not included.

## Program

Open [nonzero_average.asm](nonzero_average.asm) in emu8086, select **Emulate**, and step to `ket_thuc` before executing `RET`. Inspect AX; the program does not print to the screen.

The program follows the original direct array-loop style. It uses `ARR[si]` and has no procedure calls or explicit PUSH/POP instructions. A standard DOS `.COM` startup initializes DS to the program segment; the final RET uses the standard `.COM` startup stack.

| Name | Meaning | Size |
|---|---|---|
| `ARR` | Signed input elements | One byte per element |
| `N` | Number of elements to process | 16 bits |
| `tong` | Running sum | Signed 16 bits |
| `dem` | Number of nonzero elements | 16 bits |
| `SI` | Current element index | 16 bits |
| `AX` | Signed integer average | 16 bits |

For each nonzero element, CBW sign-extends AL into AX before addition. After the loop, CWD sign-extends the sum into DX:AX, then IDIV BX leaves the quotient in AX and the remainder in DX. Integer division truncates toward zero.

For the supplied array, the sum is `4` and the nonzero count is `4`, so **AX = 0001h**. By convention, an empty array or an array containing only zeros returns AX = 0; the exercise does not specify this case.

## Limits and validation

Keep N consistent with the array length, use `0 <= N <= 32767`, and keep every running sum within `-32768..32767`. The array, code, data and startup stack must fit the `.COM` segment. The program assumes valid declarations and does not detect overflow.

[verify_nonzero_average.py](verify_nonzero_average.py) assembles the source instructions with FASM after translating emu8086 variable operands into FASM memory syntax, then executes the resulting 16-bit machine code with Unicorn. Set `FASM` to the assembler executable if it is not on PATH, install the Python `unicorn` package, and run:

```text
python verify_nonzero_average.py
```

The check covers the supplied array, negative values, signed-byte endpoints, positive and negative fractional averages, zero count, and both signed 16-bit sum endpoints. It inspects AX, the sum, the nonzero count and the unchanged input array before the final RET. It does not validate the emu8086 application or DOS termination.
