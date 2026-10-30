#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import math
from pathlib import Path


def fnum(x):
    try:
        if x is None or x == "":
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def dump_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def parse_d(s: str) -> dt.date:
    return dt.date.fromisoformat(s[:10])


def monday_week(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def stdev_p(xs: list[float]) -> float:
    if not xs:
        return float("nan")
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def corr(xs, ys):
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx < 1e-18 or dy < 1e-18:
        return None
    return num / (dx * dy)


def percentile(xs: list[float], p: float) -> float:
    ys = sorted(xs)
    if not ys:
        return float("nan")
    if p <= 0:
        return ys[0]
    if p >= 1:
        return ys[-1]
    k = (len(ys) - 1) * p
    f = int(math.floor(k))
    c = int(math.ceil(k))
    if f == c:
        return ys[f]
    return ys[f] * (c - k) + ys[c] * (k - f)


def logret(a, b):
    if a is None or b is None or a <= 0 or b <= 0:
        return None
    return math.log(b / a)


def add_months(ym: str, k: int) -> str:
    y, m = int(ym[:4]), int(ym[5:7])
    m0 = y * 12 + (m - 1) + k
    y2, m2 = divmod(m0, 12)
    return f"{y2:04d}-{m2 + 1:02d}"


def _gauss_solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-14:
            return None
        m[col], m[piv] = m[piv], m[col]
        div = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= div
        for r in range(n):
            if r == col:
                continue
            fac = m[r][col]
            for j in range(col, n + 1):
                m[r][j] -= fac * m[col][j]
    return [m[i][n] for i in range(n)]


def ols(y, X, intercept=True):
    n = len(y)
    if n < 5 or not X or len(X) != n:
        return None
    k0 = len(X[0])
    cols = []
    if intercept:
        cols.append([1.0] * n)
    for j in range(k0):
        cols.append([X[i][j] for i in range(n)])
    k = len(cols)
    xtx = [[0.0] * k for _ in range(k)]
    xty = [0.0] * k
    for i in range(n):
        for a in range(k):
            xty[a] += cols[a][i] * y[i]
            for b in range(k):
                xtx[a][b] += cols[a][i] * cols[b][i]
    beta = _gauss_solve(xtx, xty)
    if beta is None:
        return None
    resid = []
    for i in range(n):
        s = sum(beta[j] * cols[j][i] for j in range(k))
        resid.append(y[i] - s)
    rss = sum(r * r for r in resid)
    my = mean(y)
    tss = sum((yi - my) ** 2 for yi in y)
    r2 = 1.0 - rss / tss if tss > 1e-18 else 0.0
    return {"beta": beta, "rss": rss, "tss": tss, "r2": r2, "n": n}


def standardize_cols(X):
    n, k = len(X), len(X[0])
    out = [[0.0] * k for _ in range(n)]
    for j in range(k):
        col = [X[i][j] for i in range(n)]
        m = mean(col)
        sd = stdev_p(col)
        for i in range(n):
            out[i][j] = 0.0 if sd < 1e-12 else (X[i][j] - m) / sd
    return out


def partial_r2(y, Xstd, j):
    full = ols(y, Xstd, True)
    if full is None:
        return None
    k = len(Xstd[0])
    if k == 1:
        return full["r2"]
    Xr = [[row[c] for c in range(k) if c != j] for row in Xstd]
    red = ols(y, Xr, True)
    if red is None or red["rss"] < 1e-18:
        return None
    return (red["rss"] - full["rss"]) / red["rss"]
