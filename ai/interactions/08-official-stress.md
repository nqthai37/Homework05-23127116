# Interaction 08 — Run and assess the official Stress test

## Prompt

Run the official Stress scenario against `POST /api/register` with 400 users, 20-second ramp-up, 60-second duration, and 100–500 ms pacing. Save a fresh JTL, HTML dashboard, JMeter log, and system-resource CSV. Do not modify the SUT. Analyze saturation using throughput and tail latency as well as error rate, then clean up generated users.

## AI response/action

I ran JMeter in non-GUI mode and collected backend working-set, system CPU, available-memory, and disk counters in parallel. The JTL contained 11,213 samples with no errors and 183.877 requests/s. Despite the zero error rate, p95 reached 2,473.40 ms and p99 reached 2,802.76 ms. I therefore classified the run as failing the 2-second latency criterion rather than claiming that zero errors meant the system was healthy. After evidence capture, 11,213 uniquely prefixed test users were removed and the cleanup check found zero remaining matches.

## Human verification / decision

- Verify the JMeter HTML dashboard opens and matches the JTL-derived metrics.
- Capture the required dashboard screenshot manually if the rubric requires one.
- Keep the conclusion that 400 users is an overload point for acceptable latency.
- Do not treat the cleanup operation as a change to SUT source code; it only removes generated test data.

## Artifacts

- `results/23127116_Stress_20260818.jtl`
- `html-reports/stress/index.html`
- `evidence/stress/resources-20260818.csv`
- `evidence/stress/stress-summary-20260818.md`
