# Official Spike Test Summary — 2026-08-18

## Configuration

- Endpoint: `POST /api/admin/coupons`
- Setup: one admin login outside the measured business phases
- Baseline: 5 users, 5-second ramp, 20-second scheduled duration
- Spike: 200 users, 1-second ramp, 10-second scheduled duration, starts at 20 seconds
- Recovery: 5 users, 5-second ramp, 20-second scheduled duration, starts at 30 seconds
- Pacing: 1 second
- SUT source code: unchanged

## Phase results

| Phase | Samples | Errors | Throughput | Average | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 85 | 0.00% | 4.605 req/s | 12.45 ms | 18.00 ms | 31.48 ms | 55 ms |
| Spike | 1,247 | 0.00% | 140.302 req/s | 390.91 ms | 1,316.10 ms | 1,540.00 ms | 1,606 ms |
| Recovery | 85 | 0.00% | 4.642 req/s | 9.46 ms | 17.80 ms | 25.00 ms | 25 ms |

The one setup-login sample took 609 ms and is excluded from the three phase comparisons.

## Resource observations

- Resource samples: 22
- Average backend working set: 71.49 MB
- Maximum backend working set: 88.07 MB
- Average system CPU: 19.88%
- Maximum system CPU: 43.60%
- Minimum available memory: 3,878 MB

## Interpretation

The sudden 200-user phase increased p95 from 18.00 ms to 1,316.10 ms while maintaining a 0% error rate. Recovery p95 returned to 17.80 ms, slightly below the pre-spike baseline, and recovery throughput was comparable to baseline. This supports a recovery claim for this run; it does not prove recovery under every load or environment.

Verdict: **PASS** — no errors, spike p95 remained below 2 seconds, and post-spike latency returned to baseline.

## Traceability

- JTL: `results/23127116_Spike_20260818.jtl`
- HTML dashboard: `html-reports/spike/index.html`
- Resource log: `evidence/spike/resources-20260818.csv`
- JMeter log: `evidence/spike/spike-20260818-jmeter.log`
- Cleanup: 1,417 `PERF_` coupons deleted; zero matching coupons remained.
