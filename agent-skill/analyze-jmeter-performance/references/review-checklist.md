# Performance Analysis Review Checklist

## Metric scope

- Confirm whether throughput covers the whole plan or one label/phase.
- Separate setup, baseline, spike and recovery samples.
- Exclude the documented warm-up period when reporting steady-state endurance.
- State the percentile method when reproducing p95/p99 outside JMeter.
- Pair throughput with latency and error acceptance criteria.

## Test validity

- Check response assertions, not only HTTP transport success.
- Identify data collisions, account lockout and authentication failures separately
  from capacity failures.
- Confirm CSV rows and generated identifiers are unique where the SUT requires it.
- Record whether load generator and SUT shared hardware.
- Compare resource trends over time, not only a single peak screenshot.

## Causal claims

- Do not infer a database, CPU, memory or network bottleneck from latency alone.
- Require source/config evidence that a proposed component actually exists.
- Treat cache, connection pool, index and WAL suggestions as hypotheses until a
  controlled before/after benchmark reproduces improvement.
- Reject redundant recommendations such as indexing an already unique column.

## Human-review finding format

1. AI claim.
2. Exact raw-log value and label/filter used.
3. Why the interpretation is incorrect or incomplete.
4. Corrected conclusion.
5. Additional evidence required for causality.

