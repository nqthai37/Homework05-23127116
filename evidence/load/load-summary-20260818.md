# Official Load summary - 2026-08-18

- Endpoint: `GET /api/products`.
- Configuration: 20 users, 30-second ramp-up, 120-second duration, randomized
  think time 1-3 seconds.
- Raw JTL: `results/23127116_Load_20260818.jtl`.
- HTML report: `html-reports/load/index.html`.
- Resource log: `evidence/load/resources-20260818.csv`.

| Samples | Errors | Error rate | Throughput | Average | p50 | p90 | p95 | p99 | Maximum |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,045 | 0 | 0.000% | 8.914 RPS | 1.61 ms | 2 ms | 2 ms | 3 ms | 3 ms | 28 ms |

The resource log contains 45 observations. Backend working set averaged 53.64 MB
and peaked at 57.60 MB. Whole-system CPU averaged 18.04%; it includes JMeter and
other laptop activity and is not attributed solely to the backend.

The run met the working Load criteria of error rate below 1% and p95 below two
seconds. Throughput reflects the configured user think time and must not be
reported as the read endpoint's capacity ceiling.
