"""Optional rebuild of Fed H.15 / H.41 / H.3 / FiscalData / NY Fed / BLS.

Rate-limited. Invoked by `python run.py --fetch`.
"""
from __future__ import annotations

import csv
import io
import json
import time
import urllib.request
import zipfile
from pathlib import Path

UA = "third-way-backtest/2.0 (research)"
TIMEOUT = 60


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def fetch_h15_zip(dest: Path) -> None:
    raw = get("https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&filetype=zip")
    dest.write_bytes(raw)
    print("H.15 zip", dest, dest.stat().st_size)


def fetch_h41_zip(dest: Path) -> None:
    dest.write_bytes(get("https://www.federalreserve.gov/datadownload/Output.aspx?rel=H41&filetype=zip"))
    print("H.41 zip", dest)


def fetch_h3_zip(dest: Path) -> None:
    dest.write_bytes(get("https://www.federalreserve.gov/datadownload/Output.aspx?rel=H3&filetype=zip"))
    print("H.3 zip", dest)


def fetch_cpi_bls() -> list[dict]:
    rows = []
    for start, end in (("1990", "1999"), ("2000", "2009"), ("2010", "2019"), ("2020", "2026")):
        payload = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": start, "endyear": end}).encode()
        req = urllib.request.Request(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            data=payload,
            headers={"User-Agent": UA, "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            blob = json.loads(r.read().decode())
        ser = (blob.get("Results") or {}).get("series") or []
        data = (ser[0].get("data") if ser else []) or []
        for rec in data:
            if str(rec.get("period", "")).startswith("M"):
                rows.append(rec)
        time.sleep(0.5)
    return rows
