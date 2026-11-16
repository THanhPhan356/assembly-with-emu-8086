org 100h
jmp start

N dw 4
A dw 2, 5, 8, 3

start:
    push cs
    pop ds

    mov ax, offset A
    push ax
    push N
    call CountOdd
    add sp, 4               ; Caller removes both arguments without changing AX.
    ret

CountOdd PROC
    push bp
    mov bp, sp
    push cx
    push si

    mov cx, [bp+4]          ; N
    mov si, [bp+6]          ; Offset of A in DS
    xor ax, ax
    jcxz count_done

next_element:
    test word ptr [si], 1
    jz next_word
    inc ax

next_word:
    add si, 2
    loop next_element

count_done:
    pop si
    pop cx
    pop bp
    ret
CountOdd ENDP
