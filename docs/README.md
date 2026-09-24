# 🏆 TÀI LIỆU QUY CHẾ VÀ TIÊU CHÍ CHẤM ĐIỂM (TRACK A - WESOME AI)

Thư mục này lưu trữ 2 tài liệu chính thức về thể lệ và khung chấm điểm của cuộc thi AI Agent:

1. **`Rule (1).pdf`**: Thể lệ cuộc thi, các rào chẩn tuân thủ (Compliance & Safety Gate) và tiêu chuẩn kỹ thuật.
2. **`Scoring Criteria (1).pdf`**: Khung tiêu chí và thang điểm chi tiết (100 điểm) của Ban Giám khảo.

---

## 📊 TÓM TẮT KHUNG ĐIỂM (TỔNG 100 ĐIỂM)

### 1. Technical Implementation (Kỹ thuật & Đóng gói) – 30 điểm
- **1.1 Role Definition & Positioning (4đ)**: Tên Agent rõ ràng, mô tả vai trò đủ 4 yếu tố (Nhiệm vụ cốt lõi, Đối tượng phục vụ, Phong cách giao tiếp, Prompt định hướng).
- **1.2 Persona Design & Quality (9đ)**: Ảnh bìa/avatar thiết kế riêng, độ nét cao, viền sạch, đồng bộ phong cách nghiệp vụ (tránh dùng avatar mặc định).
- **1.3 Knowledge Base & Materials (12đ - Điểm số cao nhất)**:
  - Tài liệu: $\ge$ 8 văn bản, $\ge$ 3.000 ký tự (PDF/Word).
  - Hình ảnh: $\ge$ 10 ảnh $\ge$ 720P, không dính watermark.
  - Video: $\ge$ 4 video $\ge$ 30s, MP4 $\ge$ 1080P (*Lưu ý: Nếu quá nặng, ghi nhận trạng thái "Chưa làm / Pending" trong `video_resources.md`*).
  - Q&A: $\ge$ 15 câu hỏi Q&A có phân loại category chuẩn.
  - Tên file: Phải đặt tên có ý nghĩa, cấm đặt tên dạng số thứ tự `1.pdf`, `2.pdf` (bị trừ 0.5đ mỗi file).
- **1.4 Room / Scene Configuration (5đ)**: Background Web (1920x1080 / 16:9), Mobile (750x1624), Menu phân loại rõ ràng (pic, file, video, url).

### 2. Application Value (Giá trị Ứng dụng Thực tiễn) – 30 điểm
- **2.1 Scenario & Need (8đ)**: Pain point có thật của sinh viên/giảng viên HCMUS, có căn cứ thực tế.
- **2.2 Business Closed Loop (10đ)**: Quy trình khép kín đầu-cuối (User Need $\rightarrow$ Router $\rightarrow$ Specialist Agents $\rightarrow$ Aggregator $\rightarrow$ Action Plan).
- **2.3 Practical Effectiveness & Scalability (7đ)**: Phản hồi chính xác qua nhiều lượt hội thoại (multi-turn), có khả năng mở rộng.
- **2.4 Workspace Completeness (5đ)**: Toàn bộ Workspace có $\ge$ 10 Agent hợp lệ, bao quát $\ge$ 3 phân vùng nghiệp vụ rõ rệt.

### 3. Innovation & Experience (Đổi mới & Trải nghiệm) – 25 điểm
- **3.1 Creativity & Differentiation (15đ)**: Kiến trúc hệ sinh thái đa Agent độc đáo, khác biệt so với template thông thường.
- **3.2 Interactive Experience (10đ)**: Hội thoại tự nhiên, mượt mà, phản hồi cảm xúc và thấu hiểu ngữ cảnh.

### 4. Presentation (Thuyết trình & Demo) – 15 điểm
- **4.1 Demonstration Completeness (15đ)**: Luồng demo trơn tru, chứng minh được các chức năng cốt lõi.
