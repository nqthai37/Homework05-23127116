# Optimization review against source, schema, and evidence

SUT reference: commit `85af3ba875c88283615e22cb108f13e2fccaf0e9` plus the recorded dirty runtime database. This review proposes experiments only; it does not modify the SUT.

| Proposal | Classification | Evidence and reasoning | Required before/after benchmark |
|---|---|---|---|
| SQLite WAL | Feasible experiment | `database.js:1-5` opens one SQLite database; no WAL PRAGMA was found. JTL cannot prove locking. | Repeat Registration calibration/Spike with fixed data; compare RPS, p95, errors, CPU and disk. |
| Index `users.email` | Feasible, with correctness decision | `database.js:50-60` has no email index/UNIQUE; duplicate registration is reproduced. UNIQUE changes semantics and needs migration; non-unique only helps lookup. | Query plan and login/register benchmark; separately test duplicate semantics/migration. |
| Index `coupons.code` | Redundant | `coupons.code` is `UNIQUE` at `database.js:29-38`; SQLite backs it with an index. | Confirm using `PRAGMA index_list/index_info`; add no duplicate index. |
| Redis product cache | Conditional, currently unsupported | Official Load p95 is 3 ms and Endurance p95 4 ms. Cache adds invalidation/operations cost. | Only after production-like profiling; compare hit rate, p95 and consistency. |
| Database connection pool | Redundant/inapplicable as stated | The app uses one `sqlite3.Database`, not a client/server driver. | Profile queue/locking first; benchmark an architectural change. |
| Increase RAM | Unsupported | Backend working set was 86.26 vs 86.46 MB first/last post-ramp minute. Host memory includes JMeter/other apps. | Separate generator/SUT; collect RSS/heap/GC before buying resources. |
| Parameterized product search | Security/correctness fix; performance unproven | `server.js:141-155` interpolates `search` into `LIKE '%...%'`; parameterization removes injection risk, not leading-wildcard scans. | Injection tests, query plan and Load/Endurance with a larger table. |

Priority: fix authorization and data-integrity defects; experiment with WAL/email indexing for Registration; retain caching/hardware changes only when profiling supports them.
