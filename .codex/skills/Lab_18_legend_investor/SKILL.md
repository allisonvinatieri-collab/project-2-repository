---
name: legend-investor
description: Analyze a public company with the Buffett-style 10-K checks when a user asks for a repeatable SEC EDGAR fundamentals review.
---

Use this skill for a Buffett-style business-quality review based only on SEC EDGAR company facts.

1. Run `scripts/Lab_18_edgar_buffett.py` for the requested ticker with a SEC-compliant User-Agent that contains the user's name and email. The script is the source of every numeric value.
2. Do not use price data, paid services, estimates, or figures that the script did not print. Keep `not found` and `not known` exactly as reported.
3. Write a short memo in the voice of a disciplined long-term business owner. Choose **own the business**, **watch it**, or **pass**; judge the business, never its price. If an owner-earnings input is missing, say the business cannot be judged on owner earnings.
4. Save the memo as `Lab_18_<TICKER>_buffett_memo.md` in the working directory. Before saving it, run the script with `--memo` to validate that every number in the memo also appears in the printed output.

The script applies these fixed rules: 10-K annual facts only; latest filing wins for a duplicated fiscal period; specified XBRL-tag fallbacks; five fiscal years labelled by fiscal-year-end date; and all three checks computed in code.
