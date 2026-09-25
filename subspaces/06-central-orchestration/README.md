# Subspace 06 — Điều phối Trung tâm

Gói nội dung cho Campus Router Agent và Campus Aggregator Agent thuộc HCMUS Smart Campus, prototype do sinh viên xây dựng. Router có thể được đặt làm điểm vào Main Space; gói tài nguyên vẫn thuộc subspace 06.

## Trạng thái

Gói này cung cấp hướng dẫn vai trò, knowledge, Q&A, tài nguyên menu và kịch bản đánh giá. Chưa có tích hợp gọi agent tự động, truy cập SIS hay bộ nhớ lâu dài. `space_config.json` là cấu hình bàn giao nội bộ, không phải định dạng import Wesome đã được xác nhận.

Nguồn chuẩn: `shared/agent-directory.yaml` (17 agent: 15 chuyên trách và 2 điều phối), `shared/agent-relationships.yaml`, `shared/routing-rules.yaml`, `shared/routing-score-criteria.yaml`, `shared/handoff-protocol.md`, `shared/user-memory-policy.md`. Đường dẫn trên tính từ gốc repo. Không sửa trực tiếp `related-agents.yaml`.

## Tài liệu và cách cập nhật

- Mỗi agent có `info.md`, `agent/knowledge.md`, `agent/qa.json` làm nguồn biên tập; bản Word/Excel được xuất từ các nguồn này.
- `agent/QA.xlsx` giữ ba cột của mẫu repo: Question, Answer, Display as Suggested Question? yes/no. Chỉ một số câu được đánh dấu gợi ý.
- Danh mục và trường bàn giao trong knowledge được lấy từ metadata chuẩn khi build; không sửa bản sao này trong Word.
- `archive/router-original/` giữ nguyên các bản Router trước khi chuẩn hóa. Chỉ upload bản chuẩn `agent/knowledge.docx`; không upload archive hoặc các bản đánh số như `knowledge6.docx`, `knowledge7.docx`.
- `evaluation/cases.json` là bộ tình huống đánh giá hành vi, không phải kết quả chạy agent thật.

Từ gốc repo, cài `python-docx`, `openpyxl` và các dependency của repo, rồi chạy `python scripts/build_orchestration_package.py`. Kiểm tra bằng `python scripts/validate_orchestration_package.py`, ba validator trong README gốc và `python -m unittest discover -s tests`.

## Đưa lên Wesome

1. Tạo hai agent theo tên và vai trò trong `info.docx`; dùng `system-prompt.md` làm chỉ dẫn vận hành nếu nền tảng có trường tương ứng.
2. Upload `agent/knowledge.docx` và `agent/QA.xlsx`; đặt `agent/background.png` làm nền.
3. Thiết lập lời chào, câu gợi ý và menu theo `space/space_config.json`; kiểm tra thủ công khả năng nhận định dạng của nền tảng.
4. Điền URL thật vào `deployment/agent-links.json` sau khi nhóm cung cấp. Giá trị null nghĩa là chưa cấu hình; không công bố nút trỏ đến URL giả.
5. Nếu hỗ trợ gọi agent: kiểm tra truyền ngữ cảnh tối thiểu và nhận response theo hợp đồng trước khi bật tự động. Nếu chưa hỗ trợ: Router chỉ giới thiệu agent và cung cấp bản tóm tắt để người dùng chuyển tiếp; Aggregator nhận kết quả người dùng dán vào.
6. Chạy các ca đánh giá trên nền tảng, ghi phản hồi thật và pass/fail vào `evaluation/results-template.csv`. Chỉ đánh dấu hoàn thành triển khai khi đã có bằng chứng.

## Tiêu chí nghiệm thu

Không định tuyến đến agent đã bỏ; không giả vờ đã gọi agent; không tự tạo thông tin trường; không chuyển dữ liệu ngoài phạm vi; kết quả một phần và mâu thuẫn phải được nêu rõ. Mỗi agent chuyên trách có ít nhất một ca đánh giá. Các ca về dữ liệu nhạy cảm, agent không tồn tại, nguồn chưa xác minh và thiếu kết quả bắt buộc đạt. Mục tiêu đề xuất cho các ca còn lại: ít nhất 90% đạt, sau đó sửa các ca lỗi và đánh giá lại.

Các trường hợp wellbeing đi kèm nhu cầu khác cần rà lại chính sách chung (`multi_intent_allowed: false` hiện có) trước khi tự động thực thi. Trong gói hướng dẫn, ưu tiên hỗ trợ wellbeing và không tự chuyển nội dung nhạy cảm sang tác vụ khác.
