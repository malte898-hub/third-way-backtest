"""T7 lag scan. Partial R2 only (overlapping forwards). source=default."""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import (
    REPORT_DIR,
    RESULTS,
    T6_FWD,
    T7_BEST_K_HI,
    T7_BEST_K_LO,
    T7_K_HI,
    T7_K_LO,
    T7_PR2_MULT,
    T7_SAMPLE_A,
    T7_SAMPLE_B,
)
from src.charts_r3 import line_chart
from src.panel import monthly_panel, targets_at, x_row
from src.util import add_months, dump_csv, ols


def _x3_at(by, ym, with_move=True, with_bill=True):
    ym3 = add_months(ym, -3)
    if ym not in by or ym3 not in by:
        return None
    xs = x_row(by[ym], by[ym3], with_move, with_bill)
    return None if xs is None else xs[2]


def _dmove(by, ym):
    prev = add_months(ym, -1)
    if ym not in by or prev not in by:
        return None
    a, b = by[prev].get("move"), by[ym].get("move")
    if a is None or b is None:
        return None
    return b - a


def _dlog_res(by, ym):
    prev = add_months(ym, -1)
    if ym not in by or prev not in by:
        return None
    a, b = by[prev].get("reserves"), by[ym].get("reserves")
    if not a or not b or a <= 0 or b <= 0:
        return None
    return math.log(b) - math.log(a)


def _dbill(by, ym):
    prev = add_months(ym, -1)
    if ym not in by or prev not in by:
        return None
    a, b = by[prev].get("bill_share"), by[ym].get("bill_share")
    if a is None or b is None:
        return None
    return b - a


def _scan(by, months, xfun, yfun):
    recs = []
    for k in range(T7_K_LO, T7_K_HI + 1):
        Y, X = [], []
        for ym in months:
            xym = add_months(ym, -k)
            xv = xfun(by, xym)
            yv = yfun(by, ym)
            if xv is None or yv is None:
                continue
            Y.append(yv)
            X.append([xv])
        fit = ols(Y, X, True) if len(Y) >= 24 else None
        recs.append({
            "k": k,
            "n": len(Y),
            "pr2": None if fit is None else fit["r2"],
            "beta": None if fit is None else fit["beta"][1],
        })
    return recs


def _best(recs):
    ok = [r for r in recs if r["pr2"] is not None]
    if not ok:
        return None
    return max(ok, key=lambda r: r["pr2"])


def run() -> dict:
    rows = monthly_panel()
    by = {r["ym"]: r for r in rows}
    months = [r["ym"] for r in rows]
    samples = {
        "from_2003": [m for m in months if m >= T7_SAMPLE_A],
        "from_2021": [m for m in months if m >= T7_SAMPLE_B],
    }
    ymap = {
        "spx": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("spx"),
        "y1": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y1"),
        "y2": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y2"),
        "y3": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y3"),
        "y4": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y4"),
        "dlog_res": _dlog_res,
        "dbill": _dbill,
    }
    out7a, out7b = {}, {}
    csv_rows = []
    for sname, sm in samples.items():
        out7a[sname], out7b[sname] = {}, {}
        for yname, yfun in ymap.items():
            if yname in ("dlog_res", "dbill"):
                continue
            recs = _scan(by, sm, lambda by, ym: _x3_at(by, ym, True, True), yfun)
            out7a[sname][yname] = recs
            for r in recs:
                csv_rows.append({"branch": "7a", "sample": sname, "y": yname, **r})
        for yname, yfun in ymap.items():
            recs = _scan(by, sm, _dmove, yfun)
            out7b[sname][yname] = recs
            for r in recs:
                csv_rows.append({"branch": "7b", "sample": sname, "y": yname, **r})

    dump_csv(RESULTS / "t7_lags.csv", csv_rows, ["branch", "sample", "y", "k", "n", "pr2", "beta"])

    # prediction: 7b 2021→ ΔMOVE → T4 target (spx); best k in [3,9] and pr2 >= 2 * k=1
    recs = out7b["from_2021"]["spx"]
    best = _best(recs)
    k1 = next((r for r in recs if r["k"] == 1), None)
    ok_k = best is not None and T7_BEST_K_LO <= best["k"] <= T7_BEST_K_HI
    ok_mult = (
        best is not None
        and k1 is not None
        and k1["pr2"] is not None
        and best["pr2"] is not None
        and best["pr2"] >= T7_PR2_MULT * max(k1["pr2"], 1e-12)
    )
    flat = best is not None and k1 is not None and k1["pr2"] is not None and best["pr2"] is not None and best["pr2"] < 1.1 * k1["pr2"]
    fail_k = best is not None and best["k"] <= 2
    verdict_7b = "PASS" if ok_k and ok_mult else "FAIL"
    if flat or fail_k:
        verdict_7b = "FAIL"

    # charts: 7a X3→y1 and 7b ΔMOVE→spx / dlog_res
    def curve(recs):
        return [(r["k"], r["pr2"] or 0.0) for r in recs]

    line_chart(
        REPORT_DIR / "t7a_lags.png",
        [
            ("2003 y1", curve(out7a["from_2003"]["y1"])),
            ("2021 y1", curve(out7a["from_2021"]["y1"])),
            ("2003 spx", curve(out7a["from_2003"]["spx"])),
            ("2021 spx", curve(out7a["from_2021"]["spx"])),
        ],
        "T7a X3 lagged k → targets (partial R2)",
    )
    line_chart(
        REPORT_DIR / "t7b_lags.png",
        [
            ("2021 MOVE→spx", curve(out7b["from_2021"]["spx"])),
            ("2021 MOVE→dlog_res", curve(out7b["from_2021"]["dlog_res"])),
            ("2021 MOVE→dbill", curve(out7b["from_2021"]["dbill"])),
            ("2003 MOVE→spx", curve(out7b["from_2003"]["spx"])),
        ],
        "T7b dMOVE lagged k → targets / liquidity (partial R2)",
    )

    return {
        "verdict": verdict_7b,
        "source": "default",
        "branch_scored": "7b 2021 dMOVE → 6m-forward SPX",
        "best_k": None if best is None else best["k"],
        "best_pr2": None if best is None else best["pr2"],
        "k1_pr2": None if k1 is None else k1["pr2"],
        "criterion": f"7b 2021→ best k in [{T7_BEST_K_LO},{T7_BEST_K_HI}] and pr2 >= {T7_PR2_MULT}× k=1; flat or best k<=2 → FAIL",
        "reason": (
            f"best k={None if best is None else best['k']} pr2={None if best is None else round(best['pr2'],4)}; "
            f"k1 pr2={None if k1 is None else round(k1['pr2'] or 0,4)}"
        ),
        "note": "overlapping 6m-forward windows: partial R2 only, no p-values",
        "7a_best": {s: {y: _best(out7a[s][y]) for y in out7a[s]} for s in out7a},
        "7b_best": {s: {y: _best(out7b[s][y]) for y in out7b[s]} for s in out7b},
    }
