# Lab_19 — Legend Panel Workbook

**Question:** When three investors' skills read the same 10-K facts, where do they agree, where do they split — and would you trust the panel?

**Company used for the known-answer check:** Costco Wholesale Corporation (`COST`)

## Opener: explain the different lenses

Before looking at the screen, explain to a partner one way Graham or Burry would read Costco differently from Buffett.

- **Buffett:** focuses on high return on equity and owner earnings, asking whether the business consistently converts investment into owner cash.
- **Graham:** is more conservative about short-term liquidity. A company can be profitable but still fail his current-ratio rule.
- **Burry:** emphasizes cash conversion and leverage. He asks whether earnings become operating cash flow and whether liabilities are manageable relative to equity.

Partner discussion notes:

> Our discussion identified that Graham can pass a company on conservative liquidity and earnings tests while Buffett remains watchful about owner-earnings quality and Burry rejects it over a cash-flow or leverage concern. NVDA demonstrates that same difference: the investors use the same 10-K facts but prioritize different risks.

## Build: panel rules and same facts

All three investors use the same SEC EDGAR 10-K facts and retain missing inputs as `not known`.

| Investor | Checks computed in code |
|---|---|
| Buffett | ROE of 15% or more every year; owner earnings positive every year; owner earnings grew from first year to last |
| Graham | Latest current ratio of 2.0 or more; net income positive every year; net income grew from first year to last |
| Burry | Operating cash flow at least net income every year; latest liabilities no more than twice equity |

Formula: **current ratio = AssetsCurrent ÷ LiabilitiesCurrent**.

## Verify: COST facts and panel

| FY end | Current ratio | Liabilities ÷ equity |
|---|---:|---:|
| 2022-08-28 | 1.02 | 2.11 |
| 2023-09-03 | 1.07 | 1.75 |
| 2024-09-01 | 0.97 | 1.96 |
| 2025-08-31 | 1.03 | 1.64 |
| 2026-08-30 | 1.06 | 1.49 |

| Investor | Check | COST result |
|---|---|---|
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Graham | Current ratio of 2.0 or more, latest year | fail (1.06) |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first year to last | pass |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year | pass (1.49) |

**Panel summary:** Buffett is 3 of 3; Graham is 2 of 3; Burry is 2 of 2.

## Memos: COST

### Buffett memo

**Verdict: pass.**

Costco passes the Buffett business-quality checks: owner earnings are positive and growing, while return on equity clears the required level in every reported fiscal year. This is a durable business-quality result from the same SEC 10-K facts used by the full panel.

### Graham memo

**Verdict: fail.**

Costco's latest current ratio is 1.06, below Graham's 2.0 liquidity requirement. Net income is positive in every reported fiscal year and grows from the first year to the last, but the conservative liquidity screen keeps this verdict at fail.

**Threshold kept: current ratio ≥ 2.0.** I kept Graham's original conservative liquidity rule so the screen remains a clearly defined financial-strength test.

### Burry memo

**Verdict: pass.**

Operating cash flow meets or exceeds net income in every reported fiscal year. Latest liabilities divided by equity are 1.49, within the maximum of twice equity, so the cash-flow and leverage screen passes.

### Unprinted-number check

The panel checks every memo against the values printed by the panel script. The COST Graham memo was validated with no unprinted-number flag.

## Probe: threshold as a design choice

**Probe:** Lower Graham's current-ratio threshold from 2.0 to 1.0.

**Result:** Graham passes COST because the latest current ratio is 1.06.

**What this means:** a screen’s verdict is partly a consequence of its threshold design. The same company and facts do not change; the rule changes the classification.

## Your company

**Fund selected:** `VT` (BIL is the largest portfolio allocation, but it holds Treasury bills rather than a company with a 10-K.)

**Largest-company ticker selected and run:** `NVDA`

If that company has no EDGAR 10-K, use the fund’s next-largest company that does and record the substitution.

| Item | Your response |
|---|---|
| Ticker actually run | `NVDA` |
| Any EDGAR gap or substitute company | none |
| Buffett verdict | watch |
| Graham verdict | pass |
| Burry verdict | fail |
| Where the panel agreed | The panel did not reach a shared overall verdict: each investor produced a different conclusion. |
| Where the panel split | Graham passed NVDA, Buffett marked it watch, and Burry failed it. The split shows that profitability/liquidity, owner-earnings quality, and cash-flow/leverage tests can point in different directions on the same 10-K facts. |

Paste or summarize your company’s three generated memos here after running the panel:

> **Buffett: watch.** The Buffett checks did not produce an unqualified pass, so the business should be reviewed further before treating it as a business-quality screen pass.

> **Graham: pass.** NVDA met Graham's coded liquidity and net-income tests at the selected threshold.
>
> **Threshold kept: current ratio ≥ 2.0.** I kept the default conservative liquidity threshold so the Graham result remains comparable with the COST test.

> **Burry: fail.** At least one of the cash-flow-conversion or latest leverage checks failed, so the panel identifies a balance-sheet or cash-conversion risk that needs review.

## Explain the code to a partner

Open `build_panel_report` in `Lab_19_edgar_panel.py`. Explain, line by line, how it creates Graham’s results:

1. It loads the same EDGAR report used for Buffett and adds `AssetsCurrent`, `LiabilitiesCurrent`, and `Liabilities`.
2. It calculates the current ratio only when both current-asset and current-liability inputs are available and the denominator is not zero.
3. `latest(...)` returns `not known` when the latest ratio is missing; otherwise it returns `pass` or `fail` using Graham’s threshold.
4. `every_year(...)` returns `not known` if there are not five years or any input is missing; otherwise it applies the positive-net-income test to every year.
5. The first and last net-income values determine the growth test; a missing endpoint returns `not known`.

Partner question: **What does the code do when an input is missing?**

Answer: it keeps the check as **`not known`** rather than silently treating the company as a pass or fail.

## Bull and bear discussion

Use only the panel output for your company.

| Role | Two-sentence argument |
|---|---|
| Bear case | Burry's fail is the clearest warning because it means NVDA did not meet at least one cash-flow or leverage requirement. Buffett's watch verdict adds caution: the evidence is not strong enough to call it an unconditional business-quality pass. |
| Bull case | Graham's pass shows that NVDA met the panel's conservative liquidity and net-income growth tests. That positive result means the company clears an important financial-strength screen even though the other personas demand additional evidence. |

Partner notes:

> **Partner objection:** Burry's fail should prevent NVDA from passing a Project 2 screen because a weakness in cash conversion or leverage can undermine attractive earnings.
>
> **My response:** Graham's pass is meaningful evidence of financial strength, but I agree that Buffett's watch and Burry's fail require review of the underlying printed 10-K inputs before making a decision.

## Decision

**Would I let this panel screen companies for Project 2?** Only with the condition that a split result like NVDA's triggers review of the printed 10-K facts and no company passes automatically when an investor returns fail or watch.

## Learn: a panel of AI agents

**What is it?** A panel is a set of separate investor personas applying distinct, explicit rules to the same underlying facts.

**How does it work? Why can three personas disagree?** The facts remain the same, but each persona selects different ratios and thresholds. Buffett rewards business quality and owner earnings; Graham penalizes weak liquidity; Burry emphasizes cash conversion and balance-sheet leverage.

**Explain it to a partner:** The disagreement is not necessarily a data error. It shows the investment rule each persona treats as most important.

## Reflection and checkout

1. **Where did the panel agree on your company, and where did it split?**

   The panel did not agree on an overall NVDA verdict. Graham passed it, Buffett marked it watch, and Burry failed it; the split reflects their different emphasis on liquidity and earnings growth, owner-earnings quality, and cash flow or leverage.

2. **What does the threshold probe say about any screen’s verdict?**

   A verdict is conditional on the rule design. Changing a threshold can change a pass to a fail even though the company’s reported facts stay the same; COST showed this when Graham changed from fail at 2.0 to pass at 1.0.

3. **Would you trust the panel?**

   I would trust it as a transparent first screen, not as an automatic investment decision. NVDA's split verdict is useful because it identifies exactly where follow-up is needed, but it also shows that different rules can produce different conclusions from the same 10-K facts.

## Sources

- [SEC EDGAR companyfacts API](https://data.sec.gov/api/xbrl/companyfacts/)
- [FAskills financial-researcher plugin](https://github.com/CinderZhang/FAskills)
- [Streamlit documentation](https://docs.streamlit.io/)
