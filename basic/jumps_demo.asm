; Compare the same 16 bits as signed (JL) and unsigned (JB).
; Open in emu8086, Compile, Emulate, then Run.

org 100h
jmp start

case1 db 'AX = FFFFh (-1 signed / 65535 unsigned), BX = 1', 13, 10, '$'
case2 db 'AX = 2, BX = 3', 13, 10, '$'
case3 db 'AX = 3, BX = 2', 13, 10, '$'
case4 db 'AX = 3, BX = 3', 13, 10, '$'
jl_label db '  JL (signed less):    $'
jb_label db '  JB (unsigned below): $'
taken db 'TAKEN', 13, 10, '$'
not_taken db 'NOT TAKEN', 13, 10, '$'
newline db 13, 10, '$'

start:
    push cs
    pop ds

    lea dx, [case1]
    call print_string
    mov ax, 0FFFFh
    mov bx, 1
    call compare_values

    lea dx, [case2]
    call print_string
    mov ax, 2
    mov bx, 3
    call compare_values

    lea dx, [case3]
    call print_string
    mov ax, 3
    mov bx, 2
    call compare_values

    lea dx, [case4]
    call print_string
    mov ax, 3
    mov bx, 3
    call compare_values

    mov ax, 4C00h
    int 21h

; AX and BX contain the values to compare.
compare_values:
    lea dx, [jl_label]
    call print_string

    cmp ax, bx
    jl signed_less
    lea dx, [not_taken]
    jmp show_signed
signed_less:
    lea dx, [taken]
show_signed:
    call print_string

    lea dx, [jb_label]
    call print_string

    ; Print calls can change flags, so compare again before JB.
    cmp ax, bx
    jb unsigned_below
    lea dx, [not_taken]
    jmp show_unsigned
unsigned_below:
    lea dx, [taken]
show_unsigned:
    call print_string
    lea dx, [newline]
    call print_string
    ret

; DOS function 09h needs AH and may change AL. Preserve AX and BX
; so printing cannot change the values used by either comparison.
print_string:
    push ax
    push bx
    push dx
    mov ah, 09h
    int 21h
    pop dx
    pop bx
    pop ax
    ret
