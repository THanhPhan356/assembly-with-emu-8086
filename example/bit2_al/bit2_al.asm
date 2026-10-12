org 100h

mov al, 00001000b

; Kiem tra bit 2 (khong thay doi AL)
test al, 00000100b
; ZF = 1: bit 2 dang la 0
; ZF = 0: bit 2 dang la 1

; Bat bit 2
or al, 00000100b       ; AL = 00001100b

; Tat bit 2
and al, 11111011b      ; AL = 00001000b

; Dao bit 2
xor al, 00000100b      ; AL = 00001100b

ret
