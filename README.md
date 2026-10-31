# Testing the "Third Monetary Regime" — five pre-registered tests on public data

Does Howell's three-regime thesis ([The Fed's 'Third Way'](https://capitalwars.substack.com/p/the-feds-third-way), *Capital Wars*, Oct 2026) show up in public data? Scarce-reserve rate policy (R1), QE quantity (R2), then administered rates plus Treasury collateral and plumbing tools (R3).

Filling the 2020–2026 FOMC hole and then splitting implementation notes (ADMIN unless an operational change) keeps FIRST_MOVER as FUN / RATE_EXP / FUN on 80 plumbing-defined episodes. R3 modal resolver falls back to RATE once notes stop flooding PLUMBING. Corridor R3 recovers power (Puncond=0.31, was 0.62) but the ratio is still 1.14× vs 5.64× pre-2008. T1/T4/T5 not rerun.

| Test | Frozen criterion | Result | n |
|---|---|---|---|
| T1 haven inversion | ≥80% of 1990–2018 years: mean Δ10y in 10 worst S&P weeks < 0; ≥60% of 2020–2026 > 0; 156w shock-corr sign-flip 2018–21 | FAIL 62% / 57%; flip 2019-07-29 | years |
| T2 plumbing anatomy | FIRST_MOVER RATE_EXP → VOL/FUN; RESOLVER RATE → QE_QT → PLUMBING | FAIL FM FUN/RATE_EXP/FUN; RES RATE/QE_QT/RATE | 80 |
| T3 corridor | R3 P(action\|breach)/uncond > 1.5, p<0.05, and R3>R1 | FAIL R1 5.64; R3 1.14 p=0.005 Puncond=0.31 | — |
| T4 horse race | Dominant partial R²: Δrate before 2008, Δreserves 2010–19, effective liquidity 2021→ | UNPROVEN No-MOVE X1 52.5% / X2 50% / X3 1.6% | 64 post-2021 |
| T5 structural breaks | Splits near 2008 and 2019–20 (±18m), not elsewhere | FAIL 2007-07, 2020-02, extra 2012-07; placebo p≈0.73 | — |
| T6 y1 Δ10y | X3 largest partial R² in ≥40% of windows ending 2021→ | FAIL 25.0% | 64 |
| T6 y2 slope | same | PASS 76.6% | 64 |
| T6 y3 tsy proxy | same | FAIL 31.2% | 64 |
| T6 y4 BTC | lenient criterion (X2 or X3), n=21 | PASS 100% | 21 |
| T7b ΔMOVE→SPX 2021→ | best k ∈ [3,9] and partial R² ≥ 2× k=1 | FAIL best k=2 | — |
| T8 MOVE footprint | 2 of 3 (R3 vol −20%; R3 β −20%; R3 lags p<0.05) | FAIL 0/3 | — |

Round 3 ran on 2026-10-31 with default cut-offs set before the run; the author had not specified predictions. Author-supplied values, if any, will be run once as Round 3b and reported alongside, not in place of, Round 3. T7a is reported as exploratory; it had no frozen criterion.

Round 4 (confirmatory OOS of T7a lags, source=default, frozen before GO): fit 2021-01→2023-12, test origins 2024-01→2026-04, k_SPX=5, k_SLOPE=6, k_10Y=9, k_BTC=5. PASS if X3 OOS R² > X2 and > 0 for SPX and slope. Result: FAIL (SPX X3 0.005 > X2 and > 0; slope X3 −0.603 not > 0). Decomposition (exploratory): the 2021→ lag is carried by Δbill share (X3b), not Δlog(reserves/MOVE).

Reproduce:

```
pip install pillow
python run.py --from-cache          # ≈5 min; writes report/REPORT.md
python run.py --fetch               # rebuilds data/ from public sources, ≈1 h, rate-limited
```

Classification is optional. Labelled `data/actions.csv` is committed. To re-label, set `MODEL_CMD` in `constants.py` to any local or API command (prompt in `src/classify.py`).

Pre-registration: `constants.py` was frozen before round 1. Round 2 changed instruments only (see CHANGELOG). Round 2.2 added FOMC statements 2020–2026. Round 2.3 classifies implementation notes as ADMIN unless the Desk directive records an operational change. Round 3 adds T6–T8 (source=default) without touching T1–T5 cut-offs. Round 3.1 reports T7a with X1/X2 lag controls; no new cut-offs. Round 4 is a confirmatory OOS of those lags (source=default). Thresholds were never tuned to results.

What would change the verdict: (1) a dealer-balance-sheet multiplier (NY Fed FR 2004) in place of 1/MOVE; (2) a Treasury-issuance event study for the corridor. Pull requests welcome; a PR that flips a verdict is the point.

Independent research. Not investment advice. No positions implied.

Code: MIT. `report/` text and figures: CC-BY-4.0.

Author: Malte Barth
