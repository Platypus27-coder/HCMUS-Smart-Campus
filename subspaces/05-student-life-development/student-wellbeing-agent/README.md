# Student Well-being & Support Navigator

Gói tri thức cho `student-wellbeing-agent` trong Subspace 05 – Student Life & Development. Tên hiển thị **Student Well-being & Support Navigator** là bí danh giao diện của cùng technical ID, không phải agent mới.

## Cách CORE GPT nên đọc gói này

Đọc theo thứ tự: `info.docx` để xác định phạm vi; `agent/knowledge.docx` để nắm nền tảng và nguyên tắc phản hồi; `data/safety-and-escalation.docx` cùng `data/support-strategy.docx` trước khi áp dụng công cụ; sau đó dùng toolkit, scenarios, navigation, handoff và response guidelines theo nhu cầu. `agent/QA.xlsx` là bộ đánh giá, không phải bằng chứng về một lần chạy agent thực tế.

Các tài liệu dùng ba nhãn nguồn rõ ràng:

- **FACT / VERIFIED KNOWLEDGE**: kiến thức đã kiểm tra tại nguồn có ID S01–S06.
- **PROJECT DESIGN DECISION**: quy tắc vận hành do dự án thiết kế, có ID P01–P09.
- **DEMO EXAMPLE**: tình huống hoặc câu trả lời tổng hợp, có ID D01.

## Bản đồ nội dung

| Tệp | Vai trò cho CORE GPT |
|---|---|
| `info.docx` | Hồ sơ, phạm vi, đầu vào/đầu ra, giới hạn và hành trình hỗ trợ. |
| `agent/knowledge.docx` | 21 phần kiến thức nền: stress học tập, quá tải, nghỉ ngơi, hành động ngắn, follow-up và nguồn. |
| `data/safety-and-escalation.docx` | Quy tắc W-SAFE, xử lý an toàn, ví dụ ngôn ngữ và checklist rà soát. |
| `data/support-strategy.docx` | Cách chọn L1–L4; đây là mức phản hồi, không phải chẩn đoán hay điểm mức độ bệnh. |
| `data/self-care-toolkit.docx` | 20 thẻ công cụ tự chăm sóc, mỗi thẻ có mục đích, giới hạn và bước tiếp theo. |
| `data/wellbeing-scenarios.docx` | 30 tình huống suy luận có cấu trúc. |
| `data/support-navigation.docx` | Cách nêu lựa chọn hỗ trợ và tôn trọng quyền quyết định của sinh viên. |
| `data/cross-agent-handoff.docx` | Điều kiện, ngữ cảnh tối thiểu và ngữ cảnh cấm gửi cho sáu quan hệ agent. |
| `data/response-guidelines.docx` | Giọng điệu, khung trả lời và 18 cặp phản hồi tốt/chưa phù hợp. |
| `agent/QA.xlsx` | 80 ca đánh giá và sheet nhập câu hỏi theo cấu trúc tham chiếu. |
| `data/source-registry.xlsx` | 19 bản ghi nguồn và trạng thái xác minh. |

## Ranh giới vận hành

Agent chỉ hỗ trợ wellbeing thường ngày, tự chăm sóc phi lâm sàng, lập kế hoạch ngắn và định hướng tìm người hỗ trợ. Không chẩn đoán, không kê hay điều chỉnh thuốc, không tuyên bố là chuyên gia, không bịa dịch vụ/liên hệ HCMUS và không yêu cầu dữ liệu nhạy cảm ngoài nhu cầu hiện tại. Khi có lo ngại an toàn tức thời, ưu tiên kết nối người thật hoặc dịch vụ khẩn cấp phù hợp nơi người dùng đang ở; không tiếp tục coaching năng suất.

Thông tin dịch vụ, đầu mối và liên hệ wellbeing riêng của HCMUS hiện mang nhãn `[CẦN XÁC MINH NGUỒN CHÍNH THỨC]`. Gói không đưa số điện thoại, phòng, giờ mở cửa hay cam kết dịch vụ chưa được kiểm chứng.

## Tích hợp agent

Quan hệ được quản lý từ `shared/agent-relationships.yaml`, rồi sinh ra `agent/related-agents.yaml`. Sáu đích phù hợp là Soft Skills, GPA & Academic Standing, Academic Advisor, Schedule & Deadline, Department Contact và Clubs & Activities. Wellbeing dùng bàn giao tuần tự có sự đồng ý của người dùng vì routing policy hiện giữ `multi_intent_allowed: false`; quan hệ không chứng minh có API hay runtime liên agent đang vận hành.

Ranh giới với Soft Skills: mục tiêu phát triển kỹ năng độc lập như quản lý thời gian hoặc thuyết trình thuộc Soft Skills. Khi áp lực, thiếu nghỉ hoặc quá tải là nhu cầu chính, Wellbeing hỗ trợ trước; chỉ đề xuất Soft Skills khi người dùng muốn tiếp tục phần kỹ năng.

## Nguồn và kiểm tra

`data/source-registry.xlsx` có 6 nguồn đã xác minh (WHO, NIMH, NHS, CDC), 9 tham chiếu thiết kế dự án, 3 mục HCMUS/địa phương chờ xác minh và 1 nguồn ví dụ tổng hợp. Các nguồn đã xác minh chỉ được dùng ở mức giáo dục chung; không suy chúng thành chẩn đoán hoặc chính sách HCMUS.

QA có 80 ca: 30 thường ngày, 15 phức tạp, 12 cross-agent, 12 safety/boundary, 6 mơ hồ và 5 follow-up. Mọi hàng đều có `actual_response` trống, `review_result = NOT_RUN`; đây là trạng thái đúng cho đến khi có CORE GPT/platform thật để đánh giá.

## Tài nguyên giao diện

- `space/welcome.md` là lời chào tiếng Việt và gợi ý sử dụng.
- `space/space_config.json` giữ đúng các trường/sơ đồ đã có ở academic-advisor-agent; cấu hình này chưa xác nhận import trên Wesome.
- `agent/background.png` là minh hoạ được tạo cho bối cảnh lounge học tập yên tĩnh, không khẳng định là một không gian HCMUS có thật. Prompt: “Create a finished wide 16:9 background image for a student-built university wellbeing support navigator in HCMUS Smart Campus. Calm, professional, non-clinical Vietnamese university study lounge, realistic architectural photography, sunlit tropical greenery, warm light oak tables, soft sage and muted navy upholstery, notebook and glass of water, generous uncluttered space; no people, hospital imagery, medical symbols, logos, text or watermark.”
- `menu/file/weekly-wellbeing-plan.docx` và `menu/file/self-care-checklist.docx` là worksheet cho sinh viên. `menu/url/official_links.md` chỉ có nguồn giáo dục công khai đã kiểm tra; `menu/video/README.md` chưa đăng video vì chưa có nguồn phù hợp được kiểm chứng.

## Trạng thái kiểm tra

Đã kiểm tra cấu trúc tệp Office, số lượng nội dung, liên kết nguồn, metadata quan hệ và các validator/test của repository. Có một hạn chế môi trường: công cụ render DOCX bắt buộc không tìm thấy LibreOffice/Word trong runtime đóng gói, nên chưa thể sinh và xem mọi trang PNG. Việc nghiệm thu bố cục trang DOCX cần chạy lại khi runtime có renderer; nội dung và cấu trúc OOXML vẫn đã được kiểm tra.
