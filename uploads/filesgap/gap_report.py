#!/usr/bin/env python3
"""Market gap analysis: aggregates missing-skill frequency across the latest
scan so you can see what the MARKET keeps asking for that the CV lacks.
Run after any scan:  python gap_report.py"""
import collections
import json
import sys

try:
    jobs = json.load(open("reports/latest.json", encoding="utf-8"))
except FileNotFoundError:
    sys.exit("reports/latest.json not found — run a scan first")

gaps = collections.Counter()
hard = collections.Counter()
for j in jobs:
    for m in j.get("missing", []):
        name = m.replace(" (hard req)", "")
        gaps[name] += 1
        if "(hard req)" in m:
            hard[name] += 1

lines = [f"# Market Gap Report", "",
         f"Missing-skill frequency across **{len(jobs)} scanned jobs** "
         f"(latest scan). Hard-requirement count in brackets.", ""]
for name, n in gaps.most_common(15):
    lines.append(f"- **{name}** — {n}x [{hard.get(name, 0)} hard]")
lines += ["", "_High count + high hard = the market's loudest ask. "
          "Your own insight applies: 'hard' in a JD is often aspirational — "
          "check the REVIEW band before treating it as a blocker._", ""]
import os
os.makedirs("reports", exist_ok=True)
with open("reports/gaps.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("\n".join(lines))
print("\n  -> written to reports/gaps.md")
