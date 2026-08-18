#!/usr/bin/env python3
"""Compute reproducible metrics from a CSV-format Apache JMeter JTL file."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    if len(ordered) == 1:
        return ordered[0]
    rank = (p / 100.0) * (len(ordered) - 1)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (rank - lower) * (ordered[upper] - ordered[lower])


def metrics(label: str, rows: list[dict[str, str]]) -> dict[str, object]:
    elapsed = [float(row["elapsed"]) for row in rows]
    start = min(float(row["timeStamp"]) for row in rows)
    end = max(float(row["timeStamp"]) + float(row["elapsed"]) for row in rows)
    duration = max((end - start) / 1000.0, 0.001)
    errors = sum(row["success"].strip().lower() != "true" for row in rows)
    return {
        "label": label,
        "samples": len(rows),
        "errors": errors,
        "error_rate_percent": round(errors / len(rows) * 100.0, 4),
        "duration_seconds": round(duration, 3),
        "throughput_rps": round(len(rows) / duration, 3),
        "average_ms": round(sum(elapsed) / len(elapsed), 2),
        "min_ms": round(min(elapsed), 2),
        "p50_ms": round(percentile(elapsed, 50), 2),
        "p90_ms": round(percentile(elapsed, 90), 2),
        "p95_ms": round(percentile(elapsed, 95), 2),
        "p99_ms": round(percentile(elapsed, 99), 2),
        "max_ms": round(max(elapsed), 2),
    }


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"timeStamp", "elapsed", "label", "success"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required JTL columns: {sorted(missing)}")
        return list(reader)


def as_markdown(items: Iterable[dict[str, object]]) -> str:
    headers = [
        "Label", "Samples", "Errors", "Error %", "RPS", "Average ms",
        "p50", "p90", "p95", "p99", "Max",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for item in items:
        values = (
            item["label"], item["samples"], item["errors"],
            item["error_rate_percent"], item["throughput_rps"],
            item["average_ms"], item["p50_ms"], item["p90_ms"],
            item["p95_ms"], item["p99_ms"], item["max_ms"],
        )
        lines.append("| " + " | ".join(str(value) for value in values) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jtl", type=Path)
    parser.add_argument("--label", help="Analyze only this exact JMeter label")
    parser.add_argument("--warmup-seconds", type=float, default=0.0)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    rows = load_rows(args.jtl)
    if not rows:
        raise SystemExit("JTL contains no samples")

    initial_start = min(float(row["timeStamp"]) for row in rows)
    cutoff = initial_start + args.warmup_seconds * 1000.0
    rows = [row for row in rows if float(row["timeStamp"]) >= cutoff]
    if args.label:
        rows = [row for row in rows if row["label"] == args.label]
    if not rows:
        raise SystemExit("No samples remain after applying filters")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["label"]].append(row)
    output = [metrics(label, group) for label, group in sorted(grouped.items())]

    if args.format == "json":
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(as_markdown(output))


if __name__ == "__main__":
    main()

