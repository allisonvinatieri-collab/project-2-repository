# Project 2 — Fund Universe and Mandate

## Mandate

- **Objective:** earn at least **6.0% annualized return** using the five-year monthly adjusted-price sample.
- **Hard constraint:** hold at least **10%** in the cash-and-reserve sleeve (BIL).

This is a classroom exercise, not investment advice. The return objective is a testable historical-data hurdle, not a forecast or recommendation.

## Fund universe

| Ticker | Fund | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income |
| VT | Vanguard Total World Stock ETF | Equity |

## Price-data record

`Lab_15_prices.csv` contains 60 monthly **Adj Close** observations, oldest month first. Adjusted close is used because it reflects distributions.

| Ticker | Source | Download date |
|---|---|---|
| BIL | Yahoo Finance, Historical Data (monthly Adj Close) | 2026-10-20 |
| IEF | Yahoo Finance, Historical Data (monthly Adj Close) | 2026-10-20 |
| LQD | Yahoo Finance, Historical Data (monthly Adj Close) | 2026-10-20 |
| VT | Yahoo Finance, Historical Data (monthly Adj Close) | 2026-10-20 |

To reproduce the download, run `python Lab_15_download_prices.py` from this folder. The script retrieves Yahoo Finance monthly adjusted closes and retains the latest 60 common months.

## Streamlit data flow

Streamlit reruns this script from top to bottom whenever someone moves a control. Widget values persist through Streamlit's session state, so the new target or reserve minimum flows into the optimization and the displayed mix updates automatically.
