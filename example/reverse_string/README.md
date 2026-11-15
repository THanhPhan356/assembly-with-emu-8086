# Reverse a String Using the Stack

## Problem Statement

Given a string S containing N ASCII characters, with N >= 1, write a complete 8086 assembly program using the DOS EXE template.

Declare S and N in the data segment. Reverse the characters using PUSH and POP, and store the result directly in S. Step through the program in emu8086 and inspect SP, the stack, and S.

Example: N = 5 and S = `hello` must produce `olleh`. A one-character string must remain unchanged.

## Solution

[reverse_string_exe.asm](reverse_string_exe.asm)

The solution uses two simple loops:

1. PUSH_CHAR loads successive characters into AL and pushes AX.
2. Reset SI and CX, then POP_CHAR pops AX and writes AL back into S from the beginning.

LOOP decrements CX and branches while CX is nonzero. SI advances by one because S contains bytes; each PUSH/POP transfers two bytes.

The last character pushed is the first one popped: LIFO, also called FILO. Clearing AH is unnecessary here because only AL is written back. See [stack and byte-string notes](../../basic/stack.md#byte-strings-and-reversal-with-the-stack).

## Run in emu8086

Open the source, compile it as an EXE, select Emulate, and step through both loops. Inspect the five bytes at S before the DOS exit:

| State | S |
|---|---|
| Before | hello |
| After | olleh |

After the first loop, SP is ten bytes below its starting value. After the second loop, it is restored. The result is stored in memory; the program has no screen-output routine.

## Input Assumptions

N must be positive and equal the declared byte length of S. Update both declarations together. This counted string has no automatic zero or dollar terminator. The 256-byte stack must accommodate two bytes per character plus any other stack use; the supplied five-character input uses ten bytes.

This learning version assumes valid fixed input. N = 0 is unsupported: entering a LOOP body with CX = 0 would wrap the counter instead of skipping the loop.

## Verification

[verify_reverse_string.py](verify_reverse_string.py) uses Keystone and Unicorn to execute the source instruction sequence with resolved data addresses. It checks reversed bytes, unchanged N and surrounding memory, DS initialization, stack depth and balance, and DOS exit. Cases include the supplied word, one and two characters, repeated characters, a palindrome, spaces, an embedded zero byte, and a 100-byte input.

Run `python verify_reverse_string.py` with `keystone-engine` and `unicorn` available. This checks instruction execution; it does not compile a MASM/emu8086 EXE.
