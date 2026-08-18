# Interaction 19 — PDF visual QA and submission audit

## Prompt

Build the Main Report and AI Audit PDFs, render and inspect every page, extract text to verify key metrics, inspect Git/evidence readiness, and do not create a final ZIP while signatures, video, screenshots or public URLs remain missing.

## Output / verdict / correction

Outputs: two draft PDFs under `output/pdf/` and `SUBMISSION_READINESS.md`. Verdict: **INCOMPLETE for final submission; VALID for PDF layout QA**. Four Main Report pages and three Audit pages were visually inspected. A missing flowchart in the first report build was corrected by generating and embedding `assets/continuous-performance-flow.png`, then rebuilding and rechecking every report page. A hard-coded demo credential in an older cleanup script was removed and replaced with mandatory `PSCredential`. No ZIP or commit was created.
