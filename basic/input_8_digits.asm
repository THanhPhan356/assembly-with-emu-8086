; Read eight digits into ARR. Type 0-9 consecutively; no Enter is needed.
; shortcut: assumes digit keys only; add validation before accepting arbitrary input.

org 100h
jmp start               ; Skip the array data when execution begins.

ARR db 8 dup(?)         ; Eight elements, one byte each.

start:
    mov si, 0

read_digit:
    mov ah, 01h         ; DOS: read and echo one character into AL.
    int 21h
    sub al, '0'         ; Convert the ASCII digit to its numeric value.
    mov ARR[si], al
    inc si
    cmp si, 8
    jb read_digit       ; Repeat until all eight elements are filled.

    ret
