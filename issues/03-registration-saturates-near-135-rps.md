# Registration calibration plateaus near 135 requests/s

JMeter 5.6.3/Temurin 17 and EShop ran on one Windows laptop. This is environment/profile-specific, not a guarantee.

| Users | Throughput | p95 | Errors |
|---:|---:|---:|---:|
| 25 | 53.598 RPS | 40.95 ms | 0.000% |
| 100 | 134.958 RPS | 833.60 ms | 0.000% |
| 200 | 135.065 RPS | 1,691.50 ms | 0.000% |
| 400 | 137.503 RPS | 6,014.60 ms | 3.463% |

Throughput is flat from 100 to 200 users while p95 doubles. At 400 users, throughput gains only 1.8%, p95 exceeds 6 seconds, and connection-refused errors appear. The differently configured official 400-user run had 0% errors but failed latency with p95 2,473.40 ms.

The observed saturation region begins between 100 and 200 users. SQLite/database is not asserted as the root cause without profiling.
