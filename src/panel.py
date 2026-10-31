"""Monthly panel for T4/T6–T8. Stdlib only."""
from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import DATA, T6_DURATION, T6_FWD
from src.util import add_months, fnum, load_csv, logret, parse_d


def _month_end(path, date_key, col):
    buckets = defaultdict(list)
    for r in load_csv(path):
        v = fnum(r.get(col))
        if v is None:
            continue
        d = parse_d(r[date_key])
        buckets[d.strftime("%Y-%m")].append((d, v))
    return {ym: sorted(pts)[-1][1] for ym, pts in buckets.items()}


def monthly_panel() -> list[dict]:
    effr = _month_end(DATA / "h15_daily.csv", "date", "effr")
    y2 = _month_end(DATA / "h15_daily.csv", "date", "y2")
    y10 = _month_end(DATA / "h15_daily.csv", "date", "y10")
    res = {r["date"][:7]: fnum(r["reserves_mn"]) for r in load_csv(DATA / "h41_h3_reserves.csv")}
    bill = {r["date"][:7]: fnum(r.get("bill_share")) for r in load_csv(DATA / "mspd_bill_share.csv")}
    mkt = [r for r in load_csv(DATA / "market_weekly.csv") if r.get("freq") == "M"]
    spx, move = {}, {}
    for r in mkt:
        ym = r["date"][:7]
        if fnum(r.get("spx")) is not None:
            spx[ym] = fnum(r["spx"])
        if fnum(r.get("move")) is not None:
            move[ym] = fnum(r["move"])
    btc = {}
    bp = DATA / "btc_weekly.csv"
    if bp.exists():
        bb = defaultdict(list)
        for r in load_csv(bp):
            v = fnum(r.get("close"))
            if v is None:
                continue
            d = parse_d(r["date"])
            bb[d.strftime("%Y-%m")].append((d, v))
        btc = {ym: sorted(pts)[-1][1] for ym, pts in bb.items()}
    months = sorted(set(effr) | set(res) | set(spx) | set(y10))
    rows = []
    for ym in months:
        rows.append({
            "ym": ym,
            "effr": effr.get(ym),
            "y2": y2.get(ym),
            "y10": y10.get(ym),
            "reserves": res.get(ym),
            "bill_share": bill.get(ym),
            "spx": spx.get(ym),
            "move": move.get(ym),
            "btc": btc.get(ym),
        })
    return rows


def x_row(r, p, with_move: bool, with_bill: bool):
    if None in (r["effr"], p["effr"], r["reserves"], p["reserves"]):
        return None
    if r["reserves"] <= 0 or p["reserves"] <= 0:
        return None
    x1 = r["effr"] - p["effr"]
    x2 = math.log(r["reserves"]) - math.log(p["reserves"])
    if with_move:
        if not r["move"] or not p["move"] or r["move"] <= 0 or p["move"] <= 0:
            return None
        liq = r["reserves"] * (100.0 / r["move"])
        liqp = p["reserves"] * (100.0 / p["move"])
        x3 = math.log(liq) - math.log(liqp)
        if with_bill:
            if r["bill_share"] is None or p["bill_share"] is None:
                return None
            x3 = x3 + (r["bill_share"] - p["bill_share"])
    else:
        x3 = x2
        if with_bill and r["bill_share"] is not None and p["bill_share"] is not None:
            x3 = x2 + (r["bill_share"] - p["bill_share"])
    return [x1, x2, x3]


def x3_legs(r, p):
    """X3a = 3m Δlog(reserves/MOVE); X3b = 3m Δbill share. None if missing."""
    if r["reserves"] is None or p["reserves"] is None:
        return None, None
    if r["reserves"] <= 0 or p["reserves"] <= 0:
        return None, None
    x3a = None
    if r["move"] and p["move"] and r["move"] > 0 and p["move"] > 0:
        x3a = (math.log(r["reserves"]) - math.log(p["reserves"])) - (
            math.log(r["move"]) - math.log(p["move"])
        )
    x3b = None
    if r["bill_share"] is not None and p["bill_share"] is not None:
        x3b = r["bill_share"] - p["bill_share"]
    return x3a, x3b


def targets_at(by, ym, fwd=T6_FWD):
    """6-month-forward targets from month ym. Yields in percentage points."""
    ymf = add_months(ym, fwd)
    if ym not in by or ymf not in by:
        return None
    r, f = by[ym], by[ymf]
    out = {}
    out["spx"] = logret(r["spx"], f["spx"]) if r["spx"] and f["spx"] else None
    if r["y10"] is not None and f["y10"] is not None:
        d10 = f["y10"] - r["y10"]
        out["y1"] = d10
        out["y3"] = -T6_DURATION * (d10 / 100.0) + (r["y10"] / 100.0) / 2.0
    else:
        out["y1"] = out["y3"] = None
    if None not in (r["y10"], r["y2"], f["y10"], f["y2"]):
        out["y2"] = (f["y10"] - f["y2"]) - (r["y10"] - r["y2"])
    else:
        out["y2"] = None
    out["y4"] = logret(r["btc"], f["btc"]) if r.get("btc") and f.get("btc") else None
    out["dlog_res"] = None
    if r["reserves"] and f["reserves"] and r["reserves"] > 0 and f["reserves"] > 0:
        # 1-month change used in T7/T8, not 6m; keep None here
        pass
    return out
