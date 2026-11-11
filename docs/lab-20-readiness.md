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
| Partner name | `[fill in]` |
| Date/time | `[fill in]` |
| Command used | `[paste exact command]` |
| First failure, if any | `[fill in; write “none” only if no failure]` |
| Elapsed time | `[fill in]` |
| Where the result appeared | `[fill in]` |
| Fix made and pushed, or clean-run note | `[fill in]` |
| Rerun outcome | `[fill in]` |

## Changed input — AI closed from here

Do not ask an AI to select, predict, or interpret this test. Before executing a fresh test, complete every **Pre-run** row in your own words, save it, commit it, and push it. Only then run the app and complete the outcome rows.

| Field | Record |
| --- | --- |
| **Pre-run — input and units** | `[example format only: annualized VT return estimate, 8.0% → 7.0%]` |
| **Pre-run — why it is load-bearing** | `[your words]` |
| **Pre-run — human prediction of number direction** | `[your words]` |
| **Pre-run — expected decision effect** | `[your words]` |
| **Pre-run — commit and push** | `[commit hash]` |
| Run command/date | `[fill in after the commit]` |
| Actual before/after output | `[paste values and units]` |
| Did the decision change? | `[fill in]` |
| Why the outcome matched or differed from your prediction | `[your words]` |

Afterward, copy the completed record into `docs/validation-and-ai-use.md` so the final submission contains the same evidence.

## Code explanation target

Open `Lab_15_portfolio.py` and explain `lowest_risk_mix` to your partner:

1. It enumerates long-only 5% weight combinations that sum to 100%.
2. It rejects combinations below the return objective or BIL reserve floor.
3. It calculates volatility for each feasible combination.
4. It retains the feasible combination with the lowest volatility.

Then explain how `app.py` passes the mandate controls and selected return window into this function. Record the one question your partner asks:

`[partner question and your answer]`

## Must-fix list before / at Lab 20

- [ ] Commit and push the current Project 2 package so the partner opens the same version you test.
- [ ] Personally review the app's default numbers and replace the student-sign-off wording in README and required documents only if accurate.
- [ ] Perform the partner cold run; fix its first failure or record a clean run.
- [ ] Complete the AI-closed changed-input test above; do not backfill it.
- [ ] Add completed video links and corrected transcripts before the final Project 2 submission.

The videos and their transcript placeholders are not evidence yet. They are final-project work, not something to fabricate for this readiness lab.
