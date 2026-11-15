# Three Basic Ways to Use the 8086 Stack

| Operation | Purpose | Main instructions/registers |
|---|---|---|
| Push and pop | Save and retrieve a word | PUSH, POP, SS:SP |
| Access by address | Read or change a word without removing it | MOV, BP, SS |
| Call and return | Save and recover the return address | CALL, RET, CS:IP |

The stack is memory, not a separate register. SS selects its segment; SP holds the offset of its current top. It follows **LIFO: last in, first out**.

The examples below are learning fragments, not complete programs. Assume SS:SP already identifies a valid, sufficiently large stack.

## 1. Save and Retrieve Data with PUSH and POP

For an ordinary word operand on 8086:

| Instruction | Steps |
|---|---|
| PUSH source | Subtract 2 from SP, then store the word at SS:SP |
| POP destination | Read the word at SS:SP into the destination, then add 2 to SP |

```asm
mov ax, 10
mov bx, 20
push ax
push bx
pop dx              ; DX = 20.
pop cx              ; CX = 10.
```

PUSH copies the value; it does not clear the source. POP can use a different destination register. It moves the stack top without erasing the old bytes in memory.

With initial SP = 0100h:

| After | SP | Logical stack, top first |
|---|---|---|
| PUSH AX | 00FEh | 10 |
| PUSH BX | 00FCh | 20, 10 |
| POP DX | 00FEh | 10 |
| POP CX | 0100h | Empty relative to the starting state |

On 8086, PUSH/POP operands are words, not AL or other byte registers. Immediate PUSH, such as `push 10`, is not an original 8086 instruction; load a register first.

To preserve several registers, pop them in the reverse order of their pushes. PUSHF/POPF similarly save and restore FLAGS.

## 2. Read or Write Stack Data Through BP

BP can provide a stable reference while PUSH and POP change SP. Memory operands that use BP select SS by default. Original 8086 addressing does not support `[sp]`.

Suppose the caller pushes one word argument and makes a **near CALL**. At procedure entry:

| Offset relative to entry SP | Word |
|---|---|
| +0 | Return IP |
| +2 | Argument |

Establish a frame while preserving the caller's BP:

```asm
push bp
mov bp, sp
```

The layout is now:

| Address | Word |
|---|---|
| SS:[BP] | Saved caller BP |
| SS:[BP+2] | Return IP |
| SS:[BP+4] | Argument |

```asm
mov ax, [bp+4]       ; Read a copy of the argument; SP is unchanged.
mov word ptr [bp+4], 7 ; Change the stack copy; SP is unchanged.
```

The caller's original variable is unchanged when its value was pushed: the argument is a copy. Restore BP with POP BP only after undoing any later pushes or local stack allocation.

The +4 offset depends on this exact frame and a near CALL. Far calls or extra saves before establishing BP change the layout.

## 3. Use CALL and RET for Procedures

A near CALL pushes the IP of the instruction **after CALL**, then transfers execution to the procedure. A matching near RET pops that IP and resumes the caller.

CALL is different from JMP: JMP does not save a return address.

```asm
push N              ; Copy a word argument onto the stack.
call Worker         ; Place the return IP above the argument.
add sp, 2           ; After RET, discard the argument without changing AX.
```

This is a caller fragment: N must be a word variable and Worker a near procedure. ADD changes arithmetic flags; here it preserves the result register AX.

Immediately after CALL, POP AX would retrieve the return IP, not N. Removing that address without restoring it would make RET return incorrectly. Use the BP frame above to access the argument.

RET removes the return address, not a plain value argument beneath it. Agree on one cleanup convention: the caller removes the argument here. Do not also remove it in the callee.

For comparison, a far CALL pushes CS and the return IP; the matching far return restores both. Its stack layout differs from the near-call diagrams above.

## Returning a Result and Preserving Registers

Decide which register carries the result, commonly AX. Preserve other registers as required by the caller/callee agreement.

If AX contains the result, restoring an older AX with POP AX destroys that result. Likewise, replacing the caller's cleanup with POP AX overwrites the returned AX with the argument.

Before RET, leave the correct return address at the stack top. Unbalanced pushes/pops or writing over SS:[BP+2] in the illustrated frame can corrupt the return path.

## Check Your Understanding

Starting with SP = 0100h, a caller pushes one word, makes a near CALL, and the callee executes PUSH BP / MOV BP, SP:

- SP and BP are 00FAh.
- SS:00FAh holds saved BP; SS:00FCh holds return IP; SS:00FEh holds the argument.
- Reading [BP+4] leaves SP at 00FAh.
- POP BP, then a near RET, leaves SP at 00FEh.
- The caller's ADD SP, 2 restores SP to 0100h.

These examples assume no intervening interrupt or additional stack use. Reading an empty stack or exceeding its reserved capacity is invalid; 8086 provides no automatic stack-bounds check.

Related: [LEA and OFFSET](lea_offset.md), especially the difference between calculating an address and reading its contents.
