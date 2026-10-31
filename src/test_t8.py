"""T8 MOVE-management footprint. source=default. PASS needs 2 of 3."""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import (
    DATA,
    REPORT_DIR,
    RESULTS,
    T8_BETA_DROP,
    T8_DLAGS,
    T8_EXCL_HI,
    T8_EXCL_LO,
    T8_PMAX,
    T8_R2_HI,
    T8_R2_LO,
    T8_R3_LO,
    T8_ROLL_STD_M,
    T8_VOL_DROP,
)
from src.charts_r3 import three_panel
from src.panel import monthly_panel
from src.util import add_months, dump_csv, fnum, load_csv, mean, monday_week, ols, ols_hac, parse_d, stdev_p, wald_sum


def _in_era(ym, lo, hi):
    return lo <= ym <= hi


def _excl(ym):
    return T8_EXCL_LO <= ym <= T8_EXCL_HI


def _weekly():
    """Weekly MOVE and |Δ10y|."""
    move = {}
    for r in load_csv(DATA / "market_weekly.csv"):
        if r.get("freq") != "W":
            continue
        v = fnum(r.get("move"))
        if v is None:
            continue
        move[parse_d(r["date"])] = v
    y10 = {}
    for r in load_csv(DATA / "h15_daily.csv"):
        v = fnum(r.get("y10"))
        if v is None:
            continue
        d = parse_d(r["date"])
        wk = monday_week(d)
        y10[wk] = v  # last write of the week if we iterate sorted
    # rebuild last y10 per week properly
    buckets = {}
    for r in load_csv(DATA / "h15_daily.csv"):
        v = fnum(r.get("y10"))
        if v is None:
            continue
        d = parse_d(r["date"])
        wk = monday_week(d)
        buckets.setdefault(wk, []).append((d, v))
    y10 = {wk: sorted(pts)[-1][1] for wk, pts in buckets.items()}
    weeks = sorted(set(move) & set(y10))
    recs = []
    prev_m = prev_y = None
    for w in weeks:
        m, y = move[w], y10[w]
        if prev_m is not None:
            recs.append({
                "date": w.isoformat(),
                "ym": w.strftime("%Y-%m"),
                "dmove": m - prev_m,
                "abs_d10y": abs(y - prev_y),
            })
        prev_m, prev_y = m, y
    return recs


def _beta(pairs):
    if len(pairs) < 20:
        return None
    y = [p[0] for p in pairs]
    X = [[p[1]] for p in pairs]
    fit = ols(y, X, True)
    if fit is None:
        return None
    return {"beta": fit["beta"][1], "n": fit["n"], "r2": fit["r2"]}


def _dlags(rows, ym_list, xkey, ykey="dmove"):
    by = {r["ym"]: r for r in rows}
    Y, X = [], []
    used = []
    for ym in ym_list:
        yv = by.get(ym, {}).get(ykey)
        if yv is None:
            continue
        xs = []
        ok = True
        for k in range(1, T8_DLAGS + 1):
            p = by.get(add_months(ym, -k))
            if not p or p.get(xkey) is None:
                ok = False
                break
            xs.append(p[xkey])
        if not ok:
            continue
        Y.append(yv)
        X.append(xs)
        used.append(ym)
    fit = ols_hac(Y, X, True)
    if fit is None:
        return None
    idx = list(range(1, T8_DLAGS + 1))  # skip intercept
    w = wald_sum(fit, idx)
    return {"n": fit["n"], "sum": w["sum"], "p": w["p"], "t": w["t"]}


def run() -> dict:
    rows = monthly_panel()
    # monthly ΔMOVE, Δlog res, Δbill
    by = {r["ym"]: r for r in rows}
    mrows = []
    prev = None
    for r in rows:
        rec = {"ym": r["ym"], "move": r["move"], "dmove": None, "dlog_res": None, "dbill": None}
        if prev:
            if r["move"] is not None and prev["move"] is not None:
                rec["dmove"] = r["move"] - prev["move"]
            if r["reserves"] and prev["reserves"] and r["reserves"] > 0 and prev["reserves"] > 0:
                rec["dlog_res"] = math.log(r["reserves"]) - math.log(prev["reserves"])
            if r["bill_share"] is not None and prev["bill_share"] is not None:
                rec["dbill"] = r["bill_share"] - prev["bill_share"]
        mrows.append(rec)
        prev = r
    bym = {r["ym"]: r for r in mrows}

    def era_months(lo, hi, drop_excl):
        out = []
        for r in mrows:
            ym = r["ym"]
            if not (lo <= ym <= hi):
                continue
            if drop_excl and _excl(ym):
                continue
            out.append(ym)
        return out

    def roll_std(yms):
        vals = []
        dms = [(ym, bym[ym]["dmove"]) for ym in yms if bym[ym]["dmove"] is not None]
        for i in range(T8_ROLL_STD_M - 1, len(dms)):
            window = [dms[j][1] for j in range(i - T8_ROLL_STD_M + 1, i + 1)]
            vals.append(stdev_p(window))
        return mean(vals) if vals else float("nan"), len(vals)

    results = {}
    for tag, drop in (("full", False), ("ex_covid", True)):
        r2m = era_months(T8_R2_LO, T8_R2_HI, drop)
        r3m = era_months(T8_R3_LO, "2026-12", drop)
        s2, n2 = roll_std(r2m)
        s3, n3 = roll_std(r3m)
        a_ok = s3 == s3 and s2 == s2 and s2 > 0 and s3 <= s2 * (1.0 - T8_VOL_DROP)
        results[tag] = {
            "a_std_R2": s2,
            "a_std_R3": s3,
            "a_n_R2": n2,
            "a_n_R3": n3,
            "a_drop": None if not s2 else 1.0 - s3 / s2,
            "a_pass": a_ok,
        }

        wk = _weekly()
        def wera(lo, hi):
            xs = []
            for r in wk:
                ym = r["ym"]
                if not (lo <= ym <= hi):
                    continue
                if drop and _excl(ym):
                    continue
                xs.append((r["dmove"], r["abs_d10y"]))
            return xs
        b2 = _beta(wera(T8_R2_LO, T8_R2_HI))
        b3 = _beta(wera(T8_R3_LO, "2026-12"))
        b_ok = (
            b2 is not None
            and b3 is not None
            and b2["beta"] > 0
            and b3["beta"] <= b2["beta"] * (1.0 - T8_BETA_DROP)
        )
        results[tag]["b_beta_R2"] = None if b2 is None else b2["beta"]
        results[tag]["b_beta_R3"] = None if b3 is None else b3["beta"]
        results[tag]["b_n_R2"] = None if b2 is None else b2["n"]
        results[tag]["b_n_R3"] = None if b3 is None else b3["n"]
        results[tag]["b_drop"] = None if not (b2 and b3 and b2["beta"]) else 1.0 - b3["beta"] / b2["beta"]
        results[tag]["b_pass"] = b_ok

        def c_era(lo, hi):
            yms = era_months(lo, hi, drop)
            return {
                "res": _dlags(mrows, yms, "dlog_res"),
                "bill": _dlags(mrows, yms, "dbill"),
            }
        c2 = c_era(T8_R2_LO, T8_R2_HI)
        c3 = c_era(T8_R3_LO, "2026-12")

        def c_hit(block):
            # negative and p<0.05 for BOTH series in R3; NOT in R2
            def ok(x):
                return x is not None and x["sum"] < 0 and x["p"] < T8_PMAX
            return ok(block["res"]) and ok(block["bill"])

        r3_hit = c_hit(c3)
        r2_hit = c_hit(c2)
        c_ok = r3_hit and not r2_hit
        results[tag]["c_R2"] = c2
        results[tag]["c_R3"] = c3
        results[tag]["c_pass"] = c_ok

        npass = sum(1 for k in ("a_pass", "b_pass", "c_pass") if results[tag][k])
        results[tag]["n_pass"] = npass
        results[tag]["verdict"] = "PASS" if npass >= 2 else "FAIL"

    primary = results["ex_covid"]
    # charts
    r2m = era_months(T8_R2_LO, T8_R2_HI, False)
    r3m = era_months(T8_R3_LO, "2026-12", False)
    std_series = []
    dms = [(i, r["ym"], r["dmove"]) for i, r in enumerate(mrows) if r["dmove"] is not None]
    roll = []
    for i in range(T8_ROLL_STD_M - 1, len(dms)):
        window = [dms[j][2] for j in range(i - T8_ROLL_STD_M + 1, i + 1)]
        roll.append((i, stdev_p(window)))
    three_panel(
        REPORT_DIR / "t8_move.png",
        [
            ("12m std ΔMOVE", [("std", roll)]),
            ("weekly β |Δ10y| (levels not shown)", [("dummy", [(0, 0.0), (1, primary.get("b_beta_R2") or 0), (2, primary.get("b_beta_R3") or 0)])]),
            ("identification: lower R3 vol also ZIRP/FG", [("std", roll)]),
        ],
    )
    dump_csv(RESULTS / "t8_summary.csv", [
        {"era": tag, **{k: v for k, v in blob.items() if k not in ("c_R2", "c_R3")}}
        for tag, blob in results.items()
    ], ["era", "a_std_R2", "a_std_R3", "a_drop", "a_pass", "b_beta_R2", "b_beta_R3", "b_drop", "b_pass", "c_pass", "n_pass", "verdict"])

    return {
        "verdict": primary["verdict"],
        "source": "default",
        "scored_sample": "R2/R3 with 2020-03→2021-12 excluded",
        "n_of_3": primary["n_pass"],
        "a": {k: primary[k] for k in primary if k.startswith("a_")},
        "b": {k: primary[k] for k in primary if k.startswith("b_")},
        "c": {
            "pass": primary["c_pass"],
            "R2": primary["c_R2"],
            "R3": primary["c_R3"],
        },
        "full": {k: results["full"][k] for k in ("a_pass", "b_pass", "c_pass", "verdict", "n_pass")},
        "criterion": "2 of 3: R3 12m std(ΔMOVE) −20%; R3 weekly β(ΔMOVE,|Δ10y|) −20%; R3 d-res/d-bill lags→ΔMOVE negative p<0.05, not R2",
        "identification": "lower vol in R3 is also consistent with ZIRP and forward guidance; the exclusion window is partial mitigation, not a fix",
        "reason": f"{primary['n_pass']}/3 on exclusion sample; a={primary['a_pass']} b={primary['b_pass']} c={primary['c_pass']}",
    }
