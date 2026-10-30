from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import RESULTS, RNG_SEED, T5_ANCHORS, T5_MAX_BREAKS, T5_MIN_SIDE, T5_PLACEBO_N, T5_TOL_MONTHS
from src.util import ols
from src.test_t4 import build_xy, monthly_rows
from constants import T4_FWD_MAIN


def t5_search(used, Y, X):
    def rss_split(lo, hi, br):
        if br - lo < T5_MIN_SIDE or hi - br < T5_MIN_SIDE:
            return None
        a = ols(Y[lo:br], X[lo:br], True)
        b = ols(Y[br:hi], X[br:hi], True)
        if a is None or b is None:
            return None
        return a["rss"] + b["rss"]

    def best_break(lo, hi):
        full = ols(Y[lo:hi], X[lo:hi], True)
        if full is None:
            return None
        best = None
        for br in range(lo + T5_MIN_SIDE, hi - T5_MIN_SIDE + 1):
            r = rss_split(lo, hi, br)
            if r is None:
                continue
            red = full["rss"] - r
            if best is None or red > best[0]:
                best = (red, br, r, full["rss"])
        return best

    breaks = []
    segments = [(0, len(used))]
    while len(breaks) < T5_MAX_BREAKS and segments:
        scored = []
        for lo, hi in segments:
            b = best_break(lo, hi)
            if b:
                scored.append((b[0], lo, hi, b))
        if not scored:
            break
        scored.sort(reverse=True)
        red, lo, hi, b = scored[0]
        if red <= 0:
            break
        br = b[1]
        breaks.append({"ym": used[br], "index": br, "rss_reduction": red})
        idxs = [0] + sorted(z["index"] for z in breaks) + [len(used)]
        segments = [(idxs[i], idxs[i + 1]) for i in range(len(idxs) - 1)]
    return breaks


def near(ym, anchor):
    y, m = int(ym[:4]), int(ym[5:7])
    ay, am = int(anchor[:4]), int(anchor[5:7])
    return abs((y * 12 + m) - (ay * 12 + am)) <= T5_TOL_MONTHS


def run(t4_pack=None) -> dict:
    if t4_pack and t4_pack.get("_xy_nomove"):
        used, Y, X = t4_pack["_xy_nomove"]
    else:
        rows = monthly_rows()
        used, Y, X = build_xy(rows, T4_FWD_MAIN, False, True)
    breaks = t5_search(used, Y, X)
    rng = random.Random(RNG_SEED)
    n = len(used)
    block = 12
    n_b = n // block
    stats = []
    true0 = breaks[0]["rss_reduction"] if breaks else 0.0
    for _ in range(T5_PLACEBO_N):
        order = list(range(n_b))
        rng.shuffle(order)
        Yi, Xi, Ui = [], [], []
        for bi in order:
            lo, hi = bi * block, min((bi + 1) * block, n)
            Yi.extend(Y[lo:hi])
            Xi.extend(X[lo:hi])
            Ui.extend(used[lo:hi])
        rem = n_b * block
        if rem < n:
            Yi.extend(Y[rem:]); Xi.extend(X[rem:]); Ui.extend(used[rem:])
        brs = t5_search(Ui, Yi, Xi)
        stats.append(brs[0]["rss_reduction"] if brs else 0.0)
    ge = sum(1 for s in stats if s >= true0)
    placebo_p = (ge + 1) / (T5_PLACEBO_N + 1)
    hit_2008 = any(near(b["ym"], T5_ANCHORS[0]) for b in breaks)
    hit_1920 = any(near(b["ym"], T5_ANCHORS[1]) for b in breaks)
    elsewhere = [b["ym"] for b in breaks if not near(b["ym"], T5_ANCHORS[0]) and not near(b["ym"], T5_ANCHORS[1])]
    ok = hit_2008 and hit_1920 and not elsewhere
    (RESULTS / "t5_breaks.json").write_text(json.dumps(breaks, indent=2))
    (RESULTS / "t5_placebo.json").write_text(json.dumps({"p_first_split": placebo_p, "n": T5_PLACEBO_N}, indent=2))
    return {
        "verdict": "PASS" if ok else "FAIL",
        "breaks": [b["ym"] for b in breaks],
        "placebo_p_first": placebo_p,
        "criterion": "blind splits near 2008 and 2019–20 (±18m), not elsewhere",
        "reason": f"breaks { [b['ym'] for b in breaks] }; extra={elsewhere}; placebo p={placebo_p:.2f}",
    }
