# Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên (HCMUS)

**CS423 / CSC13003 – Kiểm chứng Phần mềm (AI-augmented · 2026)**  
**CHÍNH SÁCH AI · BIỂU MẪU — 2026 v1.0**

## AI Audit Report — Mẫu 5 mục cho mỗi Artifact

Phụ lục bắt buộc đính kèm cho mọi bài tập có dùng AI (HW#01–HW#06, Seminar).

Tài liệu được biên soạn lại từ Med Kharbach, PhD (2026) — *Mẫu Chính sách Sử dụng AI cho Giáo dục Đại học*. Giấy phép CC BY-NC-SA 4.0. Phiên bản này được FIT@HCMUS điều chỉnh cho môn CS423 / CSC15003 Kiểm chứng Phần mềm.

## 1. Thông tin Sinh viên

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | NGUYỄN QUANG THÁI |
| MSSV | 23127116 |
| Lớp / Khoá | 23KTPM2 |
| Mã bài tập | HW#05 |
| Ngày làm bài | 18/08/2026 |
| Công cụ AI đã dùng | ChatGPT |
| Có sử dụng AI | [X] Có &nbsp;&nbsp; [ ] Không |

## 2. Hướng dẫn (đọc trước khi điền)

- Thêm 1 hàng cho mỗi artifact AI sinh (test case, script, checklist, OpenAPI spec, JMeter plan…).
- Dán nguyên văn prompt — **KHÔNG paraphrase**.
- Dán nguyên văn output AI (hoặc kèm screenshot có chú thích trong báo cáo).
- Gắn nhãn: **VALID / INVALID / INCOMPLETE**.
- Lý do phải dẫn chiếu slide, mục ISTQB, hoặc RFC kỹ thuật.
- Hiển thị bản sửa với phần thay đổi được tô sáng.
- Hàng mẫu in nghiêng — thay trước khi nộp.

## 3. Bảng Audit — 1 hàng / artifact

|  (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do (ISTQB/RFC) | (5) Bản SV sửa |
| --- | --- | --- | --- | --- |
|  **Tool:** ChatGPT<br>**Date:** 18/08/2026 00:21<br>**Prompt:** Bạn là trợ lý kiểm thử hiệu năng cho HW05 Performance Testing Version 1.0.

Hãy đọc toàn bộ đề bài Version 1.0 và các tài liệu hiện có trong repository
C:\Users\nguye\Documents\GitHub\HW05-23127116. Phân biệt yêu cầu của đề với
hướng dẫn hoặc nội dung mẫu trong tài liệu.

Nhiệm vụ duy nhất của bước này:
1. Liệt kê deliverable bắt buộc của Version 1.0.
2. Kiểm tra ba lựa chọn sau có đúng ba endpoint group hay không:
   - Load: GET /api/products - read-heavy.
   - Stress: POST /api/register - auth-heavy.
   - Spike: POST /api/admin/coupons - transactional.
3. Tạo hoặc cập nhật STEP_BY_STEP_HW05_V1.0.md.

Không tạo JMeter plan và không chạy test ở bước này. Nếu có điểm chưa chắc chắn,
ghi rõ thay vì suy đoán.

| Đã tạo [STEP_BY_STEP_HW05_V1.0.md](C:/Users/nguye/Documents/GitHub/HW05-23127116/STEP_BY_STEP_HW05_V1.0.md) theo đề chính thức Version 1.0.

File hiện:

- Liệt kê đầy đủ deliverable bắt buộc: report MD/PDF, 3 plans, 3 CSV riêng, 3 JTL, 3 HTML reports, evidence tài nguyên/phần cứng, video, AI Critique/Audit, README, Git log, repository link và issue nếu có.
- Tách rõ yêu cầu chính thức khỏi guide, prompt mẫu, kết quả test và checklist nội bộ.
- Xác định Agent Skill là “encouraged”, dù rubric dành 10 điểm.
- Ghi rõ các thông số như 20/400 users, p95 dưới 2 giây và 486 RPS không phải yêu cầu cố định của đề.
- Đánh giá endpoint:
  - Products/read-heavy: đúng, độ chắc chắn cao.
  - Register/auth-heavy: hợp lý nhưng cần giải trình hoặc xác nhận TA.
  - Admin Coupons/transactional: hợp lý nhưng cần nêu rõ transaction rationale.
- Ghi các điểm chưa chắc chắn, gồm rubric cộng thành 90 nhưng Total ghi 100.

Không tạo/sửa JMeter plan và không chạy test. Các thay đổi hiện có của bạn trong những file khác được giữ nguyên. | | | | 
 | | | | | |
 | | | | | |
 | | | | | |
 | | | | | |
 | | | | | |
 | | | | | |
 | | | | | |
 | | | | | |

## 4. Tổng kết Độ chính xác AI

Tổng hợp verdict từ Mục 3 và điền vào bảng dưới.

| Chỉ số | Số lượng | Tỉ lệ |
| --- | ---: | ---: |
| Tổng artifact AI sinh đã audit | | |
| VALID (đúng, dùng nguyên) | | % |
| INVALID (sai; loại bỏ) | | % |
| INCOMPLETE (chấp nhận sau khi sửa) | | % |

## 5. Kết luận — Khi nào nên / không nên dùng AI?

*Viết 80–150 chữ mô tả pattern quan sát được. AI mạnh ở đâu? AI sai ở đâu? Khuyến nghị của bạn cho việc dùng AI trong loại công việc này?*

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

________________________________________________________________________________

## 6. Mandatory Disclosure (dán nguyên văn)

> "[Test case / script / dataset / báo cáo] này được sinh phiên bản đầu bởi [tên công cụ AI]; tôi đã rà soát và chỉnh sửa [phần X], bổ sung [edge case Y, Z]; [phần W] do tôi tự viết. AI Audit Report chi tiết đính kèm ở Phụ lục A. Tôi cam đoan không dùng AI để sinh bất kỳ artifact nào thuộc danh mục bị cấm."

## Chữ ký

| Mục | Giá trị |
| --- | --- |
| Họ tên sinh viên (in hoa) | |
| MSSV | |
| Lớp / Khoá | |
| Môn học | CS423 / CSC13003 – Kiểm chứng Phần mềm |
| Giảng viên | |
| Ngày | |
| Chữ ký | |

## Tham khảo

- Kharbach, M. (2026). *AI Use Policy Templates for Higher Education*. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). *A Post-AI Learning Taxonomy*.
- Fuster Rabella, M. (2025). *OECD Education Working Paper No. 338*.
- Perkins, M., Roe, J., & Furze, L. (2025). *AI Assessment Scale*.
- Anthropic (2025). *Building reliable AI test agents* — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
