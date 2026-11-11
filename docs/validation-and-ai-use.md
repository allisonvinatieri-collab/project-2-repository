# Validation and AI Use Record — Meridian Portfolio Decision System

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
| Cold run | A clean user can follow the README from a separate folder/environment. | **To complete before submission:** record partner command, first failure, elapsed time, result location, and resolution/limitation. | Open |

## Material limitations and monitoring

- Historical estimates are not forecasts and are sensitive to the return window.
- The prototype omits costs, taxes, liquidity constraints, rebalancing mechanics, and forward performance.
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
| Test owner and timestamp | `[your name and local timestamp before run]` |
| Immutable pre-run commit | `[commit hash created before execution]` |
| Material input and units | `[e.g., VT annualized historical-return estimate: 8.00% to 7.00%]` |
| Human-authored AI-off prediction | `[your prediction of allocation, return, risk, and decision effect]` |
| Expected direction | `[e.g., more VT required / risk rises / becomes infeasible]` |
| Expected decision effect | `[e.g., pilot recommendation unchanged, or return to committee]` |
| Execution command and date | `[exact command and date]` |
| Actual old/new output | `[paste app result, including units]` |
| Actual decision effect | `[state whether recommendation changed]` |
| Reconciliation / failure diagnosis | `[explain the match or divergence, including why]` |

The previously documented one-point VT test is useful sensitivity evidence, but it is **not** presented as a Locked Changed-Input Record because this repository does not yet preserve a verified pre-run, AI-off prediction and immutable pre-run commit for it.
