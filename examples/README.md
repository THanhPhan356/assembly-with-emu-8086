# Ví dụ thực hành

## 01 — Quan sát thanh ghi

Mở [01-registers.asm](01-registers.asm) trong emu8086, chọn **Emulate** và chạy từng lệnh bằng **Single Step**. Quan sát các thanh ghi **trước khi thực thi RET**.

| Sau lệnh | Giá trị dự kiến |
| --- | --- |
| `mov ax, 1234h` | AX = 1234h; AH = 12h; AL = 34h |
| `mov bl, ah` | BL = 12h; BH vẫn giữ giá trị trước đó |
| `mov bh, al` | BH = 34h; BL = 12h; BX = 3412h |

**Kết quả thực tế:** Chưa chạy trong emu8086. Hãy ghi quan sát và thêm ảnh vào [assets/](../assets/).

Mỗi ví dụ mới cần ghi mục tiêu, cách chạy, đầu vào, đầu ra và điểm cần quan sát.
