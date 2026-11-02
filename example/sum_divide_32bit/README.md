# Midterm Exercise 2: Summing Four 32-bit Numbers and Dividing by 1000

This lesson explains the supplied 8086 program, from its EXE declarations to its arithmetic failure. It records the questions, misunderstandings, and corrections discussed while reading the code.

**Intended operation:** interpret eight words as four unsigned 32-bit numbers, add those numbers, divide the sum by 1000, and save the quotient. The source contains no keyboard-input or result-printing routine.

**Actual behavior with the supplied data:** the sum exceeds 32 bits, and the subsequent division produces a quotient that cannot fit in AX. A divide error occurs before the quotient is saved. The source is preserved for study; these defects have not been silently repaired.

## Files and Assignment Scope

| File | Purpose |
|---|---|
| [sum_divide.asm](sum_divide.asm) | Original exercise program, with declarations and procedure directives formatted on separate lines |
| [verify_sum_divide.py](verify_sum_divide.py) | Reproducible arithmetic checks and execution of a FASM-compatible 16-bit MZ EXE with Unicorn |
| This README | Explanations, detailed corrections, loop trace, and overflow diagnosis |

The original assignment requests: (a) instruction-by-instruction register and variable tracing, including a table after each loop iteration; (b) a corresponding flowchart; and (c) corresponding C code. Its general submission instructions require one `MSSV_VXL_GK.docx`, code as editable text, and results obtained using emu8086 or another tool.

This checkpoint records the lesson and diagnostic trace. A dedicated flowchart, C translation, and final Word submission have not been created here.

## 1. Why This Source Looks Different from a COM Program

The instructions still target the 8086. The difference is the program format and organization, not a different CPU or a different meaning of `MOV`, `ADD`, or `DIV`.

| Earlier COM examples | This EXE example |
|---|---|
| Use `org 100h` | Use `.MODEL SMALL`, `.STACK`, `.DATA`, and `.CODE` |
| Code and data normally share a segment | Code and data are organized into separate segments |
| DS is normally initialized suitably by the DOS COM loader or emulator | The program explicitly initializes DS for its data segment |
| A near `RET` can terminate a simple COM program when the initial stack arrangement is intact | This source requests DOS termination with `AH=4Ch` and `INT 21h` |

`org 100h` describes the expected load offset to the assembler; it is not a CPU instruction. Likewise, the EXE directives below organize the program for the assembler and linker.

### Declarations are not instructions that the CPU executes first

**Initial misunderstanding:** the CPU might execute all declarations and then jump down to `.CODE`.

**Correction:** the assembler processes the declarations when building the executable. The loader places the program in memory and initializes its execution state. `END MAIN` tells the assembler/linker which entry point to record; execution starts at the first instruction of `MAIN`, not by running `.DATA` and then jumping over it.

`.CODE` is a directive marking the code section. It is not a jump instruction.

```asm
.MODEL SMALL    ; One code segment and one data segment, each up to 64 KiB
.STACK 100h     ; Reserve 100h = 256 bytes for the stack
.DATA           ; Begin data declarations
```

The stack supports operations such as `PUSH`, `POP`, `CALL`, and `RET`. Declaring stack space does not itself perform those operations.

### MAIN is a chosen name; PROC is a directive

```asm
MAIN PROC
    ; CPU instructions
MAIN ENDP

END MAIN
```

- `MAIN` is a programmer-chosen procedure name.
- `PROC` means procedure and starts its definition.
- `ENDP` ends the procedure definition for the assembler.
- `END MAIN` ends the source module and specifies the entry point.

**Initial misunderstanding:** `MAIN PROC`, or the word `PROC` alone, might automatically tell the CPU where to start.

**Correction:** procedure definition and entry-point selection are separate. `PROC` and `ENDP` are not CPU instructions. `ENDP` does not generate a return or terminate the program. An ordinary called procedure needs an actual `RET` instruction; this entry procedure instead contains a DOS exit request.

The procedure could be named `MAIN_1` if the relevant references are changed consistently:

```asm
MAIN_1 PROC
    ; Instructions
MAIN_1 ENDP

END MAIN_1
```

This is a naming illustration, not a complete runnable program. The COM examples did not need a `MAIN PROC` declaration, so it is not a universal requirement for all Assembly source.

## 2. What the Data Declarations Allocate

```asm
NUMBERS DW 10A0h, 20E0h
        DW 30B0h, 40F0h
        DW 50C0h, 6000h
        DW 70D0h, 8000h
```

`DW` means Define Word. Each value occupies one 16-bit word, or two bytes. Commas allow multiple values in one declaration, and the following unnamed `DW` lines continue allocating data directly after the previous line. Line breaks do not create separate arrays.

There are eight words, occupying sixteen bytes. A suffix `h` denotes hexadecimal notation; for example, `03E8h` means decimal 1000.

### Is NUMBERS a variable, an array, or a label?

**Initial question:** how can one name declare so many values? Is it one variable or a label?

**Correction:** `NUMBERS` is a data label naming the beginning of the allocated words. For this program, it is useful to treat the storage as an array of eight 16-bit elements. The assembler also associates the label with its declared word type.

The label does not allocate an additional pointer variable containing the array's address. It names the location itself. The CPU does not receive a separate array object with an automatic length or bounds check.

| Location relative to NUMBERS | Stored word |
|---|---|
| `NUMBERS + 0` | `10A0h` |
| `NUMBERS + 2` | `20E0h` |
| `NUMBERS + 4` | `30B0h` |
| `NUMBERS + 6` | `40F0h` |
| `NUMBERS + 8` | `50C0h` |
| `NUMBERS + 10` | `6000h` |
| `NUMBERS + 12` | `70D0h` |
| `NUMBERS + 14` | `8000h` |

The values in the right column are data, not addresses. For example, the first location contains `10A0h`; its address is not necessarily `10A0h`.

### Two words are treated as one 32-bit number by this program

**Initial misunderstanding:** `DW 10A0h, 20E0h` might inherently declare one 32-bit number, with the first word being the high half.

**Correction:** the declaration itself allocates two words. The later instructions decide to interpret each pair as one 32-bit value, with the low word first and the high word second:

```asm
MOV AX, [SI]       ; First word: added to SUM_LOW
ADD SUM_LOW, AX
MOV AX, [SI+2]     ; Second word: added to SUM_HIGH
ADC SUM_HIGH, AX
```

Thus the first pair means:

```text
Stored word order:       10A0h, 20E0h
Role in this program:     low   high
Numeric 32-bit value:      20E010A0h
```

| Pair | Low word | High word | Unsigned 32-bit value |
|---|---|---|---|
| 1 | `10A0h` | `20E0h` | `20E010A0h` |
| 2 | `30B0h` | `40F0h` | `40F030B0h` |
| 3 | `50C0h` | `6000h` | `600050C0h` |
| 4 | `70D0h` | `8000h` | `800070D0h` |

The lower-addressed word is the low half in this representation. Do not assume that every pair of values following `DW` must form a 32-bit number; inspect how the code uses them. The unsigned interpretation here follows the use of unsigned `DIV`, not signed `IDIV`.

### Remaining variables and initial values

| Name | Allocation | Initial value | Intended role |
|---|---|---|---|
| `DIVISOR` | One word | `03E8h`, decimal 1000 | Divisor |
| `SUM_LOW` | One word | 0 | Low sixteen bits of the accumulated sum |
| `SUM_HIGH` | One word | 0 | High sixteen bits of the accumulated sum |
| `QUOTIENT_LOW` | One word | 0 | Intended low word of the saved quotient |
| `QUOTIENT_HIGH` | One word | 0 | Intended high word of the saved quotient |

The data declarations occupy 16 + 5 x 2 = 26 bytes, excluding any segment padding. `LOW` and `HIGH` are naming conventions. The CPU does not automatically combine or calculate variables merely because their names contain those words.

For example, a conceptual 32-bit sum is reconstructed as:

```text
SUM = SUM_HIGH * 65536 + SUM_LOW
```

These declarations initialize storage in the loaded program. Later `MOV SUM_LOW, 0` and `MOV SUM_HIGH, 0` are executable instructions that reset the sum at runtime.

## 3. AX, DS, and the Address of the Data Segment

```asm
MOV AX, @DATA
MOV DS, AX
```

### What @DATA means, and whether it can be renamed

`@DATA` is a predefined assembler symbol in this source dialect. It represents the segment value for the program's data group. It is not a CPU register, an instruction, an array element, or a symbol supplied by the physical CPU.

**Initial misunderstanding:** because `MAIN` can be renamed, `@DATA` might also be freely changed to `@DATA_1`.

**Correction:** `MAIN` is a user-defined label. `@DATA` is an assembler-provided symbol with a defined meaning. The assembler does not automatically define `@DATA_1`. A separately declared segment or alias is a different topic; simply changing the spelling here does not create one.

### DS is a register, but its role differs from AX, BX, and CX

All four registers are sixteen bits wide, but their roles differ:

| Register | Role in this lesson |
|---|---|
| `AX` | General-purpose arithmetic/data register; temporary holder of the data-segment value during initialization |
| `BX` | General-purpose register, also usable for certain addressing forms; unused by this source |
| `CX` | Loop counter initially, then the divisor register |
| `DS` | Data-segment register used to locate the program's data |

For example, `ADD AX, BX` is an arithmetic instruction, whereas `ADD DS, 1` is not a valid 8086 instruction.

### MOV DS, AX copies a value; it does not dereference AX

**Initial misunderstanding:** DS might receive whatever data is stored at an address that AX points to.

**Correction:** `MOV DS, AX` copies the sixteen-bit contents of AX directly into DS. There are no memory brackets around AX and no data-memory read in this instruction.

For an illustrative segment value:

```text
Before MOV DS, AX: AX = 2000h
After  MOV DS, AX: AX = 2000h, DS = 2000h
```

AX is unchanged. The number `2000h` is illustrative; the actual segment value depends on loading and relocation, so the trace does not assume a universal value for `@DATA`.

### Why AX is used as an intermediate register

**Initial misunderstanding:** DS might be the intermediate register, or using an intermediate register by itself might prevent wrong memory accesses.

**Correction:** AX is the intermediate register. The 8086 does not provide a form that loads an immediate constant directly into DS, so `MOV DS, @DATA` is not the valid replacement for these two instructions. First load the value into AX, then copy it into DS.

These are two separate ideas:

1. The intermediate AX is needed because of the available instruction forms.
2. Initializing DS to the correct segment is what makes later default data accesses use the intended data region.

### Why the instructions matter even though they do not calculate anything

Think of `.DATA` as a cabinet containing compartments named `NUMBERS`, `SUM_LOW`, and so on. DS selects the cabinet; a variable's offset identifies its compartment. Setting DS tells the CPU where the relevant cabinet is.

**Initial misunderstanding:** without these two lines, the CPU would be completely unable to access memory.

**Correction:** the CPU could still access memory, but an incorrectly initialized DS could direct it to the wrong segment. It might read or overwrite unrelated locations without a useful error message. In a normal DOS EXE startup, DS initially refers to the program's PSP rather than automatically to its declared data segment. This source therefore initializes DS explicitly.

The exact two-line sequence is not universally required if equivalent setup has already occurred. In this standalone EXE, it is the appropriate initialization. The COM examples worked differently because their usual loader initialization and shared segment made this explicit setup unnecessary.

Neither of these two instructions copies the array into a register. For a later `MOV SUM_LOW, 0`, DS selects the data segment and the assembler-supplied offset identifies `SUM_LOW` within it.

## 4. LEA, SI, Addresses, and Values

```asm
MOV SUM_LOW, 0
MOV SUM_HIGH, 0
LEA SI, NUMBERS
MOV CX, 4
```

The first two instructions reset the two words of the sum. `LEA` initializes the position used to read the array. CX is set to four because the loop processes four pairs of words.

### LEA loads an effective address, not the contents at that address

`LEA` means Load Effective Address. Here, `LEA SI, NUMBERS` puts the offset of `NUMBERS` into SI. It does not put the first array value `10A0h` into SI, and it does not read the array's contents.

**Initial misunderstanding:** `LEA` might load the array's first value, or its syntax might be another declaration.

**Correction:** this is an executable instruction that calculates/loads an offset. The later `MOV AX, [SI]` performs the data read. SI holds the position within the segment selected by DS; SI alone is not the whole segment-and-offset address.

```text
DS selects the data segment.
SI identifies the current position within that segment.

SI ---> [10A0h] [20E0h] [30B0h] [40F0h] ...
```

In this use, SI acts as a pointer: it indicates where the data is rather than holding the data value itself. It is still an ordinary register; `LEA` does not create a separate pointer object in memory.

### What the brackets in MOV AX, [SI] mean

```asm
MOV AX, [SI]
```

The brackets request the memory contents at the effective address. With SI pointing to `NUMBERS`, the instruction reads the first word into AX, so AX becomes `10A0h`.

AX is sixteen bits wide, so the operation reads one word: two bytes. It does not move the pointer or modify the source data.

| Expression or instruction | Meaning |
|---|---|
| `SI` | The offset held in the register |
| `[SI]` | Data at DS:SI for this addressing form |
| `MOV AX, SI` | Copy the offset value into AX |
| `MOV AX, [SI]` | Read a sixteen-bit value from memory into AX |
| `LEA SI, NUMBERS` | Put the array's starting offset into SI |

**Initial impression:** `[SI]` looked partly like array syntax and partly like a declaration.

**Correction:** it is a memory operand in an instruction. C array indexing also ultimately selects memory, but brackets here neither allocate an array nor declare a variable.

### [SI+2] reads elsewhere without changing SI

```asm
MOV AX, [SI]       ; Read the word containing 10A0h
MOV AX, [SI+2]     ; Read the word containing 20E0h
```

**Initial misunderstanding:** `[SI+2]` might permanently advance SI by two.

**Correction:** the CPU uses SI + 2 as the offset for that read; SI itself remains unchanged. By contrast, `ADD SI, 2` actually changes the register.

The offset is measured in bytes, not bits. Two bytes equal one word. The start addresses of the words containing `10A0h` and `20E0h` differ by two bytes; the hexadecimal values themselves are not the addresses being advanced.

### ADD SI, 4 advances by four bytes, not four words

**Initial misunderstanding:** advancing by four might mean four array elements, or perhaps only two numerical addresses because two `DW` values are crossed.

**Correction:** the 8086 memory used here is byte-addressed. Increasing an offset by four advances four address units: four bytes, which equal two sixteen-bit array elements.

For illustrative offsets:

| Byte locations | Word stored there |
|---|---|
| `0100h`–`0101h` | `10A0h` |
| `0102h`–`0103h` | `20E0h` |
| `0104h`–`0105h` | `30B0h` |
| `0106h`–`0107h` | `40F0h` |

If SI starts at `0100h`, `ADD SI, 4` makes it `0104h`. It now points to `30B0h`, the low word of the second 32-bit number. The example offsets illustrate the spacing; they are not the actual `NUMBERS` offset in every EXE.

```text
First 32-bit number       Second 32-bit number
[10A0h] [20E0h]           [30B0h] [40F0h]
 ^                        ^
 SI before                SI after ADD SI, 4
```

This is pointer arithmetic, not a control-flow jump. The instruction changes SI; it does not change the array values or jump to another instruction.

## 5. The Addition Loop and Its Stopping Condition

```asm
LOOP_SUM:
    MOV AX, [SI]
    ADD SUM_LOW, AX
    MOV AX, [SI+2]
    ADC SUM_HIGH, AX
    ADD SI, 4
    LOOP LOOP_SUM
```

`LOOP_SUM` is a chosen instruction label, not a variable, procedure declaration, or special keyword. It gives the branch a destination.

### One iteration adds one 32-bit number

| Instruction | Effect |
|---|---|
| `MOV AX, [SI]` | Read the current low word |
| `ADD SUM_LOW, AX` | Add it to the low sum word; set CF if this addition carries past bit 15 |
| `MOV AX, [SI+2]` | Read the current high word without changing CF |
| `ADC SUM_HIGH, AX` | Add the high word and the incoming carry to the high sum word |
| `ADD SI, 4` | Advance to the next pair of words |
| `LOOP LOOP_SUM` | Decrement CX and branch back if the new CX is not zero |

**Initial understanding to refine:** the program adds the first word to LOW and the second to HIGH, then moves to the next pair.

That is correct, with one essential detail: `ADC` also includes the carry from the low-word addition. Without that carry, the two independent additions would not implement a correct multiword sum when the low half wraps.

```text
ADD: destination = destination + source
ADC: destination = destination + source + incoming CF
```

For example, low `FFFFh + 1` produces low `0000h` and CF = 1. The high-word operation must add that extra 1. The intervening `MOV` is safe because it does not alter the carry flag.

The high-word `ADC` can itself produce a carry beyond the whole 32-bit sum. That is a separate overflow, discussed below. `ADD SI, 4` changes arithmetic flags, so the high carry must be examined before that instruction if it is to be detected or saved.

### LOOP has an implicit counter update

**Initial misunderstanding:** no explicit comparison or decrement appeared, so there seemed to be no stopping condition.

**Correction:** on the 8086, `LOOP` implicitly decrements CX, then jumps if CX is nonzero. It does not need a preceding `CMP` for this condition.

```text
Before the loop: CX = 4
After iteration 1: CX = 3 -> branch back
After iteration 2: CX = 2 -> branch back
After iteration 3: CX = 1 -> branch back
After iteration 4: CX = 0 -> continue below the loop
```

`LOOP` leaves the status flags unchanged. Later `MOV CX, DIVISOR` deliberately replaces the finished loop count with 1000; CX is not permanently dedicated to one role.

### Observed state after each iteration

All hexadecimal values in this table are words. The carry columns refer to the flags immediately after the low `ADD` and high `ADC`, respectively, before pointer arithmetic changes them. SI is shown relative to the start of `NUMBERS`.

| Iteration | Low word read | High word read | SUM_HIGH | SUM_LOW | AX after the high-word read | SI after advancing | CX after LOOP | Low carry | High carry |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `10A0h` | `20E0h` | `20E0h` | `10A0h` | `20E0h` | `NUMBERS + 4` | 3 | 0 | 0 |
| 2 | `30B0h` | `40F0h` | `61D0h` | `4150h` | `40F0h` | `NUMBERS + 8` | 2 | 0 | 0 |
| 3 | `50C0h` | `6000h` | `C1D0h` | `9210h` | `6000h` | `NUMBERS + 12` | 1 | 0 | 0 |
| 4 | `70D0h` | `8000h` | `41D1h` | `02E0h` | `8000h` | `NUMBERS + 16` | 0 | 1 | 1 |

After the fourth iteration, SI is one byte position past the array's last occupied byte, or one-past-the-end of the sixteen-byte array. There is no fifth array read because CX has become zero. DS and the input words are unchanged by the loop.

## 6. Preparing and Performing the Division

```asm
MOV DX, SUM_HIGH
MOV AX, SUM_LOW
MOV CX, DIVISOR
DIV CX
```

The first two instructions copy the sum from memory into a register pair:

```text
32-bit dividend = DX * 65536 + AX
                 high word    low word
```

DX is loaded because AX alone cannot hold a 32-bit dividend. CX receives the value stored in `DIVISOR`, namely 1000. This is not an average of the four input numbers: the divisor is 1000, not four.

### The divisor operand determines the DIV form

**Initial misunderstanding:** `DIV CX` might divide AX alone and put the quotient in AH and the remainder in AL.

**Correction:** this confuses both the operand width and the result order. Unsigned `DIV` has these forms:

| Instruction example | Divisor width | Dividend | Quotient | Remainder |
|---|---|---|---|---|
| `DIV BL` | 8 bits | `AX`, sixteen bits | `AL`, eight bits | `AH`, eight bits |
| `DIV CX` | 16 bits | `DX:AX`, thirty-two bits | `AX`, sixteen bits | `DX`, sixteen bits |

Even for byte division, the quotient goes to AL and the remainder to AH, not the other way around. Here CX is a word register, so the second row applies.

The colon in `DX:AX` describes concatenating the high and low register halves; it does not mean dividing DX by AX.

**Further distinction:** this register pairing is a rule of the word-divisor `DIV` instruction. It does not mean that every 32-bit operation on an 8086 must always use DX:AX, or that a 32-bit dividend implies a 32-bit quotient.

### Division overwrites the input registers

**Initial concern:** if the sum is in DX and AX, will the quotient and remainder overwrite it?

**Yes, on successful division.** The roles change:

```text
Before DIV CX: DX = high half of dividend; AX = low half
After  DIV CX: DX = remainder;             AX = quotient
```

For a valid example, DX = 0, AX = 10, and CX = 3 become AX = 3 and DX = 1.

The memory variables `SUM_HIGH` and `SUM_LOW` are unchanged, because the earlier `MOV` instructions copied their values into registers. They did not transfer ownership or erase the source storage.

These result rules assume the division succeeds. After a divide error, do not interpret AX and DX as a valid quotient/remainder pair.

## 7. Saving the Quotient and Ending the Program

```asm
MOV QUOTIENT_LOW, AX
MOV QUOTIENT_HIGH, 0

MOV AH, 4Ch
INT 21h
MAIN ENDP
```

If division succeeds, `MOV QUOTIENT_LOW, AX` saves the sixteen-bit quotient. The next instruction writes zero into its intended high word. That represents a zero-extended quotient:

```text
QUOTIENT_HIGH : QUOTIENT_LOW
    0000h    : quotient formerly in AX
```

**Potential misunderstanding:** the presence of a `QUOTIENT_HIGH` variable might imply that `DIV CX` also calculates the high half of a larger quotient.

**Correction:** it does not. `DIV CX` returns only a sixteen-bit quotient in AX. Assigning zero to another variable cannot extend the hardware quotient capacity or rescue a division that has already failed. For the supplied data, neither quotient store is reached; both variables remain at their declared initial zero values in the controlled test. Those zeros are not a computed answer.

DX would contain the remainder after a successful division, but this program does not save it to a variable and does not print it.

`MOV AH, 4Ch` selects the DOS terminate-process service, and `INT 21h` invokes it. Setting AH changes the upper byte of AX; that would be safe for the saved quotient because AX has already been copied into memory. AL supplies the DOS exit status; this exact source does not explicitly set AL to zero.

`MAIN ENDP` is only the assembler's procedure-ending directive, not the instruction that exits. `END MAIN`, below it in the source, supplies the module entry-point information. For this dataset, the normal save-and-exit sequence is not reached because division fails first.

## 8. Why the Supplied Data Overflows: Two Separate Defects

These are defects in the supplied exercise program with its given inputs, separate from the learning misunderstandings above. They are not a syntax error caused by choosing the EXE template.

### Defect 1: the exact sum needs 33 bits, but storage has only 32

```text
   20E010A0h
 + 40F030B0h
 + 600050C0h
 + 800070D0h
 ------------
  141D102E0h
```

Two sixteen-bit sum words can hold at most `FFFFFFFFh`. The exact sum, `141D102E0h`, is greater than that and needs 33 bits. The leading hexadecimal `1` is outside the available 32-bit result.

The last iteration shows exactly where the lost bit appears:

```text
Low addition:  9210h + 70D0h     = 102E0h
Stored low:                       02E0h, incoming carry to high = 1

High addition: C1D0h + 8000h + 1 = 141D1h
Stored high:                      41D1h, outgoing carry beyond 32 bits = 1
```

The code correctly propagates the low-word carry with `ADC`. Its defect is failing to preserve or report the new carry out of the high-word addition. `ADD SI, 4` then updates the flags before the source checks that carry; in fact, no such check exists.

Consequently, the stored pair is:

```text
SUM_HIGH:SUM_LOW = 41D1h:02E0h = 41D102E0h
```

That is the exact sum modulo `2^32`, not the full mathematical sum. The low-word carry itself is not an error: it is expected and handled. The unhandled carry beyond the high word is the actual 32-bit overflow.

### Defect 2: the quotient still does not fit in AX

Even after that truncation, the dividend presented to `DIV CX` is too large for a sixteen-bit quotient:

```text
DX = 41D1h
AX = 02E0h
CX = 03E8h = 1000

41D102E0h = 1,104,216,800
1,104,216,800 / 1000 = 1,104,216 remainder 800
```

The largest unsigned value in AX is `FFFFh`, or 65,535. The required quotient, 1,104,216, exceeds that limit. The CPU signals a divide error, interrupt type 0, instead of silently storing the low sixteen quotient bits and continuing.

An additional quick check for unsigned word division with a nonzero divisor is `DX >= divisor`: that guarantees quotient overflow. Here `41D1h > 03E8h`, so the division cannot succeed. This test follows from `DX:AX = DX * 65536 + AX`; if DX is already at least the divisor, the quotient is at least 65,536 before considering AX.

The value 800 above is the mathematical remainder of the truncated dividend. It is not a valid observed remainder returned by the faulting DIV instruction.

The divisor is not zero, so division by zero is not the cause. The problem is the quotient width.

### Why a partial fix is insufficient

Preserving the 33rd sum bit alone would not make the existing `DIV CX` capable of returning a larger quotient. Conversely, using a wider-quotient division strategy would not restore the sum bit already lost by the original accumulation.

A corrected implementation would need to address both the sum width and quotient width, or explicitly detect and reject values that exceed its chosen widths. Such a replacement is not included in this checkpoint; the original program is retained to make the diagnosis traceable.

## 9. How to Inspect It and What Has Actually Been Verified

### Manual inspection in emu8086

1. Select **File -> New -> exe template**.
2. Replace the template contents with [sum_divide.asm](sum_divide.asm), then save it as an `.asm` file.
3. Select **Compile and Emulate** and use **Single Step** to inspect each instruction.
4. Watch DS initialization, SI, CX, and the two sum variables through all four iterations. Compare with the loop table above. Inspect CF immediately after the relevant ADD or ADC; pointer arithmetic changes the flags afterward.
5. Immediately before `DIV CX`, verify DX = `41D1h`, AX = `02E0h`, and CX = `03E8h`.
6. Expect a division error rather than a saved quotient. Do not report the initial zero quotient variables as a successful result.

The source does not print numerical results. Register and variable inspection is required; compiling an EXE successfully does not prove that its arithmetic can finish.

### Reproducible check performed for this checkpoint

[verify_sum_divide.py](verify_sum_divide.py) compiles a FASM-compatible version as a 16-bit MZ EXE, applies its relocation entries when loading it into Unicorn, and starts execution at the EXE's recorded entry point. The adapter translates the MASM-style segment/procedure directives and memory-operand syntax; the original instructions and data are preserved.

The check verifies:

- All four 32-bit interpretations and the exact sum `141D102E0h`.
- The truncated stored sum `41D102E0h` and its mathematical quotient/remainder.
- Actual sum words, AX, SI, and CX after all four machine-code loop iterations.
- Both the low and high carries, including the two carries in iteration four.
- The register inputs to DIV and the divide-error interrupt 0.
- The preserved sum variables and the unreached quotient stores.

Run it with Python, FASM, and the Python `unicorn` package available:

```sh
python verify_sum_divide.py
```

Set the `FASM` environment variable to the compiler executable if it is not on PATH.

The check passed and reproduced the expected fault. **The source has not been compiled or run in the emu8086 application during this checkpoint.** The test validates the arithmetic and machine-code behavior of the adapted EXE; it does not claim to validate emu8086's own compiler, loader, or error dialog.
