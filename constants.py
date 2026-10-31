#!/usr/bin/env python3
"""Frozen thresholds. Copied from round 2. Do not edit to fit results."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
REPORT_DIR = ROOT / "report"

RNG_SEED = 42

R1_END = "2008-08-31"
R2_START = "2008-09-01"
R2_END = "2019-08-31"
R3_START = "2019-09-01"

T1_WORST_WEEKS = 10
T1_ROLL_WEEKS = 156
T1_SPX_SHOCK = -0.02
T1_PRE2018_NEG_SHARE = 0.80
T1_POST2020_POS_SHARE = 0.60
T1_FLIP_LO = "2018-01-01"
T1_FLIP_HI = "2021-12-31"

T2_DD = 0.08
T2_VOL_Z = 2.0
T2_VIX = 30.0
T2_FUN_Z = 2.0
T2_RATE_EXP_Z = 2.0
T2_MERGE_WEEKS = 4
T2_RESOLVER_WEEKS = 6
T2_Z_WINDOW_DAYS = 504

T3_PCT = 0.95
T3_LOOK_DAYS = 28
T3_PLACEBO_N = 1000
T3_RATIO_MIN = 1.5
T3_P_MAX = 0.05

T4_WINDOW = 60
T4_STEP = 1
T4_FWD_MAIN = 6
T4_FWD_ROBUST = (3, 12)
T4_UNPROVEN_SHARE = 0.40

T5_MIN_SIDE = 60
T5_MAX_BREAKS = 3
T5_TOL_MONTHS = 18
T5_ANCHORS = ("2008-09-01", "2019-12-01")
T5_PLACEBO_N = 50

CPI_CUT = 3.0
IORB_OFFSET = 0.10
SPLICE_DATE = "2002-01-01"

# --- Round 3 (author objections). Frozen 2026-10-31 before the run. ---
# Every line tagged. Howell's name only if he supplied the number in writing.
T6_SHARE_MIN = 0.40          # source=default
T6_FWD = 6                   # source=default
T6_BTC_START = "2019-09"     # source=default
T6_DURATION = 8              # source=default  (Treasury return proxy duration)
T7_K_LO = 1                  # source=default
T7_K_HI = 12                 # source=default
T7_BEST_K_LO = 3             # source=default
T7_BEST_K_HI = 9             # source=default
T7_PR2_MULT = 2.0            # source=default
T7_SAMPLE_A = "2003-01"      # source=default
T7_SAMPLE_B = "2021-01"      # source=default
T8_R2_LO = "2010-01"         # source=default
T8_R2_HI = "2019-08"         # source=default
T8_R3_LO = "2019-09"         # source=default
T8_VOL_DROP = 0.20           # source=default
T8_BETA_DROP = 0.20          # source=default
T8_PMAX = 0.05               # source=default
T8_EXCL_LO = "2020-03"       # source=default
T8_EXCL_HI = "2021-12"       # source=default
T8_DLAGS = 6                 # source=default
T8_ROLL_STD_M = 12           # source=default

LABELS = ("RATE", "QE_QT", "PLUMBING", "REGULATORY", "ADMIN", "OTHER")
CLASSIFIER_CHECK_N = 50
CLASSIFIER_MODEL = "glm-4.7-flash"
MODEL_CMD = ""  # set to re-label, e.g. ollama run glm-4.7-flash

CLASSIFIER_PROMPT = """You classify US Fed/Treasury press-release TITLES only.
Return exactly one JSON object, no prose: {{"label":"RATE|QE_QT|PLUMBING|REGULATORY|OTHER","confidence":0.0,"rmp":0}}

Definitions:
RATE = policy-rate decision, FOMC target, discount-rate, IORB/IOER/ON RRP rate setting, or a scheduled FOMC statement that is a rate decision.
QE_QT = asset purchase or runoff/SOMA reinvestment-cap programs (LSAP, QE, QT, Taper of purchases). NOT reserve-management bill purchases.
PLUMBING = repo, SRF, ON RRP facility operations, swap lines, credit facilities, PDCF/CPFF/MMLF/BTFP, reserve management, bill-issuance tilt, buybacks, SLR relief, standing repo.
REGULATORY = banking/consumer regulatory policy, stress tests, capital rules (except SLR relief which is PLUMBING).
OTHER = speeches, beige book, enforcement, appointments, data releases, surveys, everything else.

If the title is a reserve-management purchase (RMP) of bills (e.g. Dec 2025-type bill purchases for reserve management), label PLUMBING and set rmp=1. Never label those QE_QT.
Example: "Federal Reserve issues FOMC statement" -> RATE. Example: "Federal Reserve announces additional large-scale asset purchases" -> QE_QT. Example: "Federal Reserve announces repurchase operations" -> PLUMBING.

Title: {title}
Source: {source}
"""
