# Committee Adoption Brief: Project 2

## Decision in two layers

A committee can adopt this application as a controlled, transparent decision-support workflow. It should **not** adopt the displayed allocation for capital deployment yet. The distinction matters: the application makes assumptions, data limits, constraints, and sensitivity visible; the allocation remains a historical teaching result rather than an investable recommendation.

## Decisions deliberately made in the design

| Design choice | Why it was chosen | Trade-off / rejected alternative |
| --- | --- | --- |
| Long-only 5% allocation grid | It makes every candidate allocation explainable and reproducible in a classroom committee setting. | A continuous optimizer or 1% grid appears more precise but would obscure the decision rule and overstate precision in a short sample. A 10% grid is too coarse. |
| Lowest-volatility feasible selection | The app first enforces the return and BIL-reserve rules, then chooses the least volatile allocation that meets both. | Maximizing return would ignore risk discipline; minimizing volatility without the return floor would fail the stated mandate. |
| BIL as the only reserve-eligible sleeve | The mandate’s cash/reserve requirement is made explicit and auditable in a single weight. | Treating IEF or LQD as reserve-eligible would change the constraint and must be approved by the mandate owner, not assumed by the model. |
| Net objective with a separate annual-cost control | It separates a visible policy assumption from the historical gross-price sample and lets the committee stress cost directly. | Pretending costs are zero in deployment would be misleading; presenting an invented detailed cost model would be less defensible than the explicit scenario control. |
| CPI as a point-in-time monitoring signal, not an optimizer input | It demonstrates that an observation cannot be used before its recorded release date without claiming that one CPI reading determines portfolio weights. | Feeding CPI into the allocation engine without a documented causal model would create unjustified complexity. |
| 20-point allocation-shift escalation trigger | The last-36-month window changes the selected mix by 20 points, so this threshold is tied to an observed material sensitivity. | A purely verbal “material change” standard is harder to govern and defend. |

## Verification discipline

The final engine uses 5% increments. A prior draft stated a 66% BIL / 34% VT one-point stress result, which is impossible under that grid. The final-engine rerun produced 65% BIL / 35% VT, and the automated known-answer test now prevents that mismatch from returning. This is the specific check that should be discussed in the defense video: the documented result was tested against the actual engine rather than accepted as AI-generated text.

## What a committee receives

- A fixed input sample and a visible as-of boundary.
- A transparent decision rule rather than a black-box allocation.
- Baselines for comparison, named sensitivity cases, and a point-in-time data gate.
- A stated action, a zero-capital starting position, and numeric review/escalation triggers.
- Runnable instructions, a dependency file, a cold-run record, and automated known-answer tests.

## What a committee must still approve before deployment

The mandate owner must approve a forward-looking objective, define reserve eligibility, document implementation costs and liquidity policy, test more return windows and correlations, and authorize any capital allocation. Until then, this app is suitable as a governance and analysis prototype—not as trading authorization.
