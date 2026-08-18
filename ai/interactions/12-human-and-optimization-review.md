# Interaction 12 — Human claim audit and optimization review

## Prompt

Audit every first-pass claim using raw JTL labels/timestamps, resources, source and schema. Check averages/percentiles, denominators, phases, ramp-up, functional versus performance defects, causality and sustained thresholds. Classify proposed optimizations and specify before/after evidence.

## Output / verdict / correction

Outputs: `analysis/results-summary.md`, `analysis/ai-misinterpretation-review.md`, `analysis/optimization-review.md`. Verdict: **VALID**. Review tightened comparability/scope; coupon indexing is redundant, pooling mismatches SQLite, and extra RAM is unsupported.
