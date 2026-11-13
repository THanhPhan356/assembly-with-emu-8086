# Exercise 3: Count the Set Bits of a 16-bit Integer

## Problem Statement (15 points)

Rewrite the following C function in 8086 assembly language. Pass the function argument through the stack and return the result in the accumulator register (AX).

```c
/* Count the number of 1 bits in a two-byte integer. */
int Count(int a)
{
    int s = 0;
    while (a != 0) {
        if ((a & 1) != 0)
            s++;
        a >>= 1;
    }
    return s;
}
```

## Provided Program Framework

The main program and the procedure use the following framework to pass an argument through the stack. Students only need to write the code at the marked placeholder.

```asm
.CODE
MAIN PROC
    ...
    PUSH N          ; Push the value of N onto the stack.
    CALL Count      ; Count the 1 bits in the two-byte integer N.
    POP N           ; Remove the argument from the stack after use.
    ...
MAIN ENDP

Count PROC
    PUSH AX         ; Also save any other registers used by the procedure.

    ; WRITE THE CODE THAT COUNTS THE 1 BITS HERE.

    POP AX          ; Also restore any other registers used by the procedure.
    RET
Count ENDP

END MAIN
```

This framework is reproduced from the assignment; it is not a completed solution.

## Additional Questions (2 points each)

a) How should the variable `N` be declared?

b) Inside the procedure, how can you access the value of `N` that was passed on the stack?

c) Can `POP N` be replaced with `POP AX`?

d) Are there ways to pass arguments other than through the stack?

e) When is it necessary to pass arguments through the stack?

## Source

English translation of Exercise 3 from *VXL_BaiTap Chuong2-3_CodeC.pdf* (Microprocessor Engineering Exercises, Assignment No. 3).
