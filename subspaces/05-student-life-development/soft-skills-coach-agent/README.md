# Soft Skills & Student Development Coach

Canonical ID: `soft-skills-coach-agent` (Subspace 05). Đây là gói kiến thức đọc trực tiếp cho CORE GPT, không phải backend, RAG, cơ sở dữ liệu hay tích hợp Wesome đã vận hành. Phiên bản nội dung: 1.0.0, biên soạn 2026-09-22.

## Thành phần

- `info.docx`: hồ sơ, phạm vi, nhiệm vụ và ranh giới.
- `agent/knowledge.docx`: hướng dẫn cốt lõi 27 phần; `agent/related-agents.yaml`: quan hệ sinh từ `shared/agent-relationships.yaml`; `agent/QA.xlsx`: 130 câu nhập và 130 ca đánh giá chưa chạy live; `agent/background.png`: ảnh nền minh họa AI, không mô tả cơ sở HCMUS thật.
- `data/`: 14 tài liệu miền kỹ năng, 61 tình huống role-play, 15 rubric, 20 cặp phản hồi và `source-registry.xlsx` (16 dòng nguồn/trạng thái).
- `menu/file/`: 7 biểu mẫu tự điền; `menu/url/`: liên kết chung đã kiểm; `menu/video/`: ghi chú chưa có video đủ điều kiện; `space/`: lời chào và bản nháp cấu hình theo keyset của agent tham chiếu.
- `knowledge-upload-5-files/`: đúng 5 DOCX gộp từ 19 tài liệu profile/core/domain/role-play/rubric/feedback để tải vào mục Knowledge khi nền tảng giới hạn năm tệp. Các biểu mẫu menu, QA và registry vẫn giữ riêng; không tính vào năm tệp Knowledge.

## Hành vi sử dụng

Agent hỏi mục tiêu và bối cảnh tối thiểu, chọn đúng một hành vi để luyện, nêu vai/nhiệm vụ, đợi sinh viên thử, dùng rubric định tính cho điều đã quan sát, phản hồi cụ thể rồi mời thử lại. Không chấm khi chưa có bài thử; không tạo điểm chính xác giả hoặc hứa kết quả tuyển dụng. Khi yêu cầu dữ kiện hiện hành, chuyển đúng agent chuyên trách hoặc nói cần nguồn xác minh. Người dùng giữ quyền quyết định.

Nguồn phân loại trong registry: `S` kiến thức ngoài đã kiểm, `P` tài liệu/thiết kế dự án, `H` thông tin HCMUS chưa xác minh, `D` ví dụ giả lập. Không lấy ví dụ giả lập hoặc nguồn nước ngoài làm quy định HCMUS. Không yêu cầu MSSV, CCCD, OTP, mật khẩu, hồ sơ sức khỏe, bảng điểm đầy đủ. Wellbeing/khẩn cấp được ưu tiên khi phù hợp, không biến coaching thành chẩn đoán.

## Triển khai và kiểm tra

`space/space_config.json` là bản nháp đúng cấu trúc tham chiếu trong repo; chưa xác nhận các trường đó được Wesome import tự động. `QA.xlsx` gồm `Sheet1` ba cột để thử import và `Evaluation` có expected behavior cùng trạng thái `NOT_RUN`. Hãy kiểm thử hội thoại thực tế với năm DOCX trong `knowledge-upload-5-files/` và xác minh nguồn HCMUS trước khi công bố thông tin hiện hành.

Ảnh nền được tạo cho gói này bằng prompt về nhóm sinh viên luyện trình bày trong không gian học tập xanh-trắng, không có logo hoặc cơ sở HCMUS xác định; dùng làm minh họa, không làm bằng chứng cơ sở vật chất.
