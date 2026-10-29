"""Lab 16: point-in-time (as-of) provenance filter."""

import csv
from datetime import date
from io import StringIO


# Editable inputs
DECISION_DATE = "2026-03-31"
TABLE = """row,ticker,month_measured,published_on,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""


def read_rows(table):
    """Turn the editable CSV text into records with real dates and numbers."""
    rows = []
    for raw in csv.DictReader(StringIO(table.strip())):
        rows.append(
            {
                "row": int(raw["row"]),
                "ticker": raw["ticker"].strip(),
                "month": raw["month_measured"],
                "published": date.fromisoformat(raw["published_on"]),
                "index": float(raw["index"]),
            }
        )
    return rows


def remove(rows, predicate):
    """Return kept rows and the original row numbers removed by a rule."""
    removed = [row["row"] for row in rows if predicate(row)]
    kept = [row for row in rows if not predicate(row)]
    return kept, removed


def deduplicate(rows):
    """Keep the first occurrence of an otherwise identical observation."""
    seen = set()
    kept, removed = [], []
    for row in rows:
        key = (row["ticker"], row["month"], row["published"], row["index"])
        if key in seen:
            removed.append(row["row"])
        else:
            seen.add(key)
            kept.append(row)
    return kept, removed


def latest_revisions(rows):
    """For each ticker/month, retain its latest publication."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or row["published"] > latest[key]["published"]:
            latest[key] = row
    kept = sorted(latest.values(), key=lambda row: row["row"])
    kept_numbers = {row["row"] for row in kept}
    removed = [row["row"] for row in rows if row["row"] not in kept_numbers]
    return kept, removed


def print_panel(rows, title):
    print(f"\n{title}")
    print("row  ticker  month     published   index")
    for row in sorted(rows, key=lambda item: (item["ticker"], item["month"])):
        print(
            f"{row['row']:>3}  {row['ticker']:<6}  {row['month']}  "
            f"{row['published'].isoformat()}  {row['index']:.1f}"
        )


def print_signals(rows, title):
    print(f"\n{title}")
    tickers = sorted({row["ticker"] for row in rows})
    for ticker in tickers:
        history = sorted((row for row in rows if row["ticker"] == ticker), key=lambda row: row["month"])
        if len(history) < 2:
            print(f"{ticker}: not enough monthly observations")
            continue
        previous, latest = history[-2:]
        change = (latest["index"] / previous["index"] - 1) * 100
        print(
            f"{ticker}: {change:+.2f}% to {latest['month']} "
            f"({previous['index']:.1f} to {latest['index']:.1f})"
        )


def main():
    decision_date = date.fromisoformat(DECISION_DATE)
    original = read_rows(TABLE)

    # Rules 1 and 2 establish the clean base used by both comparisons.
    no_missing_ticker, missing_ticker_rows = remove(original, lambda row: not row["ticker"])
    clean_rows, duplicate_rows = deduplicate(no_missing_ticker)

    # Rules 3 and 4 create the point-in-time panel available on the decision date.
    published_by_decision, late_rows = remove(clean_rows, lambda row: row["published"] > decision_date)
    asof_panel, revision_rows = latest_revisions(published_by_decision)

    # The naive comparison deliberately skips the decision-date filter.
    naive_panel, _ = latest_revisions(clean_rows)

    print("ROW FUNNEL")
    print(f"1. Missing ticker: removed {len(missing_ticker_rows)} row(s): {missing_ticker_rows}")
    print(f"2. Exact duplicate: removed {len(duplicate_rows)} row(s): {duplicate_rows}")
    print(f"3. Published after {DECISION_DATE}: removed {len(late_rows)} row(s): {late_rows}")
    print(f"4. Older revision: removed {len(revision_rows)} row(s): {revision_rows}")

    print_panel(asof_panel, f"AS-OF PANEL - knowable on {DECISION_DATE}")
    print_signals(asof_panel, "AS-OF SIGNALS")
    print_signals(naive_panel, "NAIVE SIGNALS - ignores publication date")


if __name__ == "__main__":
    main()
