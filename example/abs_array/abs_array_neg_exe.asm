.MODEL SMALL
.STACK 100h

.DATA
N equ 5
A dw -5, 0, 7, -12, 3
B dw N dup(0)

.CODE
MAIN PROC
    mov ax, @DATA
    mov ds, ax         ; EXE startup DS points to the PSP, not our data.

start:
    mov si, 0
    mov cx, N
    jcxz done

next_element:
    mov ax, A[si]
    cmp ax, 0
    jge store_result    ; Nonnegative: keep AX

    neg ax              ; Negative: AX = 0 - AX

store_result:
    mov B[si], ax
    add si, 2           ; Next 16-bit element
    loop next_element   ; CX--; repeat if CX != 0

done:
    mov ah, 4Ch
    int 21h
MAIN ENDP

END MAIN
