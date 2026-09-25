# 📘 HƯỚNG DẪN ĐÓNG GÓI CHUẨN CURATED AGENT (TRACK A - WESOME AI)
> **Dành cho các thành viên trong nhóm phụ trách Sub-space 1, Sub-space 2 và Sub-space 5.**  
> Mục tiêu: Đạt điểm tối đa **100/100 điểm**, đặc biệt là **12 điểm Knowledge Base** và **5 điểm Room Configuration** theo `Scoring Criteria.pdf` và `Agent Set Up.pdf` (trang 14 - 15).

---

## 🎯 1. CHECKLIST TIÊU CHUẨN ĐẦU RA CHO MỖI AGENT (ACCEPTANCE CRITERIA)

Mỗi Agent được xem là hoàn chỉnh khi và chỉ khi đạt đủ 6 tiêu chuẩn sau:

| Hạng mục | Chỉ tiêu Curated Agent | Quy cách kỹ thuật | Lưu ý quan trọng |
| :--- | :---: | :--- | :--- |
| **📄 Documents (`menu/file/`)** | $\ge$ **8 tài liệu** | Định dạng `.docx` hoặc `.pdf`. Tổng ký tự $\ge 3.000$. | **CẤM đặt tên số thứ tự trơn** (`1.pdf`, `2.docx`) $\rightarrow$ bị trừ 0.5đ/file. Phải đặt tên tiếng Việt mô tả rõ nội dung. |
| **🖼️ Images (`menu/pic/`)** | $\ge$ **10 hình ảnh** | Độ phân giải $1600 \times 900$ hoặc $1920 \times 1080$ (16:9). Định dạng `.png` hoặc `.jpg`. | **100% KHÔNG CÓ WATERMARK**. Thiết kế dạng sơ đồ tư duy, infographic 4 bước, bảng tra cứu SLA. |
| **❓ Q&A (`agent/QA.xlsx`)** | $\ge$ **15 câu hỏi** | File Excel gồm các cột: `Question`, `Answer`, `Display as Suggested Question` (hoặc có thêm `Category`, `Sub_Topic`). | **Bắt buộc có 4-5 câu hỏi nhận diện hệ sinh thái**: Giới thiệu bản thân là ai, cùng Sub-space có ai, điều hướng câu hỏi chéo sang Agent nào. |
| **🎬 Video (`menu/video/`)** | $\ge$ **4 kịch bản video** | Tạo file `menu/video/video_resources.md`. | **Hoãn sản xuất MP4 nặng**, nhưng ghi rõ kịch bản 4 phân cảnh (Script & Storyboard) cho từng video để lấy trọn điểm rubric. |
| **📝 Character Prompt** | **1 – 1.000 ký tự** | File `01_Character_Prompt.txt`. | **GIỚI HẠN CỨNG 1.000 KÝ TỰ** trên Wesome AI (nếu vượt quá dù 1 ký tự hệ thống sẽ báo đỏ và chặn lưu). Phải có khối `[PHỐI HỢP SUB-SPACE]`. |
| **🧠 Knowledge Base** | $\ge$ **3.000 ký tự** | File `agent/knowledge.docx`. | **Bắt buộc có chương**: `HỆ SINH THÁI HCMUS SMART CAMPUS & SƠ ĐỒ ĐIỀU HƯỚNG CÁC AGENT ĐỒNG NGHIỆP` để AI đọc hiểu khi nạp RAG. |

---

## 📁 2. CẤU TRÚC THƯ MỤC CHUẨN CỦA MỖI AGENT

Mỗi Agent phải được tổ chức đúng cấu trúc như mẫu tại `template/agent-template/`:

```
[Ten_Agent]/
├── 01_Character_Prompt.txt                # Prompt ngắn gọn (<= 1000 chars) copy trực tiếp vào web
├── info.docx                              # Hồ sơ lý lịch, lời chào và hướng dẫn tương tác
├── agent/
│   ├── background.png                     # Ảnh nền phòng chat (1920x1080, không watermark)
│   ├── knowledge.docx                     # Tri thức nhân vật (> 3.000 chars, có chương phối hợp)
│   ├── QA.xlsx                            # Ngân hàng Q&A (có gắn tag Category & câu hỏi nhận diện)
│   └── related-agents.yaml                # Metadata liên kết theo đồ thị trường
├── menu/
│   ├── file/                              # Tối thiểu 8 tài liệu Word/PDF chuyên môn
│   ├── pic/                               # Tối thiểu 10 ảnh Infographic sơ đồ 1600x900
│   ├── url/
│   │   ├── links.txt                      # Danh sách link trang chính thức HCMUS
│   │   └── official_links.md              # Bảng phân loại liên kết
│   └── video/
│       └── video_resources.md             # Kịch bản chi tiết 4 video bài giảng/hướng dẫn
└── space/
    ├── space_config.json                  # Cấu hình UI phòng chat Wesome AI
    └── welcome.md                         # Tin nhắn chào mừng và 4 gợi ý câu hỏi mẫu
```

---

## 🔗 3. CÁCH ĐỂ CÁC AGENT "BIẾT NHAU" TRÊN WEB WESOME AI

Để Agent không bị "mù" thông tin về đồng nghiệp khi người dùng chat thử trên web:

1. **Trong `01_Character_Prompt.txt`:** Bổ sung mục:
   ```
   [PHỐI HỢP CÙNG SUB-SPACE ...]
   - Khi người dùng hỏi về [chủ đề A] -> Gợi ý kết nối với [Tên Agent A].
   - Khi người dùng hỏi về [chủ đề B] -> Gợi ý kết nối với [Tên Agent B].
   ```
2. **Trong `agent/knowledge.docx`:** Thêm phần:
   `PHẦN ĐẶC BIỆT: HỆ SINH THÁI HCMUS SMART CAMPUS & SƠ ĐỒ PHỐI HỢP CÁC AGENT ĐỒNG NGHIỆP`
   Nêu rõ: Mình là ai? Đồng nghiệp trong Sub-space là ai? Khi người dùng hỏi lệch chuyên môn thì chuyển giao thế nào?
3. **Trong `agent/QA.xlsx`:** Bổ sung ít nhất 4 câu hỏi:
   - *"Bạn có biết các Agent khác trong HCMUS Smart Campus không?"*
   - *"Trong Sub-space ... này có những Agent nào phụ trách?"*
   - *"Nếu tôi muốn hỏi về [chủ đề của Agent đồng nghiệp] thì hỏi ai?"*
   - *"Ai là Agent điều phối trung tâm toàn trường?"* (Campus Router Agent).

---

## 🚀 4. QUY TRÌNH UPLOAD LÊN WEB WESOME AI

Khi tạo Agent trên web `wesome.ai`:
1. **Tab Character:** 
   - Đặt tên Agent rõ ràng theo quy ước.
   - Dán nội dung từ `01_Character_Prompt.txt` vào ô Prompt (kiểm tra đảm bảo $\le 1000$ ký tự).
   - Chọn avatar phong cách học đường chỉn chu.
2. **Tab Knowledge Base (Tri thức):** 
   - Upload file `agent/knowledge.docx`.
   - Upload toàn bộ các file trong `menu/file/`.
3. **Tab Q&A:** 
   - Upload file `agent/QA.xlsx`.
4. **Tab Menu Bar & Background:** 
   - Upload `agent/background.png` làm ảnh nền.
   - Upload các ảnh trong `menu/pic/` vào mục hình ảnh bổ trợ.
   - Cung cấp các liên kết từ `menu/url/links.txt`.
