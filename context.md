# HCMUS SMART CAMPUS – AI UNIVERSITY LIFE HUB
> **Tagline:** One Campus. One AI Gateway. Every Student Service.  
> **Kiến trúc:** 1 Main Space → 6 Sub-spaces → 16 Specialized Agents → 1 Router → 1 Aggregator → 1 Unified Service Journey.  
> **Định danh chính thức:** *HCMUS Smart Campus – Student-built prototype demonstrating an AI-native university service ecosystem using publicly available HCMUS information.*

---

## 1. Ý tưởng Tổng thể & Bối cảnh Thực tế (Pain Points)

Trong môi trường đại học hiện nay tại Trường ĐH Khoa học Tự nhiên, ĐHQG-HCM (HCMUS), thông tin sinh viên nằm phân mảnh ở rất nhiều kênh:
- **Phòng Đào tạo:** Quản lý thời khóa biểu, kế hoạch đào tạo, đăng ký học phần, quy chế thi cử, tốt nghiệp.
- **Phòng Công tác Sinh viên (CTSV):** Quản lý học bổng, miễn giảm học phí, trợ cấp xã hội, điểm rèn luyện, ngoại trú, sinh hoạt công dân.
- **Thư viện HCMUS:** Quản lý tài nguyên học thuật, cơ sở dữ liệu số (IEEE, ScienceDirect, SpringerLink), dịch vụ phòng học nhóm, mượn trả sách.
- **Các Khoa chuyên môn & Bộ môn:** Quản lý chương trình đào tạo, đề cương môn học, điều kiện tiên quyết, đồ án/khóa luận tốt nghiệp.
- **Sổ tay Sinh viên:** Chứa hệ thống quy chế, quy định khen thưởng kỷ luật và khung xử lý vi phạm.

### Giải pháp AI-Native: Điểm vào duy nhất (Single Point of Entry)
Thay vì sinh viên phải tự xác định: *"Câu hỏi này hỏi Phòng Đào tạo? Hay CTSV? Hay Thư viện? Hay Khoa? Hay Sổ tay sinh viên?"*, hệ thống cung cấp một điểm vào duy nhất:

```
                  HCMUS SMART CAMPUS
                          │
                     User Request
                          │
                          ▼
                 CAMPUS ROUTER AGENT
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼
Sub-space 1          Sub-space 2          Sub-space 3
(Academic)           (Services)           (Admin)
     │                    │                    │
     └────────────────────┼────────────────────┘
                          │
                   Specialist Agents
                          │
                          ▼
                CAMPUS AGGREGATOR AGENT
                          │
                          ▼
                Unified Final Response & Action Plan
```

**Điểm khác biệt cốt lõi:** Người dùng không cần biết Agent nào phải được gọi. Họ chỉ mô tả mục tiêu bằng ngôn ngữ tự nhiên; hệ thống phân tích intent, chuyển yêu cầu sang các Agent chuyên trách rồi tổng hợp kết quả.

> **Lưu ý triển khai Wesome AI:** Nếu nền tảng chưa hỗ trợ nested Space → Sub-space thật sự, Sub-space được triển khai ở tầng product bằng menu, section và nhóm Agent.

---

## 2. Sơ đồ Cấu trúc: 6 Sub-spaces | 16 Specialized Agents

| Sub-space | Tên Sub-space | Danh sách Agents | Trọng tâm nhiệm vụ |
|:---|:---|:---|:---|
| **SUB-SPACE 1** | **HỌC VỤ & ĐÀO TẠO** | • `schedule-deadline-agent`<br>• `gpa-academic-standing-agent`<br>• `academic-advisor-agent` *(Flagship)* | Tra cứu lịch học, lịch thi, deadline; Tính toán mô phỏng GPA, cảnh báo học vụ; Định hướng lộ trình học tập, chuẩn đầu ra, môn tiên quyết. |
| **SUB-SPACE 2** | **DỊCH VỤ SINH VIÊN** | • `scholarship-matching-agent` *(Flagship)*<br>• `library-research-agent`<br>• `clubs-activities-agent` | Khớp và xếp hạng học bổng phù hợp hồ sơ; Tra cứu tài nguyên số, dịch vụ thư viện; Định hướng CLB, hoạt động phong trào và điểm rèn luyện. |
| **SUB-SPACE 3** | **HÀNH CHÍNH & MỘT CỬA** | • `administrative-procedure-agent`<br>• `regulation-qa-agent`<br>• `department-contact-agent` | Hướng dẫn thủ tục, giấy tờ, biểu mẫu một cửa; Trả lời quy chế, nội quy học đường; Tra cứu đầu mối phòng ban, hotline, địa chỉ làm việc. |
| **SUB-SPACE 4** | **GIẢNG VIÊN & NGHIÊN CỨU** | • `teaching-material-assistant`<br>• `research-assistant`<br>• `class-support-agent` | Hỗ trợ soạn đề cương, bài tập, học liệu an toàn học thuật; Hướng dẫn phương pháp nghiên cứu, tìm kiếm tài liệu; Hỗ trợ quản lý lớp học. |
| **SUB-SPACE 5** | **ĐỜI SỐNG & PHÁT TRIỂN** | • `student-wellbeing-agent`<br>• `soft-skills-coach-agent` | Tư vấn sức khỏe tinh thần, điều hướng PSY.US, tự chăm sóc; Luyện giao tiếp, thuyết trình, kỹ năng mềm, định hướng nghề nghiệp. |
| **SUB-SPACE 6** | **ĐIỀU PHỐI TRUNG TÂM** | • `campus-router-agent` *(Flagship)*<br>• `campus-aggregator-agent` | Phân tích intent, bóc tách đa ý định, phân luồng yêu cầu; Tổng hợp câu trả lời từ nhiều agent, giải quyết xung đột, lập Action Plan. |

---

## 3. Đặc tả Chi tiết Phân vùng Sub-space 1 & Sub-space 2 (Phạm vi đảm nhiệm)

### 🎓 SUB-SPACE 1: HỌC VỤ & ĐÀO TẠO

#### 1. `schedule-deadline-agent` (Trợ lý Lịch trình & Hạn chót)
- **Nhiệm vụ:** Tra cứu kế hoạch năm học 2025-2026, lịch thi giữa kỳ, cuối kỳ, thời hạn nộp hồ sơ chính sách, giờ học 2 cơ sở, tuyến xe buýt.
- **Data/Tool:** Kế hoạch đào tạo chính thức, Quy chế khảo thí, Quy định đào tạo tín chỉ, Public timetable.
- **Ranh giới an toàn:** Không giả vờ kết nối API thời gian thực nếu chưa được cấp quyền; nêu rõ tính dự kiến của văn bản.

#### 2. `gpa-academic-standing-agent` (Trợ lý Điểm số & Tình trạng Học vụ)
- **Nhiệm vụ:** Tính GPA học kỳ, GPA tích lũy; mô phỏng kịch bản điểm số ("What-if simulation"); cảnh báo nguy cơ học vụ (buộc thôi học, cảnh báo mức 1, mức 2); xếp loại học lực và tốt nghiệp.
- **Data/Tool:** Công thức tính GPA theo Điều 11 & Điều 15 (QĐ 1175/QĐ-KHTN), Calculator logic + dữ liệu do sinh viên tự nhập.
- **Ranh giới an toàn (Guardrails):** **Tuyệt đối không tự truy cập điểm cá nhân hoặc giả lập kết nối SIS.** Prototype an toàn: Sinh viên nhập `[GPA hiện tại] + [Số TC tích lũy] + [Số TC kỳ tới] + [Điểm kỳ vọng]` → Agent chạy mô phỏng chính xác bằng công thức toán học.

#### 3. `academic-advisor-agent` (Cố vấn Học tập Thông minh — ⭐ Flagship Agent)
- **Nhiệm vụ:** Phân tích tiến độ học tập, phát hiện lỗ hổng môn học, kiểm tra điều kiện học phần tiên quyết/song hành, gợi ý lộ trình môn học tối ưu cho từng học kỳ.
- **Data/Tool:** Khung chương trình đào tạo các ngành, Quy chế đào tạo tín chỉ, CSDL môn học và tiên quyết.
- **Flow xử lý:** `Current progress → Missing requirements → Prerequisite analysis → Recommended semester plan → Risk detection`.
- **Ranh giới an toàn:** Luôn khuyến cáo sinh viên tham khảo thêm ý kiến Cố vấn học tập chính thức của Khoa đối với các quyết định mang tính pháp lý.

---

### 🌟 SUB-SPACE 2: DỊCH VỤ SINH VIÊN

#### 4. `scholarship-matching-agent` (Sàng lọc & Khớp Học bổng — ⭐ Flagship Agent)
- **Nhiệm vụ:** Không chỉ liệt kê danh sách học bổng, mà thực hiện phân tích hồ sơ sinh viên để xếp hạng độ phù hợp (Match Percentage), chỉ ra tiêu chí còn thiếu và đề xuất hành động cụ thể kèm deadline.
- **Data/Tool:** CSDL học bổng Phòng CTSV, Quy định học bổng QĐ 622, điều kiện học bổng tài trợ doanh nghiệp.
- **Flow xử lý:** `Student Profile → Academic eligibility → Training-score condition → Year/major condition → Financial/special conditions → Deadline filter → Rank scholarships`.
- **Actionable Output:**
  ```markdown
  Suitable scholarships:
  1. Học bổng Khuyến khích Học tập (Loại Xuất sắc) — 95% Match
  2. Học bổng Doanh nghiệp A — 82% Match (Hạn chót: 15/10/2025)
  Missing requirement: → Minh chứng hoạt động rèn luyện Tiêu chí 3
  Next action: → Chuẩn bị bảng điểm + Giấy xác nhận ngoại trú trước ngày 03/10/2025
  ```

#### 5. `library-research-agent` (Trợ lý Nghiên cứu & Thư viện)
- **Nhiệm vụ:** Hướng dẫn khai thác 15 CSDL điện tử quốc tế (IEEE, ScienceDirect, SpringerLink, ProQuest...), tra cứu mục lục sách Sierra/EDS, hướng dẫn mượn trả tài liệu, đặt phòng học nhóm, quản lý trích dẫn.
- **Data/Tool:** CSDL Thư viện Trung tâm ĐHQG-HCM, Quy trình thư viện HCMUS (Lầu 9-10 CS1, Dãy C CS2).
- **Flow:** `Topic → Search strategy → Suitable database → Keyword generation → Citation management`.

#### 6. `clubs-activities-agent` (Trợ lý Hoạt động & CLB)
- **Nhiệm vụ:** Gợi ý Câu lạc bộ/Đội/Nhóm phù hợp sở thích và định hướng nghề nghiệp; cập nhật các phong trào tình nguyện, sự kiện học thuật; hướng dẫn cách tích lũy và tối ưu hóa điểm rèn luyện.
- **Data/Tool:** CSDL Đoàn - Hội, danh mục CLB trực thuộc, bảng khung điểm rèn luyện chi tiết.

---

## 4. Ba Flagship Agents Đầu tư Trọng điểm
1. ⭐ **`campus-router-agent`:** Thể hiện năng lực phát hiện đa ý định (Intent Detection) và điều phối không gian đa agent (Multi-Agent Orchestration).
2. ⭐ **`academic-advisor-agent`:** Thể hiện độ sâu tri thức (Knowledge Depth), logic suy luận tiên quyết và cá nhân hóa lộ trình học tập.
3. ⭐ **`scholarship-matching-agent`:** Thể hiện giá trị ứng dụng thực tiễn cao, biến thông tin thụ động thành kế hoạch hành động cụ thể cho sinh viên.

---

## 5. Kịch bản Demo Tiêu biểu (Closed-loop User Journey)

**Câu hỏi Demo của Sinh viên:**
> *"Tôi là sinh viên năm hai ngành Công nghệ thông tin. Tôi muốn xin học bổng kỳ này, nhưng không biết GPA hiện tại (3.25/4 với 65 TC) có đủ không. Nếu chưa đủ, hãy giúp tôi lập kế hoạch học kỳ tới và tìm thêm tài liệu chuyên ngành ở thư viện."*

**Luồng điều phối thực tế:**
```
                     Campus Router Agent
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    [GPA Agent]      [Scholarship Agent]   [Academic Advisor]
 (Mô phỏng 3.25)       (Lọc điều kiện)       (Lên lộ trình HK)
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
                   [Library Research Agent]
                  (Tìm sách & CSDL IEEE)
                              │
                              ▼
                    Campus Aggregator Agent
                              │
                              ▼
                     BÁO CÁO TỔNG HỢP:
  1. CURRENT STATUS: Đánh giá GPA 3.25 & đối chiếu học bổng.
  2. GAP ANALYSIS: Các tiêu chí rèn luyện hoặc điểm số còn thiếu.
  3. ACADEMIC PLAN: Danh sách môn học khuyến nghị kỳ tới.
  4. RESOURCES: Giáo trình, CSDL IEEE Xplore cần khai thác.
  5. NEXT ACTIONS: Các bước nộp hồ sơ hành chính kèm deadline.
```

---

## 6. Đáp ứng Bộ Tiêu chí Rubric Chấm điểm Track A

| Tiêu chí Rubric Track A | Triển khai tại HCMUS Smart Campus | Minh chứng kỹ thuật |
|:---|:---|:---|
| **Số lượng Agent (≥10)** | **16 Agents** phân bổ trên 6 Sub-spaces | Vượt chuẩn, cấu trúc phân tầng rõ ràng |
| **Độ phủ Kịch bản (≥3)** | 6 Sub-spaces bao quát toàn bộ đời sống đại học | Học vụ, Học bổng, Hành chính, Nghiên cứu, Tâm lý |
| **Tính hoàn thiện Kỹ thuật** | RAG tri thức sâu + Calculator + Matching Logic + Semantic Router | Không phụ thuộc API giả, mô phỏng toán học chính xác |
| **Giá trị Thực tiễn (Real need)** | Giải quyết bài toán phân mảnh thông tin lâu năm tại HCMUS | Căn cứ trực tiếp Sổ tay Sinh viên 2025-2026 chính thức |
| **Vòng lặp Dịch vụ (Closed loop)** | `Need → Router → Specialists → Aggregator → Action Plan` | Người dùng nhận được kế hoạch hành động trọn vẹn |
| **Khả năng Nhân rộng (Scalability)** | Kiến trúc Module hóa theo từng Sub-space độc lập | Dễ dàng mở rộng cho các trường đại học khác |