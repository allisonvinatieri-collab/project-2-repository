# Price Data Card — Project 2

| Field | Record |
| --- | --- |
| File | `Lab_15_prices.csv` |
| Assets | BIL, IEF, LQD, and VT |
| Source and retrieval method | Yahoo Finance chart endpoint; retrieved by `Lab_15_download_prices.py` using the documented monthly `adjclose` field for each ticker |
| Values | Monthly adjusted-close prices used to calculate monthly percentage returns |
| Sample boundary | 1 November 2021 through 20 October 2026; 60 price observations and 59 monthly returns |
| Intended use | Classroom historical-return, volatility, and correlation estimates for the constrained-search prototype |
| Controls | `estimates_from_prices` requires `Date` first, oldest-to-newest order, unique dates, and no missing values; the default known-answer test locks the resulting base allocation and metrics |
| Original retrieval timestamp | The static CSV does not preserve the original request timestamp. Its data boundary is evidenced by the dates in the committed file; a future production run must save the retrieval timestamp and raw response. |
| Adjustment limitation | The download script requests Yahoo Finance's `adjclose` series. The project does not independently audit Yahoo's adjustment methodology. |
| Decision limitation | The sample is adequate for the classroom prototype but not sufficient for capital deployment without source verification, an adjustment-method audit, additional history, and implementation-cost/liquidity review. |

The price sample is deliberately separated from the point-in-time CPI monitoring input. The CPI data card and publication-date control are documented in `Lab_17.md`; CPI is not used to estimate returns or choose portfolio weights.
