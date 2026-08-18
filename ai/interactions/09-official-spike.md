# Interaction 09 — Run and assess the official Spike test

## Prompt

Run the official three-phase Spike scenario for `POST /api/admin/coupons`: baseline at 5 users, a sudden 200-user spike, and recovery at 5 users. Keep credentials outside tracked files, save JTL/HTML/resource evidence, compare each phase independently, and clean up generated coupons without changing SUT source code.

## AI response/action

I supplied the demo admin credentials only as process environment variables and ran JMeter non-GUI. I separated samples by their explicit phase labels instead of averaging the entire test. Baseline p95 was 18.00 ms, spike p95 was 1,316.10 ms, and recovery p95 was 17.80 ms; all three phases had 0% errors. Recovery throughput (4.642 requests/s) was also comparable to baseline (4.605 requests/s). I classified this run as recovered, with the conclusion scoped to this environment and execution. After capture, 1,417 generated `PERF_` coupons were deleted and none remained.

## Human verification / decision

- Inspect the HTML dashboard and capture the rubric-required screenshot manually.
- Retain phase-specific metrics; do not use the all-samples average as the recovery proof.
- Keep credentials out of commits and reports.

## Artifacts

- `results/23127116_Spike_20260818.jtl`
- `html-reports/spike/index.html`
- `evidence/spike/resources-20260818.csv`
- `evidence/spike/spike-summary-20260818.md`
