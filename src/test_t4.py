from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import DATA, RESULTS, T4_FWD_MAIN, T4_STEP, T4_UNPROVEN_SHARE, T4_WINDOW
from src.util import (
    add_months,
    dump_csv,
    fnum,
    load_csv,
    logret,
    ols,
    parse_d,
    partial_r2,
    standardize_cols,
)


def month_end_h15(col):
    buckets = defaultdict(list)
    for r in load_csv(DATA / "h15_daily.csv"):
        v = fnum(r.get(col))
        if v is None:
            continue
        d = parse_d(r["date"])
        buckets[d.strftime("%Y-%m")].append((d, v))
    return {ym: sorted(pts)[-1][1] for ym, pts in buckets.items()}


def monthly_rows():
    effr = month_end_h15("effr")
    res = {r["date"][:7]: fnum(r["reserves_mn"]) for r in load_csv(DATA / "h41_h3_reserves.csv")}
    bill = {r["date"][:7]: fnum(r.get("bill_share")) for r in load_csv(DATA / "mspd_bill_share.csv")}
    mkt = [r for r in load_csv(DATA / "market_weekly.csv") if r.get("freq") == "M"]
    spx, move, hyg, lqd = {}, {}, {}, {}
    for r in mkt:
        ym = r["date"][:7]
        if fnum(r.get("spx")) is not None:
            spx[ym] = fnum(r["spx"])
        if fnum(r.get("move")) is not None:
            move[ym] = fnum(r["move"])
        if fnum(r.get("hyg")) is not None:
            hyg[ym] = fnum(r["hyg"])
        if fnum(r.get("lqd")) is not None:
            lqd[ym] = fnum(r["lqd"])
    months = sorted(set(effr) & set(res) & set(spx))
    rows = []
    for ym in months:
        rows.append({
            "ym": ym,
            "effr": effr.get(ym),
            "reserves": res.get(ym),
            "bill_share": bill.get(ym),
            "spx": spx.get(ym),
            "move": move.get(ym),
            "hyg": hyg.get(ym),
            "lqd": lqd.get(ym),
        })
    return rows


def build_xy(rows, fwd, with_move, with_bill):
    by = {r["ym"]: r for r in rows}
    Y, X, used = [], [], []
    for r in rows:
        ym, ym3, ymf = r["ym"], add_months(r["ym"], -3), add_months(r["ym"], fwd)
        if ym3 not in by or ymf not in by:
            continue
        p = by[ym3]
        if None in (r["effr"], p["effr"], r["reserves"], p["reserves"], r["spx"], by[ymf]["spx"]):
            continue
        if r["reserves"] <= 0 or p["reserves"] <= 0:
            continue
        x1 = r["effr"] - p["effr"]
        x2 = math.log(r["reserves"]) - math.log(p["reserves"])
        if with_move:
            if not r["move"] or not p["move"] or r["move"] <= 0 or p["move"] <= 0:
                continue
            liq = r["reserves"] * (100.0 / r["move"])
            liqp = p["reserves"] * (100.0 / p["move"])
            x3 = math.log(liq) - math.log(liqp)
            if with_bill:
                if r["bill_share"] is None or p["bill_share"] is None:
                    continue
                x3 = x3 + (r["bill_share"] - p["bill_share"])
        else:
            x3 = x2
            if with_bill and r["bill_share"] is not None and p["bill_share"] is not None:
                x3 = x2 + (r["bill_share"] - p["bill_share"])
        yv = logret(r["spx"], by[ymf]["spx"])
        if yv is None:
            continue
        Y.append(yv)
        X.append([x1, x2, x3])
        used.append(ym)
    return used, Y, X


def rolling(used, Y, X):
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


def shares(recs):
    def sh(pred, cond):
        xs = [r for r in recs if cond(r)]
        if not xs:
            return 0.0, 0
        return sum(1 for r in xs if r["dominant"] == pred) / len(xs), len(xs)

    s1, n1 = sh("X1", lambda r: r["end_ym"] < "2008-01")
    s2, n2 = sh("X2", lambda r: "2010-01" <= r["end_ym"] <= "2019-12")
    s3, n3 = sh("X3", lambda r: r["end_ym"] >= "2021-01")
    unproven = any(s < T4_UNPROVEN_SHARE for s in (s1, s2, s3))
    ok = s1 > 0.5 and s2 > 0.5 and s3 > 0.5
    verdict = "UNPROVEN" if (unproven and not ok) else ("PASS" if ok else "FAIL")
    if unproven and not ok:
        verdict = "UNPROVEN"
    return {
        "verdict": verdict,
        "share_X1_pre2008": s1,
        "n_pre2008": n1,
        "share_X2_2010_2019": s2,
        "n_2010_2019": n2,
        "share_X3_2021": s3,
        "n_2021": n3,
        "n_windows": len(recs),
    }


def run() -> dict:
    rows = monthly_rows()
    used_m, Ym, Xm = build_xy(rows, T4_FWD_MAIN, True, True)
    rec_m = rolling(used_m, Ym, Xm)
    dump_csv(RESULTS / "t4_rolling.csv", rec_m, ["end_ym", "start_ym", "pr1", "pr2", "pr3", "dominant", "r2"])
    used, Y, X = build_xy(rows, T4_FWD_MAIN, False, True)
    rec = rolling(used, Y, X)
    dump_csv(RESULTS / "t4_rolling_nomove.csv", rec, ["end_ym", "start_ym", "pr1", "pr2", "pr3", "dominant", "r2"])
    sh_m, sh = shares(rec_m), shares(rec)
    return {
        "verdict": sh["verdict"],
        "with_MOVE": sh_m,
        "without_MOVE": sh,
        "criterion": "dominant partial R²: X1 majority windows ending <2008; X2 in 2010–2019; X3 in 2021→",
        "reason": (
            f"no-MOVE X1={sh['share_X1_pre2008']:.1%} n={sh['n_pre2008']}; "
            f"X2={sh['share_X2_2010_2019']:.1%}; X3={sh['share_X3_2021']:.1%}"
        ),
        "_xy_nomove": (used, Y, X),
    }
