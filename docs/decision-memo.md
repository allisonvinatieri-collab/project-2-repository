# Decision Memo — Meridian Portfolio Decision System

**AI announcement — student sign-off required before submission:** Generative AI assisted with code and documentation. Replace this sentence only after personal review: “I verified the reported calculations and own the analysis and decision.” **Education, not investment advice.**

## Committee ask and recommendation

**Ask:** authorize a limited pilot only after the mandate owner approves the return objective, reserve definition, and implementation assumptions.

**Recommendation:** **pilot, not adopt and not allocate capital yet.** The app's constrained historical estimate meets the displayed classroom rules, but it is sensitive to the estimation window and omits material real-world inputs. A pilot should begin at **0% investable allocation** until the validation conditions below are satisfied; any later allocation range must be set by the mandate owner after costs, liquidity, and a forward test are documented.

## Mandate and current result

| Item | Record |
| --- | --- |
| Objective | At least 6.0% annualized historical-return estimate. |
| Universe | BIL, IEF, LQD, and VT. |
| Hard constraint | At least 10% in BIL. |
| Risk measure | Annualized volatility from monthly adjusted-price returns. |
| Base window | November 2021–October 2026; 59 monthly returns. |
| Base constrained result | 70% BIL / 0% IEF / 0% LQD / 30% VT. |
| Historical return estimate / volatility | 6.07% / 4.54%. |
| Rule verdict | Passes the stated historical-return and BIL-reserve rules. |

The equal-weight and inverse-volatility baselines are displayed alongside the constrained portfolio in `app.py`. They make the central limitation visible: neither baseline clears the 6.0% historical-return objective under the supplied sample, while the constrained search is selected precisely at the feasibility boundary.

## Evidence and stress result

When the sample changes from all available observations to the last 36 monthly returns, the lowest-risk feasible allocation changes from 70% BIL / 30% VT to 85% BIL / 5% LQD / 10% VT. The largest individual allocation change is 20 percentage points. In the one-point return-estimate stress, reducing VT's annualized historical-return estimate by one percentage point produces a feasible but different portfolio: 66% BIL / 34% VT, with a 6.04% historical-return estimate and 5.13% volatility.

The point-in-time CPI panel is a monitoring control rather than an optimizer input. It permits an observation only after its recorded publication date, preventing the use of an inflation release that was not knowable on the decision date.

## Conditions, monitoring, and reversal trigger

Do not move from pilot to an investable allocation until all of the following are complete:

1. Document a mandate-approved forward-looking objective, approved reserve eligibility, transaction-cost assumption, and liquidity policy.
2. Re-run the analysis over additional non-overlapping windows and plausible return/correlation/cost assumptions.
3. Verify the exact price source, adjusted-price methodology, as-of date, and every point-in-time input.
4. Pre-register and execute the Locked Changed-Input Record in the validation file.

Return the process to committee review—and stop any pilot—if a reasonable stress produces no feasible allocation, the selected mix shifts materially across approved windows, the BIL floor is breached, a source cannot be traced as of its decision date, or realized operating conditions materially differ from the assumed cost/liquidity conditions.

## Principal limitations

This is a teaching prototype, not an investable model. It uses a short historical sample, arithmetic annualization, no trading costs or taxes, no rebalancing simulation, and a coarse 5% allocation grid. It should not be treated as a forecast, personalized advice, or authorization to trade.
