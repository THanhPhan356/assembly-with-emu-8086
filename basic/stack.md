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

## SS, DS, and Arrays

SS is the **Stack Segment register**. In 8086 real mode, a segment register and an offset together identify a memory location:

`physical address = segment * 16 + offset`

SS has a concrete 16-bit value. In a normal DOS EXE, the loader initializes SS:SP using the executable's stack information, and your procedure usually leaves SS unchanged. Its value is not a universal constant across programs or runs. DS must be initialized separately to access the program's data.

### Choosing the Segment for a Memory Access

| Memory operand | Segment used |
|---|---|
| `[bx]`, `[si]`, `[di]` | DS by default |
| `[bp]`, `[bp+4]` | SS by default |
| `ss:[bx+4]` | SS explicitly |

`SS:` is a **segment override**. It selects the segment for that memory access; it does not change SS or SP.

```asm
mov dx, ss:[bx+4]    ; Read a word from SS at offset BX + 4.
```

MOV reads a copy without removing anything from the stack. BX must already hold the intended offset; adding SS: does not turn an arbitrary value into a valid stack address.

If an array actually resides in the stack segment, access its elements using SS and their offsets. BP selects SS automatically; BX, SI, and DI require an explicit SS override for such accesses.

### A Data Array Whose Address Is Passed on the Stack

Suppose `ARR DW 2, 5, 8, 3` is declared in .DATA and DS has been initialized:

```asm
lea bx, ARR          ; BX receives the offset of ARR, not its first element.
mov dx, [bx]        ; Read DS:BX: DX = 2.
push bx             ; Push a copy of the offset; ARR stays in .DATA.
pop bx              ; Balance this standalone example's PUSH.
```

Pushing the offset does not move the array into the stack. In CountOdd, read the offset argument from SS, then use it to read the array elements from DS.

Loading the first element into AX gives AX the value 2, not an address. AX can hold an offset, but original 8086 addressing does not support `[ax]` or `[sp]`; use a legal address register such as BX or SI.

### Reading the Arguments Without BP

Assume the caller executes PUSH N, PUSH of ARR's offset, and a **near CALL**, in that order. At the start of the callee:

```asm
push bx
mov bx, sp          ; Keep a stable copy of SP in BX.
mov si, ss:[bx+4]   ; ARR's offset, stored on the stack.
mov cx, ss:[bx+6]   ; N, stored on the stack.
```

Here SS:[BX] holds saved BX and SS:[BX+2] holds the return IP. Later pushes do not change BX or these offsets. Read array elements through `[si]`, which selects DS by default. Undo any later pushes, restore BX with POP BX, and leave the return IP at the top before RET. Preserve SI and CX too if required by your register agreement.

### Do Not Change SS Just to Read Stack Data

`mov ss, 1` is invalid: MOV cannot load an immediate constant directly into a segment register. `mov ss, ax` is a valid instruction, but it changes the stack segment while leaving SP unchanged. A new segment with an unrelated SP can make PUSH, POP, CALL, or RET access the wrong memory. You do not need to change SS in this exercise.

Self-check: if SS = 2000h and BX = 0100h, `ss:[bx+4]` accesses physical address 20104h. The instruction `mov dx, ss:[bx+4]` leaves SS, BX, and SP unchanged.

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

## Byte Strings and Reversal with the Stack

LIFO (last in, first out) is also called FILO (first in, last out). Push the characters of `hello` from left to right, then pop them: they come out as `olleh`.

### What DB Declares

```asm
N dw 5
S db 'hello'
```

N is a two-byte count. S labels the beginning of five consecutive bytes containing ASCII character codes:

| Byte offset from S | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Character | h | e | l | l | o |
| Hexadecimal code | 68 | 65 | 6C | 6C | 6F |

There is no automatic string object, length field, or bounds check. This declaration adds neither a zero terminator nor a DOS `# Three Basic Ways to Use the 8086 Stack

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

## SS, DS, and Arrays

SS is the **Stack Segment register**. In 8086 real mode, a segment register and an offset together identify a memory location:

`physical address = segment * 16 + offset`

SS has a concrete 16-bit value. In a normal DOS EXE, the loader initializes SS:SP using the executable's stack information, and your procedure usually leaves SS unchanged. Its value is not a universal constant across programs or runs. DS must be initialized separately to access the program's data.

### Choosing the Segment for a Memory Access

| Memory operand | Segment used |
|---|---|
| `[bx]`, `[si]`, `[di]` | DS by default |
| `[bp]`, `[bp+4]` | SS by default |
| `ss:[bx+4]` | SS explicitly |

`SS:` is a **segment override**. It selects the segment for that memory access; it does not change SS or SP.

```asm
mov dx, ss:[bx+4]    ; Read a word from SS at offset BX + 4.
```

MOV reads a copy without removing anything from the stack. BX must already hold the intended offset; adding SS: does not turn an arbitrary value into a valid stack address.

If an array actually resides in the stack segment, access its elements using SS and their offsets. BP selects SS automatically; BX, SI, and DI require an explicit SS override for such accesses.

### A Data Array Whose Address Is Passed on the Stack

Suppose `ARR DW 2, 5, 8, 3` is declared in .DATA and DS has been initialized:

```asm
lea bx, ARR          ; BX receives the offset of ARR, not its first element.
mov dx, [bx]        ; Read DS:BX: DX = 2.
push bx             ; Push a copy of the offset; ARR stays in .DATA.
pop bx              ; Balance this standalone example's PUSH.
```

Pushing the offset does not move the array into the stack. In CountOdd, read the offset argument from SS, then use it to read the array elements from DS.

Loading the first element into AX gives AX the value 2, not an address. AX can hold an offset, but original 8086 addressing does not support `[ax]` or `[sp]`; use a legal address register such as BX or SI.

### Reading the Arguments Without BP

Assume the caller executes PUSH N, PUSH of ARR's offset, and a **near CALL**, in that order. At the start of the callee:

```asm
push bx
mov bx, sp          ; Keep a stable copy of SP in BX.
mov si, ss:[bx+4]   ; ARR's offset, stored on the stack.
mov cx, ss:[bx+6]   ; N, stored on the stack.
```

Here SS:[BX] holds saved BX and SS:[BX+2] holds the return IP. Later pushes do not change BX or these offsets. Read array elements through `[si]`, which selects DS by default. Undo any later pushes, restore BX with POP BX, and leave the return IP at the top before RET. Preserve SI and CX too if required by your register agreement.

### Do Not Change SS Just to Read Stack Data

`mov ss, 1` is invalid: MOV cannot load an immediate constant directly into a segment register. `mov ss, ax` is a valid instruction, but it changes the stack segment while leaving SP unchanged. A new segment with an unrelated SP can make PUSH, POP, CALL, or RET access the wrong memory. You do not need to change SS in this exercise.

Self-check: if SS = 2000h and BX = 0100h, `ss:[bx+4]` accesses physical address 20104h. The instruction `mov dx, ss:[bx+4]` leaves SS, BX, and SP unchanged.

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

 terminator; the program uses N to determine the length. Use DB for this byte string.

### S[SI] Uses a Byte Offset

`mov al, S[si]` reads one byte from DS at offset `OFFSET S + SI`. With SI = 0 it reads h; with SI = 1 it reads e. Since each character is one byte, increasing SI by 1 reaches the next character. For word arrays, consecutive elements are two bytes apart.

### Why PUSH Uses AX Rather Than AL

8086 cannot execute `push al` or `pop al`: these stack operations transfer words. Load a character into AL, push AX, later pop AX, and copy AL back to the string. Each saved character uses two stack bytes even though it uses one byte in S.

`mov ah, 0` is optional for this particular reversal. For example, AH = 12h and AL = 68h produce AX = 1268h. PUSH/POP preserves that word, and writing only AL still writes 68h, the code for h. Clearing AH makes AX easier to inspect, but does not change the reversed string. The high byte matters if a later operation uses AX as a complete number.

Use two passes: push all characters, reset SI and CX, then pop them into S from the beginning. A balanced sequence restores SP to its initial value.

Self-check: five characters use ten stack bytes at the deepest point. SI advances by one per character; PUSH decreases SP by two and POP increases it by two.

Complete exercise and solution: [Reverse a String Using the Stack](../example/reverse_string/README.md).

Related: [LEA and OFFSET](lea_offset.md), especially the difference between calculating an address and reading its contents.
