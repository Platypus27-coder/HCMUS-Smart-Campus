# Gói bàn giao subspace 06

Giải nén `subspace-06-upload.zip` trước khi sử dụng. Đây là gói gom tài nguyên để bàn giao, không phải định dạng import ZIP đã xác nhận của Wesome.

Với mỗi agent:

1. Dùng `info.docx` làm thông tin vai trò; dán `system-prompt.md` vào phần chỉ dẫn nếu nền tảng hỗ trợ.
2. Upload `agent/knowledge.docx` và `agent/QA.xlsx` vào các mục phù hợp.
3. Đặt `agent/background.png` làm nền; dùng lời chào và gợi ý trong `space/`.
4. Đưa tài liệu Word trong `menu/file/` lên menu. Các file Markdown khác là hướng dẫn dành cho người cấu hình; không mặc định nền tảng render Mermaid hoặc Markdown.
5. Điền URL thật của các agent vào `deployment/agent-links.json`, kiểm tra từng link rồi cấu hình điều hướng. URL null nghĩa là chưa cấu hình.
6. Dùng bộ demo và đánh giá trong `evaluation/`; lưu kết quả hội thoại thật. Tất cả trường hợp hiện để NOT_RUN.

Chưa có tích hợp gọi agent tự động hoặc video demo đã quay. Khi dùng luồng thủ công, nói rõ việc chuyển tiếp là do người dùng thực hiện. Bộ kiểm tra file đã có trong repo không xác nhận hành vi hội thoại trên nền tảng.
