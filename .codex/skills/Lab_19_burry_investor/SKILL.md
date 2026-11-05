---
name: lab-19-burry-investor
description: Run the Lab_19 Burry-style 10-K cash-flow and leverage screen from SEC EDGAR facts and write a number-verified Burry memo.
---

# Lab_19 Burry Investor

Use this skill for the Burry column of the Lab_19 investor panel.

1. Run `Lab_19_edgar_panel.py` with a SEC-compliant name-and-email User-Agent. Its printed annual 10-K facts are the sole numeric source.
2. Apply the code-defined checks: operating cash flow at least net income every year, and latest liabilities no more than twice equity.
3. Save `Lab_19_<TICKER>_burry_memo.md` in the working directory. State the Burry verdict (pass, watch, or fail) and use only values printed by the script.
4. Validate the memo with `--memo`; retain any missing inputs as `not known`, never as a pass or fail.
