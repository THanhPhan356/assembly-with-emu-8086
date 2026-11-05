.MODEL SMALL
.STACK 100h

.DATA
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

.CODE
MAIN PROC
    mov ax, @DATA
    mov ds, ax         ; EXE startup DS points to the PSP, not our data.

start:
    mov si, 0

nhap:
    mov ah, 07h        ; Read without echo: stdout contains only the result row.
    int 21h
    cmp al, '0'
    jb nhap
    cmp al, '9'
    ja nhap
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

; The problem leaves empty-group extrema unspecified; print zero for both.
    cmp soluong, 0
    jne empty_A_done
    mov min, 0
empty_A_done:
    cmp soluong_B, 0
    jne empty_B_done
    mov min_B, 0
empty_B_done:
    cmp soluong_C, 0
    jne empty_C_done
    mov min_C, 0
empty_C_done:

; The twelve result bytes are contiguous, in the required output order.
    lea si, soluong
    mov cx, 12
print_results:
    mov al, [si]
    call print_u8
    inc si
    dec cx
    jz print_done
    mov dl, ' '
    mov ah, 02h
    int 21h
    jmp print_results

print_done:
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    mov ax, 4C00h
    int 21h

; AL is in 0..72. Print one or two decimal digits; preserve AX, BX, DX.
print_u8:
    push ax
    push bx
    push dx
    mov ah, 0
    mov bl, 10
    div bl
    push ax           ; Keep the units digit across DOS output.
    cmp al, 0
    je print_units
    mov dl, al
    add dl, '0'
    mov ah, 02h
    int 21h
print_units:
    pop ax
    mov dl, ah
    add dl, '0'
    mov ah, 02h
    int 21h
    pop dx
    pop bx
    pop ax
    ret
MAIN ENDP

END MAIN
