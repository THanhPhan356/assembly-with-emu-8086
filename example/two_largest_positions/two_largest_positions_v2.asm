; Version 2: one pass, maxima in AX/DX, zero-based positions in memory.
; Equal values at different positions are allowed; earlier positions win ties.
; shortcut: assumes N >= 2, add a length guard before using shorter arrays.
; Sample result: AX = 12, DX = 12, pos1 = 1, pos2 = 3.

org 100h
jmp start

ARR  dw -7, 12, 5, 12, -2
N    equ 5
pos1 dw 0
pos2 dw 0

start:
    mov si, 0
    mov ax, ARR[si]       ; AX = max1
    mov dx, ARR[si+2]     ; DX = max2
    mov pos1, 0
    mov pos2, 1

    cmp ax, dx
    jge prepare_loop

    ; Hoan doi hai gia tri va vi tri ban dau
    mov bx, ax
    mov ax, dx
    mov dx, bx
    mov pos1, 1
    mov pos2, 0

prepare_loop:
    mov si, 4
    mov cx, N-2
    jcxz done

cmploop:
    mov bx, ARR[si]

    cmp bx, ax
    jg greater_than_max1
    jmp versus_max2

greater_than_max1:
    mov dx, ax           ; max2 = max1 cu
    mov ax, bx           ; max1 = phan tu moi

    mov bx, pos1
    mov pos2, bx         ; pos2 = pos1 cu

    mov bx, si
    shr bx, 1            ; Doi offset byte thanh chi so
    mov pos1, bx
    jmp check

versus_max2:
    cmp bx, dx
    jg greater_than_max2
    jmp check

greater_than_max2:
    mov dx, bx           ; max2 = phan tu moi

    mov bx, si
    shr bx, 1
    mov pos2, bx

check:
    add si, 2
    loop cmploop

done:
    ret
