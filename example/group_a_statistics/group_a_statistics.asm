; Read eight digits and calculate statistics for values divisible by 3.
; shortcut: accepts digit keys only; add validation before allowing other input.
; shortcut: an empty group keeps max=0 and min=9; define empty-group output before printing.

org 100h
jmp start

ARR db 8 dup(?)
soluong db 0
tong db 0
max db 0
min db 9

start:
    mov si, 0

nhap:
    mov ah, 01h
    int 21h
    sub al, '0'
    mov ARR[si], al
    inc si
    cmp si, 8
    jb nhap

; Group A: count, sum, maximum, and minimum of values divisible by 3.
    mov soluong, 0
    mov tong, 0
    mov max, 0
    mov min, 9
    mov si, 0
    mov bl, 3

check_A:
    mov al, ARR[si]
    mov ah, 0           ; DIV BL divides the full AX register.
    div bl
    cmp ah, 0
    jne ko_chia_het

    inc soluong
    mov al, ARR[si]     ; Reload the original value; DIV replaced AL with the quotient.
    add tong, al

    cmp al, max
    jbe max_done
    mov max, al

max_done:
    cmp al, min
    jge min_done
    mov min, al

min_done:
ko_chia_het:
    inc si
    cmp si, 8
    jb check_A

    ret
