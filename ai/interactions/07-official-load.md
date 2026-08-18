# Interaction 07 - Official Load

## (1) Prompt and tool

- Tool: Codex.
- Date: 2026-08-18.
- Prompt:

> Run only Bước 7 official Load using 20 users, 30-second ramp-up, 120-second
> duration and 1-3 second think time. Run JMeter non-GUI with resource monitoring,
> create a new JTL and HTML report, refuse to overwrite existing output, calculate
> metrics from raw JTL, do not commit and stop before Stress.

## (2) AI output

- `results/23127116_Load_20260818.jtl`.
- `html-reports/load/`.
- `evidence/load/resources-20260818.csv`.
- `evidence/load/load-20260818-jmeter.log`.
- `evidence/load/load-summary-20260818.md`.

Result: 1,045 samples, 0 errors, 8.914 RPS, average 1.61 ms, p95 3 ms and
maximum 28 ms.

## (3) Verdict

**VALID.**

## (4) Reason

The JTL contains the expected endpoint label, all HTTP/business assertions
passed, the HTML report opens successfully and independently calculated metrics
match the run evidence. The resource monitor ran concurrently.

## (5) Student-reviewed correction

Use the result as official Load evidence, but describe 8.914 RPS as the expected
workload rate created by think time rather than a capacity threshold. The student
still needs to capture the required same-frame scenario screenshot.
