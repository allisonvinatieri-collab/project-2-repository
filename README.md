# Project 2 — Meridian Portfolio Decision System

**AI announcement:** Generative AI assisted with code and documentation. I verified the reported calculations and own the analysis and decision. **Education, not investment advice.**

## Committee decision

**Recommendation: pilot, not adopt.** The constrained allocation can meet the classroom historical-return and BIL-reserve rules, but the allocation changes when the estimation window changes. Do not allocate capital until the return objective, reserve definition, implementation costs, and robustness criteria are approved. See [the decision memo](docs/decision-memo.md).

## What this app does

The Streamlit app compares an equal-weight baseline, an inverse-volatility baseline, and a 5%-increment long-only constrained allocation across BIL, IEF, LQD, and VT. It tests the historical-return objective and BIL reserve floor, shows a one-input stress run, and displays an inflation-monitoring signal using a dated CPI vintage record.

The historical price sample runs from November 2021 through October 2026. Historical estimates are not forecasts.

## Run locally

Requires Python 3.11+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints. No API keys, network calls, or external downloads are required.

## Repository map

| Location | Purpose |
| --- | --- |
| `app.py` | Final runnable investment-management app. |
| `Lab_15_portfolio.py` | Historical-estimate and constrained-search engine. |
| `lab_14_portfolio.py` | Portfolio math and baseline-weight functions. |
| `Lab_15_prices.csv` | Monthly adjusted-price input for BIL, IEF, LQD, and VT. |
| `ALFRED_CPIAUCSL_vintages.csv` | Dated CPI vintage record for the point-in-time monitoring gate. |
| `docs/decision-memo.md` | Committee recommendation and conditions. |
| `docs/validation-and-ai-use.md` | Data, validation, limitations, AI-use record, and Locked Changed-Input Record. |
| `docs/visible-output.md` | Executed default-run inputs and results viewable without starting the app. |
| `docs/transcript-video-*.txt` | Corrected transcripts to add after recording the three required videos. |

## Mandate

- **Objective:** at least a 6.0% annualized historical-return estimate.
- **Universe:** BIL (reserve/cash), IEF (Treasury bonds), LQD (investment-grade corporate bonds), and VT (global equities).
- **Benchmark / baselines:** equal weight and inverse volatility.
- **Risk measure:** annualized volatility calculated from monthly adjusted-price returns.
- **Hard limit:** at least 10% in BIL.

## Data and known limitations

- The price file contains a limited historical sample and has no transaction costs, taxes, liquidity costs, or forward returns.
- The app searches allocations only in 5% increments; it is deliberately transparent, not a production optimizer.
- CPI is a monitoring signal rather than a return-model input. The app admits an observation only when its recorded publication date is on or before the selected decision date.
- A pass in the app means only that the stated historical estimate and reserve rule passed. It does not mean the strategy is suitable for investment or will meet its objective.

## Reproducibility check

With the defaults (all available returns, 6.0% objective, 10% BIL floor), the constrained search should return 70% BIL / 30% VT, a 6.07% annualized historical-return estimate, 4.54% annualized volatility, and 70% BIL. The complete validation record is in [docs/validation-and-ai-use.md](docs/validation-and-ai-use.md).
