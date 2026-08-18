# HW05 Performance Testing — 23127116

This repository contains a Version 1.0 performance-testing submission for EShop. No SUT source code is copied or modified here.

## Verified result snapshot

| Scenario | Endpoint | Key result |
|---|---|---|
| Load | `GET /api/products` | 1,045 samples, 0%, p95 3 ms |
| Stress | `POST /api/register` | 11,213 samples, 0%, p95 2,473.40 ms — latency fail |
| Spike | `POST /api/admin/coupons` | burst p95 1,316.10 ms; recovery p95 17.80 ms |
| Endurance | `GET /api/products` | post-ramp 481.001 RPS, p95 4 ms, 0% |

## Artifact map

- `test-plans/`, `data/`: JMeter plans and separate datasets.
- `results/`, `html-reports/`: raw JTL and generated dashboards.
- `evidence/`: environment, calibration, official resource/log summaries.
- `analysis/`: verified summary, AI claim audit and optimization review.
- `ai/`: first pass, critique, prompt-level interactions and Audit Report.
- `issues/`: evidence-backed drafts; not automatically published.
- `continuous-performance/`: proposed CI performance flow.
- `agent-skill/`: validated reusable JTL analyzer.
- `report/`: main Markdown report.

## Reproduce analysis

Use Python 3 standard library:

```powershell
python agent-skill/analyze-jmeter-performance/scripts/analyze_jtl.py results/23127116_Spike_20260818.jtl --label "SPIKE POST /api/admin/coupons" --format json
python agent-skill/analyze-jmeter-performance/scripts/analyze_jtl.py results/23127116_Endurance_20260818.jtl --warmup-seconds 30 --format json
```

##  Assessment Template

| **No.** | **Criteria** | **Grade** | **Self-Assessed Grade** |
| --- | --- | --- | --- |
| **1** | Task 1 — Load testing | 20 | 20 |
| **2** | Task 1 — Stress testing | 20 | 20 |
| **3** | Task 1 — Spike testing | 20 | 20 |
| **4** | Task 2 — AI analysis + misinterpretation hunt (with correct values from raw logs) | 10 | 10 |
| **5** | Task 3 — Continuous Performance Testing proposal (G9.6) | 10 | 10 |
| **6** | Agent Skills | 10 | 10 |
|  | **Total** | **100** | 100 |

## Self-assessment and incomplete manual items



The automated/test-analysis portion is evidence-backed and reproducible. The repository is **not submission-ready** until the student adds uniqueness evidence, simultaneous run screenshots, public GitHub/Issue URLs, a ≥6-minute Vietnamese Unlisted video URL, and a personally reviewed signature. These are intentionally not fabricated.

- Public repository: **TODO**
- Video: **TODO**
- Issue URLs: **TODO**
- Student signature: **TODO**
