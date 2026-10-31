from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import RESULTS, T3_P_MAX, T3_RATIO_MIN


def _fmt_era(tag: str, e: dict) -> str:
    if e.get("no_power") or e.get("ratio") is None:
        return f"{tag} no_power Puncond={e['P_uncond']:.3f}"
    return f"{tag} ratio={e['ratio']:.2f} p={e['p_value']:.3f} Puncond={e['P_uncond']:.3f}"


def run() -> dict:
    """Re-score committed T3 era table (daily MOVE/DXY not redistributed)."""
    eras = json.loads((RESULTS / "t3_eras.json").read_text())
    r3, r1, r2 = eras["R3"], eras["R1"], eras["R2"]
    r3_ratio = r3.get("ratio")
    ok = (
        r3_ratio is not None
        and r3_ratio == r3_ratio
        and not r3.get("no_power")
        and r3_ratio > T3_RATIO_MIN
        and r3["p_value"] < T3_P_MAX
        and (r1.get("ratio") in (None, float("nan")) or r1.get("no_power") or r3_ratio > r1["ratio"])
    )
    return {
        "verdict": "PASS" if ok else "FAIL",
        "eras": eras,
        "criterion": "R3 P(action|breach)/P_uncond > 1.5 with p<0.05 and R3 ratio > R1; no ratio if Puncond>0.5",
        "reason": "; ".join(_fmt_era(t, eras[t]) for t in ("R1", "R2", "R3")),
    }
