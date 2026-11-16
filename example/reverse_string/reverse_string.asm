org 100h
jmp start

N dw 5
S db 'hello'

start:
    push cs
    pop ds

    ; shortcut: fixed nonempty input; validate N and stack capacity for runtime input.
    mov si, 0
    mov cx, N

PUSH_CHAR:
    mov al, S[si]
    push ax
    inc si
    loop PUSH_CHAR

    mov si, 0
    mov cx, N

POP_CHAR:
    pop ax
    mov S[si], al
    inc si
    loop POP_CHAR

    ret
