from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.util import load_csv
from constants import RESULTS, R1_END, R2_END


def era(start: str) -> str:
    if start <= R1_END:
        return "R1"
    if start <= R2_END:
        return "R2"
    return "R3"


def run() -> dict:
    """Re-score committed plumbing episodes (daily MOVE not redistributed)."""
    rows = load_csv(RESULTS / "episodes_plumbing.csv")
    m_fm, m_rs = {}, {}
    for e in ("R1", "R2", "R3"):
        xs = [r for r in rows if era(r["start"]) == e]
        fm = [r["FIRST_MOVER"] for r in xs if r.get("FIRST_MOVER") not in ("NONE", "", None)]
        rs = [r["RESOLVER"] for r in xs if r.get("RESOLVER") not in ("NONE", "", None)]
        m_fm[e] = Counter(fm).most_common(1)[0][0] if fm else None
        m_rs[e] = Counter(rs).most_common(1)[0][0] if rs else None
    fm_ok = m_fm.get("R1") == "RATE_EXP" and m_fm.get("R3") in ("VOL", "FUN")
    rs_ok = "RATE" in (m_rs.get("R1") or "") and "QE_QT" in (m_rs.get("R2") or "") and "PLUMBING" in (m_rs.get("R3") or "")
    verdict = "PASS" if fm_ok and rs_ok else "FAIL"
    return {
        "verdict": verdict,
        "n_episodes": len(rows),
        "modal_FIRST_MOVER": m_fm,
        "modal_RESOLVER": m_rs,
        "criterion": "modal FIRST_MOVER RATE_EXP → any → VOL/FUN; RESOLVER RATE → QE_QT → PLUMBING",
        "reason": f"FM {m_fm}; RES {m_rs}; n={len(rows)} plumbing-defined episodes",
    }
