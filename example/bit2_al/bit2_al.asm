org 100h

mov al, 00001000b

; Test bit 2 without changing AL
test al, 00000100b
; ZF = 1: bit 2 is 0
; ZF = 0: bit 2 is 1

; Set bit 2
or al, 00000100b       ; AL = 00001100b

; Clear bit 2
and al, 11111011b      ; AL = 00001000b

; Toggle bit 2
xor al, 00000100b      ; AL = 00001100b

ret
