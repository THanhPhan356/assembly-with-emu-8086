# Bài 3: Kiểm tra, bật, tắt và đảo bit 2 của AL

## Đề bài

AL có 8 bit, đánh số từ 0 đến 7: bit 0 là LSB, bit 7 là MSB. Viết đoạn chương trình kiểm tra, bật, tắt và đảo bit 2 của AL; các bit khác giữ nguyên.

## Code emu8086

[bit2_al.asm](bit2_al.asm)

Bit 2 có mặt nạ `00000100b` (`04h`); mặt nạ để tắt bit 2 là `11111011b` (`FBh`).

| Thao tác | Lệnh | Ý nghĩa |
|---|---|---|
| Kiểm tra | `test al, 00000100b` | Không đổi AL; ZF = 1 nếu bit 2 là 0, ZF = 0 nếu bit 2 là 1 |
| Bật | `or al, 00000100b` | Đặt bit 2 thành 1 |
| Tắt | `and al, 11111011b` | Đặt bit 2 thành 0 |
| Đảo | `xor al, 00000100b` | Đổi bit 2 từ 0 sang 1 hoặc từ 1 sang 0 |

## Cách chạy và kết quả

Mở file trong emu8086, chọn **Emulate** và chạy từng lệnh. Xem cờ `ZF` ngay sau `TEST`, vì các lệnh tiếp theo thay đổi cờ.

Với `AL = 00001000b`, chuỗi kết quả là:

- Sau `TEST`: AL giữ nguyên `00001000b`, ZF = 1.
- Sau `OR`: AL = `00001100b`.
- Sau `AND`: AL = `00001000b`.
- Sau `XOR`: AL = `00001100b`.

Các thao tác được thực hiện lần lượt trên cùng AL. Chương trình không in ra màn hình.
