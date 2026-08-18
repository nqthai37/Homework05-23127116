# Products capacity calibration - plan check 2026-08-18

## Scope

- Plan: `test-plans/23127116_Load_20260818.jmx`.
- Endpoint/label: `GET /api/products`.
- JMeter: 5.6.3 with Temurin Java 17.0.19+10.
- Common settings: ramp-up 5 seconds, duration 30 seconds, no think time.
- SUT and JMeter ran on the same laptop.

These are short capacity-calibration runs used to select a conservative
Endurance concurrency level. They are not the official Load or Endurance runs.

## Results calculated from raw JTL

| Users | Samples | Errors | Error rate | Throughput | Average | p95 | p99 | Maximum |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 72,935 | 0 | 0.000% | 2,443.629 RPS | 9.32 ms | 14 ms | 18 ms | 79 ms |
| 50 | 75,142 | 0 | 0.000% | 2,518.079 RPS | 18.18 ms | 26 ms | 33 ms | 107 ms |
| 100 | 75,484 | 0 | 0.000% | 2,529.031 RPS | 36.31 ms | 50 ms | 64 ms | 122 ms |

Percentiles use linear interpolation over sorted JTL `elapsed` values.
Throughput is sample count divided by the interval from the first sample start
to the last sample end.

## Resource observations

| Users | Resource samples | Backend working-set average | Backend working-set maximum | Whole-system CPU average | Minimum available RAM |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 14 | 86.28 MB | 86.64 MB | 32.96% | 2,835 MB |
| 50 | 14 | 89.16 MB | 89.38 MB | 32.93% | 2,932 MB |
| 100 | 14 | 108.92 MB | 118.57 MB | 33.04% | 2,715 MB |

Whole-system CPU includes JMeter, the backend and other laptop activity. It
must not be attributed solely to the SUT.

## Saturation and Endurance selection

- From 25 to 50 users, throughput increased about 3.05%, while p95 increased
  from 14 to 26 ms.
- From 50 to 100 users, throughput increased only about 0.44%, while p95 nearly
  doubled from 26 to 50 ms and backend memory increased.
- Short-run read throughput therefore plateaus near 2,500 RPS under this local
  setup.

The conservative Endurance choice is **50 concurrent users**. It achieved within
0.44% of the 100-user throughput with substantially lower p95 and backend memory.
This selects concurrency only; the official Endurance threshold must come from a
separate run sustained for at least ten minutes.

## Raw evidence

| Users | Raw JTL | Resource CSV | JMeter log |
| ---: | --- | --- | --- |
| 25 | `results/calibration/products-25-plancheck-20260818.jtl` | `evidence/calibration/products-25-plancheck-20260818-resources.csv` | `evidence/calibration/products-25-plancheck-20260818-jmeter.log` |
| 50 | `results/calibration/products-50-plancheck-20260818.jtl` | `evidence/calibration/products-50-plancheck-20260818-resources.csv` | `evidence/calibration/products-50-plancheck-20260818-jmeter.log` |
| 100 | `results/calibration/products-100-plancheck-20260818.jtl` | `evidence/calibration/products-100-plancheck-20260818-resources.csv` | `evidence/calibration/products-100-plancheck-20260818-jmeter.log` |
