# Kịch bản demo — dữ liệu minh họa

Các ví dụ dưới đây không phải dữ liệu sinh viên thật, không phải phản hồi live từ agent. Dùng để diễn tập luồng thủ công khi chưa có tích hợp. Khi demo khả năng thật, phải thay bằng phản hồi thực tế và ghi lại kết quả đánh giá.

## Demo 1: Một nhu cầu

Người dùng: “Giải thích cây nhị phân giúp tôi.”

Router cần chọn Core Foundations Tutor Agent, nêu lý do ngắn và cách mở agent. Không hỏi GPA, không chọn Library chỉ vì đây là câu hỏi học tập. Trên nền tảng, mở agent theo URL thật đã cấu hình; nếu chưa có thì nêu rõ bước chuyển thủ công.

## Demo 2: Chuỗi phụ thuộc

Người dùng: “Tôi muốn mô phỏng GPA rồi kiểm tra học bổng và lập kế hoạch học kỳ tới.”

Router xác định GPA, Scholarship và Academic Advisor. Tác vụ dùng kết quả GPA phải đợi phản hồi tính toán; không tự suy luận rằng GPA là đủ để xét học bổng. Mỗi specialist nhận bản tóm tắt đúng phạm vi.

Người demo thu phản hồi thực tế, giữ sources, assumptions, missing_information, limitations; dán vào Aggregator cùng yêu cầu ban đầu. Aggregator phải trình bày kết quả đã có, thông tin còn thiếu và thứ tự việc tiếp theo, không bịa ngưỡng học bổng hoặc danh sách môn học.

## Demo 3: Kết quả một phần

Mở `partial-responses.example.json`: các response minh họa cho thấy GPA đã có mô phỏng, Scholarship thiếu điểm rèn luyện, Advisor lỗi. Aggregator phải giữ phép tính theo dữ liệu minh họa, chưa kết luận học bổng, chưa có lộ trình, đề xuất bổ sung dữ liệu và thử lại Advisor.

## Cách ghi đánh giá

Chạy lần lượt `cases.json`, lưu phản hồi thật và pass/fail vào `results-template.csv`. Chấm theo hành vi và agent mong đợi, không yêu cầu trùng câu chữ. Các kiểm tra file tự động không thay thế việc đánh giá hội thoại trên Wesome.
