# Registration Stress calibration — plan check 2026-08-18

## Scope

- Plan: `test-plans/23127116_Stress_20260818.jmx`.
- Endpoint: `POST /api/register`.
- Label: `STRESS POST /api/register`.
- Data: `data/register_users.csv` with runtime email
  `${email_prefix}_${__UUID}@${email_domain}`.
- Common calibration settings: ramp-up 5 seconds, duration 30 seconds, uniformly
  distributed pacing 100–500 ms.
- JMeter 5.6.3 with Temurin Java 17.
- SUT and JMeter ran on the same laptop.

These are short calibration runs, not the official Stress run.

## Baseline

The first two 4–5 second attempts each completed only one successful sample
because their initial connection took about 8 seconds. Changing `localhost` to
`127.0.0.1` did not remove the delay, so there was no evidence to change the plan
host. A 15-second confirmation baseline separated this startup effect from later
iterations:

```text
Samples: 35
HTTP/assertion errors: 0
Average: 237 ms
Minimum: 6 ms
Maximum: 8,069 ms (initial connection)
```

No plan change was made for the startup outlier. Test users were cleaned after
the baseline.

## Calibration results

Percentiles use linear interpolation over the sorted JTL `elapsed` values.
Throughput is sample count divided by the interval from the first sample start to
the last sample end.

| Users | Samples | Errors | Error rate | Throughput | Average | p95 | Maximum |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 25 | 1,582 | 0 | 0.000% | 53.598 RPS | 111.17 ms | 40.95 ms | 8,250 ms |
| 100 | 4,059 | 0 | 0.000% | 134.958 RPS | 367.90 ms | 833.60 ms | 8,575 ms |
| 200 | 4,086 | 0 | 0.000% | 135.065 RPS | 1,038.32 ms | 1,691.50 ms | 9,269 ms |
| 400 | 4,274 | 148 | 3.463% | 137.503 RPS | 2,259.90 ms | 6,014.60 ms | 9,848 ms |

All 148 failures at 400 users were connection failures reported as
`HttpHostConnectException: Connection refused`; they also failed the HTTP 200
assertion. The backend was reachable again immediately after the run, so this
evidence shows transient refusal under the tested load, not a proven permanent
process crash.

## Saturation interpretation

- From 25 to 100 users, throughput increased materially.
- From 100 to 200 users, throughput was effectively flat (134.958 to 135.065
  RPS), while p95 more than doubled (833.60 to 1,691.50 ms).
- From 200 to 400 users, throughput increased only about 1.8%, while p95 rose to
  6,014.60 ms and errors appeared.

The observed saturation plateau for this calibration is therefore approximately
**135 RPS**, with the saturation region beginning between **100 and 200 users**.
The 400-user profile is an overload observation, not an acceptable threshold.
Zero errors at 100 or 200 users alone does not establish a pass; latency and the
selected service objective must also be considered.

## Raw evidence

| Users | Raw JTL | Resource CSV | JMeter log |
| ---: | --- | --- | --- |
| 25 | `results/calibration/stress-25-plancheck-20260818.jtl` | `evidence/calibration/stress-25-plancheck-20260818-resources.csv` | `evidence/calibration/stress-25-plancheck-20260818-jmeter.log` |
| 100 | `results/calibration/stress-100-plancheck-20260818.jtl` | `evidence/calibration/stress-100-plancheck-20260818-resources.csv` | `evidence/calibration/stress-100-plancheck-20260818-jmeter.log` |
| 200 | `results/calibration/stress-200-plancheck-20260818.jtl` | `evidence/calibration/stress-200-plancheck-20260818-resources.csv` | `evidence/calibration/stress-200-plancheck-20260818-jmeter.log` |
| 400 | `results/calibration/stress-400-plancheck-20260818.jtl` | `evidence/calibration/stress-400-plancheck-20260818-resources.csv` | `evidence/calibration/stress-400-plancheck-20260818-jmeter.log` |

Each resource CSV contains 17 timestamped observations. Peak backend working set
increased from about 68.02 MB at 25 users to 98.86 MB at 400 users. Backend CPU
fields are blank because the collection account could read process memory but
not `TotalProcessorTime` for the externally owned Node process. System CPU and
disk counters are present; they include JMeter and other machine activity and
must not be attributed solely to the backend.

## Cleanup

`scripts/cleanup-register-users.ps1` authenticates with a caller-supplied
`PSCredential`, selects only emails matching
`^perf_register_.*@example\.invalid$`, deletes each exact returned user ID, and
verifies that no matching user remains. It contains no hard-coded password and
does not query or delete coupons.

Cleanup after the final calibration reported:

```text
MatchedUsers: 4,126
DeletedUsers: 4,126
RemainingMatchingUsers: 0
```
