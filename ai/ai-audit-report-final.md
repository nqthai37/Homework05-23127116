# AI Audit Report — HW05 Performance Testing

## Student information

| Field | Value |
|---|---|
| Student | NGUYỄN QUANG THÁI |
| Student ID | 23127116 |
| Class | 23KTPM2 |
| Assignment | HW#05, Version 1.0 |
| Date | 18/08/2026 |
| AI tool | ChatGPT / Codex |
| AI used | Yes |

## Audit method

Each interaction below is evaluated independently. Full prompt/output/action records are preserved under `ai/interactions/`; raw JTL, resource and source evidence take precedence over AI prose. The existing partially edited `ai/ai-audit-report.md` is preserved and was not overwritten.

## Artifact 01 — Scope and endpoint mapping

1. **Prompt + tool:** Read available HW05 materials, distinguish requirements from templates, list deliverables, and review the Products/Register/Admin-Coupons mapping. ChatGPT, 18/08/2026.
2. **Output:** `STEP_BY_STEP_HW05_V1.0.md`.
3. **Verdict:** **INCOMPLETE**.
4. **Reason:** The first AI response claimed it had read an official Version 1.0 brief although the new repository did not contain that source.
5. **Student correction:** Retained only the technically supported mapping and changed the guide to state that official requirements still require lecturer/TA source verification.

## Artifact 02 — Source review and dynamic API smoke

1. **Prompt + tool:** Verify schema/auth/status/validation/source for the three APIs, then dynamically test Products, duplicate Register, no-token/Admin/normal-user Coupon and exact-ID cleanup. ChatGPT, 18/08/2026.
2. **Output:** `evidence/smoke-test-20260818.md`, `evidence/authorization-test-20260818.md`.
3. **Verdict:** **VALID**.
4. **Reason:** Static and dynamic evidence are separated; duplicate email and missing role enforcement were reproduced and cleaned up without storing secrets.
5. **Student correction:** Verified actual status/body/IDs and retained no JWT/password.

## Artifact 03 — Hardware and environment

1. **Prompt + tool:** Collect hostname, OS/build, hardware, Java/JMeter and SUT Git state using real commands; do not fabricate Task Manager images. ChatGPT, 18/08/2026.
2. **Output:** `evidence/hardware/environment-20260818.md` and hardware images.
3. **Verdict:** **VALID**.
4. **Reason:** Java/JMeter versions and SUT attribution were command-verified.
5. **Student correction:** Selected Temurin 17 for official runs and personally supplied DxDiag/Task Manager screenshots.

## Artifact 04 — Products CSV

1. **Prompt + tool:** Create `data/products.csv` only from search terms dynamically returning non-empty JSON arrays. ChatGPT, 18/08/2026.
2. **Output:** `data/products.csv`.
3. **Verdict:** **VALID**.
4. **Reason:** Five terms returned HTTP 200/non-empty arrays; empty candidates were excluded.
5. **Student correction:** Kept the `search_term` header aligned with JMX and added no invented product data.

## Artifact 05 — Registration CSV

1. **Prompt + tool:** Create safe registration data using `example.invalid`, cleanup prefixes and runtime UUID uniqueness. ChatGPT, 18/08/2026.
2. **Output:** `data/register_users.csv`.
3. **Verdict:** **VALID**.
4. **Reason:** Runtime `${email_prefix}_${__UUID}@${email_domain}` prevents recycled CSV rows from reusing identities.
5. **Student correction:** Limited cleanup to `perf_register_*@example.invalid`.

## Artifact 05A — Coupons CSV

1. **Prompt + tool:** Create coupon data from the real schema with runtime UUID codes and document actual backend validation. ChatGPT, 18/08/2026.
2. **Output:** `data/coupons.csv`.
3. **Verdict:** **VALID**.
4. **Reason:** Values fit the current route; `PERF_` codes support safe cleanup; output does not invent validation.
5. **Student correction:** Scoped claims to coupon creation and noted that only `code` has a UNIQUE constraint.

## Artifact 05B — Load JMX and baseline

1. **Prompt + tool:** Create a Products-only Load plan with relative CSV, configurable workload, assertions and Aggregate Report; run a small baseline. ChatGPT, 18/08/2026.
2. **Output:** Load JMX and baseline JTL.
3. **Verdict:** **VALID**.
4. **Reason:** XML/JMeter validation passed and 19/19 baseline samples passed assertions.
5. **Student correction:** Replaced weak string checks with a top-level non-empty JSON-array assertion.

## Artifact 05C — Stress JMX and calibration

1. **Prompt + tool:** Create Register Stress plan, calibrate 25/100/200/400 users, save JTL/resources and clean generated users. ChatGPT, 18/08/2026.
2. **Output:** Stress JMX and `evidence/calibration/stress-plancheck-summary-20260818.md`.
3. **Verdict:** **VALID**.
4. **Reason:** Throughput plateau and p95 growth are supported by raw calibration data.
5. **Student correction:** Did not equate zero errors with acceptable latency or assert an unprofiled root cause.

## Artifact 05D — Spike JMX and baseline

1. **Prompt + tool:** Create Coupon Spike plan with one setup login, secret-safe token sharing, phase labels, assertions and cleanup. ChatGPT, 18/08/2026.
2. **Output:** Spike JMX, baseline JTL/log and cleanup script.
3. **Verdict:** **VALID**.
4. **Reason:** Setup and three measured phases are separate; baseline passed and no JWT was committed.
5. **Student correction:** Disabled View Results Tree for the official non-GUI run to avoid listener overhead.

## Artifact 06 — Baseline and calibration

1. **Prompt + tool:** Run fresh Load/Stress/Spike baselines, Stress 25/100/200/400 calibration and Products 25/50/100 calibration; use unique paths and infer saturation from throughput plus p95. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `ai/interactions/06-baseline-and-calibration.md` and `evidence/calibration/`.
3. **Verdict:** **INCOMPLETE**.
4. **Reason:** New JTL/resource artifacts exist; Stress plateaus around 135 RPS and Products throughput plateaus from 50 to 100 users. Two zero-sample attempts are explicitly retained as failed attempts.
5. **Student correction:** Corrected the PowerShell property-expansion error, reran into fresh paths, and selected 50 users conservatively.

## Artifact 07 — Official Load

1. **Prompt + tool:** Run 20 users, 30-second ramp, 120-second Load with 1–3 second think time; save raw and resource evidence. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `ai/interactions/07-official-load.md`, official Load JTL/HTML/resources.
3. **Verdict:** VALID.
4. **Reason:** 1,045 samples, 0 errors, 8.914 RPS and p95 3 ms recalculate from raw JTL.
5. **Student correction:** Throughput is described as workload-limited, not endpoint capacity.

## Artifact 08 — Official Stress

1. **Prompt + tool:** Run 400 users, 20-second ramp, 60-second Registration Stress; assess errors and latency separately; clean generated users. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `ai/interactions/08-official-stress.md`, official Stress evidence.
3. **Verdict:** VALID.
4. **Reason:** 11,213 samples and 0 errors coexist with p95 2,473.40 ms; therefore latency fails despite availability.
5. **Student correction:** Rejected a zero-error-only pass; verified 11,213 generated users were deleted.

## Artifact 09 — Official Spike

1. **Prompt + tool:** Run baseline 5, spike 200 and recovery 5 users for coupon creation; exclude setup login and clean test coupons. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `ai/interactions/09-official-spike.md`, phase-labeled evidence.
3. **Verdict:** VALID.
4. **Reason:** Phase p95 values are 18.00, 1,316.10 and 17.80 ms with no errors; setup login is excluded.
5. **Student correction:** Used phase labels rather than the misleading whole-plan average; removed 1,417 generated coupons.

## Artifact 10 — Official Endurance

1. **Prompt + tool:** Run 50 users for at least 10 minutes, exclude 30-second ramp-up, inspect time windows and backend memory. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `ai/interactions/10-official-endurance.md`, Endurance JTL/HTML/resources.
3. **Verdict:** VALID with scope limitation.
4. **Reason:** Post-ramp result is 274,040 samples, 481.001 RPS, p95 4 ms and no errors. Backend working-set first/last minute averages differ by 0.20 MB.
5. **Student correction:** Reported final-window p95 drift to 8 ms and limited the conclusion to 10 minutes.

## Artifact 11 — First-pass JTL analysis

1. **Prompt + tool:** Analyze all four JTLs, state formulas/assumptions, preserve the first pass, and do not intentionally create errors. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `ai/ai-jtl-analysis.md`; interaction record `ai/interactions/11-first-pass-jtl-analysis.md`.
3. **Verdict:** VALID with clarification.
4. **Reason:** Values reproduce raw JTL calculations; threshold and optimization claims are qualified.
5. **Student correction:** Kept the first pass unchanged and moved comparability/causality corrections to a separate review.

## Artifact 12 — Human and optimization review

1. **Prompt + tool:** Audit every claim using labels/timestamps/resources/source/schema; classify seven optimization proposals and specify before/after evidence. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `analysis/results-summary.md`, `analysis/ai-misinterpretation-review.md`, `analysis/optimization-review.md`.
3. **Verdict:** VALID.
4. **Reason:** The review does not invent AI errors and distinguishes observation, feasibility and proof.
5. **Student correction:** Rejected redundant coupon indexing, generic pooling and unsupported extra RAM; retained WAL/email indexing only as experiments.

## Artifact 13 — Proposal and critique

1. **Prompt + tool:** Propose continuous performance gates/cadence/noise handling and write a 200–300-word evidence-based English critique. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** `continuous-performance/proposal.md`, `ai/ai-critique.md`, `ai/interactions/13-proposal-and-critique.md`.
3. **Verdict:** VALID.
4. **Reason:** The flow contains filter, skip, isolated SUT, gates, repetitions, two-of-three, warning/block and retention. Critique length is 259 words.
5. **Student correction:** Clearly labeled the pipeline as a proposal, not an implementation.

## Artifact 14 — Issue drafts

1. **Prompt + tool:** Draft only issues supported by dynamic or performance evidence; sanitize secrets and cleanup details. Tool: ChatGPT/Codex, 18/08/2026.
2. **Output:** Three Markdown drafts under `issues/`; interaction record `ai/interactions/14-evidence-backed-issues.md`.
3. **Verdict:** VALID as drafts.
4. **Reason:** Duplicate email and role authorization were dynamically reproduced; saturation uses new calibration and official JTL.
5. **Student correction:** Did not publish issues or invent URLs; avoided asserting a database root cause.

## Artifact 15 — Agent Skill

1. **Prompt + tool:** Create and officially validate a reusable JTL analyzer; reproduce one Spike phase and Endurance post-ramp metric. Tool: ChatGPT/Codex with skill-creator, 18/08/2026.
2. **Output:** `agent-skill/analyze-jmeter-performance/`, `ai/interactions/15-agent-skill.md`.
3. **Verdict:** VALID.
4. **Reason:** Official validator returned `Skill is valid!`; results match independent calculations.
5. **Student correction:** Did not treat the first missing-PyYAML validator attempt as success; reran with the local validator dependency.

## Artifact 16 — Step-level AI Audit

1. **Prompt + tool:** Create one five-part audit entry per interaction, totals, disclosure and unsigned signature section. ChatGPT/Codex, 18/08/2026.
2. **Output:** Both AI Audit Markdown files.
3. **Verdict:** **INCOMPLETE**.
4. **Reason:** Technical audit content is complete, but AI cannot perform the student's personal review/signature.
5. **Student correction:** Student must enter lecturer/date and personally sign before submission.

## Artifact 17 — Main report, README and video script

1. **Prompt + tool:** Compile verified report/README, PDF builder and a Vietnamese video script of at least six minutes while preserving manual TODOs. ChatGPT/Codex, 18/08/2026.
2. **Output:** `report/main-report.md`, `README.md`, `video-script.md`, PDF builder.
3. **Verdict:** **INCOMPLETE**.
4. **Reason:** Metrics are verified, but video/repository/Issue URLs and simultaneous scenario images remain missing.
5. **Student correction:** Student must create and verify those public/manual artifacts.

## Artifact 18 — Manual evidence inventory

1. **Prompt + tool:** Inventory personal evidence and public URLs without manufacturing missing items. ChatGPT/Codex, 18/08/2026.
2. **Output:** `MANUAL_EVIDENCE_REQUIRED.md`.
3. **Verdict:** **VALID**.
4. **Reason:** It accurately separates existing hardware evidence from missing uniqueness/scenario/video/URL/signature evidence.
5. **Student correction:** Use the checklist before signing and packaging.

## Artifact 19 — PDF and submission audit

1. **Prompt + tool:** Build/render/inspect both PDFs, verify text/secrets/Git and do not create a final ZIP while blockers remain. ChatGPT/Codex with PDF workflow, 18/08/2026.
2. **Output:** Two PDFs and `SUBMISSION_READINESS.md`.
3. **Verdict:** **INCOMPLETE**.
4. **Reason:** Four Main Report and three Audit pages passed layout QA, but mandatory manual evidence is incomplete.
5. **Student correction:** Added the missing flowchart, removed a hard-coded demo credential from the old cleanup script and correctly withheld the ZIP.

## Accuracy summary

| Verdict | Count |
|---|---:|
| VALID | 18 |
| VALID after correction / with clarification | 0 |
| INVALID | 0 |
| INCOMPLETE | 5 |

Total audited artifacts: **23**. VALID: **18 (78.26%)**. INVALID: **0 (0%)**. INCOMPLETE: **5 (21.74%)**.

## Human-use conclusion (111 words)

AI hữu ích khi tạo cấu trúc JMeter, tính lại percentile, tổ chức evidence và đề xuất giả thuyết có thể kiểm tra. Tuy nhiên, AI không nên được dùng như nguồn xác nhận yêu cầu chính thức, bằng chứng thực thi hoặc nguyên nhân gốc. Trong bài này, raw JTL cho thấy Stress có 0% lỗi nhưng vẫn thất bại về p95; phase labels sửa cách hiểu Spike; timestamps loại ramp-up khỏi Endurance; source/schema loại các optimization chung chung. Vì vậy, output AI chỉ được chấp nhận sau khi đối chiếu với request/response thật, source, schema, resource CSV và thời lượng test. Ảnh, URL công khai, video và chữ ký phải do sinh viên tự tạo và xác nhận.

## Mandatory disclosure

> Báo cáo, JMeter plan, script phân tích, dataset, issue draft và proposal này được sinh phiên bản đầu bởi ChatGPT/Codex; tôi đã rà soát và chỉnh sửa phase boundary, ramp-up, percentile, threshold, cleanup, source/schema reasoning và optimization claims; tôi bổ sung dynamic authorization/duplicate evidence và manual screenshots. AI Audit Report chi tiết đính kèm ở Phụ lục A. Tôi cam đoan không dùng AI để giả mạo execution evidence, public URL, video hoặc chữ ký.

## Student signature

| Field | Value |
|---|---|
| Student | NGUYỄN QUANG THÁI |
| Student ID | 23127116 |
| Class | 23KTPM2 |
| Lecturer | Hồ Tuấn Thanh |
| Signing date | 18/08/2026 |
| Signature | NGUYỄN QUANG THÁI |
