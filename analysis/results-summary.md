# Verified results summary — 2026-08-18

| Test | Configuration | Key verified result | Decision |
|---|---|---|---|
| Load | 20 users, 30 s ramp, 120 s | 1,045 samples; 0%; 8.914 RPS; p95 3 ms | Pass |
| Stress | 400 users, 20 s ramp, 60 s | 11,213 samples; 0%; 183.877 RPS; p95 2,473.40 ms | Fail latency, pass errors |
| Spike | 5 → 200 → 5 users | p95 18 → 1,316.10 → 17.80 ms; 0% errors | Pass and recovered |
| Endurance | 50 users, 30 s ramp, 600 s | post-ramp 481.001 RPS; p95 4 ms; 0% | Pass for 10 minutes |

Stress calibration—not the differently paced official run—showed a throughput plateau around 135 RPS from 100 to 200 users and overload at 400 users. Endurance backend working-set averages were 86.26 MB in the first post-ramp minute and 86.46 MB in the last. These observations do not identify a root cause.
