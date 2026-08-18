# Interaction 06 - Baseline and calibration evidence

## (1) Prompt and tool

- Tool: Codex.
- Date: 2026-08-18.
- Scope: Bước 6 only; no commit and no official scenario run.
- Prompt:

> Continue from Bước 6 of `REBUILD_REPO_FROM_SCRATCH.md`. Verify the independent
> Load, Stress and Spike baseline JTL files. Preserve the existing Stress
> calibration at 25/100/200/400 users. Run the missing Products capacity
> calibration at 25/50/100 users with separate JTL, JMeter log and resource CSV
> files. Do not overwrite old output. Calculate throughput and p95 from raw JTL,
> identify saturation using throughput plus latency, select a conservative
> Endurance concurrency level and stop before official Load.

## (2) AI output

Verified baseline evidence:

- Load: 19 samples, 0 errors.
- Stress selected confirmation: 35 samples, 0 errors.
- Spike: setup plus three phase labels executed with 0 errors.

Verified existing Registration calibration:

- 25 users: 53.598 RPS, p95 40.95 ms, 0 errors.
- 100 users: 134.958 RPS, p95 833.60 ms, 0 errors.
- 200 users: 135.065 RPS, p95 1,691.50 ms, 0 errors.
- 400 users: 137.503 RPS, p95 6,014.60 ms, 3.463% errors.

Created Products calibration:

- 25 users: 72,935 samples, 2,443.629 RPS, p95 14 ms, 0 errors.
- 50 users: 75,142 samples, 2,518.079 RPS, p95 26 ms, 0 errors.
- 100 users: 75,484 samples, 2,529.031 RPS, p95 50 ms, 0 errors.

Created summaries:

- `evidence/baseline/baseline-summary-20260818.md`.
- `evidence/calibration/stress-plancheck-summary-20260818.md`.
- `evidence/calibration/products-plancheck-summary-20260818.md`.

## (3) Verdict

**INCOMPLETE initially; accepted after correction.**

## (4) Reason

The first Products command passed the literal property
`load_threads=$users`, so JMeter started zero threads. A zero-sample JTL cannot
support any performance conclusion. The sequence was stopped, the invalid files
were moved to `failed-attempts`, and the JMeter log was used to identify the
property-expansion error. The corrected command was validated at 25 users before
50 and 100 users were allowed to run.

The valid data show two different saturation patterns:

- Registration throughput plateaus near 135 RPS between 100 and 200 users while
  p95 rises sharply; 400 users is overload, not an acceptable target.
- Products throughput gains only about 0.44% from 50 to 100 users while p95
  nearly doubles and backend memory increases.

This interpretation uses throughput, latency and errors together instead of
equating zero errors with success.

## (5) Student-reviewed correction

- Exclude every file under `results/failed-attempts/` and
  `evidence/failed-attempts/` from metrics and official reports.
- Use the quoted, expanded JMeter property form such as
  `"-Jload_threads=25"` for future PowerShell commands.
- Select **50 concurrent users** as the conservative Endurance concurrency level.
- Treat short Products throughput near 2,500 RPS as a calibration ceiling, not a
  ten-minute guarantee.
- Derive the final Endurance threshold only from the later ten-minute official
  soak.
