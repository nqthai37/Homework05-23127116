---
name: analyze-jmeter-performance
description: Analyze Apache JMeter CSV-format JTL logs, compute per-label latency percentiles, throughput and error rate, separate multi-phase Load/Stress/Spike/Endurance results, and challenge unsupported AI performance conclusions. Use when reviewing JMeter raw logs, comparing scenarios, finding metric misinterpretations, proposing thresholds, or judging optimization recommendations against source and resource evidence.
---

# Analyze JMeter Performance

## Workflow

1. Preserve each raw JTL and identify whether it is CSV or XML. Use this skill's
   script only for CSV JTL containing at least `timeStamp`, `elapsed`, `label`,
   and `success`.
2. Run the analyzer once for the whole file and once per meaningful label or
   phase. For an endurance result, run again with the known warm-up/ramp period
   excluded.
3. Compare error rate and latency to explicit acceptance criteria. Never treat
   0% errors alone as a pass.
4. Read `references/review-checklist.md` before accepting causal explanations or
   optimization proposals.
5. Cite the JTL path, sample count and exact corrected value in every human-review
   finding.

## Analyze a JTL

Use the bundled standard-library Python script:

```bash
python scripts/analyze_jtl.py results.jtl
python scripts/analyze_jtl.py results.jtl --label "SPIKE POST /api/resource"
python scripts/analyze_jtl.py endurance.jtl --warmup-seconds 30 --format json
```

The script computes sample count, errors, error rate, duration, throughput,
average, min, p50, p90, p95, p99 and max for every label. Percentiles use linear
interpolation over sorted elapsed values.

## Review AI conclusions

For each AI claim, produce:

- the original claim;
- the exact raw-log value and calculation scope;
- the interpretation error;
- the corrected conclusion;
- the evidence still missing for causal claims.

Separate setup, baseline, burst and recovery labels in Spike tests. Separate
ramp-up from steady state in Endurance tests. Explain when throughput is capped
by pacing rather than server capacity.

## Judge recommendations

Inspect the SUT's actual database, middleware, queries and deployment before
classifying a recommendation. Use `feasible`, `conditional/unsupported`, or
`hallucinated/redundant`. Require a controlled before/after benchmark for every
performance optimization.

## Output requirements

Never fabricate a JTL, resource measurement, screenshot, threshold or causal
explanation. Clearly distinguish observation from inference and proposal.

