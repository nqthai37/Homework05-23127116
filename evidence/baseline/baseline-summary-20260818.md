# Baseline plan-check summary - 2026-08-18

## Purpose

These runs validate data loading, authentication, requests, assertions and phase
labels before calibration. They are plan checks, not capacity measurements or
official scenario results.

## Selected baseline evidence

| Plan | Selected JTL | Samples | Errors | Review result |
| --- | --- | ---: | ---: | --- |
| Load | `results/baseline/23127116_Load_plancheck_20260818.jtl` | 19 | 0 | Five expected product-search labels returned successful samples. |
| Stress | `results/baseline/23127116_Stress_plancheck_confirmed_20260818.jtl` | 35 | 0 | Register status/message/id assertions passed. The first connection was an 8,069 ms startup outlier. |
| Spike | `results/baseline/23127116_Spike_plancheck_20260818.jtl` | 11 | 0 | Setup login, baseline, spike and recovery labels all executed successfully. |

## Interpretation

- Load is valid for calibration because the CSV supplied all five search terms
  and every sampler/assertion passed.
- The earlier short Stress attempts produced only one sample because the first
  connection took about eight seconds. The 15-second confirmation run is the
  selected baseline; the earlier attempts remain as diagnostic evidence.
- Spike confirms Admin login/JWT propagation and the three transactional phase
  labels. Its tiny sample counts and startup outliers must not be interpreted as
  performance results.

All three plans therefore passed functional baseline validation. Calibration and
official runs must use separate output files.
