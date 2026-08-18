# Interaction 10 — Run and assess the official Endurance test

## Prompt

Run a 10-minute Endurance test for `GET /api/products` at the conservative load selected from calibration. Save fresh JTL, HTML, log, and resource artifacts. Exclude ramp-up for steady-state metrics, inspect time-window drift and backend memory, and avoid claiming that a short run proves long-term stability.

## AI response/action

I selected 50 users because calibration showed a throughput plateau from 50 to 100 users while tail latency almost doubled. The official run generated 281,645 successful samples. After excluding the 30-second ramp-up, throughput was 481.001 requests/s, p95 was 4 ms, and the error rate was 0%. Five equal post-ramp windows showed p95 rising from 2 ms in the first window to 8 ms in the final window, with final-window throughput 3.74% below the first. Backend working-set averages were 86.26 MB in the first post-ramp minute and 86.46 MB in the last, so this run did not show material backend-memory growth.

## Human verification / decision

- Accept the 10-minute run as passing the current thresholds.
- Preserve the late-window drift in the report rather than using only aggregate metrics.
- Do not generalize the result to multi-hour or production endurance.
- Capture any dashboard/resource screenshot required by the rubric manually.

## Artifacts

- `results/23127116_Endurance_20260818.jtl`
- `html-reports/endurance/index.html`
- `evidence/endurance/resources-20260818.csv`
- `evidence/endurance/endurance-summary-20260818.md`
