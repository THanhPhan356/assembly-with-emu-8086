org 100h
jmp start

N equ 5
A dw -5, 0, 7, -12, 3
B dw N dup(0)

start:
    push cs
    pop ds

    mov si, 0
    mov cx, N
    jcxz done

next_element:
    mov ax, A[si]
    cmp ax, 0
    jge store_result    ; Nonnegative: keep AX

    not ax              ; Negative: invert all 16 bits
    inc ax              ; Add 1 to complete two's complement negation

store_result:
    mov B[si], ax
    add si, 2           ; Next 16-bit element
    loop next_element   ; CX--; repeat if CX != 0

done:
    ret
