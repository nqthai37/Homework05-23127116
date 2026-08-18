# Kịch bản video HW05 — tối thiểu 6 phút

Trạng thái: kịch bản; video chưa được quay hoặc upload.

## 0:00–0:35 — Giới thiệu

Hiển thị MSSV 23127116, HW05 Version 1.0, repository và commit SUT được kiểm thử. Nói rõ không sửa mã nguồn SUT và ba nhóm là Products/read-heavy, Register/auth-heavy, Admin Coupons/transactional.

## 0:35–1:20 — Dữ liệu và JMX

Mở ba CSV riêng, chỉ ra email/coupon động để không trùng dữ liệu. Mở từng JMX và chỉ ra Thread Group, ramp/duration, assertion, CSV Data Set, timer và listener/report khác nhau. Không hiển thị password/JWT.

## 1:20–2:40 — Load và Stress

Mở JMeter/terminal cùng resource monitor trong một khung hình đối với evidence scenario. Load: 20 users, 120 giây, 1.045 mẫu, p95 3 ms. Stress: 400 users, 11.213 mẫu, 0 lỗi nhưng p95 2.473,40 ms; giải thích vì sao vẫn fail latency. Mở HTML dashboard và resource CSV.

## 2:40–3:35 — Spike

Trình bày ba pha 5 → 200 → 5 users và setup login bị loại. Nêu p95 baseline 18 ms, burst 1.316,10 ms, recovery 17,80 ms; chứng minh recovery bằng phase label, không dùng average toàn plan. Nói rõ 1.417 coupon test đã cleanup.

## 3:35–4:25 — Endurance và tài nguyên

Nêu 50 users được chọn từ calibration, chạy đủ 10 phút. Phân biệt full-run với sau 30 giây ramp: 481,001 RPS, p95 4 ms, 0 lỗi. Trình bày window cuối p95 8 ms và working set đầu/cuối 86,26/86,46 MB. Hiển thị Task Manager và resource CSV; không gán whole-system CPU riêng cho backend.

## 4:25–5:15 — AI review và optimization

Mở `ai/ai-jtl-analysis.md`, rồi file human review. Nói rõ 0% error không đồng nghĩa pass; Spike phải tách phase; Endurance phải bỏ ramp. Trình bày WAL/email index là experiment, coupon index redundant, pool/RAM/Redis chưa có bằng chứng.

## 5:15–5:50 — Issues, proposal và Agent Skill

Mở ba issue draft và các GitHub Issue thật sau khi tự đăng. Mở flowchart continuous testing. Chạy Agent Skill trên Spike label và Endurance warm-up để tái tạo số liệu.

## 5:50–6:20 — Kết luận và disclosure

Mở README, main report và AI Audit. Đọc disclosure, nói rõ phần AI hỗ trợ và phần sinh viên đã kiểm chứng. Hiển thị public repository URL và YouTube Unlisted URL sau khi có.

## Checklist quay thủ công

- JMeter/terminal và resource monitor cùng khung hình cho ba scenario bắt buộc.
- Âm thanh tiếng Việt rõ, thời lượng thực tế ít nhất 6 phút.
- Không lộ JWT/password.
- Upload YouTube Unlisted; thử link trong cửa sổ đăng xuất.
