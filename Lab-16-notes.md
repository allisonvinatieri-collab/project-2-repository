# Lab 16 Notes — Provenance Gate

## Known-answer proof

The row funnel matches the required answer:

| Step | Removed rows |
| --- | --- |
| Quarantined: no ticker | 11 |
| Exact duplicate | 7 |
| Published after 31 March 2026 | 3, 8, 10 |
| Older vintage replaced by a revision | 2 |

The as-of panel is rows **1, 4, 5, 6, 9, 12**.

| Ticker | As-of signal | Naive signal |
| --- | --- | --- |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

With decision date `2026-04-15`, all publications are available, so the as-of signals equal the naive signals ticker by ticker.

## Explain rule 4: retain the latest revision

```python
def latest_revisions(rows):
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or row["published"] > latest[key]["published"]:
            latest[key] = row
```

- `latest = {}` creates an empty place to store one winning row for each ticker and month.
- The loop examines every row remaining after the publication-date filter.
- `key` combines the ticker and month, so AAA February is compared only with other AAA February rows.
- If this is the first row for that key, it becomes the saved row.
- Otherwise, it replaces the saved row only if its publication date is later.
- Therefore, AAA February keeps row 4 (published 25 March) instead of row 2 (published 10 March). This changes the as-of result from the obsolete +2.97% to the correct +1.98%.

## Point-in-time learning

**What is look-ahead bias?** It is using information in an analysis or backtest that was not available on the date the decision would have been made.

**How it works:**

- *Event time* is when the underlying activity occurred, such as card spending in February.
- *Publication time* is when that February observation was released, such as 10 March or 5 April.
- A *revision* is a later publication that changes an earlier measurement.

A point-in-time analysis must use publication time to decide whether a value was knowable. Event time alone is not enough.

**AAA example:** On 31 March, the March value of 109.0 had not been published; it appeared on 10 April. The latest known AAA data were January 101.0 and the 25 March revision to February 103.0, giving +1.98%. The naive +5.83% uses March 109.0, so it looks stronger only because it includes data that arrived after the decision date.

## Reflection

The rule that matters most is the publication-date rule: it removes rows 3, 8, and 10, which are future information on 31 March. For AAA, however, rule 4 is also crucial because it replaces the outdated February value of 104.0 with the latest knowable revision of 103.0.

A backtest based on the naive column would claim stronger or different signals than a trader could actually have observed. It would overstate performance by allowing future releases and later revisions to influence earlier decisions.
