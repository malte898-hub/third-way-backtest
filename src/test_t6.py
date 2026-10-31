"""T6 target substitution. Frozen share 40%, source=default."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import (
    REPORT_DIR,
    RESULTS,
    T4_STEP,
    T4_WINDOW,
    T6_BTC_START,
    T6_FWD,
    T6_SHARE_MIN,
)
from src.charts_r3 import line_chart
from src.panel import monthly_panel, targets_at, x_row
from src.util import add_months, dump_csv, ols, partial_r2, standardize_cols


def _build(rows, ykey, with_move, with_bill, min_ym=None):
    by = {r["ym"]: r for r in rows}
    Y, X, used = [], [], []
    for r in rows:
        ym = r["ym"]
        if min_ym and ym < min_ym:
            continue
        ym3 = add_months(ym, -3)
        if ym3 not in by:
            continue
        xs = x_row(r, by[ym3], with_move, with_bill)
        if xs is None:
            continue
        tg = targets_at(by, ym, T6_FWD)
        if tg is None or tg.get(ykey) is None:
            continue
        Y.append(tg[ykey])
        X.append(xs)
        used.append(ym)
    return used, Y, X


def _rolling(used, Y, X):
    recs = []
    for end in range(T4_WINDOW - 1, len(used), T4_STEP):
        lo = end - T4_WINDOW + 1
        y = Y[lo : end + 1]
        xs = standardize_cols(X[lo : end + 1])
        fit = ols(y, xs, True)
        if fit is None:
            continue
        pr = [partial_r2(y, xs, j) for j in range(3)]
        if any(p is None for p in pr):
            continue
        recs.append({
            "end_ym": used[end],
            "start_ym": used[lo],
            "pr1": pr[0],
            "pr2": pr[1],
            "pr3": pr[2],
            "dominant": ["X1", "X2", "X3"][max(range(3), key=lambda j: pr[j] or -1)],
            "r2": fit["r2"],
        })
    return recs


def _share_x3(recs, want=("X3",)):
    xs = [r for r in recs if r["end_ym"] >= "2021-01"]
    if not xs:
        return 0.0, 0
    n = sum(1 for r in xs if r["dominant"] in want)
    return n / len(xs), len(xs)


def run() -> dict:
    rows = monthly_panel()
    targets = [
        ("y1", "d10y", ("X3",), None),
        ("y2", "d_slope", ("X3",), None),
        ("y3", "tsy_ret", ("X3",), None),
        ("y4", "btc", ("X3", "X2"), T6_BTC_START),
    ]
    out = {
        "acm": "skipped — NY Fed ACM file is Excel (.xls), not keyless CSV",
        "source": "default",
        "criterion": f"X3 (or X2 for y4) largest partial R2 in >={T6_SHARE_MIN:.0%} of windows ending 2021→",
        "caveat": "reserves and yields share the Fed reaction function; a positive result is consistent with reverse causation",
        "targets": {},
    }
    all_verdicts = []
    for ykey, name, want, min_ym in targets:
        used, Y, X = _build(rows, ykey, True, True, min_ym)
        rec = _rolling(used, Y, X)
        dump_csv(
            RESULTS / f"t6_{ykey}_rolling.csv",
            rec,
            ["end_ym", "start_ym", "pr1", "pr2", "pr3", "dominant", "r2"],
        )
        sh, n = _share_x3(rec, want)
        # also no-MOVE
        used2, Y2, X2 = _build(rows, ykey, False, True, min_ym)
        rec2 = _rolling(used2, Y2, X2)
        sh2, n2 = _share_x3(rec2, want)
        verdict = "PASS" if sh >= T6_SHARE_MIN and n > 0 else "FAIL"
        if n == 0:
            verdict = "UNPROVEN"
        all_verdicts.append(verdict)
        out["targets"][ykey] = {
            "name": name,
            "verdict": verdict,
            "share_X3or_want_2021_withMOVE": sh,
            "n_2021_withMOVE": n,
            "want": list(want),
            "share_withoutMOVE": sh2,
            "n_withoutMOVE": n2,
            "n_windows": len(rec),
            "date_range": f"{used[0]} → {used[-1]}" if used else None,
        }
        if rec:
            series = [
                ("X1", [(i, r["pr1"]) for i, r in enumerate(rec)]),
                ("X2", [(i, r["pr2"]) for i, r in enumerate(rec)]),
                ("X3", [(i, r["pr3"]) for i, r in enumerate(rec)]),
            ]
            line_chart(REPORT_DIR / f"t6_{ykey}.png", series, f"T6 {ykey} ({name}) partial R2")
    fails = [k for k, v in out["targets"].items() if v["verdict"] == "FAIL"]
    out["verdict"] = "FAIL" if fails else ("PASS" if all(v == "PASS" for v in all_verdicts) else "MIXED")
    out["reason"] = "; ".join(
        f"{k} {v['verdict']} share={v['share_X3or_want_2021_withMOVE']:.1%} n={v['n_2021_withMOVE']}"
        for k, v in out["targets"].items()
    )
    return out
