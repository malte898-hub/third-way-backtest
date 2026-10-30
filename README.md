# Testing the "Third Monetary Regime" — five pre-registered tests on public data

Does Howell's three-regime thesis ([The Fed's 'Third Way'](https://capitalwars.substack.com/p/the-feds-third-way), *Capital Wars*, Oct 2026) show up in public data? Scarce-reserve rate policy (R1), QE quantity (R2), then administered rates plus Treasury collateral and plumbing tools (R3).

Toolkit migration is confirmed: on 80 plumbing-defined stress episodes, crisis resolvers move RATE → QE → PLUMBING once FOMC statement bodies are labelled. The asset-pricing half is not supported: reserve *quantity* dominates a reserves×(1/MOVE) multiplier in 60/64 post-2021 rolling windows; the corridor reaction is 5.6× pre-2008 versus 1.2× post-2019 (p=0.054); a blind break search finds 2008 clearly, while 2020 is no better than a 12-month block-shuffle placebo (p≈0.73). Treasuries-sold-with-risk: two weeks in 36 years.

| Test | Frozen criterion | Round 2 | Why |
|---|---|---|---|
| T1 haven inversion | ≥80% of 1990–2018 years: mean Δ10y in 10 worst S&P weeks < 0; ≥60% of 2020–2026 > 0; 156w shock-corr sign-flip 2018–21 | FAIL | 62% / 57%; flip 2019-07-29 |
| T2 plumbing anatomy | FIRST_MOVER RATE_EXP → VOL/FUN; RESOLVER RATE → QE_QT → PLUMBING | FAIL | RESOLVER path holds; FIRST_MOVER is FUN / RATE_EXP / FUN (n=80) |
| T3 corridor | R3 P(action\|breach)/uncond > 1.5, p<0.05, and R3>R1 | FAIL | R1 5.64 (p=0.001); R3 1.19 (p=0.054) |
| T4 horse race | Dominant partial R²: Δrate before 2008, Δreserves 2010–19, effective liquidity 2021→ | UNPROVEN | No-MOVE: X1 52.5%, X2 50%, X3 1.6% (X3 < 40% share) |
| T5 structural breaks | Splits near 2008 and 2019–20 (±18m), not elsewhere | FAIL | 2007-07 and 2020-02 hit; 2012-07 extra; first-split placebo p≈0.73 |

Reproduce:

```
pip install pillow
python run.py --from-cache          # ≈5 min; writes report/REPORT.md
python run.py --fetch               # rebuilds data/ from public sources, ≈1 h, rate-limited
```

Classification is optional. Labelled `data/actions.csv` is committed. To re-label, set `MODEL_CMD` in `constants.py` to any local or API command (prompt in `src/classify.py`).

Pre-registration: `constants.py` was frozen before round 1. Round 2 changed instruments only (see CHANGELOG). Thresholds were never tuned to results.

What would change the verdict: (1) a dealer-balance-sheet multiplier (NY Fed FR 2004) in place of 1/MOVE; (2) a Treasury-issuance event study for the corridor. Pull requests welcome; a PR that flips a verdict is the point.

Independent research. Not investment advice. No positions implied.

Code: MIT. `report/` text and figures: CC-BY-4.0.

Author: Malte Barth
