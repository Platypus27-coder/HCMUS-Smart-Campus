# 📦 AGENT TEMPLATE (CHUẨN HÓA THEO SCORING CRITERIA TRACK A)

Thư mục mẫu này được xây dựng chuẩn xác theo đặc tả trong README.md của kho mã nguồn và đáp ứng tối đa khung tiêu chí chấm điểm cuộc thi Wesome AI:

`	ext
agent-template/
├── README.md                      (Hướng dẫn sử dụng template)
├── info.docx                      (Hồ sơ thiết kế Agent: 4 thành phần định vị, guardrails, năng lực)
├── agent/
│   ├── QA.xlsx                    (Bộ câu hỏi Q&A >= 15 câu, chuẩn Sheet1 Wesome AI)
│   ├── knowledge.docx             (Tài liệu tri thức cốt lõi >= 3.000 ký tự)
│   ├── background.png             (Ảnh bìa Web tỷ lệ 16:9 Full HD 1920x1080)
│   └── related-agents.yaml        (Khai báo liên kết Router/Aggregator đa agent)
├── menu/
│   ├── file/
│   │   └── Mau_Tai_Lieu_Huong_Dan_Chuyen_Nganh.docx (File tải về, tên có ý nghĩa)
│   ├── pic/
│   │   └── README.md              (Quy chuẩn ảnh >= 720P, không watermark, >= 10 ảnh)
│   ├── video/
│   │   └── video_resources.md     (GHI NHẬN: Chưa làm video do dung lượng + Kịch bản)
│   └── url/
│       ├── links.txt              (Danh sách URL thô)
│       └── official_links.md      (Danh mục liên kết chính thức có mô tả)
└── space/
    ├── space_config.json          (Cấu hình Wesome AI: persona, starter prompts, instructions)
    └── welcome.md                 (Lời chào mở đầu không gian Agent)
`

---

## 🎯 CÁC QUY CHUẨN ĐẠT ĐIỂM TỐI ĐA (BENCHMARKS):
1. **Role Definition (Scoring 1.1 - 4đ):** Phải có đủ 4 yếu tố trong info.docx (Nhiệm vụ, Đối tượng, Phong cách, Prompt định hướng).
2. **Persona & Background (Scoring 1.2 & 1.4 - 14đ):** Ảnh bìa tỉ lệ 16:9, không dính watermark, kích thước 1920x1080 (Web) / 750x1624 (Mobile).
3. **Knowledge Base (Scoring 1.3 - 12đ):**
   - Tài liệu: >= 8 tài liệu, >= 3.000 ký tự (Word/PDF).
   - Q&A: >= 15 câu hỏi có gắn tag/category.
   - Tên file: Có tên mô tả ý nghĩa rõ ràng (không đặt 1.pdf, 2.pdf).
4. **Video Resources:** Ghi nhận rõ ràng trạng thái hoãn sản xuất trong ideo_resources.md kèm kịch bản dự kiến để không bị mất điểm cấu hình.
