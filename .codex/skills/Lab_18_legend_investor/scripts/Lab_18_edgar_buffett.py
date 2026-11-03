#!/usr/bin/env python3
"""Retrieve 10-K company facts and calculate Buffett-style business checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import requests

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"

METRICS: dict[str, tuple[str, ...]] = {
    "Revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"),
    "Net income": ("NetIncomeLoss",),
    "Operating cash flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "Capital spending": (
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ),
    "Equity": ("StockholdersEquity",),
}
FLOW_METRICS = {"Revenue", "Net income", "Operating cash flow", "Capital spending"}


def sec_get(url: str, user_agent: str) -> dict[str, Any]:
    response = requests.get(
        url,
        headers={"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate", "Host": "www.sec.gov" if "www.sec.gov" in url else "data.sec.gov"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_cik(ticker: str, user_agent: str) -> int:
    records = sec_get(TICKERS_URL, user_agent)
    ticker = ticker.upper()
    for record in records.values():
        if record.get("ticker", "").upper() == ticker:
            return int(record["cik_str"])
    raise ValueError(f"Ticker not found in SEC ticker list: {ticker}")


def is_annual_flow(fact: dict[str, Any]) -> bool:
    if fact.get("form") != "10-K" or fact.get("fp") != "FY" or not fact.get("start"):
        return False
    try:
        days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    except (KeyError, TypeError, ValueError):
        return False
    return 300 <= days <= 380


def is_year_end_instant(fact: dict[str, Any]) -> bool:
    return fact.get("form") == "10-K" and fact.get("fp") == "FY" and not fact.get("start")


def tagged_values(company_facts: dict[str, Any], tags: tuple[str, ...], flow: bool) -> dict[str, tuple[float, str]]:
    """Return end-date values, preferring the listed XBRL tags and latest filing."""
    facts = company_facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        units = facts.get(tag, {}).get("units", {}).get("USD", [])
        qualifying = [f for f in units if (is_annual_flow(f) if flow else is_year_end_instant(f))]
        by_end: dict[str, dict[str, Any]] = {}
        for fact in qualifying:
            end = fact.get("end")
            if end and (end not in by_end or fact.get("filed", "") > by_end[end].get("filed", "")):
                by_end[end] = fact
        if by_end:
            return {end: (float(fact["val"]), tag) for end, fact in by_end.items()}
    return {}


def millions(value: float | None) -> float | None:
    return None if value is None else value / 1_000_000


def shown(value: float | None, decimals: int = 0) -> str:
    if value is None:
        return "not found"
    return f"{value:,.{decimals}f}"


def build_report(ticker: str, user_agent: str) -> dict[str, Any]:
    cik = get_cik(ticker, user_agent)
    facts = sec_get(FACTS_URL.format(cik=cik), user_agent)
    collected = {metric: tagged_values(facts, tags, metric in FLOW_METRICS) for metric, tags in METRICS.items()}
    all_ends = sorted(set().union(*(set(values) for values in collected.values())))
    fiscal_ends = all_ends[-5:]
    rows: list[dict[str, Any]] = []
    for end in fiscal_ends:
        row: dict[str, Any] = {"fiscal_year_end": end}
        for metric in METRICS:
            raw = collected[metric].get(end)
            row[metric] = millions(raw[0]) if raw else None
            row[f"{metric} tag"] = raw[1] if raw else "not found"
        income, equity = row["Net income"], row["Equity"]
        row["ROE"] = (income / equity * 100) if income is not None and equity is not None and equity > 0 else None
        row["ROE tag"] = "NetIncomeLoss / StockholdersEquity" if row["ROE"] is not None else "not known"
        ocf, capex = row["Operating cash flow"], row["Capital spending"]
        row["Owner earnings"] = ocf - capex if ocf is not None and capex is not None else None
        row["Owner earnings tag"] = "Operating cash flow - Capital spending" if row["Owner earnings"] is not None else "not known"
        rows.append(row)

    roe_values = [row["ROE"] for row in rows]
    owner_values = [row["Owner earnings"] for row in rows]
    checks = {
        "ROE of 15% or more every year": "pass" if len(rows) == 5 and all(v is not None and v >= 15 for v in roe_values) else ("not known" if any(v is None for v in roe_values) else "fail"),
        "Owner earnings positive every year": "pass" if len(rows) == 5 and all(v is not None and v > 0 for v in owner_values) else ("not known" if any(v is None for v in owner_values) else "fail"),
        "Owner earnings grew, first year to last": "pass" if len(rows) == 5 and owner_values[0] is not None and owner_values[-1] is not None and owner_values[-1] > owner_values[0] else ("not known" if len(rows) != 5 or owner_values[0] is None or owner_values[-1] is None else "fail"),
    }
    return {"ticker": ticker.upper(), "cik": f"{cik:010d}", "rows": rows, "checks": checks}


def print_report(report: dict[str, Any]) -> None:
    print(f"{report['ticker']} - SEC EDGAR 10-K facts ($ millions)")
    columns = ["Fiscal year end", *METRICS.keys(), "ROE %", "Owner earnings"]
    print(" | ".join(columns))
    print(" | ".join(["---"] * len(columns)))
    for row in report["rows"]:
        values = [row["fiscal_year_end"]]
        values += [shown(row[metric]) for metric in METRICS]
        values += [shown(row["ROE"], 1) if row["ROE"] is not None else "not known", shown(row["Owner earnings"])]
        print(" | ".join(values))
        print("Tags: " + "; ".join(f"{metric}={row[f'{metric} tag']}" for metric in METRICS))
        print(f"Tags: ROE={row['ROE tag']}; Owner earnings={row['Owner earnings tag']}")
    print("\nBuffett checks")
    for check, result in report["checks"].items():
        print(f"- {check}: {result}")


def allowed_numbers(report: dict[str, Any]) -> set[str]:
    allowed: set[str] = set()
    for row in report["rows"]:
        allowed.add(row["fiscal_year_end"])
        for metric in [*METRICS.keys(), "ROE", "Owner earnings"]:
            value = row.get(metric)
            if value is not None:
                allowed.add(shown(value, 1 if metric == "ROE" else 0).replace(",", ""))
    return allowed


def memo_unprinted_numbers(memo_path: Path, report: dict[str, Any]) -> list[str]:
    text = memo_path.read_text(encoding="utf-8")
    tokens = re.findall(r"(?<![\w.-])\$?\d[\d,]*(?:\.\d+)?%?(?![\w.-])", text)
    allowed = allowed_numbers(report)
    flagged = []
    for token in tokens:
        normalized = token.lstrip("$").rstrip("%").replace(",", "")
        if normalized not in allowed:
            flagged.append(token)
    return flagged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--user-agent", default=os.getenv("SEC_USER_AGENT"), help="Required: name and email for SEC EDGAR")
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    parser.add_argument("--memo", type=Path, help="Validate every memo number against the report")
    args = parser.parse_args()
    if not args.user_agent or "@" not in args.user_agent:
        parser.error("Provide --user-agent 'Your Name you@example.com' or set SEC_USER_AGENT.")
    try:
        report = build_report(args.ticker, args.user_agent)
        print(json.dumps(report, indent=2) if args.json else "")
        if not args.json:
            print_report(report)
        if args.memo:
            flags = memo_unprinted_numbers(args.memo, report)
            print("\nMemo number check: " + ("all memo numbers were printed" if not flags else "FLAGGED: " + ", ".join(flags)))
            return 1 if flags else 0
        return 0
    except (requests.RequestException, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
