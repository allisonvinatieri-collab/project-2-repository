# Visible Executed Output — Default Run

Run date: 10 November 2026. Command: `streamlit run app.py`.

**AI announcement:** Generative AI assisted with code and documentation. I verified the reported calculations and own the analysis and decision. **Education, not investment advice.**

## Inputs

| Input | Value |
| --- | --- |
| Price sample | `Lab_15_prices.csv`, 1 November 2021–20 October 2026 |
| Return window | All available monthly returns (59) |
| Return objective | 6.0% annualized historical-return estimate |
| Reserve-eligible asset and minimum | BIL; 10% minimum weight |
| Allocation search | Long only, 5% increments |
| Point-in-time monitoring date | 30 September 2026 |

## Result

| Portfolio | Annualized historical return | Annualized volatility | BIL reserve weight | Mandate verdict |
| --- | ---: | ---: | ---: | --- |
| Equal weight | 3.25% | 7.55% | 25% | Fail: return objective |
| Inverse volatility | 3.46% | 1.32% | 88% | Fail: return objective |
| Constrained search | 6.07% | 4.54% | 70% | Pass |

The constrained portfolio is 70% BIL, 0% IEF, 0% LQD, and 30% VT.

## Stress and monitoring output

- Reducing the VT annualized historical-return estimate by one percentage point yields 66% BIL / 0% IEF / 0% LQD / 34% VT, a 6.04% return estimate, and 5.13% volatility.
- For a 30 September 2026 decision date, the point-in-time CPI gate admits the August 2026 CPI value (334.131), published on 11 September 2026, and excludes the September observation because it was published on 14 October 2026.
- Recommendation: **pilot, not adopt**. See [the decision memo](decision-memo.md) for the conditions and reversal triggers.
