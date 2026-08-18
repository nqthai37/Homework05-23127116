# Human review of the first-pass AI analysis

| AI claim | Raw value / check | Problem | Corrected conclusion |
|---|---|---|---|
| Load p95 is 3 ms and throughput 8.914 RPS. | 1,045 samples; think time 1–3 s. | Correct, but RPS is workload-limited. | Keep metrics; do not call 8.914 RPS the capacity ceiling. |
| Stress has 0% errors but p95 2,473.40 ms. | 11,213 samples, zero failures. | Correct. Zero errors do not override latency failure. | Fail the 2-second latency gate; separately pass the error gate. |
| Calibration plateaus near 135 RPS. | 100/200 users: 134.958/135.065 RPS; official: 183.877 under a different profile. | Correct for calibration only. | Call 135 RPS an observed calibration plateau, not universal capacity. |
| Spike recovered. | Phase p95: 18.00/1,316.10/17.80 ms; setup is separate. | Correct; the first pass did not merge phases. | Keep phase-specific conclusion scoped to this run. |
| Endurance excludes 30 s ramp. | 274,040 samples; p95 4 ms; 481.001 RPS. | Correct. | Use post-ramp values for sustained thresholds. |
| Final endurance window shows drift. | Window 1 p95 2 ms; window 5 p95 8 ms. | Correct observation, not a root cause/leak proof. | Report small drift and retain the 10-minute scope. |
| Candidate optimizations may help. | JTL has timings, not profiles/query plans. | Correctly qualified as experiments. | Require source/schema review and before/after measurement. |

Mandatory checks passed: average was not called p95; denominators are label-specific; Spike phases were not merged; Endurance ramp-up was excluded; duplicate email is a functional defect, not a performance error; no observation became a proven cause; and proposed thresholds are tied to maintained load.

Verdict: **VALID with scope clarifications**. No numerical AI error was invented.
