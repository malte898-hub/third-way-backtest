from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import (
    DATA,
    RESULTS,
    T1_FLIP_HI,
    T1_FLIP_LO,
    T1_POST2020_POS_SHARE,
    T1_PRE2018_NEG_SHARE,
    T1_ROLL_WEEKS,
    T1_SPX_SHOCK,
    T1_WORST_WEEKS,
)
from src.util import corr, dump_csv, fnum, load_csv, mean, monday_week, parse_d


def run() -> dict:
    h15 = load_csv(DATA / "h15_daily.csv")
    mkt = [r for r in load_csv(DATA / "market_weekly.csv") if r.get("freq") == "W"]
    y10w = {}
    buckets = defaultdict(list)
    for r in h15:
        v = fnum(r.get("y10"))
        if v is None:
            continue
        d = parse_d(r["date"])
        buckets[monday_week(d)].append((d, v))
    for w, pts in buckets.items():
        y10w[w] = sorted(pts)[-1][1]
    spx = {}
    for r in mkt:
        v = fnum(r.get("spx"))
        if v is None:
            continue
        spx[parse_d(r["date"])] = v
    weeks = sorted(set(spx) & set(y10w))
    weeks = [w for w in weeks if w.year >= 1990]
    recs = []
    for i in range(1, len(weeks)):
        w0, w1 = weeks[i - 1], weeks[i]
        recs.append({
            "week": w1,
            "r_spx": spx[w1] / spx[w0] - 1.0 if spx[w0] else None,
            "d10_bp": (y10w[w1] - y10w[w0]) * 100.0,
            "year": w1.year,
        })
    by_year = defaultdict(list)
    for r in recs:
        if r["r_spx"] is not None:
            by_year[r["year"]].append(r)
    year_rows = []
    for year in range(1990, 2027):
        xs = by_year.get(year, [])
        if len(xs) < T1_WORST_WEEKS:
            year_rows.append({"year": year, "n": len(xs), "mean_d10_bp": "", "share_d10_pos": ""})
            continue
        worst = sorted(xs, key=lambda z: z["r_spx"])[:T1_WORST_WEEKS]
        md = mean([z["d10_bp"] for z in worst])
        share = sum(1 for z in worst if z["d10_bp"] > 0) / len(worst)
        year_rows.append({
            "year": year,
            "n": len(xs),
            "n_worst": len(worst),
            "mean_d10_bp": md,
            "share_d10_pos": share,
            "used_weeks": ",".join(z["week"].isoformat() for z in worst),
        })
    dump_csv(RESULTS / "t1_years.csv", year_rows, ["year", "n", "n_worst", "mean_d10_bp", "share_d10_pos", "used_weeks"])
    roll = []
    first_flip = None
    prev = None
    for i, r in enumerate(recs):
        window = recs[max(0, i - T1_ROLL_WEEKS + 1) : i + 1]
        shock = [z for z in window if z["r_spx"] is not None and z["r_spx"] < T1_SPX_SHOCK]
        c = corr([z["r_spx"] for z in shock], [z["d10_bp"] for z in shock]) if len(shock) >= 8 else None
        roll.append({"week": r["week"].isoformat(), "cond_corr": c})
    for z in roll:
        if not (T1_FLIP_LO <= z["week"] <= T1_FLIP_HI) or z["cond_corr"] is None:
            continue
        sg = 1 if z["cond_corr"] > 0 else -1
        if prev is not None and sg != prev and first_flip is None:
            first_flip = z["week"]
        prev = sg
    pre = [r for r in year_rows if 1990 <= int(r["year"]) <= 2018 and r["mean_d10_bp"] != ""]
    post = [r for r in year_rows if 2020 <= int(r["year"]) <= 2026 and r["mean_d10_bp"] != ""]
    pre_neg = sum(1 for r in pre if float(r["mean_d10_bp"]) < 0) / len(pre) if pre else 0.0
    post_pos = sum(1 for r in post if float(r["mean_d10_bp"]) > 0) / len(post) if post else 0.0
    flipped = first_flip is not None
    verdict = "PASS" if (pre_neg >= T1_PRE2018_NEG_SHARE and post_pos >= T1_POST2020_POS_SHARE and flipped) else "FAIL"
    return {
        "verdict": verdict,
        "n_weeks": len(recs),
        "date_range": f"{weeks[0]} → {weeks[-1]}" if weeks else None,
        "pre2018_share_neg_mean": pre_neg,
        "post2020_share_pos_mean": post_pos,
        "first_sign_flip_date": first_flip,
        "criterion": "mean d10y <0 in ≥80% of 1990–2018 years; >0 in ≥60% of 2020–2026; corr sign flip 2018–2021",
        "reason": f"neg-share {pre_neg:.1%} (need 80%); pos-share {post_pos:.1%} (need 60%); flip {first_flip}",
    }
