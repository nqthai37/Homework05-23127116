# Official Stress Test Summary — 2026-08-18

## Configuration

- Endpoint: `POST /api/register`
- Concurrent users: 400
- Ramp-up: 20 seconds
- Hold duration: 60 seconds
- Pacing: 100–500 ms
- Execution mode: JMeter non-GUI
- SUT source code: unchanged

## Results

| Metric | Value |
|---|---:|
| Samples | 11,213 |
| Errors | 0 (0.00%) |
| Measured duration | 60.981 s |
| Throughput | 183.877 requests/s |
| Average | 1,515.37 ms |
| p50 | 1,609.00 ms |
| p90 | 2,287.00 ms |
| p95 | 2,473.40 ms |
| p99 | 2,802.76 ms |
| Maximum | 3,414.00 ms |

## Resource observations

- Resource samples: 26
- Average backend working set: 81.98 MB
- Maximum backend working set: 94.64 MB
- Average system CPU: 25.74%
- Maximum system CPU: 64.13%
- Minimum available memory: 3,598 MB

## Interpretation

The run had no HTTP/application errors, but p95 was 2,473.40 ms and therefore exceeded the 2,000 ms latency threshold used by this submission. The endpoint remained available at 400 users, while latency degradation confirms that this load is beyond the acceptable operating level. Saturation is assessed from both the earlier throughput plateau and the official-run latency, not from error rate alone.

Verdict: **FAIL for latency acceptance; PASS for error-rate acceptance**.

## Traceability

- JTL: `results/23127116_Stress_20260818.jtl`
- HTML dashboard: `html-reports/stress/index.html`
- Resource log: `evidence/stress/resources-20260818.csv`
- JMeter log: `evidence/stress/stress-20260818-jmeter.log`
- Cleanup result: 11,213 generated `perf_register_*@example.invalid` users deleted; zero matching users remained.
