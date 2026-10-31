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
from src import test_t1, test_t2, test_t3, test_t4, test_t5, test_t6, test_t7, test_t8


def write_report(out: dict) -> None:
    t1, t2, t3, t4, t5 = out["T1"], out["T2"], out["T3"], out["T4"], out["T5"]
    t6, t7, t8 = out.get("T6") or {}, out.get("T7") or {}, out.get("T8") or {}
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
    lines.append("## Round 3 — tests from the author's reply")
    lines.append("")
    lines.append("Howell did not supply numerical predictions in writing. Every cut-off below is source=default, frozen before the run. T1–T5 constants were not edited.")
    lines.append("")
    lines.append("| Test | Who set it | Frozen value | Result |")
    lines.append("|---|---|---|---|")
    if t6:
        for k, v in (t6.get("targets") or {}).items():
            lines.append(
                f"| T6 {k} ({v.get('name')}) | default | X3 (X2 or X3 for y4) largest partial R² in ≥40% of windows ending 2021→ | {v.get('verdict')} share={v.get('share_X3or_want_2021_withMOVE', 0):.1%} n={v.get('n_2021_withMOVE')} |"
            )
        lines.append(f"| T6 ACM y2b | default | skip if no CSV | skipped (NY Fed ACM is Excel, not CSV) |")
        lines.append(f"| T6 caveat | — | reverse causation | {t6.get('caveat')} |")
    if t7:
        lines.append(
            f"| T7b 2021→ ΔMOVE→SPX | default | best k ∈ [3,9] and partial R² ≥ 2× k=1; flat or k≤2 → FAIL | {t7.get('verdict')} {t7.get('reason')} |"
        )
        lines.append("| T7 p-values | default | none (overlapping forwards) | partial R² only |")
    if t8:
        lines.append(
            f"| T8 MOVE footprint | default | 2 of 3: R3 12m std(ΔMOVE) −20%; R3 weekly β −20%; R3 d-res/d-bill → ΔMOVE negative p<0.05 not R2 | {t8.get('verdict')} {t8.get('reason')} |"
        )
        lines.append(f"| T8 identification | — | exclusion 2020-03→2021-12 is partial mitigation | {t8.get('identification')} |")
    lines.append("")
    expl = (t7 or {}).get("t7a_exploratory") or []
    if expl:
        lines.append("## T7a — exploratory, no frozen criterion")
        lines.append("")
        lines.append(t7.get("t7a_note") or "12 lags scanned, overlapping 6m forwards, n≈64 months in 2021→ — treat as hypothesis-generating.")
        lines.append("")
        lines.append("| Target | X3 k=1 | X3 best k | X3 best | X2 k=1 | X2 best k | X2 best | n |")
        lines.append("|---|---|---|---|---|---|---|---|")
        any_flag = False
        for r in expl:
            def f(x):
                return "—" if x is None else f"{x:.3f}"
            lines.append(
                f"| {r['target']} | {f(r['X3_k1'])} | {r['X3_best_k']} | {f(r['X3_best'])} | "
                f"{f(r['X2_k1'])} | {r['X2_best_k']} | {f(r['X2_best'])} | {r['n']} |"
            )
        lines.append("")
        for r in expl:
            x3b, x2b = r.get("X3_best"), r.get("X2_best")
            if r.get("X3_gt_X2_at_best"):
                any_flag = True
                sent = (
                    f"{r['target']}: X3 best-lag partial R² {x3b:.3f} (k={r['X3_best_k']}) exceeds "
                    f"X2 {x2b:.3f} (k={r['X2_best_k']}). This revisits the round-2 T4 reading that "
                    f"reserve quantity dominated effective liquidity in 2021→ windows."
                )
            else:
                sent = (
                    f"{r['target']}: X2 best-lag partial R² {x2b:.3f} (k={r['X2_best_k']}) is not below "
                    f"X3 {x3b:.3f} (k={r['X3_best_k']}). Does not reverse the round-2 T4 reading."
                )
            lines.append(sent)
            lines.append("")
        if not any_flag:
            lines.append("No target has X3 > X2 at the best lag, so T7a does not reverse the round-2 T4 reading.")
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
    t6 = test_t6.run()
    t7 = test_t7.run()
    t8 = test_t8.run()
    out = {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5, "T6": t6, "T7": t7, "T8": t8}
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
