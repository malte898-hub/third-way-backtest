"""Label FOMC/press titles. Prompt frozen in constants.CLASSIFIER_PROMPT.

To re-label, set MODEL_CMD in constants.py to a shell command that reads stdin
and writes a JSON object to stdout, e.g. `ollama run glm-4.7-flash`.
Committed data/actions.csv is the round-2 labelled set.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from constants import CLASSIFIER_PROMPT, DATA, LABELS, MODEL_CMD
from src.util import dump_csv, load_csv


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
        c = classify_title(r.get("title") or "Federal Reserve issues FOMC statement")
        out.append({**r, **c})
    dump_csv(DATA / "actions.csv", out, ["date", "url", "label", "confidence", "rmp", "rate"])
    print("wrote", DATA / "actions.csv", len(out))


if __name__ == "__main__":
    main()
