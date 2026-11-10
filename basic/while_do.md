# WHILE...DO: Check the Condition Before the Body

A `while...do` loop checks its condition first. If the condition is true, it runs the body and checks again. If the condition is false at the start, the body runs zero times.

## Basic Structure

```text
while condition do
    body
```

8086 has no `WHILE` instruction. Build this structure with a comparison and jumps:

```asm
while_loop:
    cmp si, 6
    jae end_while       ; The condition SI < 6 is false: leave the loop.

    ; Body: do some work and update SI.

    jmp while_loop      ; Check the condition again.

end_while:
```

`CMP SI, 6` sets flags without changing SI. `JAE` exits when SI is greater than or equal to 6, using an unsigned comparison. `JMP` returns to the condition unconditionally. See [signed and unsigned jumps](jumps.md) for other conditions.

## Example: Sum 1 Through 5

The [complete program](while_do.asm) implements:

```text
i = 1
sum = 0
while i < 6 do
    sum = sum + i
    i = i + 1
```

SI holds `i`; AX holds `sum`.

| SI at the check | SI < 6? | AX after the body |
|---|---|---|
| 1 | Yes | 1 |
| 2 | Yes | 3 |
| 3 | Yes | 6 |
| 4 | Yes | 10 |
| 5 | Yes | 15 |
| 6 | No: exit | 15 (unchanged) |

Open `while_do.asm` in emu8086, choose **Compile**, then **Emulate**, and step until `RET` is the next instruction. Check **AX = 000Fh (15 decimal)** and **SI = 0006h**. The program does not print output.

For a zero-iteration check, change `mov si, 1` to `mov si, 6` and compile again. Execution should jump directly to `end_while`, leaving **AX = 0** and **SI = 6**.

## Common Mistakes

- Putting the condition after the body creates a loop that always executes the body at least once, unlike this `while` loop.
- Omitting `INC SI` here keeps SI below 6 forever, so the loop never ends.
- Using `JA` instead of `JAE` also processes SI = 6, producing 21 instead of 15.

The source assembles with the bundled FASM. Machine-code checks cover the normal result and initially false conditions; direct execution in the emu8086 application has not been verified.
