# Price Data Card — Project 2

| Field | Record |
| --- | --- |
| File | `Lab_15_prices.csv` |
| Assets | BIL, IEF, LQD, and VT |
| Values | Monthly adjusted-close prices used to calculate monthly percentage returns |
| Sample boundary | 1 November 2021 through 20 October 2026; 60 price observations and 59 monthly returns |
| Intended use | Classroom historical-return, volatility, and correlation estimates for the constrained-search prototype |
| Controls | `estimates_from_prices` requires `Date` first, oldest-to-newest order, unique dates, and no missing values; the default known-answer test locks the resulting base allocation and metrics |
| Vendor / adjustment provenance | The committed course sample does not contain a vendor identifier, download timestamp, or adjustment-method documentation. The app does not claim independent vendor verification. |
| Decision limitation | The sample is adequate for the classroom prototype but not sufficient for capital deployment without source verification, a documented adjusted-price methodology, additional history, and implementation-cost/liquidity review. |

The price sample is deliberately separated from the point-in-time CPI monitoring input. The CPI data card and publication-date control are documented in `Lab_17.md`; CPI is not used to estimate returns or choose portfolio weights.
