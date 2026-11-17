# Validation and AI Use Record: Project 2 Portfolio Mandate & Stress-Test Decision System

**AI announcement:** Generative AI assisted with code and documentation. I verified the reported calculations and own the analysis and decision. **Education, not investment advice.**

## Data, source boundary, and point-in-time control

| Input | Source / as-of boundary | Control | Limitation |
| --- | --- | --- | --- |
| `Lab_15_prices.csv` | Included monthly adjusted-price sample, November 2021–October 2026. | CSV schema, monotonic-date, duplicate-date, and missing-value checks run in `estimates_from_prices`. | The stored file is a limited historical sample; the app does not independently verify the vendor or adjustment methodology. |
| `ALFRED_CPIAUCSL_vintages.csv` | CPIAUCSL/FRED-ALFRED record downloaded 29 October 2026; publication dates are stored with observations. | The app includes only rows published on or before the selected decision date. | The supplied vintage table is a documented monitoring record, not a complete production vintage database. |

The CPI data card is documented in `Lab_17.md`. CPI is a monitoring signal only; it is not used to estimate portfolio returns or select weights.

## Tests and observed results

| Test | Expected result | Observed result | Status |
| --- | --- | --- | --- |
| Default constrained search | A feasible 5%-increment mix satisfying a 6.0% annualized historical-return objective and 10% BIL minimum. | 70% BIL / 30% VT; 6.07% return estimate, 4.54% volatility, 70% BIL. | Pass |
| Last-36-month window | A feasible mix may differ because estimates depend on the sample. | 85% BIL / 5% LQD / 10% VT; 6.08% return estimate, 1.48% volatility. Largest change from full sample: 20 points. | Pass; material sensitivity identified |
| One-point VT estimate reduction | A feasible mix may require more VT and higher volatility. | 66% BIL / 34% VT; 6.04% return estimate, 5.13% volatility. | Pass; estimation risk identified |
| Point-in-time CPI gate | A CPI release dated after the chosen decision date must be excluded. | On 30 September 2026, September CPI is excluded because its recorded publication date is 14 October 2026. | Pass |
| Cold run | A clean user can follow the README from a separate folder/environment. | On 17 November 2026, a partner followed the README setup/run command, reached the Streamlit app in 2 minutes 30 seconds, and reported no first failure. Result: local Streamlit browser at `http://localhost:8501`; no fix or rerun was needed. | Pass |

## Material limitations and monitoring

- Historical estimates are not forecasts and are sensitive to the return window.
- The prototype uses an illustrative annual-cost stress assumption but omits measured trading costs, taxes, liquidity constraints, rebalancing mechanics, and forward performance.
- The 5% allocation grid is transparent but does not establish global precision.
- A failed point-in-time data gate, an infeasible stress case, or material allocation instability triggers committee review.

## AI-use disclosure and verification log

| AI tool / model / date | Material use | Student verification and disposition |
| --- | --- | --- |
| Codex / GPT-5 / 10 November 2026 | Helped organize the existing lab code into the runnable `app.py` and draft repository documentation. | Re-run the app using the README defaults; verify every number against the app and source files before submission. Do not claim this row is complete until you have performed and documented that check. |
| **Add any other tool used** | **Describe the prompt/output or coding assistance that materially affected the work.** | **Record the specific source, calculation, or test used to accept, qualify, correct, or reject it.** |

## Locked Changed-Input Record — required before execution

> Do not backfill this section. Before running a new changed-input test, write your own prediction with AI off, replace the bracketed fields below, commit the file to GitHub, and record that commit hash. Then run the test with no AI assistance and complete the outcome fields.

| Field | Record |
| --- | --- |
| Test owner and timestamp | Student; 17 November 2026, before execution. |
| Immutable pre-run commit | `f4f8368` — Record Lab 20 changed-input prediction. |
| Material input and units | Minimum BIL reserve weight: 10% → 20%. |
| Human-authored AI-off prediction | Portfolio weight, return estimate, and volatility would increase; feasibility would decrease, meaning fewer allocations meet the rules; the committee decision would remain pilot. |
| Expected direction | More BIL, higher return estimate, higher volatility, and fewer feasible allocations. |
| Expected decision effect | Pilot recommendation unchanged. |
| Execution command and date | `python -m streamlit run app.py`; 17 November 2026. |
| Actual old/new output | Before and after: 70% BIL / 0% IEF / 0% LQD / 30% VT; 6.07% annualized historical-return estimate; 4.54% annualized volatility; 70% BIL reserve weight. The app found a feasible allocation in both runs; it does not display the number of feasible allocations. |
| Actual decision effect | No change: pilot, not adopt. |
| Reconciliation / failure diagnosis | The allocation, return estimate, and volatility did not change because the 20% BIL floor was nonbinding: the selected base allocation already held 70% BIL. The test therefore did not establish whether the number of feasible allocations declined. |

The previously documented one-point VT test is useful sensitivity evidence, but it is **not** presented as a Locked Changed-Input Record because this repository does not yet preserve a verified pre-run, AI-off prediction and immutable pre-run commit for it.
