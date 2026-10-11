# Assembly with emu8086

Nhật ký học Assembly x86 16-bit và kiến trúc bộ xử lý 8086 của Thanh Phan, thực hành với emu8086.

Nội dung theo [bản tiếng Việt book_assembly_8086_vi](https://github.com/THanhPhan356/book_assembly_8086_vi) và [sách gốc của gurugio](https://github.com/gurugio/book_assembly_8086). Repo lưu cách hiểu, mã thực hành và kết quả quan sát của mình; trạng thái ban đầu của các bài là **chưa bắt đầu**.

## Mục tiêu

- Hiểu thanh ghi, cách định địa chỉ, bộ nhớ, FLAGS và luồng thực thi của 8086.
- Tự viết chương trình nhỏ và giải thích từng bước bằng trạng thái thanh ghi/bộ nhớ.
- Ghi lại lỗi, cách sửa và kết quả thực nghiệm để có thể tự ôn tập.

## Bắt đầu

1. Mở [bài 01](notes/01-introemu8086.md) và đọc nguồn được dẫn trong bài.
2. Mở [ví dụ thanh ghi](examples/01-registers.asm) bằng emu8086, chọn **Emulate**, rồi **Single Step**.
3. So sánh trạng thái với [bảng kết quả dự kiến](examples/README.md).
4. Bổ sung ghi chép, ảnh quan sát và bài tập tự làm. Đánh dấu đã hoàn thành sau khi chạy và giải thích được.

## Cấu trúc

| Thư mục | Nội dung |
| --- | --- |
| [notes/](notes/) | Ghi chép theo 26 bài trong sách |
| [examples/](examples/) | Các chương trình nhỏ để quan sát hành vi |
| [exercises/](exercises/) | Bài tập tự giải và cách kiểm chứng |
| [projects/](projects/) | Các dự án nhỏ sau khi nắm kiến thức cần thiết |
| [journal/](journal/) | Nhật ký học và việc cần làm tiếp |
| [assets/](assets/) | Ảnh emu8086 và sơ đồ tự vẽ |
| [templates/](templates/) | Mẫu ghi chép một bài |

## Tiến độ

| Bài | Chủ đề | Trạng thái |
| --- | --- | --- |
| 01 | [Làm quen với emu8086](notes/01-introemu8086.md) | Chưa bắt đầu |
| 02 | [Hệ đếm và biểu diễn số](notes/02-number.md) | Chưa bắt đầu |
| 03 | [Kiến trúc bộ xử lý 8086](notes/03-8086arch.md) | Chưa bắt đầu |
| 04 | [Lệnh MOV](notes/04-mov.md) | Chưa bắt đầu |
| 05 | [Đọc và ghi bộ nhớ](notes/05-memoryreadwrite.md) | Chưa bắt đầu |
| 06 | [Các cách định địa chỉ](notes/06-addressing.md) | Chưa bắt đầu |
| 07 | [Thực hành MOV](notes/07-usemov.md) | Chưa bắt đầu |
| 08 | [Biến](notes/08-variable.md) | Chưa bắt đầu |
| 09 | [Mảng](notes/09-array.md) | Chưa bắt đầu |
| 10 | [Địa chỉ của biến và con trỏ](notes/10-pointer.md) | Chưa bắt đầu |
| 11 | [Vì sao học Assembly 8086?](notes/11-whyassembly.md) | Chưa bắt đầu |
| 12 | [Phép toán logic và FLAGS](notes/12-logicoperation.md) | Chưa bắt đầu |
| 13 | [Cộng, trừ và nhân](notes/13-addsubmul.md) | Chưa bắt đầu |
| 14 | [Phép chia](notes/14-div.md) | Chưa bắt đầu |
| 15 | [INC và DEC](notes/15-incdec.md) | Chưa bắt đầu |
| 16 | [Lệnh nhảy và hàm](notes/16-jump.md) | Chưa bắt đầu |
| 17 | [Nhảy có điều kiện](notes/17-conditionaljump.md) | Chưa bắt đầu |
| 18 | [So sánh giá trị](notes/18-compare.md) | Chưa bắt đầu |
| 19 | [Vòng lặp](notes/19-repeat.md) | Chưa bắt đầu |
| 20 | [Stack](notes/20-stack.md) | Chưa bắt đầu |
| 21 | [Hàm](notes/21-function.md) | Chưa bắt đầu |
| 22 | [Gọi hàm qua stack và biến cục bộ](notes/22-functioncalling.md) | Chưa bắt đầu |
| 23 | [Macro](notes/23-macrofunc.md) | Chưa bắt đầu |
| 24 | [Thư viện emu8086.inc](notes/24-howtoemu8086inc.md) | Chưa bắt đầu |
| 25 | [Học tiếp Assembly hiện đại](notes/25-gofurther.md) | Chưa bắt đầu |
| 26 | [Interrupt do BIOS cung cấp](notes/26-biosinterrupt.md) | Chưa bắt đầu |

## Cách ghi một bài học

Ghi bằng lời của mình: khái niệm → ví dụ → kết quả dự đoán → kết quả thực tế → điều chưa hiểu. Với mỗi đoạn Assembly, nêu đầu vào, đầu ra, thanh ghi bị thay đổi và cách chạy. Nếu tham khảo mã từ sách, ghi nguồn tại tệp.

## Nguồn và giấy phép

- Sách gốc: [gurugio/book_assembly_8086](https://github.com/gurugio/book_assembly_8086).
- Bản tiếng Việt dùng để học: [THanhPhan356/book_assembly_8086_vi](https://github.com/THanhPhan356/book_assembly_8086_vi).
- Mã và ghi chép trong repo được cung cấp theo [GNU GPL v3](LICENSE). Mã tham khảo cần giữ thông tin tác giả và nguồn.
