| Series | Source | First date | Frequency | Transform | Script |
|---|---|---|---|---|---|
| EFFR, 3m bill, 2y, 10y | Fed H.15 DDP zip `rel=H15` https://www.federalreserve.gov/datadownload/Output.aspx?rel=H15&filetype=zip | 1990-01-02 | daily | levels, percent | `src/fetch_fed.py` |
| Reserves (spliced) | H.3 `RESTR14A_N.M` to 2001-12; H.4.1 `RESH4R_N.WW` from 2002 | 1959-01 | monthly | USD millions; `splice` column | `src/fetch_fed.py` |
| Bill share | FiscalData MSPD table 1, Marketable https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/debt/mspd/mspd_table_1 | 2001-01 | monthly | bills / total marketable (incl. TIPS, FRN), percent | `src/fetch_fed.py` |
| SOFR, EFFR, p99, target | NY Fed markets API `search.json` 500-day windows | 2018-04-02 | daily | IORB = target_to − 0.10 | `src/fetch_fed.py` |
| Funding-stress proxy | H.15 then NY Fed | 1990-01 | daily | pre-2018 EFFR−3m bill (bp, 2y z); 2018→ SOFR−IORB | `src/fetch_fed.py` |
| S&P, MOVE, VIX, DXY, HYG, LQD | Yahoo chart API | see file | weekly + monthly | last close of week / month | `src/fetch_market.py` |
| FOMC statements | federalreserve.gov `fomchistorical{YYYY}.htm` → statement URL | 1997 | event | labels in `actions.csv` | `src/classify.py` |
| CPI y/y | BLS public API v2 series CUUR0000SA0 | 1990 | annual | December y/y (else last month) | `src/fetch_fed.py` |

Yahoo-derived series: derived weekly/monthly aggregates; raw daily not redistributed; rebuild with `--fetch`.
