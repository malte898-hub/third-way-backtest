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
    lines.append("## Scoreboard (round 2.3)")
    lines.append("")
    lines.append("| Test | Frozen criterion | Result | Reason |")
    lines.append("|---|---|---|---|")
    lines.append(f"| T1 haven inversion | ≥80% of 1990–2018 worst-week mean Δ10y < 0; ≥60% of 2020–2026 > 0; corr sign-flip 2018–21 | {t1['verdict']} | {t1['reason']} |")
    lines.append(f"| T2 plumbing episodes | FIRST_MOVER RATE_EXP→VOL/FUN; RESOLVER RATE→QE_QT→PLUMBING | {t2['verdict']} | {t2['reason']} |")
    lines.append(f"| T3 corridor | R3 ratio > 1.5, p<0.05, R3>R1 | {t3['verdict']} | {t3['reason']} |")
    lines.append(f"| T4 horse race | X1 / X2 / X3 majority in R1 / R2 / R3 windows | {t4['verdict']} | {t4['reason']} |")
    lines.append(f"| T5 breaks | 2008 and 2019–20 ±18m, not elsewhere | {t5['verdict']} | {t5['reason']} |")
    lines.append("")
    lines.append("## Round 2 vs 2.2 vs 2.3 (T1/T4/T5 not rerun)")
    lines.append("")
    lines.append("| Test | Round 2 | Round 2.2 | Round 2.3 |")
    lines.append("|---|---|---|---|")
    lines.append("| T1 | FAIL 62% / 57%; flip 2019-07-29 | unchanged | unchanged |")
    lines.append("| T2 plumbing n | 80 | 80 | 80 |")
    lines.append("| T2 plumbing FM | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN |")
    lines.append("| T2 plumbing RES | RATE / QE_QT / PLUMBING | RATE / QE_QT / PLUMBING+RATE | RATE / QE_QT / RATE |")
    lines.append("| T2 equity RES | RATE / QE_QT / RATE | RATE / QE_QT / PLUMBING+RATE | not rerun (press feed has no notes) |")
    lines.append("| T3 n_actions | 78 | 138 | 104 |")
    lines.append("| T3 R1 | 5.64× p=0.001 | 5.64× p=0.001 | 5.64× p=0.001 Puncond=0.010 |")
    lines.append("| T3 R2 | 0.74× p=1.00 | 0.74× p=1.00 | 0.74× p=1.00 Puncond=0.471 |")
    lines.append("| T3 R3 | 1.19× p=0.054 | 1.13× p=0.001; Puncond=0.62 no_power | 1.14× p=0.005 Puncond=0.312 |")
    lines.append("| PLUMBING rows / 60d / 30d | — | 56 / 6 / 52 | 12 / 9 / 9 |")
    lines.append("| T4 | UNPROVEN X1 52.5% / X2 50% / X3 1.6% | unchanged | unchanged |")
    lines.append("| T5 | FAIL 2020-02, 2007-07, 2012-07; placebo p≈0.73 | unchanged | unchanged |")
    lines.append("")
    lines.append("## 2025 vignette (2.1 correction)")
    lines.append("")
    lines.append("Oct–Nov 2025: reserve drain → QT ended 2025-12-01 and reserve-management bill purchases began 2025-12-12, announced at the 2025-10-29 and 2025-12-10 FOMC meetings alongside two 25 bp cuts. First STRESS print 2025-10-15; first plumbing announcement 2025-10-29 (10 sessions).")
    lines.append("")
    lines.append("2025-10-29 statement: \"The Committee decided to conclude the reduction of its aggregate securities holdings on December 1.\"")
    lines.append("")
    lines.append("2025-12-10 statement: \"The Committee judges that reserve balances have declined to ample levels and will initiate purchases of shorter-term Treasury securities…\"")
    lines.append("")
    lines.append("The 2025-10-29 statement gives no money-market attribution; press-conference remarks are not in the corpus.")
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
