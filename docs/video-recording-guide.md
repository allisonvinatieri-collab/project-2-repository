# Project 2 Video Recording Guide

Record with a small webcam view and clear audio throughout. Use the three transcripts as the words you actually say; do not read the setup notes below into the recording. After recording, compare the YouTube captions to the transcript and correct financial terms, tickers, names, and material numbers. The maximum running times are strict: Video 1 is 3:00; Videos 2 and 3 are 5:00 each.

## Video 1 — System change and AI-output check (maximum 3:00)

Open the Streamlit app on **Committee view**. Begin speaking immediately with the AI and education statement in `transcript-video-1.txt`. While discussing the all-months and last-36-month results, point to the portfolio comparison, allocation panel, and stress table. When discussing the 66% / 34% discrepancy, show `docs/validation-and-ai-use.md` at the **Final-engine verification catch** heading or show `tests/test_project2.py`. Do not turn this into a code walkthrough; its purpose is your thinking change and the AI-output check.

## Video 2 — Codebase walkthrough (maximum 5:00)

Start at the repository root in File Explorer or your editor. Open, in order: `README.md`, `app.py`, `Lab_15_portfolio.py`, `tests/test_project2.py`, and `docs/validation-and-ai-use.md`. Use a terminal to run `python -m unittest discover -s tests -v` and leave the passing result visible. The transcript identifies exactly what to show from each file. This is the technical-ownership video, so explain the input-to-output flow rather than reading the README aloud.

## Video 3 — Investment-committee presentation (maximum 5:00)

Start with the live Streamlit app already open on **Committee view**. Do not begin on a terminal, title slide, editor, or desktop. Begin speaking immediately with the AI and education statement in `transcript-video-3.txt`, then state the committee decision. Show the default result, change the VT stress slider from 1.0% to 2.0%, and leave the resulting allocation and metrics visible while describing the result. Point to the stress table when stating the 20-point reversal threshold. End with the committee ask while the app is still on screen.

## Before uploading

Upload three separate, descriptively titled YouTube videos as **Unlisted** or **Public**, never Private. Test every link in an incognito/private browser session. Record each final title, duration, URL, and relevant timestamps in the Brightspace manifest. Do not revise or replace a recording after the deadline.
