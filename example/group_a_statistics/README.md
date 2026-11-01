# Classifying Eight Digits: Group A Statistics

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

[group_a_statistics.asm](group_a_statistics.asm) implements keyboard input and the four statistics for **group A only**. It preserves the variable names and control flow used during the lesson. Groups B and C, result printing, the flowchart, and the C version are not implemented in this checkpoint.

| Variable | Meaning |
|---|---|
| `ARR` | Eight numeric values, stored as bytes |
| `soluong` | Number of values in group A |
| `tong` | Sum of values in group A |
| `max` | Maximum value in group A |
| `min` | Minimum value in group A |

The program divides each value by 3 and checks the remainder in `AH`. It reloads the original value before adding to `tong`, because `DIV BL` overwrites `AL` with the quotient. Only values in group A update the statistics. A byte is sufficient for each result: the count is at most 8 and the sum is at most 72.

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

Input validation is not implemented: only digit keys `0` through `9` are supported. The original problem does not specify what to print for an empty group's minimum and maximum. If `soluong = 0`, this checkpoint retains the initialization values `max = 0` and `min = 9`; these are not valid extrema for an empty group.
