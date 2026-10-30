"""Yahoo chart API helpers for --fetch. Writes weekly/monthly aggregates only."""
from __future__ import annotations

import datetime as dt
import json
import time
import urllib.parse
import urllib.request

UA = "third-way-backtest/2.0 (research)"


def yahoo_chunk(symbol: str, interval: str, p1: int, p2: int) -> list[tuple[str, float]]:
    enc = urllib.parse.quote(symbol, safe="")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{enc}?period1={p1}&period2={p2}&interval={interval}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        blob = json.loads(r.read().decode())
    res = ((blob.get("chart") or {}).get("result") or [None])[0]
    if not res:
        return []
    ts = res.get("timestamp") or []
    closes = ((res.get("indicators") or {}).get("quote") or [{}])[0].get("close") or []
    out = []
    for i, t in enumerate(ts):
        d = dt.datetime.utcfromtimestamp(int(t)).date().isoformat()
        c = closes[i] if i < len(closes) else None
        if c is not None:
            out.append((d, float(c)))
    return out


def yahoo_history(symbol: str, interval: str = "1d") -> list[tuple[str, float]]:
    start = dt.datetime(1980, 1, 1, tzinfo=dt.timezone.utc)
    end = dt.datetime.now(dt.timezone.utc)
    all_rows = []
    cur = start
    while cur < end:
        nxt = min(dt.datetime(cur.year + 4, 1, 1, tzinfo=dt.timezone.utc), end)
        try:
            all_rows.extend(yahoo_chunk(symbol, interval, int(cur.timestamp()), int(nxt.timestamp())))
        except Exception as e:
            print("skip", symbol, cur.date(), e)
        cur = nxt
        time.sleep(0.15)
    by = {d: v for d, v in all_rows}
    return [(d, by[d]) for d in sorted(by)]
