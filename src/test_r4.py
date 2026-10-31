"""Round 4: confirmatory OOS of T7a lags. Frozen k and windows. source=default."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import (
    REPORT_DIR,
    RESULTS,
    T6_FWD,
    R4_FIT_HI,
    R4_FIT_LO,
    R4_FWD_END,
    R4_K_10Y,
    R4_K_BTC,
    R4_K_SLOPE,
    R4_K_SPX,
    R4_TEST_HI,
    R4_TEST_LO,
)
from src.charts_r3 import line_chart
from src.panel import monthly_panel, targets_at, x3_legs, x_row
from src.util import add_months, dump_csv, mean, ols
from src.test_t7 import _best, _scan


KS = {"spx": R4_K_SPX, "y2": R4_K_SLOPE, "y1": R4_K_10Y, "y4": R4_K_BTC}
LABEL = {"spx": "SPX", "y2": "slope", "y1": "10y", "y4": "BTC"}


def _xj(by, ym, j):
    ym3 = add_months(ym, -3)
    if ym not in by or ym3 not in by:
        return None
    xs = x_row(by[ym], by[ym3], True, True)
    return None if xs is None else xs[j]


def _leg(by, ym, which):
    ym3 = add_months(ym, -3)
    if ym not in by or ym3 not in by:
        return None
    a, b = x3_legs(by[ym], by[ym3])
    return a if which == "a" else b


def _pairs(by, months, k, ykey, xfun):
    Y, X, used = [], [], []
    for ym in months:
        xv = xfun(by, add_months(ym, -k))
        tg = targets_at(by, ym, T6_FWD)
        yv = None if tg is None else tg.get(ykey)
        if xv is None or yv is None:
            continue
        Y.append(yv)
        X.append([xv])
        used.append(ym)
    return used, Y, X


def _fit_predict(Ytr, Xtr, Yte, Xte):
    fit = ols(Ytr, Xtr, True) if len(Ytr) >= 12 else None
    if fit is None:
        return None
    a, b = fit["beta"][0], fit["beta"][1]
    yhat = [a + b * row[0] for row in Xte]
    sse = sum((yi - yh) ** 2 for yi, yh in zip(Yte, yhat))
    my = mean(Yte)
    tss = sum((yi - my) ** 2 for yi in Yte)
    r2 = None if tss < 1e-18 else 1.0 - sse / tss
    return {"a": a, "b": b, "n_fit": fit["n"], "n_test": len(Yte), "oos_r2": r2, "yhat": yhat}


def run() -> dict:
    rows = monthly_panel()
    by = {r["ym"]: r for r in rows}
    months = [r["ym"] for r in rows]
    fit_m = [m for m in months if R4_FIT_LO <= m <= R4_FIT_HI]
    # last origin with 6m forward in the tape
    test_m = [m for m in months if R4_TEST_LO <= m <= R4_FWD_END]
    yfun = {
        "spx": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("spx"),
        "y1": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y1"),
        "y2": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y2"),
        "y4": lambda by, ym: (targets_at(by, ym, T6_FWD) or {}).get("y4"),
    }
    xfuns = {
        "X1": lambda by, ym: _xj(by, ym, 0),
        "X2": lambda by, ym: _xj(by, ym, 1),
        "X3": lambda by, ym: _xj(by, ym, 2),
    }

    per = {}
    fwd_rows = []
    fit_rows = []
    for ykey, k in KS.items():
        per[ykey] = {"k": k, "label": LABEL[ykey]}
        used_te = None
        Yte = None
        for xn, xf in xfuns.items():
            utr, Ytr, Xtr = _pairs(by, fit_m, k, ykey, xf)
            ute, Yte, Xte = _pairs(by, test_m, k, ykey, xf)
            used_te = ute
            pred = _fit_predict(Ytr, Xtr, Yte, Xte)
            if pred is None:
                per[ykey][xn] = {"oos_r2": None, "n_fit": 0, "n_test": 0}
                continue
            per[ykey][xn] = {
                "oos_r2": pred["oos_r2"],
                "n_fit": pred["n_fit"],
                "n_test": pred["n_test"],
                "a": pred["a"],
                "b": pred["b"],
            }
            fit_rows.append({
                "target": ykey, "x": xn, "k": k,
                "a": pred["a"], "b": pred["b"],
                "n_fit": pred["n_fit"], "n_test": pred["n_test"],
                "oos_r2": pred["oos_r2"],
            })
            yh = pred["yhat"]
            for i, ym in enumerate(ute):
                fwd_rows.append({
                    "ym": ym,
                    "target": ykey,
                    "x": xn,
                    "k": k,
                    "y": Yte[i],
                    "xval": Xte[i][0],
                    "yhat": yh[i],
                })
        r3 = (per[ykey].get("X3") or {}).get("oos_r2")
        r2 = (per[ykey].get("X2") or {}).get("oos_r2")
        r1 = (per[ykey].get("X1") or {}).get("oos_r2")
        per[ykey]["pass_cell"] = (
            r3 is not None and r2 is not None and r3 > r2 and r3 > 0
        )

    spx_ok = per["spx"]["pass_cell"]
    slope_ok = per["y2"]["pass_cell"]
    verdict = "PASS" if spx_ok and slope_ok else "FAIL"

    dump_csv(
        RESULTS / "t7a_oos_fit.csv",
        fit_rows,
        ["target", "x", "k", "a", "b", "n_fit", "n_test", "oos_r2"],
    )
    dump_csv(
        RESULTS / "t7a_forward.csv",
        sorted(fwd_rows, key=lambda r: (r["ym"], r["target"], r["x"])),
        ["ym", "target", "x", "k", "y", "xval", "yhat"],
    )

    # Decomposition: T7a lag scan X3a vs X3b, 2021→, exploratory
    sm = [m for m in months if m >= "2021-01"]
    decomp = {}
    drows = []
    for ykey in KS:
        rec_a = _scan(by, sm, lambda by, ym: _leg(by, ym, "a"), yfun[ykey])
        rec_b = _scan(by, sm, lambda by, ym: _leg(by, ym, "b"), yfun[ykey])
        ba, bb = _best(rec_a), _best(rec_b)
        decomp[ykey] = {
            "X3a_best_k": None if ba is None else ba["k"],
            "X3a_best": None if ba is None else ba["pr2"],
            "X3b_best_k": None if bb is None else bb["k"],
            "X3b_best": None if bb is None else bb["pr2"],
        }
        for r in rec_a:
            drows.append({"y": ykey, "leg": "X3a", **r})
        for r in rec_b:
            drows.append({"y": ykey, "leg": "X3b", **r})
    dump_csv(RESULTS / "t7a_decomp.csv", drows, ["y", "leg", "k", "n", "pr2", "beta"])

    def curve(recs):
        return [(r["k"], r["pr2"] or 0.0) for r in recs]

    line_chart(
        REPORT_DIR / "t7a_decomp.png",
        [
            ("SPX X3a res/MOVE", curve(_scan(by, sm, lambda by, ym: _leg(by, ym, "a"), yfun["spx"]))),
            ("SPX X3b bill", curve(_scan(by, sm, lambda by, ym: _leg(by, ym, "b"), yfun["spx"]))),
            ("slope X3a", curve(_scan(by, sm, lambda by, ym: _leg(by, ym, "a"), yfun["y2"]))),
            ("slope X3b", curve(_scan(by, sm, lambda by, ym: _leg(by, ym, "b"), yfun["y2"]))),
        ],
        "T7a decomp 2021→ partial R2 by k (exploratory)",
    )

    def which_leg(ykey):
        d = decomp[ykey]
        a, b = d["X3a_best"], d["X3b_best"]
        if a is None and b is None:
            return "none"
        if b is None or (a is not None and a >= (b or -1)):
            return "X3a Δlog(reserves/MOVE)"
        return "X3b Δbill share"

    return {
        "verdict": verdict,
        "source": "default",
        "criterion": "X3 OOS R² > X2 OOS R² and > 0 for SPX and slope",
        "fit": f"{R4_FIT_LO}→{R4_FIT_HI}",
        "test": f"{R4_TEST_LO}→{R4_TEST_HI} (origins through {R4_FWD_END})",
        "k": dict(KS),
        "per": per,
        "spx_ok": spx_ok,
        "slope_ok": slope_ok,
        "decomp": decomp,
        "decomp_leg": {LABEL[y]: which_leg(y) for y in KS},
        "reason": (
            f"SPX X3={per['spx'].get('X3', {}).get('oos_r2'):.3f} X2={per['spx'].get('X2', {}).get('oos_r2'):.3f} "
            f"{'ok' if spx_ok else 'fail'}; "
            f"slope X3={per['y2'].get('X3', {}).get('oos_r2'):.3f} X2={per['y2'].get('X2', {}).get('oos_r2'):.3f} "
            f"{'ok' if slope_ok else 'fail'}"
        ),
        "note": "Coefficients frozen on fit window; t7a_forward.csv is the holdout tape (no refit).",
    }
