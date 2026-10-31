"""Classifier.

Statements: frozen title/body prompt in constants.CLASSIFIER_PROMPT (MODEL_CMD).
Implementation notes: default ADMIN. Promote only on an operational-change
delta vs the previous note. Deterministic regex; model is a tiebreak hook
(MODEL_CMD) unused unless the ops skeleton changed and no named rule hit.

Committed data/actions.csv is the labelled set. --from-cache does not re-label.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import CLASSIFIER_PROMPT, DATA, LABELS, MODEL_CMD
from src.util import dump_csv, load_csv

RATE_NOISE = re.compile(
    r"""
    \b(?:january|february|march|april|may|june|july|august|september|october|november|december)
      \s+\d{1,2}(?:,\s*\d{4})? |
    \b(?:effective)\s+[^.]{0,40} |
    \b(?:target\s+range\s+of)\s+[\d\s/to\-‑–¼½¾.]+(?:\s*percent)? |
    \b(?:interest\s+rate\s+paid\s+on\s+reserve\s+balances)\s+(?:to|at)\s+[\d.]+(?:\s*percent)? |
    \b(?:primary\s+credit\s+rate)\s+(?:to|at)\s+[\d.]+(?:\s*percent)? |
    \b(?:offering\s+rate\s+of)\s+[\d.]+(?:\s*percent)? |
    \b(?:minimum\s+bid\s+rate\s+of)\s+[\d.]+(?:\s*percent)? |
    \b(?:at\s+a\s+rate\s+of)\s+[\d.]+(?:\s*percent)? |
    \b\d+\s*-\s*\d+/\d+\s+to\s+[\d\s/]+(?:\s*percent)? |
    \b\d+(?:\.\d+)?\s*percent
    """,
    re.I | re.X,
)
WS = re.compile(r"\s+")
PLUMBING_DELTA = [
    (re.compile(r"reserve[\s-]*management|ample\s+level\s+of\s+reserves|purchases?\s+of\s+treasury\s+bills", re.I), "rmp"),
    (re.compile(r"standing\s+overnight\s+repurchase|standing\s+repo|srf\b|fima", re.I), "srf"),
    (re.compile(r"per-counterparty\s+limit", re.I), "rrp_limit"),
    (re.compile(r"aggregate\s+operation\s+limit", re.I), "agg_limit"),
    (re.compile(r"swap\s+line|liquidity\s+swap|new\s+facility|establish(?:ed|ment)|terminat(?:e|ed|ion)\s+the", re.I), "facility"),
    (re.compile(r"bill-purchase|purchases?\s+of\s+shorter-term\s+treasury", re.I), "bills"),
]
QE_DELTA = [
    re.compile(r"monthly\s+cap|cap\s+of\s+\$|runoff|reinvest(?:ment)?(?:\s+cap)?|redeem\s+treasury|taper|increase\s+the\s+system\s+open\s+market\s+account\s+holdings\s+of\s+treasury\s+securities\s+by", re.I),
    re.compile(r"conclude\s+the\s+reduction|roll\s+over\s+at\s+auction\s+all\s+principal", re.I),
]


def is_implementation_note(href: str, title: str = "") -> bool:
    h = (href or "").lower()
    t = (title or "").lower()
    return h.endswith("a1.htm") or "implementation note" in t


def extract_directive(text: str) -> str:
    t = text.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    m = re.search(
        r"directs the Open Market Desk.{0,200}to:(.+?)(?:In a related action|This information will be updated)",
        t,
        re.I | re.S,
    )
    if m:
        return m.group(1)
    m = re.search(r"directs the Desk to:(.+?)(?:In a related action|This information will be updated)", t, re.I | re.S)
    return m.group(1) if m else t


def ops_norm(text: str) -> str:
    d = extract_directive(text)
    d = d.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
    d = d.replace("\u2011", "-").replace("‑", "-").replace("–", "-")
    d = RATE_NOISE.sub(" ", d)
    d = re.sub(
        r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b",
        " MONTH ",
        d,
        flags=re.I,
    )
    d = re.sub(r"\$[\d,.]+(?:\s*billion)?", " $N ", d, flags=re.I)
    d = re.sub(r"\b\d+\b", " N ", d)
    d = re.sub(r"\bstanding overnight repurchase", " overnight repurchase", d, flags=re.I)
    d = re.sub(r"\bstanding overnight reverse", " overnight reverse", d, flags=re.I)
    return WS.sub(" ", d).strip().lower()


def _grams(s: str) -> set[str]:
    w = s.split()
    return {" ".join(w[i : i + 4]) for i in range(max(0, len(w) - 3))}


def classify_note(body: str, prev_norm: str | None) -> dict:
    """Default ADMIN. Promote only if the ops skeleton changed.

    PLUMBING: RMP start/size, SRF terms, ON RRP counterparty-limit change,
    new/extended/terminated facility or swap, bill-purchase instructions.
    QE_QT: reinvestment-cap or runoff-pace change, purchase-programme start/taper.
    ADMIN: IORB / RRP / discount / primary-credit reset that follows the target
    range; routine restatement of ongoing ops.
    """
    cur = ops_norm(body)
    if prev_norm is not None and cur == prev_norm:
        return {"label": "ADMIN", "rmp": 0, "rule": "ops_unchanged", "ops_norm": cur, "tiebreak": 0}
    added = cur if prev_norm is None else " ".join(sorted(_grams(cur) - _grams(prev_norm)))
    if prev_norm is None:
        est = bool(re.search(r"establish|standing overnight repurchase|reserve management|monthly cap of", body, re.I))
        if not est:
            return {"label": "ADMIN", "rmp": 0, "rule": "first_note_default_admin", "ops_norm": cur, "tiebreak": 0}
        src = body
    else:
        src = added
    plumbing_hits = []
    rmp = 0
    for rx, name in PLUMBING_DELTA:
        if rx.search(src):
            plumbing_hits.append(name)
            if name in ("rmp", "bills"):
                rmp = 1
    qe = any(rx.search(src) for rx in QE_DELTA)
    if plumbing_hits and qe:
        if any(n in plumbing_hits for n in ("rmp", "srf", "rrp_limit", "facility", "bills")):
            lab, rule = "PLUMBING", "delta_plumbing_over_qe:" + "+".join(plumbing_hits)
        else:
            lab, rule = "QE_QT", "delta_qe_and_weak_plumbing"
    elif plumbing_hits:
        lab, rule = "PLUMBING", "delta_plumbing:" + "+".join(plumbing_hits)
    elif qe:
        lab, rule = "QE_QT", "delta_qe_qt"
    elif re.search(r"purchase|reinvest|cap|counterparty limit|standing repo|swap line", added, re.I):
        lab, rule = "PLUMBING", "delta_untyped_ops_regex"
    else:
        lab, rule = "ADMIN", "delta_untyped_treated_admin"
    return {"label": lab, "rmp": rmp, "rule": rule, "ops_norm": cur, "tiebreak": 0}


def classify_title(title: str, source: str = "Fed") -> dict:
    prompt = CLASSIFIER_PROMPT.format(title=title, source=source)
    cmd = MODEL_CMD or os.environ.get("MODEL_CMD", "")
    if not cmd:
        raise SystemExit("MODEL_CMD not set; committed actions.csv is used by --from-cache")
    p = subprocess.run(cmd, shell=True, input=prompt.encode(), capture_output=True, timeout=120)
    text = p.stdout.decode("utf-8", "replace")
    i, j = text.find("{"), text.rfind("}")
    obj = json.loads(text[i : j + 1]) if i >= 0 and j > i else {}
    lab = str(obj.get("label", "OTHER")).upper()
    if lab not in LABELS:
        lab = "OTHER"
    return {"label": lab, "confidence": obj.get("confidence", 0), "rmp": obj.get("rmp", 0)}


def main():
    rows = load_csv(DATA / "fomc_statements.csv")
    out = []
    for r in rows:
        href = r.get("url") or r.get("href") or ""
        if is_implementation_note(href, r.get("title") or ""):
            # Bodies are not redistributed. Keep committed label if present.
            out.append({**r, "label": r.get("label") or "ADMIN", "rmp": r.get("rmp") or 0})
            continue
        c = classify_title(r.get("title") or "Federal Reserve issues FOMC statement")
        out.append({**r, **c})
    dump_csv(DATA / "actions.csv", out, ["date", "url", "label", "confidence", "rmp", "rate", "doc_type"])
    print("wrote", DATA / "actions.csv", len(out))


if __name__ == "__main__":
    main()
