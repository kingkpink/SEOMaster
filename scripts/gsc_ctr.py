#!/usr/bin/env python3
"""Flag CTR underperformers in a Google Search Console Performance export.

Input: the CSV that GSC's Performance report exports (Pages or Queries tab)
with columns like: Top pages/Top queries, Clicks, Impressions, CTR, Position.
Column detection is case-insensitive and tolerant of ordering.

Benchmarks mirror ctr-optimization.md (heuristics, as of 2026).

Usage:
  python3 scripts/gsc_ctr.py Pages.csv
  python3 scripts/gsc_ctr.py Queries.csv --min-impressions 200
"""

import argparse
import csv
import sys

# (max_position_inclusive, action_threshold_ctr_percent)
THRESHOLDS = [
    (1.5, 20.0),
    (2.5, 10.0),
    (3.5, 6.0),
    (5.5, 3.0),
    (10.5, 1.0),
]
DEFAULT_MIN_IMPRESSIONS = 100


def threshold_for(position: float) -> float | None:
    for max_pos, ctr in THRESHOLDS:
        if position <= max_pos:
            return ctr
    return None  # position > 10: fix ranking before CTR


def parse_number(raw: str) -> float:
    cleaned = raw.replace("%", "").replace(",", "").strip()
    return float(cleaned) if cleaned else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="GSC CTR underperformer report")
    parser.add_argument("csv_file")
    parser.add_argument("--min-impressions", type=int, default=DEFAULT_MIN_IMPRESSIONS)
    args = parser.parse_args()

    with open(args.csv_file, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            sys.exit("empty CSV")
        cols = {name.lower(): name for name in reader.fieldnames}

        def col(*candidates: str) -> str:
            for c in candidates:
                if c in cols:
                    return cols[c]
            sys.exit(f"column not found: {candidates} in {reader.fieldnames}")

        key_col = col("top pages", "top queries", "page", "query", "url")
        imp_col = col("impressions")
        ctr_col = col("ctr")
        pos_col = col("position", "average position")

        flagged = []
        for row in reader:
            impressions = parse_number(row[imp_col])
            if impressions < args.min_impressions:
                continue
            position = parse_number(row[pos_col])
            ctr = parse_number(row[ctr_col])
            threshold = threshold_for(position)
            if threshold is not None and ctr < threshold:
                flagged.append((row[key_col], impressions, position, ctr, threshold))

    if not flagged:
        print(f"No underperformers at >= {args.min_impressions} impressions. ")
        return

    flagged.sort(key=lambda r: -r[1])
    print(f"{len(flagged)} CTR underperformers (>= {args.min_impressions} impressions):\n")
    print(f"{'impressions':>12}  {'pos':>5}  {'ctr':>6}  {'bench':>6}  page/query")
    for key, impressions, position, ctr, threshold in flagged:
        print(f"{impressions:>12.0f}  {position:>5.1f}  {ctr:>5.1f}%  {threshold:>5.1f}%  {key}")
    print("\nFix order: rewrite title (front-load keyword, add number/date),")
    print("then description, then eligible structured data. See ctr-optimization.md.")


if __name__ == "__main__":
    main()
