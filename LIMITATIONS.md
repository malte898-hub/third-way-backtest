- Action-feed coverage (labelled files; year × source × doc_type):

| years | source | doc_type | n |
|---|---|---|---|
| 1997–2019 | Fed | statement | 8/yr typical (1997=1; 2001=11; 2008=11) |
| 2019-09-17 | NYFed | desk_statement | 1 (ad-hoc repo) |
| 2020 | Fed | statement | 13 |
| 2021–2026 | Fed | statement | 9, 11, 9, 9, 9, 8 |
| 2021–2026 | Fed | implementation_note | 8, 8, 8, 8, 8, 7 |
| 2026-08-01 | Treasury | buyback | 2 (XML+PDF schedule only) |

Refresh via https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm (feed goes stale by one year per year). Statements only — press-conference remarks not coded, so plumbing motivation is under-counted. Pre-2020 minutes were not counted as actions (n=0). 1996–2015 year press archives 404; those years rest on FOMC statement bodies.

- MOVE available from 2002 only; with-MOVE tests cannot see pre-2008.
- Reserves series is a splice: H.3 total reserves to 2001, H.4.1 balances from 2002; not the same concept, no level adjustment.
- Pre-2018 funding-stress proxy (EFFR − 3m bill) cannot observe repo.
- Treasury actions almost unobserved (n=2 buyback files, 2026); corridor test is Fed-only. First Treasury-follows-breach year: 2026.
- Episode-level Treasury sign hides intra-episode spikes (Mar 2020); see MAX_10Y_RISE_4W.
- Classifier is an LLM on titles/bodies; 20 new-row spot-check in results/classifier_check_r22.csv. Implementation notes every ~6 weeks are often PLUMBING; 60-day clustering yields 6 episodes, 30-day clustering yields 52. QT/RMP language saturates R3 (Puncond>0.5).
- Rolling regressions on 6m-forward S&P have low R² by nature (partial R² ≈ 0.08); claims are relative, not absolute.
