# Official Endurance Test Summary — 2026-08-18

## Configuration and rationale

- Endpoint: `GET /api/products`
- Concurrent users: 50
- Ramp-up: 30 seconds
- Scheduled duration: 600 seconds
- Pacing: random 80–120 ms
- Execution mode: JMeter non-GUI
- SUT source code: unchanged

Calibration showed almost no throughput benefit when increasing from 50 to 100 users (+0.44%), while p95 increased from 26 ms to 50 ms. Fifty users was therefore selected as the conservative endurance level.

## Overall and steady-state results

| Scope | Samples | Errors | Throughput | Average | p95 | p99 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full run | 281,645 | 0.00% | 469.620 req/s | 2.08 ms | 4 ms | 9 ms | 369 ms |
| After 30 s ramp-up | 274,040 | 0.00% | 481.001 req/s | 2.11 ms | 4 ms | 9 ms | 369 ms |

## Steady-state time windows

The 570-second post-ramp interval was divided into five equal 114-second windows.

| Window | Samples | Throughput | Average | p95 | Errors |
|---|---:|---:|---:|---:|---:|
| 1 | 56,149 | 492.540 req/s | 0.99 ms | 2 ms | 0 |
| 2 | 56,059 | 491.750 req/s | 1.06 ms | 2 ms | 0 |
| 3 | 53,558 | 469.810 req/s | 2.29 ms | 5 ms | 0 |
| 4 | 54,222 | 475.630 req/s | 1.84 ms | 4 ms | 0 |
| 5 | 54,052 | 474.140 req/s | 4.45 ms | 8 ms | 0 |

The final window had higher latency and 3.74% lower throughput than the first window. The absolute p95 remained only 8 ms and no requests failed, so the run passes the current acceptance thresholds. The increase is reported as a small late-run drift, not hidden by the aggregate.

## Resource observations

- Total resource samples: 153
- Post-ramp resource samples: 141
- First post-ramp minute average backend working set: 86.26 MB
- Last post-ramp minute average backend working set: 86.46 MB
- Post-ramp average backend working set: 85.75 MB
- Maximum backend working set: 86.77 MB
- Post-ramp average system CPU: 23.97%

Backend working set increased only 0.20 MB between the first and last post-ramp minute averages, which does not show a material monotonic backend-memory leak in this 10-minute run. System-level available memory fell substantially and CPU briefly peaked near the end, but these host-wide counters include JMeter and report generation; they cannot be attributed solely to the backend process.

Verdict: **PASS for this 10-minute run**, with a documented small late-window latency drift and no claim about longer-duration behavior.

## Traceability

- JTL: `results/23127116_Endurance_20260818.jtl`
- HTML dashboard: `html-reports/endurance/index.html`
- Resource log: `evidence/endurance/resources-20260818.csv`
- JMeter log: `evidence/endurance/endurance-20260818-jmeter.log`
