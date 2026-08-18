# First-pass AI analysis of official JTL files

Date: 2026-08-18. This is the preserved first pass produced before reading any human-correction artifact.

## Method and assumptions

For each label, let `N` be its sample count, `E` the count whose `success` field is not `true`, and `t0`/`t1` the earliest sample start and latest sample end. Error rate is `E / N × 100%`; throughput is `N / ((t1 - t0) / 1000)`; average is the arithmetic mean of `elapsed`. Percentiles are calculated from sorted elapsed times with linear interpolation. Spike phases are kept separate by label. Endurance steady state excludes the first 30 seconds.

## Official results

| Scenario / label | Samples | Error rate | RPS | Avg | p50 | p90 | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Load — `GET /api/products` | 1,045 | 0.000% | 8.914 | 1.61 ms | 2 ms | 2 ms | 3 ms | 3 ms | 28 ms |
| Stress — `POST /api/register` | 11,213 | 0.000% | 183.877 | 1,515.37 ms | 1,609 ms | 2,287 ms | 2,473.40 ms | 2,802.76 ms | 3,414 ms |
| Spike baseline — coupon create | 85 | 0.000% | 4.605 | 12.45 ms | 11 ms | 15.60 ms | 18 ms | 31.48 ms | 55 ms |
| Spike burst — coupon create | 1,247 | 0.000% | 140.302 | 390.91 ms | 228 ms | 1,017 ms | 1,316.10 ms | 1,540 ms | 1,606 ms |
| Spike recovery — coupon create | 85 | 0.000% | 4.642 | 9.46 ms | 7 ms | 17 ms | 17.80 ms | 25 ms | 25 ms |
| Endurance — full `GET /api/products` | 281,645 | 0.000% | 469.620 | 2.08 ms | 1 ms | 3 ms | 4 ms | 9 ms | 369 ms |
| Endurance — after 30 s ramp | 274,040 | 0.000% | 481.001 | 2.11 ms | 1 ms | 3 ms | 4 ms | 9 ms | 369 ms |

The strongest official degradation is Registration Stress: p95 is 2.473 seconds despite zero errors. The Spike burst raises p95 sharply but recovers to baseline afterward. Endurance remains fast overall, although its final time window has p95 8 ms versus 2 ms initially.

## Working thresholds

- Error rate: below 1%.
- Interactive latency: p95 below 2,000 ms.
- Registration capacity: calibration suggests a plateau near 135 requests/s between 100 and 200 users; treat this as an observed saturation region, not a guarantee.
- Endurance: 50 users for 10 minutes is supported by this run. A conservative throughput gate could start below the sustained post-ramp rate, for example 430 requests/s, and be re-baselined on a controlled runner.

## First-pass optimization ideas

Candidate experiments are SQLite WAL mode, an index for email lookups, confirming whether `coupons.code` already has an index, parameterizing product search, caching product reads, reviewing database concurrency/pooling, and increasing host resources only if profiling shows pressure. None is a proven root cause from JTL alone; each needs a controlled before/after benchmark.
