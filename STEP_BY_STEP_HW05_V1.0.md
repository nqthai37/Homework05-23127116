# HW05 Performance Testing — Version 1.0

## Phạm vi rà soát của bước này

Ngày rà soát: 2026-08-18.

Repository được yêu cầu: `C:\Users\nguye\Documents\GitHub\HomeWork05-23127116`.

Các file nội dung hiện có trong repository tại thời điểm rà soát:

- `ai/ai-audit-report.md` — biểu mẫu **Chính sách AI 2026 v1.0** đã được điền một phần.
- `.gitattributes` — cấu hình Git, không chứa yêu cầu HW05.

Repository không có đề **HW05 Performance Testing Version 1.0**, rubric, README,
SUT source/API specification hoặc tài liệu giảng viên khác. Lịch sử Git chỉ có
commit khởi tạo chứa `.gitattributes`; `ai/ai-audit-report.md` đang là file
untracked. Vì vậy tài liệu này không suy đoán những yêu cầu không có nguồn.

## 1. Deliverable bắt buộc của Version 1.0

### 1.1. Điều có thể xác minh trực tiếp

Không thể liệt kê đầy đủ và xác nhận các deliverable bắt buộc của **HW05
Performance Testing Version 1.0**, vì đề/rubric Version 1.0 không có trong
repository.

Tài liệu duy nhất cho phép xác nhận một nghĩa vụ là **Chính sách AI 2026 v1.0**,
không phải đề HW05:

- Nếu bài tập có dùng AI, phải đính kèm **AI Audit Report**.
- Audit phải có một mục/hàng cho mỗi artifact do AI sinh, gồm nguyên văn prompt,
  nguyên văn output, verdict `VALID`/`INVALID`/`INCOMPLETE`, lý do có dẫn chiếu,
  và bản sinh viên sửa.
- Biểu mẫu còn yêu cầu bảng tổng kết độ chính xác AI, kết luận 80–150 chữ,
  mandatory disclosure theo mẫu và phần chữ ký.

Các mục trên là yêu cầu của chính sách/biểu mẫu AI. Không được dùng chúng để suy
ra toàn bộ deliverable của HW05 Performance Testing.

### 1.2. Nội dung không phải bằng chứng về yêu cầu của đề

Trong `ai/ai-audit-report.md`, phần output AI cũ có nhắc đến JMX, JTL, HTML
report, CSV, báo cáo Markdown/PDF, endurance result, screenshot, video,
continuous-performance proposal, Agent Skill, Git log, README và GitHub Issues.
Đây là **output do AI tạo** và danh sách trạng thái/thiếu sót của một repository
khác (`HW05-23127116`), không phải nguyên văn đề hoặc rubric. Do đó chưa thể đánh
dấu các mục này là deliverable bắt buộc của Version 1.0 từ nguồn hiện có.

Muốn chốt danh sách deliverable bắt buộc, cần bổ sung vào repository ít nhất một
trong các nguồn chính thức sau: đề Version 1.0, rubric Version 1.0, hoặc link/file
LMS do giảng viên cung cấp.

## 2. Kiểm tra ba lựa chọn endpoint group

| Scenario | Lựa chọn | Đánh giá kỹ thuật | Xác nhận theo đề Version 1.0 |
| --- | --- | --- | --- |
| Load | `GET /api/products` — read-heavy | **Phù hợp về ngữ nghĩa**: thao tác GET đọc danh sách/tìm kiếm sản phẩm và không thể hiện ghi dữ liệu trong mô tả hiện có. | **Chưa thể xác nhận** vì thiếu đề/rubric và source/API spec trong repository. |
| Stress | `POST /api/register` — auth-heavy | **Phù hợp có điều kiện**: đăng ký thuộc workflow tài khoản/xác thực và tạo user; tuy nhiên đây không phải thao tác login/token verification theo nghĩa hẹp. | **Chưa thể xác nhận** taxonomy “auth-heavy” của đề có bao gồm registration hay không. |
| Spike | `POST /api/admin/coupons` — transactional | **Phù hợp về ngữ nghĩa**: tạo coupon là thao tác ghi có thay đổi trạng thái; output AI cũ mô tả một lần insert database. | **Chưa thể xác nhận** vì source/API spec và định nghĩa nhóm của đề không có trong repository. |

### Kết luận về “đúng ba endpoint group”

Ba lựa chọn là **ba endpoint khác nhau** và các nhãn được đề xuất cũng là **ba
nhóm khác nhau**: read-heavy, auth-heavy và transactional. Xét theo ngữ nghĩa API
thông thường, cách phân nhóm là hợp lý. Tuy nhiên chưa đủ bằng chứng để tuyên bố
“đúng theo Version 1.0”; đặc biệt mapping Register → auth-heavy cần đối chiếu định
nghĩa/rubric chính thức.

Ngoài ra, chưa có tài liệu chính thức trong repository để kiểm tra quy tắc mỗi
scenario phải dùng đúng một group, group có được trùng nhau hay không, hoặc thành
viên trong nhóm có được chọn trùng endpoint/workflow hay không.

## 3. Phân biệt nguồn yêu cầu, hướng dẫn và mẫu

| Nội dung | Phân loại | Cách sử dụng |
| --- | --- | --- |
| Dòng “Phụ lục bắt buộc…” trong `ai/ai-audit-report.md` | Yêu cầu của **chính sách AI** | Áp dụng khi bài có dùng AI; không đại diện cho toàn bộ đề HW05. |
| Mục “Hướng dẫn (đọc trước khi điền)” | Hướng dẫn điền biểu mẫu | Dùng để hoàn thiện AI Audit Report. |
| Các hàng Artifact trống, câu kết luận in nghiêng, mandatory disclosure | Mẫu/placeholder | Phải thay/điền bằng nội dung thật; không coi là kết quả đã hoàn thành. |
| Prompt và output dài trong Artifact #1 | Nội dung AI cũ | Chỉ là nguồn tham khảo cần kiểm chứng; không phải yêu cầu chính thức. |
| Danh sách “Artifact thiếu” trong output AI cũ | Nhận định trạng thái của AI | Không dùng làm deliverable bắt buộc nếu chưa đối chiếu đề/rubric. |
| Ba scenario trong prompt của Artifact #1 | Lựa chọn do người dùng đưa cho AI kiểm tra | Không chứng minh đề Version 1.0 bắt buộc đúng ba mapping này. |

## 4. Giới hạn của bước này

- Không tạo hoặc sửa JMeter plan.
- Không chạy smoke, load, stress, spike hay endurance test.
- Không dùng kết quả/artifact từ repository có tên gần giống
  `C:\Users\nguye\Documents\GitHub\HW05-23127116` để thay cho nguồn chính thức
  trong repository được yêu cầu.
- Khi đề/rubric Version 1.0 được bổ sung, cần rà soát lại mục 1 và cột “Xác nhận
  theo đề Version 1.0” ở mục 2.
