# Testing the Third Monetary Regime

Independent research. Not investment advice. No positions implied.

## Scoreboard (round 2.3)

| Test | Frozen criterion | Result | Reason |
|---|---|---|---|
| T1 haven inversion | ≥80% of 1990–2018 worst-week mean Δ10y < 0; ≥60% of 2020–2026 > 0; corr sign-flip 2018–21 | FAIL | neg-share 62.1% (need 80%); pos-share 57.1% (need 60%); flip 2019-07-29 |
| T2 plumbing episodes | FIRST_MOVER RATE_EXP→VOL/FUN; RESOLVER RATE→QE_QT→PLUMBING | FAIL | FM {'R1': 'FUN', 'R2': 'RATE_EXP', 'R3': 'FUN'}; RES {'R1': 'RATE', 'R2': 'QE_QT', 'R3': 'RATE'}; n=80 plumbing-defined episodes |
| T3 corridor | R3 ratio > 1.5, p<0.05, R3>R1 | FAIL | R1 ratio=5.64 p=0.001 Puncond=0.010; R2 ratio=0.74 p=1.000 Puncond=0.471; R3 ratio=1.14 p=0.005 Puncond=0.312 |
| T4 horse race | X1 / X2 / X3 majority in R1 / R2 / R3 windows | UNPROVEN | no-MOVE X1=52.5% n=61; X2=50.0%; X3=1.6% |
| T5 breaks | 2008 and 2019–20 ±18m, not elsewhere | FAIL | breaks ['2020-02', '2007-07', '2012-07']; extra=['2012-07']; placebo p=0.73 |

## Round 2 vs 2.2 vs 2.3 (T1/T4/T5 not rerun)

| Test | Round 2 | Round 2.2 | Round 2.3 |
|---|---|---|---|
| T1 | FAIL 62% / 57%; flip 2019-07-29 | unchanged | unchanged |
| T2 plumbing n | 80 | 80 | 80 |
| T2 plumbing FM | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN |
| T2 plumbing RES | RATE / QE_QT / PLUMBING | RATE / QE_QT / PLUMBING+RATE | RATE / QE_QT / RATE |
| T2 equity RES | RATE / QE_QT / RATE | RATE / QE_QT / PLUMBING+RATE | not rerun (press feed has no notes) |
| T3 n_actions | 78 | 138 | 104 |
| T3 R1 | 5.64× p=0.001 | 5.64× p=0.001 | 5.64× p=0.001 Puncond=0.010 |
| T3 R2 | 0.74× p=1.00 | 0.74× p=1.00 | 0.74× p=1.00 Puncond=0.471 |
| T3 R3 | 1.19× p=0.054 | 1.13× p=0.001; Puncond=0.62 no_power | 1.14× p=0.005 Puncond=0.312 |
| PLUMBING rows / 60d / 30d | — | 56 / 6 / 52 | 12 / 9 / 9 |
| T4 | UNPROVEN X1 52.5% / X2 50% / X3 1.6% | unchanged | unchanged |
| T5 | FAIL 2020-02, 2007-07, 2012-07; placebo p≈0.73 | unchanged | unchanged |

## 2025 vignette (2.1 correction)

Oct–Nov 2025: reserve drain → QT ended 2025-12-01 and reserve-management bill purchases began 2025-12-12, announced at the 2025-10-29 and 2025-12-10 FOMC meetings alongside two 25 bp cuts. First STRESS print 2025-10-15; first plumbing announcement 2025-10-29 (10 sessions).

2025-10-29 statement: "The Committee decided to conclude the reduction of its aggregate securities holdings on December 1."

2025-12-10 statement: "The Committee judges that reserve balances have declined to ample levels and will initiate purchases of shorter-term Treasury securities…"

The 2025-10-29 statement gives no money-market attribution; press-conference remarks are not in the corpus.

## Key numbers

{
  "T1": {
    "verdict": "FAIL",
    "n_weeks": 1921,
    "date_range": "1990-01-01 \u2192 2026-10-26",
    "pre2018_share_neg_mean": 0.6206896551724138,
    "post2020_share_pos_mean": 0.5714285714285714,
    "first_sign_flip_date": "2019-07-29",
    "criterion": "mean d10y <0 in \u226580% of 1990\u20132018 years; >0 in \u226560% of 2020\u20132026; corr sign flip 2018\u20132021",
    "reason": "neg-share 62.1% (need 80%); pos-share 57.1% (need 60%); flip 2019-07-29"
  },
  "T2": {
    "verdict": "FAIL",
    "n_episodes": 80,
    "modal_FIRST_MOVER": {
      "R1": "FUN",
      "R2": "RATE_EXP",
      "R3": "FUN"
    },
    "modal_RESOLVER": {
      "R1": "RATE",
      "R2": "QE_QT",
      "R3": "RATE"
    },
    "criterion": "modal FIRST_MOVER RATE_EXP \u2192 any \u2192 VOL/FUN; RESOLVER RATE \u2192 QE_QT \u2192 PLUMBING",
    "reason": "FM {'R1': 'FUN', 'R2': 'RATE_EXP', 'R3': 'FUN'}; RES {'R1': 'RATE', 'R2': 'QE_QT', 'R3': 'RATE'}; n=80 plumbing-defined episodes"
  },
  "T3": {
    "verdict": "FAIL",
    "eras": {
      "R1": {
        "n_days": 4818,
        "n_breach": 647,
        "date_min": "1990-01-01",
        "date_max": "2008-08-29",
        "P_action_given_breach": 0.05409582689335394,
        "P_uncond": 0.009587328053355566,
        "ratio": 5.642429944224178,
        "p_value": 0.000999000999000999,
        "no_power": false
      },
      "R2": {
        "n_days": 2772,
        "n_breach": 482,
        "date_min": "2008-09-02",
        "date_max": "2019-08-30",
        "P_action_given_breach": 0.34647302904564314,
        "P_uncond": 0.47056686046511625,
        "ratio": 0.7362886300645637,
        "p_value": 1.0,
        "no_power": false
      },
      "R3": {
        "n_days": 1806,
        "n_breach": 495,
        "date_min": "2019-09-03",
        "date_max": "2026-10-30",
        "P_action_given_breach": 0.35555555555555557,
        "P_uncond": 0.3124300111982083,
        "ratio": 1.1380326563122263,
        "p_value": 0.004995004995004995,
        "no_power": false
      }
    },
    "criterion": "R3 P(action|breach)/P_uncond > 1.5 with p<0.05 and R3 ratio > R1; no ratio if Puncond>0.5",
    "reason": "R1 ratio=5.64 p=0.001 Puncond=0.010; R2 ratio=0.74 p=1.000 Puncond=0.471; R3 ratio=1.14 p=0.005 Puncond=0.312"
  },
  "T4": {
    "verdict": "UNPROVEN",
    "with_MOVE": {
      "verdict": "UNPROVEN",
      "share_X1_pre2008": 0.0,
      "n_pre2008": 0,
      "share_X2_2010_2019": 0.525,
      "n_2010_2019": 120,
      "share_X3_2021": 0.0625,
      "n_2021": 64,
      "n_windows": 219
    },
    "without_MOVE": {
      "verdict": "UNPROVEN",
      "share_X1_pre2008": 0.5245901639344263,
      "n_pre2008": 61,
      "share_X2_2010_2019": 0.5,
      "n_2010_2019": 120,
      "share_X3_2021": 0.015625,
      "n_2021": 64,
      "n_windows": 281
    },
    "criterion": "dominant partial R\u00b2: X1 majority windows ending <2008; X2 in 2010\u20132019; X3 in 2021\u2192",
    "reason": "no-MOVE X1=52.5% n=61; X2=50.0%; X3=1.6%"
  },
  "T5": {
    "verdict": "FAIL",
    "breaks": [
      "2020-02",
      "2007-07",
      "2012-07"
    ],
    "placebo_p_first": 0.7254901960784313,
    "criterion": "blind splits near 2008 and 2019\u201320 (\u00b118m), not elsewhere",
    "reason": "breaks ['2020-02', '2007-07', '2012-07']; extra=['2012-07']; placebo p=0.73"
  }
}
