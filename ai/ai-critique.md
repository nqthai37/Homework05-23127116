# AI Critique

AI was useful for turning raw JMeter files into a repeatable analysis, but its output still required human control over scope and causality. The most important risk was treating a zero error rate as proof of acceptable performance. The official Registration Stress run returned no failed samples, yet its p95 was 2,473.40 ms, above the two-second working objective. A separate pass/fail decision for errors and latency corrected that interpretation.

Phase boundaries created another risk. Combining the Spike setup login, baseline, burst, and recovery would have produced a convenient but meaningless average. Reading label-specific samples showed p95 moving from 18.00 ms to 1,316.10 ms and then back to 17.80 ms. Likewise, Endurance needed a post-ramp calculation rather than only the full-run aggregate. Its steady-state p95 was 4 ms, but time windows still exposed a small rise to 8 ms in the final window.

Generic optimization advice was the weakest AI contribution. A new coupon-code index was rejected because the schema already declares the column UNIQUE. A generic database connection pool does not fit the application's single SQLite handle, and more RAM was unsupported because backend working set remained approximately 86 MB after ramp-up. Redis caching was deferred because product-read latency was already very low. WAL mode and an email index remain experiments, not proven fixes. Parameterizing product search is justified for security and correctness, but its performance benefit is unproven.

The practical lesson is that AI can calculate, structure, and suggest hypotheses, while the student must verify raw labels, timestamps, source, schema, resources, and test duration before accepting any conclusion.
