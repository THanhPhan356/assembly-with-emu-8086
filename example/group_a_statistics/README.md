# Classifying Eight Digits: Groups A, B, and C Statistics

[Bài làm đầy đủ câu a–d bằng tiếng Việt](BAI_LAM.md), gồm lưu đồ, mô tả biến, Assembly, C và kết quả kiểm thử.

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

[group_a_statistics.asm](group_a_statistics.asm) and [group_a_statistics.c](group_a_statistics.c) implement keyboard input, all four statistics for **groups A, B, and C**, and the required single output row. Both preserve the variable names and three separate passes used during the lesson. The [report](BAI_LAM.md) contains the flowchart, detailed variable descriptions, and test results for parts a–d.

For an empty group, print `0 0 0 0`. The assignment leaves empty-group extrema unspecified; the last two zeros are an explicit convention, not mathematical extrema. Non-digit input is ignored; only the first eight digits are processed. The Assembly input does not echo typed keys.

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

Initialize the running minimum to 9 before the scan. The pasted declaration `min_B db 0` is safe here only because `mov min_B, 9` executes before processing B. Before printing, the completed version sets an empty group's minimum to zero, leaving its count, sum, and maximum at zero.

## Validation

[test_statistics.py](test_statistics.py) passed **120 cases in both compiled C and assembled 16-bit x86**, including 100 deterministic random arrays, repeated digits, empty groups, ignored non-digit input, and two-digit sums. It checks all result bytes, exact output, memory write bounds, and stack balance, plus three C EOF cases.

The test compiles C with GCC using `-std=c11 -Wall -Wextra -Werror -pedantic`. For Assembly, it adapts only memory-operand syntax to FASM, assembles the resulting source, and executes the binary with Unicorn and hooks for DOS input/output/exit. **It has not been compiled or run in the emu8086 application.**

With GCC, FASM, and Python `unicorn` available:

```sh
python test_statistics.py
```

Set `FASM` or `CC` to the appropriate compiler executable if needed.

## Running in emu8086

1. Open the Assembly file and select **Compile and Emulate**.
2. Select **Run** and type eight digits in the emulator screen.
3. Typed keys do not appear because input uses DOS `AH=07h`. No Enter is needed; non-digit keys are ignored.
4. The program prints all twelve values on one line, separated by one space, then exits.

For `12345678`, the output is:

```text
2 9 6 3 3 13 7 1 3 14 8 2
```

## Running the C version

```sh
gcc -std=c11 -Wall -Wextra -Werror -pedantic group_a_statistics.c -o statistics
./statistics
```

On Windows, run `statistics.exe`. A line-buffered terminal may require Enter after the input. EOF before eight digits produces an error on stderr and exit code 1.

| Input | A: count, sum, max, min | B: count, sum, max, min | C: count, sum, max, min |
|---|---|---|---|
| `12345678` | `2 9 6 3` | `3 13 7 1` | `3 14 8 2` |
| `03699912` | `6 36 9 0` | `1 1 1 1` | `1 2 2 2` |
| `99999999` | `8 72 9 9` | `0 0 0 0` | `0 0 0 0` |
| `77777777` | `0 0 0 0` | `8 56 7 7` | `0 0 0 0` |
| `88888888` | `0 0 0 0` | `0 0 0 0` | `8 64 8 8` |
| `00000000` | `8 0 0 0` | `0 0 0 0` | `0 0 0 0` |
| `24824824` | `0 0 0 0` | `0 0 0 0` | `8 34 8 2` |
