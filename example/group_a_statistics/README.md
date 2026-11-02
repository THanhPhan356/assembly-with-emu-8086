# Classifying Eight Digits: Groups A, B, and C Statistics

## Original Problem Statement

Read eight integers from the keyboard, each between 0 and 9, and store them in `ARR[0..7]`. Classify each value into exactly one group:

| Group | Condition | Possible values |
|---|---|---|
| A | Divisible by 3 | 0, 3, 6, 9 |
| B | Odd and not divisible by 3 | 1, 5, 7 |
| C | Even and not divisible by 3 | 2, 4, 8 |

For each group, calculate, in this order:

1. Number of elements.
2. Sum of the elements.
3. Maximum value.
4. Minimum value.

Print all twelve results on one line, separated by a single space:

```text
A1 A2 A3 A4 B1 B2 B3 B4 C1 C2 C3 C4
```

The assignment also asks for a flowchart, detailed variable descriptions, and corresponding Assembly and C implementations using the same variable names and structure. Test both implementations with your own input. The flowchart does not need to show the details of input and output.

## Current Checkpoint

[group_a_statistics.asm](group_a_statistics.asm) implements keyboard input and the four statistics for **groups A, B, and C**. It preserves the variable names and control flow used during the lesson. Result printing, the flowchart, and the C version are not implemented in this checkpoint.

| Variable | Meaning |
|---|---|
| `ARR` | Eight numeric values, stored as bytes |
| `soluong` | Number of values in group A |
| `tong` | Sum of values in group A |
| `max` | Maximum value in group A |
| `min` | Minimum value in group A |
| `soluong_B` | Number of values in group B |
| `tong_B` | Sum of values in group B |
| `max_B` | Maximum value in group B |
| `min_B` | Minimum value in group B |
| `soluong_C` | Number of values in group C |
| `tong_C` | Sum of values in group C |
| `max_C` | Maximum value in group C |
| `min_C` | Minimum value in group C |

The program divides each value by 3 and checks the remainder in `AH`. It reloads the original value before adding to `tong`, because `DIV BL` overwrites `AL` with the quotient. Group A updates only its own statistics. A second pass resets `SI` to zero and selects group B by checking for an odd remainder after division by 2, then a nonzero remainder after division by 3. Reloading `ARR[si]` before each division is necessary because `DIV BL` overwrites `AL`. Group B uses separate statistics and leaves the array and group A results unchanged. A third pass resets `SI = 0` and initializes the group C statistics, including `min_C = 9`. It keeps even values not divisible by 3 (2, 4, and 8), using separate `_C` variables and the same update structure. A byte is sufficient for each result: the count is at most 8 and the sum is at most 72.

## Group B: Mistakes and Explanations from the Lesson

### Reload the original value after DIV

The first attempt divided by 2 and then divided by 3 without reloading `AL`. After `DIV BL`, `AL` holds the quotient and `AH` holds the remainder; neither preserves the original number. For example, dividing 7 by 2 leaves `AL = 3`, so another division would test 3 instead of 7.

Reload `AL` from `ARR[si]` and clear `AH` before testing division by 3. Reload `AL` again before adding to the sum or comparing extrema. `DIV` changes registers, not the array.

### Skip numbers divisible by 3

The first attempt used `JNE next_B` after testing the remainder from division by 3. That skipped the values group B should keep.

Group B requires **both** an odd value **and** a value not divisible by 3. Thus 3 and 9 belong only to group A, while group B contains 1, 5, and 7. Use:

```asm
cmp ah, 0
je next_B              ; Remainder zero: divisible by 3, so skip it.
```

### Match CMP operand order to the conditional jump

`CMP left, right` sets flags as if subtracting `right` from `left`, without changing either operand. The following jump interprets those flags, so swapping operands requires changing the jump too.

| First attempt | Problem | Correct pair |
|---|---|---|
| `cmp max_B, al` then `jbe max_done_B` | Skips when the old maximum is less than or equal to the new value, which is when an update may be needed | `cmp al, max_B` then `jbe max_done_B` |
| `cmp min_B, al` then `jge min_done_B` | Skips when the old minimum is greater than or equal to the new value, which is when an update may be needed | `cmp al, min_B` then `jge min_done_B` |

Example: with `max_B = 0` and `AL = 5`, `cmp max_B, al` followed by `JBE` skips the update because 0 <= 5. With the corrected order, 5 <= 0 is false, so the maximum becomes 5.

The original operand order is also valid with the matching jump: `cmp max_B, al` followed by `JAE`, or `cmp min_B, al` followed by `JLE`. `JBE/JAE` are unsigned comparisons; `JGE/JLE` are signed comparisons. Both work for the 0-9 values in this exercise.

### Reuse input, keep separate results

No second keyboard-input loop is needed: group A reads `ARR` without modifying it. Reset `SI = 0` and scan the same array for group B. Use the four separate `_B` variables so that updating B does not overwrite A's results.

Initialize the running minimum to 9 before the scan. The pasted declaration `min_B db 0` is safe here only because `mov min_B, 9` executes before processing B. Empty groups still need an output convention before result printing is implemented.

## Validation

217 source-instruction logic checks passed for all three groups, including repeated digits and empty groups. This check interprets the instructions used by this source; it does not replace assembling and running the program in emu8086.

## Running in emu8086

1. Open the Assembly file and select **Emulate**.
2. Set a breakpoint on the final `RET`, then run.
3. Type eight digits consecutively in the emulator screen. Do not type spaces or press Enter.
4. Inspect the variables before executing `RET`. Results are stored in memory, not printed.

| Input | `soluong` | `tong` | `max` | `min` |
|---|---:|---:|---:|---:|
| `12345678` | 2 | 9 | 6 | 3 |
| `03699912` | 6 | 36 | 9 | 0 |
| `99999999` | 8 | 72 | 9 | 9 |
| `00000000` | 8 | 0 | 0 | 0 |

Expected group B results:

| Input | `soluong_B` | `tong_B` | `max_B` | `min_B` |
|---|---:|---:|---:|---:|
| `12345678` | 3 | 13 | 7 | 1 |
| `03699912` | 1 | 1 | 1 | 1 |
| `77777777` | 8 | 56 | 7 | 7 |
| `99999999` | 0 | 0 | 0* | 9* |
| `00000000` | 0 | 0 | 0* | 9* |

Expected group C results:

| Input | `soluong_C` | `tong_C` | `max_C` | `min_C` |
|---|---:|---:|---:|---:|
| `12345678` | 3 | 14 | 8 | 2 |
| `03699912` | 1 | 2 | 2 | 2 |
| `24824824` | 8 | 32 | 8 | 2 |
| `88888888` | 8 | 64 | 8 | 8 |
| `00000000` | 0 | 0 | 0* | 9* |

`*` Initialization values for an empty group, not valid extrema.

Input validation is not implemented: only digit keys `0` through `9` are supported. The original problem does not specify what to print for an empty group's minimum and maximum. If a group's count is zero, this checkpoint retains that group's initialization values (maximum 0 and minimum 9); these are not valid extrema for an empty group.
