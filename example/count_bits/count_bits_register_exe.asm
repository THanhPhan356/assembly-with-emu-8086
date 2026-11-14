.MODEL SMALL
.STACK 100h

.DATA
    N DW 13

.CODE
MAIN PROC
    mov ax, @DATA
    mov ds, ax

    mov ax, N          ; Pass the input value in AX.
    call Count         ; AX receives the number of set bits.

    ; Inspect AX here: N = 13 gives AX = 3.
    mov ax, 4C00h
    int 21h
MAIN ENDP

; Input: AX = 16-bit bit pattern. Output: AX = set-bit count (0..16).
; Other general-purpose registers are preserved; flags may change.
Count PROC
    push si

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
    ret
Count ENDP

END MAIN
