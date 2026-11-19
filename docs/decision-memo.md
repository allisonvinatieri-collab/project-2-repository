# Decision Memo: Project 2 Portfolio Mandate & Stress-Test Decision System

**AI announcement:** Generative AI assisted with code and documentation. I verified the reported calculations and own the analysis and decision. **Education, not investment advice.**

## Committee ask and recommendation

**Ask:** adopt the application as a controlled pre-trade decision-support workflow and authorize a limited pilot only after the mandate owner approves the return objective, reserve definition, and implementation assumptions.

**Recommendation:** **adopt the workflow; pilot, do not adopt the allocation and do not allocate capital yet.** The app's constrained historical estimate meets the displayed classroom rules, but it is sensitive to the estimation window and omits material real-world inputs. A pilot begins at **0% investable allocation** until the validation conditions below are satisfied. The sensitivity envelope below is an analytical range for a future approved paper or controlled pilot; it is not capital-allocation authority.

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

## Allocation range, not false point precision

| Sleeve | Sensitivity envelope | Evidence in the named cases |
| --- | ---: | --- |
| BIL | 60%–85% | Base 70%; one-point VT stress 65%; last-36-month window 85%; two-point VT and cost stresses 60%. |
| IEF | 0% | Zero in the selected named cases. |
| LQD | 0%–5% | Last-36-month window selects 5%; other named cases select zero. |
| VT | 10%–40% | Last-36-month window 10%; base 30%; one-point VT stress 35%; two-point VT and cost stresses 40%. |

The current investable range is therefore **0% capital deployment**. The table is a model-sensitivity range only; using it for a funded pilot requires the conditions below.

## Evidence and stress result

When the sample changes from all available observations to the last 36 monthly returns, the lowest-risk feasible allocation changes from 70% BIL / 30% VT to 85% BIL / 5% LQD / 10% VT. The largest individual allocation change is 20 percentage points. In the one-point return-estimate stress, reducing VT's annualized historical-return estimate by one percentage point produces a feasible but different portfolio: 65% BIL / 35% VT, with a 6.11% historical-return estimate and 5.28% volatility. The 5%-increment constraint explains why the selected mix changes in 5-point steps.

The point-in-time CPI panel is a monitoring control rather than an optimizer input. It permits an observation only after its recorded publication date, preventing the use of an inflation release that was not knowable on the decision date.

## Conditions, monitoring, and reversal trigger

Do not move from pilot to an investable allocation until all of the following are complete:

1. Document a mandate-approved forward-looking objective, approved reserve eligibility, transaction-cost assumption, and liquidity policy.
2. Re-run the analysis over additional non-overlapping windows and plausible return/correlation/cost assumptions.
3. Verify the exact price source, adjusted-price methodology, as-of date, and every point-in-time input.
4. Pre-register and execute the Locked Changed-Input Record in the validation file.

Return the process to committee review—and stop any pilot—if a reasonable stress produces no feasible allocation, the selected mix shifts materially across approved windows, the BIL floor is breached, a source cannot be traced as of its decision date, or realized operating conditions materially differ from the assumed cost/liquidity conditions.

## Numeric reversal thresholds and review timing

Review the pilot at every month-end. Return it to committee review within five business days if any pre-specified stress produces no feasible 5%-grid allocation or if any sleeve differs by **20 percentage points or more** across approved windows. Also stop the pilot within five business days if BIL is below the approved floor or the point-in-time source control fails. These are governance triggers, not trading instructions.

## Principal limitations

This is a teaching prototype, not an investable model. It uses a short historical sample, arithmetic annualization, no trading costs or taxes, no rebalancing simulation, and a coarse 5% allocation grid. It should not be treated as a forecast, personalized advice, or authorization to trade.
