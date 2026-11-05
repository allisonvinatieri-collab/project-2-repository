---
name: lab-19-graham-investor
description: Run the Lab_19 Graham-style 10-K financial-strength screen from SEC EDGAR facts and write a number-verified Graham memo.
---

# Lab_19 Graham Investor

Use this skill for the Graham column of the Lab_19 investor panel.

1. Run `Lab_19_edgar_panel.py` with a SEC-compliant name-and-email User-Agent. Its printed annual 10-K facts are the sole numeric source.
2. Apply the code-defined checks: latest current ratio of at least 2.0, positive net income in every year, and net-income growth from the first reported year to the last.
3. Save `Lab_19_<TICKER>_graham_memo.md` in the working directory. State the Graham verdict (pass, watch, or fail) and use only values printed by the script.
4. Validate the memo with `--memo`; retain any missing inputs as `not known`, never as a pass or fail.
