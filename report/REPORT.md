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

## Round 3 — tests from the author's reply

Howell did not supply numerical predictions in writing. Every cut-off below is source=default, frozen before the run. T1–T5 constants were not edited.

| Test | Who set it | Frozen value | Result |
|---|---|---|---|
| T6 y1 (d10y) | default | X3 (X2 or X3 for y4) largest partial R² in ≥40% of windows ending 2021→ | FAIL share=25.0% n=64 |
| T6 y2 (d_slope) | default | X3 (X2 or X3 for y4) largest partial R² in ≥40% of windows ending 2021→ | PASS share=76.6% n=64 |
| T6 y3 (tsy_ret) | default | X3 (X2 or X3 for y4) largest partial R² in ≥40% of windows ending 2021→ | FAIL share=31.2% n=64 |
| T6 y4 (btc) | default | X3 (X2 or X3 for y4) largest partial R² in ≥40% of windows ending 2021→ | PASS share=100.0% n=21 |
| T6 ACM y2b | default | skip if no CSV | skipped (NY Fed ACM is Excel, not CSV) |
| T6 caveat | — | reverse causation | reserves and yields share the Fed reaction function; a positive result is consistent with reverse causation |
| T7b 2021→ ΔMOVE→SPX | default | best k ∈ [3,9] and partial R² ≥ 2× k=1; flat or k≤2 → FAIL | FAIL best k=2 pr2=0.0425; k1 pr2=0.0398 |
| T7 p-values | default | none (overlapping forwards) | partial R² only |
| T8 MOVE footprint | default | 2 of 3: R3 12m std(ΔMOVE) −20%; R3 weekly β −20%; R3 d-res/d-bill → ΔMOVE negative p<0.05 not R2 | FAIL 0/3 on exclusion sample; a=False b=False c=False |
| T8 identification | — | exclusion 2020-03→2021-12 is partial mitigation | lower vol in R3 is also consistent with ZIRP and forward guidance; the exclusion window is partial mitigation, not a fix |

## T7a — exploratory, no frozen criterion

12 lags scanned, overlapping 6m forwards, n≈64 months in 2021→ — treat as hypothesis-generating. No frozen criterion.

| Target | X3 k=1 | X3 best k | X3 best | X2 k=1 | X2 best k | X2 best | n |
|---|---|---|---|---|---|---|---|
| SPX | 0.123 | 5 | 0.315 | 0.056 | 7 | 0.107 | 64 |
| slope | 0.262 | 6 | 0.440 | 0.000 | 12 | 0.098 | 64 |
| 10y | 0.081 | 9 | 0.226 | 0.019 | 7 | 0.114 | 64 |
| BTC | 0.154 | 5 | 0.212 | 0.041 | 7 | 0.073 | 64 |

SPX: X3 best-lag partial R² 0.315 (k=5) exceeds X2 0.107 (k=7). This revisits the round-2 T4 reading that reserve quantity dominated effective liquidity in 2021→ windows.

slope: X3 best-lag partial R² 0.440 (k=6) exceeds X2 0.098 (k=12). This revisits the round-2 T4 reading that reserve quantity dominated effective liquidity in 2021→ windows.

10y: X3 best-lag partial R² 0.226 (k=9) exceeds X2 0.114 (k=7). This revisits the round-2 T4 reading that reserve quantity dominated effective liquidity in 2021→ windows.

BTC: X3 best-lag partial R² 0.212 (k=5) exceeds X2 0.073 (k=7). This revisits the round-2 T4 reading that reserve quantity dominated effective liquidity in 2021→ windows.

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
  },
  "T6": {
    "acm": "skipped \u2014 NY Fed ACM file is Excel (.xls), not keyless CSV",
    "source": "default",
    "criterion": "X3 (or X2 for y4) largest partial R2 in >=40% of windows ending 2021\u2192",
    "caveat": "reserves and yields share the Fed reaction function; a positive result is consistent with reverse causation",
    "targets": {
      "y1": {
        "name": "d10y",
        "verdict": "FAIL",
        "share_X3or_want_2021_withMOVE": 0.25,
        "n_2021_withMOVE": 64,
        "want": [
          "X3"
        ],
        "share_withoutMOVE": 0.234375,
        "n_withoutMOVE": 64,
        "n_windows": 219,
        "date_range": "2003-03 \u2192 2026-04"
      },
      "y2": {
        "name": "d_slope",
        "verdict": "PASS",
        "share_X3or_want_2021_withMOVE": 0.765625,
        "n_2021_withMOVE": 64,
        "want": [
          "X3"
        ],
        "share_withoutMOVE": 0.734375,
        "n_withoutMOVE": 64,
        "n_windows": 219,
        "date_range": "2003-03 \u2192 2026-04"
      },
      "y3": {
        "name": "tsy_ret",
        "verdict": "FAIL",
        "share_X3or_want_2021_withMOVE": 0.3125,
        "n_2021_withMOVE": 64,
        "want": [
          "X3"
        ],
        "share_withoutMOVE": 0.296875,
        "n_withoutMOVE": 64,
        "n_windows": 219,
        "date_range": "2003-03 \u2192 2026-04"
      },
      "y4": {
        "name": "btc",
        "verdict": "PASS",
        "share_X3or_want_2021_withMOVE": 1.0,
        "n_2021_withMOVE": 21,
        "want": [
          "X3",
          "X2"
        ],
        "share_withoutMOVE": 1.0,
        "n_withoutMOVE": 21,
        "n_windows": 21,
        "date_range": "2019-09 \u2192 2026-04"
      }
    },
    "verdict": "FAIL",
    "reason": "y1 FAIL share=25.0% n=64; y2 PASS share=76.6% n=64; y3 FAIL share=31.2% n=64; y4 PASS share=100.0% n=21"
  },
  "T7": {
    "verdict": "FAIL",
    "source": "default",
    "branch_scored": "7b 2021 dMOVE \u2192 6m-forward SPX",
    "best_k": 2,
    "best_pr2": 0.04248611648913603,
    "k1_pr2": 0.03982982081156505,
    "criterion": "7b 2021\u2192 best k in [3,9] and pr2 >= 2.0\u00d7 k=1; flat or best k<=2 \u2192 FAIL",
    "reason": "best k=2 pr2=0.0425; k1 pr2=0.0398",
    "note": "overlapping 6m-forward windows: partial R2 only, no p-values",
    "7a_best": {
      "from_2003": {
        "spx": {
          "k": 4,
          "n": 274,
          "pr2": 0.07015061522558985,
          "beta": 0.014169739225385768
        },
        "y1": {
          "k": 3,
          "n": 275,
          "pr2": 0.028718527636274582,
          "beta": 0.05062244365216205
        },
        "y2": {
          "k": 4,
          "n": 274,
          "pr2": 0.10579114410546087,
          "beta": 0.07580890876420568
        },
        "y3": {
          "k": 3,
          "n": 275,
          "pr2": 0.029733707476125693,
          "beta": -0.004263450662838732
        },
        "y4": {
          "k": 4,
          "n": 140,
          "pr2": 0.17532698012853265,
          "beta": 0.12941106105974617
        }
      },
      "from_2021": {
        "spx": {
          "k": 5,
          "n": 64,
          "pr2": 0.31460607218822834,
          "beta": 0.03762878505460638
        },
        "y1": {
          "k": 9,
          "n": 64,
          "pr2": 0.2259978872062447,
          "beta": -0.10346409553682762
        },
        "y2": {
          "k": 6,
          "n": 64,
          "pr2": 0.44033336036750403,
          "beta": 0.20289964074854153
        },
        "y3": {
          "k": 9,
          "n": 64,
          "pr2": 0.187183371201059,
          "beta": 0.008022037352062505
        },
        "y4": {
          "k": 5,
          "n": 64,
          "pr2": 0.21157591810706,
          "beta": 0.13583662453856918
        }
      }
    },
    "7b_best": {
      "from_2003": {
        "spx": {
          "k": 10,
          "n": 271,
          "pr2": 0.016314175180286328,
          "beta": -0.0008881916138661631
        },
        "y1": {
          "k": 2,
          "n": 279,
          "pr2": 0.006244906547245521,
          "beta": 0.0030925762518399366
        },
        "y2": {
          "k": 7,
          "n": 274,
          "pr2": 0.004937150516311495,
          "beta": -0.0021342298728099715
        },
        "y3": {
          "k": 2,
          "n": 279,
          "pr2": 0.006384254539523959,
          "beta": -0.0002585032600568607
        },
        "y4": {
          "k": 2,
          "n": 140,
          "pr2": 0.01640760393621421,
          "beta": -0.005489577523321532
        },
        "dlog_res": {
          "k": 10,
          "n": 277,
          "pr2": 0.011504570560395999,
          "beta": 0.002081422188173302
        },
        "dbill": {
          "k": 11,
          "n": 275,
          "pr2": 0.00809405744360514,
          "beta": 0.005159364944787944
        }
      },
      "from_2021": {
        "spx": {
          "k": 2,
          "n": 64,
          "pr2": 0.04248611648913603,
          "beta": -0.0012726040005132055
        },
        "y1": {
          "k": 1,
          "n": 64,
          "pr2": 0.056059491734067546,
          "beta": 0.008882380725281344
        },
        "y2": {
          "k": 3,
          "n": 64,
          "pr2": 0.02783135941985726,
          "beta": -0.004939521586401028
        },
        "y3": {
          "k": 1,
          "n": 64,
          "pr2": 0.05777600380296888,
          "beta": -0.000768231530044101
        },
        "y4": {
          "k": 1,
          "n": 64,
          "pr2": 0.01951326100340456,
          "beta": -0.0037931523160401274
        },
        "dlog_res": {
          "k": 1,
          "n": 70,
          "pr2": 0.04893389863962894,
          "beta": 0.0007090619337496387
        },
        "dbill": {
          "k": 2,
          "n": 69,
          "pr2": 0.0588222717848621,
          "beta": -0.009636849458111163
        }
      }
    },
    "t7a_exploratory": [
      {
        "target": "SPX",
        "y": "spx",
        "n": 64,
        "X3_k1": 0.12328488957333927,
        "X3_best_k": 5,
        "X3_best": 0.31460607218822834,
        "X2_k1": 0.05583810936586253,
        "X2_best_k": 7,
        "X2_best": 0.10661073493879392,
        "X3_gt_X2_at_best": true
      },
      {
        "target": "slope",
        "y": "y2",
        "n": 64,
        "X3_k1": 0.2617827215821589,
        "X3_best_k": 6,
        "X3_best": 0.44033336036750403,
        "X2_k1": 0.0004985081563539939,
        "X2_best_k": 12,
        "X2_best": 0.09775807475783915,
        "X3_gt_X2_at_best": true
      },
      {
        "target": "10y",
        "y": "y1",
        "n": 64,
        "X3_k1": 0.08101912444435477,
        "X3_best_k": 9,
        "X3_best": 0.2259978872062447,
        "X2_k1": 0.018514963110276006,
        "X2_best_k": 7,
        "X2_best": 0.11363640016553367,
        "X3_gt_X2_at_best": true
      },
      {
        "target": "BTC",
        "y": "y4",
        "n": 64,
        "X3_k1": 0.15401447807638258,
        "X3_best_k": 5,
        "X3_best": 0.21157591810706,
        "X2_k1": 0.041203486920064036,
        "X2_best_k": 7,
        "X2_best": 0.07282508060884219,
        "X3_gt_X2_at_best": true
      }
    ],
    "t7a_note": "12 lags scanned, overlapping 6m forwards, n\u224864 months in 2021\u2192 \u2014 treat as hypothesis-generating. No frozen criterion."
  },
  "T8": {
    "verdict": "FAIL",
    "source": "default",
    "scored_sample": "R2/R3 with 2020-03\u21922021-12 excluded",
    "n_of_3": 0,
    "a": {
      "a_std_R2": 9.700877342382542,
      "a_std_R3": 15.229621575296571,
      "a_n_R2": 105,
      "a_n_R3": 53,
      "a_drop": -0.5699220841355537,
      "a_pass": false
    },
    "b": {
      "b_beta_R2": 30.71675926734963,
      "b_beta_R3": 36.19581073946821,
      "b_n_R2": 503,
      "b_n_R3": 278,
      "b_drop": -0.17837335717712044,
      "b_pass": false
    },
    "c": {
      "pass": false,
      "R2": {
        "res": {
          "n": 116,
          "sum": -20.33513705729522,
          "p": 0.5702992633418436,
          "t": -0.567610812870987
        },
        "bill": {
          "n": 116,
          "sum": 1.0764834791329694,
          "p": 0.7075608402857136,
          "t": 0.3751339619561519
        }
      },
      "R3": {
        "res": {
          "n": 64,
          "sum": -37.49415391354562,
          "p": 0.7169572948153577,
          "t": -0.3625282793708484
        },
        "bill": {
          "n": 64,
          "sum": -2.4561854762401287,
          "p": 0.6076521721481764,
          "t": -0.513427701636083
        }
      }
    },
    "full": {
      "a_pass": false,
      "b_pass": false,
      "c_pass": false,
      "verdict": "FAIL",
      "n_pass": 0
    },
    "criterion": "2 of 3: R3 12m std(\u0394MOVE) \u221220%; R3 weekly \u03b2(\u0394MOVE,|\u039410y|) \u221220%; R3 d-res/d-bill lags\u2192\u0394MOVE negative p<0.05, not R2",
    "identification": "lower vol in R3 is also consistent with ZIRP and forward guidance; the exclusion window is partial mitigation, not a fix",
    "reason": "0/3 on exclusion sample; a=False b=False c=False"
  }
}
