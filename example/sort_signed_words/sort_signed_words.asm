org 100h
jmp start

N   dw 6
ARR dw 7, -3, 12, 0, -8, 7

start:
    push cs
    pop ds

    mov cx, N
    cmp cx, 1
    jbe sort_done
    dec cx                  ; The outer loop needs N-1 passes.

    mov dx, N
    shl dx, 1               ; DX = N*2: exclusive byte-offset limit.

    mov si, 0

outer_loop:
    mov ax, ARR[si]

    mov di, si
    add di, 2               ; Start with the element immediately after SI.

inner_loop:
    cmp di, dx
    jae next_i

    mov bx, ARR[di]
    cmp ax, bx
    jle next_j              ; Signed comparison: keep AX when AX <= BX.

    xchg ax, bx
    mov ARR[si], ax
    mov ARR[di], bx

next_j:
    add di, 2
    jmp inner_loop

next_i:
    add si, 2
    loop outer_loop         ; Decrement CX and repeat while CX is nonzero.

sort_done:
    ret
