; WHILE i < 6 DO: add i to the sum, then increment i.
; Inspect AX = 15 and SI = 6 after the loop; nothing is printed.

org 100h

mov si, 1               ; i = 1
mov ax, 0               ; sum = 0

while_loop:
    cmp si, 6
    jae end_while       ; Exit when i >= 6 (unsigned comparison).

    add ax, si
    inc si
    jmp while_loop

end_while:
    ret
