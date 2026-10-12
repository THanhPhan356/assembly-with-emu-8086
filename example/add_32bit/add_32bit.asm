org 100h

push cs
pop ds

; Cong 16 bit thap
mov ax, [a]
add ax, [b]

; Cong 16 bit cao + bit nho
mov dx, [a + 2]
adc dx, [b + 2]

; Lay bit nho thu 33: MOV giu nguyen CF
mov cx, 0
adc cx, 0

; Luu ket qua
mov [sum], ax
mov [sum + 2], dx
mov [nho], cx

ret

; Word thap truoc, word cao sau
a   dw 0FFFFh, 0FFFFh   ; FFFFFFFFh
b   dw 0001h, 0000h     ; 00000001h

sum dw 0, 0
nho dw 0
