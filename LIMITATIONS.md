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
- Classifier: statements still LLM-on-bodies. Implementation notes default ADMIN and promote only on a Desk-directive operational change (RMP / SRF terms / ON RRP counterparty limit / new facility or swap / bill-purchase instructions → PLUMBING; reinvestment-cap or runoff-pace / purchase-programme start-taper → QE_QT; IORB/RRP/discount/primary-credit following the target range → ADMIN). Without this split, notes every ~6 weeks glue PLUMBING under a 30-day gap and push R3 Puncond above 0.5. 2.3: 34 ADMIN / 9 QE_QT / 4 PLUMBING notes; R3 Puncond=0.31. Spot-check: data/classifier_check_r23.csv.
- Rolling regressions on 6m-forward S&P have low R² by nature (partial R² ≈ 0.08); claims are relative, not absolute.
- Round 3 T6: reserves and yields share the Fed reaction function; a positive horse-race cell is consistent with reverse causation.
- Round 3 T8: lower MOVE in R3 would also be consistent with ZIRP and forward guidance; dropping 2020-03→2021-12 is partial mitigation, not a fix. ACM term premium skipped (Excel, not CSV).
