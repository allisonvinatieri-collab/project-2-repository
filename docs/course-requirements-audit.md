# Project 2 Course-Requirements Audit

Audit basis: the course [Project 2 brief](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-2-investment-management-application.md), the [major-project submission architecture](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/PROJECT-SUBMISSION-ARCHITECTURE.md), and the [student checklist](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/major-project-student-checklist.md). Reviewed 19 November 2026.

## Eight Project 2 base requirements

| Requirement | Evidence in this repository | Status |
| --- | --- | --- |
| Runnable Python web app a stranger can operate from the README | `app.py`, `README.md`, `requirements.txt`, partner cold-run record in `docs/lab-20-readiness.md`, and a fresh-clone cold run in `docs/validation-and-ai-use.md` | Complete |
| Mandate: objective, universe, benchmark, risk measure, and limits | `README.md`, `docs/decision-memo.md`, and Technical detail view in `app.py` | Complete |
| Equal-weight baseline, second transparent baseline, constrained portfolio, and verdicts | Committee view in `app.py`: equal weight, inverse volatility, and constrained search with pass/fail rule text | Complete |
| Point-in-time signal with data card | CPI availability panel and in-app data-card expander; `Lab_17.md` and `docs/price-data-card.md` | Complete |
| Estimate, window, cost, and constraint stresses plus stop condition | `scenario_rows` in `app.py`, decision memo, visible output, and validation record | Complete |
| Locked Changed-Input Record | `docs/validation-and-ai-use.md`, immutable pre-run commit `f4f8368`, actual result, and reconciliation | Complete |
| Recommendation, allocation range, and monitoring triggers | `docs/decision-memo.md`: zero-capital action, sensitivity envelope, 20-point trigger, monthly review, and five-business-day escalation | Complete |
| AI/ownership and education-not-advice statements at the opening of README, memo, and videos | `README.md`, `docs/decision-memo.md`, and all three final transcript scripts | Complete |

## Reproducibility and ownership evidence

| Requirement | Evidence | Status |
| --- | --- | --- |
| Visible executed output without running code | `docs/visible-output.md` | Complete |
| Named AI-use disclosure and material check | `docs/validation-and-ai-use.md` | Complete |
| Final-engine known answer and validation | `tests/test_project2.py`; `python -m unittest discover -s tests -v` passes five tests | Complete |
| Correction of a checked AI/draft output | The impossible 66%/34% result is documented, corrected to 65%/35%, and regression-tested | Complete |
| Decision memo in Markdown | `docs/decision-memo.md` | Complete |
| Validation record in Markdown | `docs/validation-and-ai-use.md` | Complete |
| Three distinct video scripts within course time limits | `docs/transcript-video-1.txt` (about 301 spoken words; 2:17 recorded), `transcript-video-2.txt` (about 428), and `transcript-video-3.txt` (about 391) | Video 1 recorded; Videos 2–3 ready to record |
| Brightspace evidence manifest | `docs/brightspace-manifest.md` | Ready; final URLs, durations, and timestamps require the actual recordings |

## Final student-owned completion steps

1. Record the three scripts with a visible webcam and clear audio. The on-screen sequence is in `docs/video-recording-guide.md`.
2. Keep Video 1 at or below 3:00 and Videos 2–3 at or below 5:00. Video 3 must begin on the running app.
3. Upload each as a separate descriptively titled YouTube video, Unlisted or Public, with captions enabled; verify every link logged out.
4. Correct the plain-text transcripts to match what was actually said, including all finance terms and final numbers.
5. Enter each stable video URL, exact title, final duration, and actual timestamp index in `docs/brightspace-manifest.md`; commit and push that final update.
6. Attach the required Markdown files and corrected transcript files to Brightspace, along with the final manifest and repository/video links.

## Stronger-but-optional final validation

The recorded Locked Changed-Input test is complete but its 10% to 20% BIL-floor change was nonbinding. A stronger second record would require the student—not AI—to write a new prediction before any assistance, commit it, and then run a binding change such as a 10% to 75% BIL floor. Do this only if there is enough time to execute the complete sequence honestly; do not backfill a prediction.
