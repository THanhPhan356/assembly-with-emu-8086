.MODEL SMALL
.STACK 100h

.DATA
    N DW 13

.CODE
MAIN PROC
    mov ax, @DATA
    mov ds, ax

    push N
    call Count
    pop N

    ; Inspect AX here: N = 13 gives AX = 3.
    mov ax, 4C00h
    int 21h
MAIN ENDP

Count PROC
    push bp
    mov bp, sp
    push si

    mov ax, [bp+4]      ; Read the stack argument above saved BP and return IP.
    mov si, 0

count_bit_1:
    cmp ax, 0
    je count_done

    test ax, 1
    jz shift_a
    inc si

shift_a:
    shr ax, 1
    jmp count_bit_1

count_done:
    mov ax, si
    pop si
    pop bp
    ret
Count ENDP

END MAIN
