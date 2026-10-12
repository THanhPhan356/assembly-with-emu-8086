# Cộng hai số nguyên 32 bit

## Đề bài

Viết chương trình cộng hai số nguyên **không dấu 32 bit** bằng C và Assembly; bản Assembly chạy trên emu8086. Lưu 32 bit thấp của tổng và tách bit nhớ thứ 33 nếu phép cộng vượt phạm vi 32 bit.

Mỗi số đầu vào thuộc khoảng `0` đến `4294967295`. Hai chương trình có cùng phép tính; bản C nhập số hệ 10 từ bàn phím, bản Assembly khai báo sẵn dữ liệu.

## Code

- [Code C](add_32bit.c): dùng `uint32_t`, tính `tong = a + b` và `nho = (tong < a)`.
- [Code Assembly cho emu8086](add_32bit.asm): chia mỗi số thành hai word 16 bit, cộng phần thấp bằng `ADD`, phần cao kèm bit nhớ bằng `ADC`.

## Chạy bản C

Biên dịch với GCC:

```sh
gcc -std=c11 -Wall -Wextra add_32bit.c -o add_32bit
```

Chạy `./add_32bit` trên Linux/macOS hoặc `.\add_32bit.exe` trên PowerShell. Nhập hai số hệ 10 hợp lệ trong phạm vi đã nêu.

Ví dụ nhập:

```text
4294967295 1
```

Kết quả:

```text
Tong 32 bit = 0
Bit nho = 1
```

## Chạy bản Assembly

Mở `add_32bit.asm` trong emu8086, chọn **Emulate**, rồi chạy từng lệnh để xem thanh ghi và bộ nhớ. Chương trình lưu kết quả vào biến, không in ra màn hình.

Mỗi số được khai báo theo thứ tự **word thấp trước, word cao sau**:

```asm
a dw 0FFFFh, 0FFFFh   ; FFFFFFFFh
b dw 0001h, 0000h     ; 00000001h
```

- `[a]` đọc word thấp; `[a + 2]` đọc word cao, vì mỗi word chiếm 2 byte.
- `ADD` tạo cờ nhớ `CF`; `ADC` cộng thêm `CF`.
- `MOV` giữ nguyên `CF`. Không thay `mov cx, 0` bằng `xor cx, cx`, vì `XOR` xóa cờ nhớ.
- Tổng 32 bit nằm trong `DX:AX` và được lưu vào `sum`; bit nhớ cuối nằm trong `CX` và được lưu vào `nho`.

Với dữ liệu trên: `sum = 00000000h`, `nho = 1`. Tổng đầy đủ là `100000000h` (4294967296).

## Một số kết quả đối chiếu

| A (hệ 10) | B (hệ 10) | Tổng 32 bit (hệ 10) | Bit nhớ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 10 | 20 | 30 | 0 |
| 65535 | 1 | 65536 | 0 |
| 4294967295 | 1 | 0 | 1 |
| 4294967295 | 4294967295 | 4294967294 | 1 |

Trong bản Assembly, đổi hai word của `a` và `b` để thử các trường hợp khác.
