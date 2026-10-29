"""Download five years of Yahoo Finance monthly adjusted closing prices."""

from datetime import datetime, timezone

import pandas as pd
import requests

TICKERS = ("BIL", "IEF", "LQD", "VT")
URL = "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def download_ticker(ticker: str, start: int, end: int) -> pd.Series:
    """Return Yahoo Finance monthly adjusted closes for one ticker."""
    response = requests.get(
        URL.format(ticker=ticker),
        params={"period1": start, "period2": end, "interval": "1mo", "events": "history"},
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()["chart"]["result"][0]
    dates = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_localize(None).normalize()
    values = result["indicators"]["adjclose"][0]["adjclose"]
    return pd.Series(values, index=dates, name=ticker, dtype="float64")


def main() -> None:
    now = datetime.now(timezone.utc)
    end = int(now.timestamp())
    start = int(now.replace(year=now.year - 5).timestamp())
    prices = pd.concat(
        [download_ticker(ticker, start, end) for ticker in TICKERS], axis=1, sort=True
    )
    prices = prices.dropna().sort_index()
    # Yahoo includes a separate current-day point in addition to the current month.
    prices = prices.loc[~prices.index.to_period("M").duplicated(keep="last")].tail(60)
    if len(prices) != 60:
        raise ValueError(f"Expected 60 common monthly observations; found {len(prices)}.")
    prices.index.name = "Date"
    prices.to_csv("Lab_15_prices.csv", float_format="%.6f")
    print(f"Wrote {len(prices)} monthly observations for {', '.join(TICKERS)}.")


if __name__ == "__main__":
    main()
