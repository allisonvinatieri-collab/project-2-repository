"""Build a point-in-time ALFRED vintage table for monthly CPI."""

import csv
import io
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen


SERIES_ID = "CPIAUCSL"
SERIES_NAME = "CPIAUCSL - Consumer Price Index for All Urban Consumers: All Items"
MONTHS_TO_KEEP = 26
OUTPUT_CSV = Path("ALFRED_CPIAUCSL_vintages.csv")
OUTPUT_CHECKS = Path("ALFRED_CPIAUCSL_spot_checks.md")
DOWNLOAD_PAGE = f"https://alfred.stlouisfed.org/series/downloaddata?seid={SERIES_ID}"
CSV_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage}"


def get_text(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def month_start(value):
    return date.fromisoformat(value)


def subtract_months(value, count):
    """Return the first day of the month count months before value."""
    year = value.year
    month = value.month - count
    while month <= 0:
        year -= 1
        month += 12
    return date(year, month, 1)


def parse_snapshot(vintage):
    text = get_text(CSV_URL.format(series_id=SERIES_ID, vintage=vintage))
    reader = csv.DictReader(io.StringIO(text))
    return {
        row["observation_date"]: row[next(name for name in row if name != "observation_date")]
        for row in reader
        if row[next(name for name in row if name != "observation_date")] not in {"", "."}
    }


def main():
    page = get_text(DOWNLOAD_PAGE)
    vintage_dates = sorted(set(re.findall(r'<option\s+value="(\d{4}-\d{2}-\d{2})">', page)))
    if not vintage_dates:
        raise RuntimeError("No ALFRED vintage dates were found.")

    latest_snapshot = parse_snapshot(vintage_dates[-1])
    latest_month = max(month_start(month) for month in latest_snapshot)
    cutoff = subtract_months(latest_month, MONTHS_TO_KEEP - 1)
    selected_vintages = [vintage for vintage in vintage_dates if date.fromisoformat(vintage) >= cutoff]

    with ThreadPoolExecutor(max_workers=5) as executor:
        snapshots = dict(zip(selected_vintages, executor.map(parse_snapshot, selected_vintages)))

    previous = {}
    rows = []
    for vintage in selected_vintages:
        snapshot = snapshots[vintage]
        for month, value in sorted(snapshot.items()):
            if month_start(month) < cutoff or previous.get(month) == value:
                continue
            rows.append([SERIES_NAME, month[:7], vintage, value])
            previous[month] = value

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Series name", "Month measured", "Published on", "Value"])
        writer.writerows(rows)

    checks = [rows[0], rows[len(rows) // 2], rows[-1]]
    with OUTPUT_CHECKS.open("w", encoding="utf-8") as file:
        file.write("# ALFRED CPI spot checks\n\n")
        file.write("Check these rows yourself in ALFRED before Thursday. Each link opens the relevant vintage.\n\n")
        for _, month, vintage, value in checks:
            url = CSV_URL.format(series_id=SERIES_ID, vintage=vintage)
            file.write(f"- {month} published {vintage}: {value} - {url}\n")

    print(f"Wrote {len(rows)} new or revised observations to {OUTPUT_CSV}.")
    print(f"Coverage: {cutoff:%Y-%m} through {latest_month:%Y-%m}; {len(selected_vintages)} vintages.")
    print(f"Spot-check instructions: {OUTPUT_CHECKS}")


if __name__ == "__main__":
    main()
