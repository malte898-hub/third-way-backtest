from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import RESULTS, T3_P_MAX, T3_RATIO_MIN


def run() -> dict:
    """Re-score committed T3 era table (daily MOVE/DXY not redistributed)."""
    eras = json.loads((RESULTS / "t3_eras.json").read_text())
    r3, r1, r2 = eras["R3"], eras["R1"], eras["R2"]
    ok = (
        r3["ratio"] == r3["ratio"]
        and r3["ratio"] > T3_RATIO_MIN
        and r3["p_value"] < T3_P_MAX
        and (r1["ratio"] != r1["ratio"] or r3["ratio"] > r1["ratio"])
    )
    np3 = " no_power" if r3.get("no_power") else ""
    return {
        "verdict": "PASS" if ok else "FAIL",
        "eras": eras,
        "criterion": "R3 P(action|breach)/P_uncond > 1.5 with p<0.05 and R3 ratio > R1",
        "reason": (
            f"R1 ratio={r1['ratio']:.2f} p={r1['p_value']:.3f}; "
            f"R2 ratio={r2['ratio']:.2f} p={r2['p_value']:.3f}; "
            f"R3 ratio={r3['ratio']:.2f} p={r3['p_value']:.3f} Puncond={r3['P_uncond']:.3f}{np3}"
        ),
    }
