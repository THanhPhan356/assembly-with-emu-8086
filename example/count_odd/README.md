# Exercise 3 (Variant): Count Odd Elements in an Array

## Problem Statement

Rewrite the following C function in 8086 assembly language. Pass the function arguments through the stack and return the result in AX.

Each array element is a two-byte signed integer. Assume that `0 <= n <= the number of elements in the array`.

```c
/* Count the odd elements in an array. */
int CountOdd(int a[], int n)
{
    int i, s = 0;
    for (i = 0; i < n; i++) {
        if ((a[i] & 1) != 0)
            s++;
    }
    return s;
}
```

For example, for `A = {2, 5, 8, 3}` and `n = 4`, the function returns `2`. If `n = 0`, it returns `0`.

## Instructions (15 points)

Write a complete `.EXE` program with `.MODEL`, `.STACK`, `.DATA`, and `.CODE`. Initialize DS and terminate the program using a DOS service. Declare the array `A` and the variable `N` with predefined values; keyboard input and output are not required yet.

Complete the missing parts of the main program and procedure below. Pass **the offset address of A in DS and the value of N through the stack**. The caller must remove the arguments from the stack after the function returns, while preserving the result in AX.

```asm
.CODE
MAIN PROC
    ...                 ; Initialize DS.
    ...                 ; Pass the two arguments through the stack.
    CALL CountOdd
    ...                 ; Remove the arguments, keeping the result in AX.
    ...                 ; Terminate the program.
MAIN ENDP

CountOdd PROC
    ...                 ; Save the registers that must be preserved.
    ; WRITE THE CODE THAT COUNTS THE ODD ELEMENTS HERE.
    ...                 ; Restore the saved registers.
    RET
CountOdd ENDP

END MAIN
```

## Additional Questions (2 points each)

a) How should the array `A` and the variable `N` be declared?

b) Why pass the address of the array instead of pushing each element onto the stack?

c) Inside the procedure, how can BP be used to access the two arguments on the stack?

d) When moving from `A[i]` to `A[i+1]`, by how many bytes must the address increase? Why?

e) After `CALL CountOdd`, can `POP AX` be used to remove an argument from the stack while keeping the result in AX?

## Source

English translation of *Bai_tap_8086_CountOdd.pdf*, a Microprocessor Engineering practice exercise on arrays and the stack.
