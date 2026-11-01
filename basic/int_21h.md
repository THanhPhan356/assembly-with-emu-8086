# INT 21h: Reading a Keyboard Character

`INT` is a software-interrupt instruction. Interrupt `21h` provides DOS services, and `AH` selects the requested service. It is not exclusively an output instruction.

With `AH = 01h`, DOS waits for one keyboard character, echoes it on the screen, and returns its character code in `AL`:

```asm
mov ah, 01h      ; Select the DOS character-input service.
int 21h          ; Wait for a key; return its character code in AL.
```

`AH` selects the service; `AL` receives the character. They are separate halves of `AX`, so setting `AH` does not prevent receiving input in `AL`. Keep the `h` suffix: `21h` is hexadecimal, while `21` alone is decimal and names a different interrupt.

## Converting a Digit to a Number

The input service reads characters, not integer values. The ASCII codes for `'0'` through `'9'` are consecutive, so subtracting `'0'` converts one digit to its numeric value:

```asm
mov ah, 01h
int 21h
sub al, '0'      ; For key '5': 35h - 30h = 05h.
```

`'0'` means the character code `30h` (48 decimal), not the numeric value zero. Subtraction works only after confirming or assuming that the character is a digit. This service has no option that parses a signed or multi-digit integer automatically; that requires reading more characters and converting them in your own code.

## Storing Eight Digits

The [input_8_digits.asm](input_8_digits.asm) example stores eight values in a byte array. Each call reads one character, so type digits consecutively without spaces or Enter. The example assumes valid digit keys and does not validate other input.

The [`group_a_statistics.asm` example](../example/group_a_statistics/group_a_statistics.asm) adds classification and statistics after the input loop.
