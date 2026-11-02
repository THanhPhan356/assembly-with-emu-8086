; Read eight digits and calculate statistics for groups A, B, and C.
; shortcut: accepts digit keys only; add validation before allowing other input.
; shortcut: an empty group keeps max=0 and min=9; define empty-group output before printing.

org 100h
jmp start

ARR db 8 dup(?)
soluong db 0
tong db 0
max db 0
min db 9

soluong_B db 0
tong_B db 0
max_B db 0
min_B db 0

soluong_C db 0
tong_C db 0
max_C db 0
min_C db 0

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

; Group B: odd values that are not divisible by 3.
    mov si, 0
    mov soluong_B, 0
    mov max_B, 0
    mov min_B, 9
    mov tong_B, 0

check_B:
    mov al, ARR[si]
    mov ah, 0
    mov bl, 2
    div bl
    cmp ah, 0
    je next_B

    mov al, ARR[si]     ; Reload the original value before testing divisibility by 3.
    mov ah, 0
    mov bl, 3
    div bl
    cmp ah, 0
    je next_B

    inc soluong_B
    mov al, ARR[si]
    add tong_B, al

    cmp al, max_B
    jbe max_done_B
    mov max_B, al

max_done_B:
    cmp al, min_B
    jge min_done_B
    mov min_B, al

min_done_B:
next_B:
    inc si
    cmp si, 8
    jb check_B

; Group C: even values that are not divisible by 3.
    mov si, 0
    mov soluong_C, 0
    mov tong_C, 0
    mov max_C, 0
    mov min_C, 9

check_C:
    mov al, ARR[si]
    mov ah, 0
    mov bl, 2
    div bl
    cmp ah, 0
    jne next_C

    mov al, ARR[si]
    mov ah, 0
    mov bl, 3
    div bl
    cmp ah, 0
    je next_C

    inc soluong_C
    mov al, ARR[si]
    add tong_C, al

    cmp al, max_C
    jbe max_done_C
    mov max_C, al

max_done_C:
    cmp al, min_C
    jge min_done_C
    mov min_C, al

min_done_C:
next_C:
    inc si
    cmp si, 8
    jb check_C

    ret
