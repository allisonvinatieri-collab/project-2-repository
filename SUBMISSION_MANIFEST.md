# Project 2 Submission Manifest

## Reproducible application package

| Artifact | Location | Verification |
| --- | --- | --- |
| Runnable entry point | `app.py` | `streamlit run app.py` opens the dashboard. |
| Historical-estimate and search engine | `Lab_15_portfolio.py` | Used directly by the application and regression tests. |
| Portfolio math | `lab_14_portfolio.py` | Imported by the engine and application. |
| Price input | `Lab_15_prices.csv` | Fixed monthly sample; schema is checked in the engine. |
| Point-in-time CPI input | `ALFRED_CPIAUCSL_vintages.csv` | Publication-date gate is tested. |
| Dependencies | `requirements.txt` | Pinned runtime dependencies. |
| Instructions and headline result | `README.md` | Includes clean-environment setup, test, run, and expected result. |
| Tests | `tests/test_project2.py` | Run with `python -m unittest discover -s tests -v`; 5 tests passed on 17 November 2026. |

## Decision and audit record

| Artifact | Location | Contents |
| --- | --- | --- |
| Decision memo | `docs/decision-memo.md` | Committee action, evidence, conditions, and numeric reversal trigger. |
| Validation and AI-use record | `docs/validation-and-ai-use.md` | Data boundary, known answers, stress checks, cold run, AI disclosure, and locked changed-input record. |
| Visible output | `docs/visible-output.md` | Executed default inputs, result, stress result, and monitoring gate. |
| Cold-run and defense readiness | `docs/lab-20-readiness.md` | Partner cold-run record and code-explanation record. |

## Submission checks completed in this repository

- Default known-answer test: 70% BIL / 30% VT; 6.07% net historical return; 4.54% volatility.
- Final-engine VT-stress known-answer test: 65% BIL / 35% VT; 6.11% net historical return; 5.28% volatility.
- Point-in-time CPI availability test and invalid reserve-floor control.
- Partner cold run recorded as clean on 17 November 2026.
- Locked changed-input record includes its immutable pre-run commit `f4f8368`.

## Items that require the student's own recorded evidence

The three course videos cannot be created or attested by repository code. Before submitting, record them with the student's face visible, add their actual hosted links or files to this manifest, and replace the three transcript files with the spoken transcripts. Video 3 must open with the live Streamlit app, change a bounded driver, state the 20-percentage-point / five-business-day reversal trigger, and show the result.
