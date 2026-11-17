# Lab 20 Readiness — Bring This to Tuesday

Repository: `https://github.com/allisonvinatieri-collab/project-2-repository`

## Decision line

**Pilot, not adopt:** do not allocate capital until the return objective, reserve definition, implementation costs, and robustness review are approved; reverse this position and return to committee review if a reasonable stress is infeasible, allocations are materially unstable across approved windows, or a point-in-time data control fails.

## Starting point for your partner's cold run

Send only the repository link above. They should follow this command from the README:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Expected default result: 70% BIL / 0% IEF / 0% LQD / 30% VT; 6.07% annualized historical-return estimate; 4.54% volatility; 70% BIL reserve weight; decision: **pilot, not adopt**.

### Partner cold-run note — complete in class

| Field | Partner's record |
| --- | --- |
| Partner name | Catie Moe |
| Date/time | 17 November 2026, during Lab 20 |
| Command used | README setup and run command: `python -m venv .venv`; `.\.venv\Scripts\Activate.ps1`; `python -m pip install -r requirements.txt`; `python -m streamlit run app.py` |
| First failure, if any | None |
| Elapsed time | 2 minutes 30 seconds |
| Where the result appeared | Streamlit app in the local browser (`http://localhost:8501`) |
| Fix made and pushed, or clean-run note | Clean cold run; no fix needed. |
| Rerun outcome | Not needed; first run reached the result. |

## Changed input — AI closed from here

Do not ask an AI to select, predict, or interpret this test. Before executing a fresh test, complete every **Pre-run** row in your own words, save it, commit it, and push it. Only then run the app and complete the outcome rows.

| Field | Record |
| --- | --- |
| **Pre-run — input and units** | Minimum BIL reserve weight: 10% → 20%. |
| **Pre-run — why it is load-bearing** | The minimum BIL reserve weight is a hard mandate constraint, so it determines which allocations can pass the mandate. |
| **Pre-run — human prediction of number direction** | I predict portfolio weight to increase, return estimate to increase, volatility to increase, and feasibility to decrease, meaning fewer allocations meet the rules. |
| **Pre-run — expected decision effect** | I expect the committee decision to stay pilot. |
| **Pre-run — commit and push** | `[commit hash]` |
| Run command/date | `python -m streamlit run app.py`; 17 November 2026. |
| Actual before/after output | Before and after raising the BIL floor from 10% to 20%, the app returned 70% BIL / 0% IEF / 0% LQD / 30% VT; 6.07% annualized historical-return estimate; 4.54% annualized volatility; 70% BIL reserve weight. A feasible allocation appeared in both runs. The app does not display a count of feasible allocations. |
| Did the decision change? | No. The recommendation remained pilot, not adopt. |
| Why the outcome matched or differed from your prediction | The prediction did not match the observed allocation and return/risk results. The 20% BIL floor was nonbinding because the selected base allocation already held 70% BIL, so increasing the floor from 10% to 20% did not force a different allocation. |

Afterward, copy the completed record into `docs/validation-and-ai-use.md` so the final submission contains the same evidence.

## Code explanation target

Open `Lab_15_portfolio.py` and explain `lowest_risk_mix` to your partner:

1. It enumerates long-only 5% weight combinations that sum to 100%.
2. It rejects combinations below the return objective or BIL reserve floor.
3. It calculates volatility for each feasible combination.
4. It retains the feasible combination with the lowest volatility.

Then explain how `app.py` passes the mandate controls and selected return window into this function. Record the one question your partner asks:

**Catie Moe's question:** Why do you return the lowest-volatility feasible long-only allocation in 5% steps, instead of 1% or 10% steps?

**My answer:** I use 5% steps because they balance transparency and precision. A 10% grid is too coarse and could miss a reasonably lower-risk feasible allocation, while a 1% grid creates far more combinations and suggests more precision than this short historical sample supports. The 5% grid is simple enough to explain and reproduce, while still showing how the mandate constraints affect the portfolio.

## Must-fix list before / at Lab 20

- [ ] Commit and push the current Project 2 package so the partner opens the same version you test.
- [ ] Personally review the app's default numbers and replace the student-sign-off wording in README and required documents only if accurate.
- [x] Partner cold run completed: clean first run in 2 minutes 30 seconds; no fix needed.
- [ ] Complete the AI-closed changed-input test above; do not backfill it.
- [ ] Add completed video links and corrected transcripts before the final Project 2 submission.

The videos and their transcript placeholders are not evidence yet. They are final-project work, not something to fabricate for this readiness lab.
