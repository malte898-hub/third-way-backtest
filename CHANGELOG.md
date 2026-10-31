# Changelog

## 3.0 — tests from the author's reply (T6–T8)

GO 2026-10-31. T1–T5 constants not edited. T6–T8 frozen as source=default (no numerical predictions supplied in writing). Run once, published either way.

- DATA: BTC-USD weekly 2014-09→. ACM 10y term premium skipped (NY Fed file is Excel, not CSV).
- T6 target substitution on T4's 60-month horse race. y1 Δ10y FAIL (X3 25% of 2021→ windows); y2 slope PASS (77%); y3 Treasury-return proxy FAIL (31%); y4 BTC PASS (X2/X3 100%, n=21). Reverse-causation caveat in the report.
- T7 lag scan: 7b 2021→ ΔMOVE→6m SPX best k=2, partial R² not ≥ 2× k=1 → FAIL (frozen: k≤2 fails).
- T8 MOVE footprint (exclusion sample): 0/3. R3 12m std(ΔMOVE) is *higher* than R2, not 20% lower; weekly β also higher; distributed lags on reserves/bills not significant. Identification problem stated.

## 2.1 — correction

Oct–Nov 2025: reserve drain → QT ended 2025-12-01 and reserve-management bill purchases began 2025-12-12, announced at the 2025-10-29 and 2025-12-10 FOMC meetings alongside two 25 bp cuts. First STRESS print 2025-10-15; first plumbing announcement 2025-10-29 (10 sessions). No T1–T5 numbers changed in 2.1.

## 2.2 — FOMC statements 2020–2026 added; T2/T3 rerun; what moved

Hole: fomchistorical{YYYY}.htm exists only for years with released transcripts (five-year lag). Labelled FOMC statements after 2019-12-11 were missing from the public action table (a few 2020 historical statements were present; 2021–2026 were not). No 2022-05-04 QT plan, no 2025-10-29 QT end, no 2025-12-10 RMP.

Fix: harvest fomccalendars.htm Statement + Implementation Note links. Same prompt and model on bodies. Gates: 2020-03-15 QE_QT; 2022-05-04 QE_QT; 2025-10-29 QE_QT+RATE; 2025-12-10 PLUMBING rmp=1+RATE — all PASS. Added NY Fed 2019-09-17 desk repo as source=NYFed PLUMBING. Treasury 2026-08-01 buyback XML/PDF source=Treasury (n=2), excluded from Fed PLUMBING counts. Pre-2020 minutes as actions: 0.

Moved (T2/T3 only; T1/T4/T5 not rerun; thresholds frozen):

| | Round 2 | Round 2.2 |
|---|---|---|
| actions n | 192 | 298 |
| T2 plumbing n | 80 | 80 |
| T2 plumbing FIRST_MOVER | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN |
| T2 plumbing RESOLVER | RATE / QE_QT / PLUMBING | RATE / QE_QT / PLUMBING+RATE |
| T2 equity RESOLVER | RATE / QE_QT / RATE | RATE / QE_QT / PLUMBING+RATE |
| T3 R1 | 5.64× p=0.001 | 5.64× p=0.001 |
| T3 R2 | 0.74× p=1.00 | 0.74× p=1.00 |
| T3 R3 | 1.19× p=0.054 | 1.13× p=0.001; Puncond=0.62 no_power |
| PLUMBING Fed+NYFed rows / 60d episodes / 30d | — | 56 / 6 / 52 |
| first Treasury-follows-breach year | 2026 | 2026 |

R3 modal resolver is a RATE/PLUMBING tie (implementation notes + cuts). Frozen PASS/FAIL still FAIL on T2 (FIRST_MOVER) and T3 (ratio < 1.5 and R3 < R1).

## 2.3 — implementation notes classified ADMIN; T2/T3 rerun; thresholds unchanged

Implementation notes (`a1.htm`) default to ADMIN. Promote only when the Desk directive’s ops skeleton changes vs the previous note (regex on purchase / reinvest / cap / counterparty limit / standing repo / swap line; IORB/RRP/primary-credit resets that follow the target range stay ADMIN). Statements keep 2.2 labels. ADMIN is excluded from T2 resolvers and the T3 action set.

Gates: 2025-12-10 note PLUMBING rmp=1; 2022-05-04 note QE_QT; 2021-07-28 note PLUMBING; 2023 notes that only reset IORB → ADMIN. Rule in `src/classify.py`.

| | Round 2 | Round 2.2 | Round 2.3 |
|---|---|---|---|
| T2 plumbing n | 80 | 80 | 80 |
| T2 plumbing FIRST_MOVER | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN | FUN / RATE_EXP / FUN |
| T2 plumbing RESOLVER | RATE / QE_QT / PLUMBING | RATE / QE_QT / PLUMBING+RATE | RATE / QE_QT / RATE |
| T3 n_actions | 78 | 138 | 104 |
| T3 R1 | 5.64× p=0.001 | 5.64× p=0.001 | 5.64× p=0.001 Puncond=0.010 |
| T3 R2 | 0.74× p=1.00 | 0.74× p=1.00 | 0.74× p=1.00 Puncond=0.471 |
| T3 R3 | 1.19× p=0.054 | 1.13× p=0.001; Puncond=0.62 no_power | 1.14× p=0.005 Puncond=0.312 |
| PLUMBING rows / 60d / 30d | — | 56 / 6 / 52 | 12 / 9 / 9 |

Frozen criteria: T2 FAIL (FIRST_MOVER). T3 FAIL (R3 1.14 < 1.5 and < R1). R3 has power again (Puncond 0.31 < 0.5). T1/T4/T5 not rerun. T2 equity-def not rerun (press feed has no implementation notes).

## Round 2 (instruments only; thresholds frozen)

- T1: same fail; added CPI y/y 2×2 and April 2025 week exhibit.
- T2: FOMC bodies labelled; plumbing-defined episodes added. RESOLVER RATE → QE_QT → PLUMBING on that incomplete feed.
- T3: action set = PLUMBING + QE_QT + RATE off the FOMC statement calendar. R1 5.6×; R3 1.19, p=0.054.
- T4: X3 without MOVE so the sample starts 1990.
- T5: 50 twelve-month block-shuffles.

Round 1 used press titles (2016+ year pages only), so QE_QT count was zero.
