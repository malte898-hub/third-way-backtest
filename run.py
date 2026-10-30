#!/usr/bin/env python3
"""Entry point. python run.py --from-cache | --fetch"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from constants import REPORT_DIR, RESULTS
from src import test_t1, test_t2, test_t3, test_t4, test_t5


def write_report(out: dict) -> None:
    t1, t2, t3, t4, t5 = out["T1"], out["T2"], out["T3"], out["T4"], out["T5"]
    sh = t4.get("without_MOVE") or {}
    lines = []
    lines.append("# Testing the Third Monetary Regime")
    lines.append("")
    lines.append("Independent research. Not investment advice. No positions implied.")
    lines.append("")
    lines.append("## Scoreboard (round 2)")
    lines.append("")
    lines.append("| Test | Frozen criterion | Result | Reason |")
    lines.append("|---|---|---|---|")
    lines.append(f"| T1 haven inversion | ≥80% of 1990–2018 worst-week mean Δ10y < 0; ≥60% of 2020–2026 > 0; corr sign-flip 2018–21 | {t1['verdict']} | {t1['reason']} |")
    lines.append(f"| T2 plumbing episodes | FIRST_MOVER RATE_EXP→VOL/FUN; RESOLVER RATE→QE_QT→PLUMBING | {t2['verdict']} | {t2['reason']} |")
    lines.append(f"| T3 corridor | R3 ratio > 1.5, p<0.05, R3>R1 | {t3['verdict']} | {t3['reason']} |")
    lines.append(f"| T4 horse race | X1 / X2 / X3 majority in R1 / R2 / R3 windows | {t4['verdict']} | {t4['reason']} |")
    lines.append(f"| T5 breaks | 2008 and 2019–20 ±18m, not elsewhere | {t5['verdict']} | {t5['reason']} |")
    lines.append("")
    lines.append("## Round-1 changelog (same frozen cut-offs)")
    lines.append("")
    lines.append("| Test | Round 1 | Round 2 |")
    lines.append("|---|---|---|")
    lines.append("| T1 | FAIL (62% / 57%, flip 2019-07-29) | FAIL (same criterion; instruments unchanged for T1) |")
    lines.append("| T2 equity-def | FAIL (FM FUN/FUN/RATE_EXP; RES all RATE) | FAIL kept; plumbing pass-path on RESOLVER only |")
    lines.append("| T2 plumbing-def | — | FAIL n=80; RESOLVER RATE→QE_QT→PLUMBING+QE_QT |")
    lines.append("| T3 | FAIL R3 ratio 0.98 p=0.73; R1 no power | FAIL R3 1.19 p=0.054; R1 ratio 5.64 p=0.001 |")
    lines.append("| T4 | UNPROVEN (X1 pre-2008 n=0, MOVE starts 2002) | UNPROVEN no-MOVE X1 52.5% / X2 50% / X3 1.6% |")
    lines.append("| T5 | FAIL 2008-10, 2013-10, 2020-02 | FAIL 2020-02, 2007-07, 2012-07; placebo p≈0.73 |")
    lines.append("")
    lines.append("## Key numbers")
    lines.append("")
    lines.append(json.dumps({k: {kk: vv for kk, vv in v.items() if not str(kk).startswith("_")} for k, v in out.items()}, indent=2, default=str))
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "REPORT.md").write_text("\n".join(lines) + "\n")
    print("wrote", REPORT_DIR / "REPORT.md")


def from_cache() -> dict:
    t1 = test_t1.run()
    t2 = test_t2.run()
    t3 = test_t3.run()
    t4 = test_t4.run()
    t5 = test_t5.run(t4)
    t4.pop("_xy_nomove", None)
    out = {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5}
    write_report(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--from-cache", action="store_true")
    g.add_argument("--fetch", action="store_true")
    args = ap.parse_args()
    if args.fetch:
        print("Rebuild data/ from public sources (slow, rate-limited).")
        print("See DATA.md. This snapshot already contains derived CSVs.")
        print("CPI: src/fetch_fed.py fetch_cpi_bls(); markets: src/fetch_market.py yahoo_history().")
        print("H.15/H.41/H.3: Federal Reserve DDP zip (rel=H15, H41, H3).")
        print("Then re-run: python run.py --from-cache")
        return 0
    from_cache()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
