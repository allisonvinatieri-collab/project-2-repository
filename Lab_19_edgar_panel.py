"""Lab_19 SEC EDGAR investor panel calculations and printable facts."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PARENT_SCRIPT = Path(__file__).parent / ".codex" / "skills" / "Lab_18_legend_investor" / "scripts"
sys.path.insert(0, str(PARENT_SCRIPT))
from Lab_18_edgar_buffett import (  # noqa: E402
    FLOW_METRICS,
    get_cik,
    memo_unprinted_numbers as base_memo_unprinted_numbers,
    millions,
    sec_get,
    shown,
    tagged_values,
)

FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
PANEL_METRICS = {
    "AssetsCurrent": ("AssetsCurrent",),
    "LiabilitiesCurrent": ("LiabilitiesCurrent",),
    "Liabilities": ("Liabilities",),
}


def every_year(values: list[float | None], predicate) -> str:
    if len(values) != 5 or any(value is None for value in values):
        return "not known"
    return "pass" if all(predicate(value) for value in values) else "fail"


def latest(value: float | None, predicate) -> str:
    if value is None:
        return "not known"
    return "pass" if predicate(value) else "fail"


def memo_unprinted_numbers(memo_path: Path, report: dict) -> list[str]:
    """Lab_19 validation also permits the two ratios printed by this panel."""
    flags = base_memo_unprinted_numbers(memo_path, report)
    allowed = set()
    for row in report["rows"]:
        for metric in ("Current ratio", "Liabilities / equity"):
            value = row.get(metric)
            if value is not None:
                allowed.add(shown(value, 2).replace(",", ""))
    allowed.add(f"{report['graham_current_ratio_threshold']:.1f}")
    return [flag for flag in flags if flag.lstrip("$").rstrip("%").replace(",", "") not in allowed]


def verdict(checks: dict[str, str]) -> str:
    results = list(checks.values())
    if "fail" in results:
        return "fail"
    if "not known" in results:
        return "watch"
    return "pass"


def build_panel_report(ticker: str, user_agent: str, graham_current_ratio_threshold: float = 2.0) -> dict:
    """Build Lab_19 results; `not known` is preserved for absent 10-K inputs."""
    from Lab_18_edgar_buffett import build_report

    report = build_report(ticker, user_agent)
    cik = get_cik(ticker, user_agent)
    facts = sec_get(FACTS_URL.format(cik=cik), user_agent)
    collected = {
        metric: tagged_values(facts, tags, metric in FLOW_METRICS)
        for metric, tags in PANEL_METRICS.items()
    }
    for row in report["rows"]:
        end = row["fiscal_year_end"]
        for metric, values in collected.items():
            raw = values.get(end)
            row[metric] = millions(raw[0]) if raw else None
            row[f"{metric} tag"] = raw[1] if raw else "not found"
        assets_current, liabilities_current = row["AssetsCurrent"], row["LiabilitiesCurrent"]
        row["Current ratio"] = assets_current / liabilities_current if assets_current is not None and liabilities_current not in (None, 0) else None
        liabilities, equity = row["Liabilities"], row["Equity"]
        row["Liabilities / equity"] = liabilities / equity if liabilities is not None and equity not in (None, 0) else None

    rows = report["rows"]
    net_income = [row["Net income"] for row in rows]
    operating_cash_flow = [row["Operating cash flow"] for row in rows]
    graham = {
        f"Current ratio of {graham_current_ratio_threshold:.1f} or more, latest year": latest(rows[-1]["Current ratio"] if rows else None, lambda value: value >= graham_current_ratio_threshold),
        "Net income positive every year": every_year(net_income, lambda value: value > 0),
        "Net income grew, first year to last": "not known" if len(net_income) != 5 or net_income[0] is None or net_income[-1] is None else ("pass" if net_income[-1] > net_income[0] else "fail"),
    }
    burry = {
        "Operating cash flow at least net income every year": "not known" if len(rows) != 5 or any(ocf is None or income is None for ocf, income in zip(operating_cash_flow, net_income)) else ("pass" if all(ocf >= income for ocf, income in zip(operating_cash_flow, net_income)) else "fail"),
        "Liabilities no more than twice equity, latest year": latest(rows[-1]["Liabilities / equity"] if rows else None, lambda value: value <= 2),
    }
    report["checks_by_investor"] = {"Buffett": report["checks"], "Graham": graham, "Burry": burry}
    report["verdicts"] = {investor: verdict(checks) for investor, checks in report["checks_by_investor"].items()}
    report["graham_current_ratio_threshold"] = graham_current_ratio_threshold
    return report


def print_panel_report(report: dict) -> None:
    print(f"{report['ticker']} - Lab_19 SEC EDGAR 10-K panel facts ($ millions)")
    for row in report["rows"]:
        print(" | ".join([
            row["fiscal_year_end"], f"Net income {shown(row['Net income'])}",
            f"Operating cash flow {shown(row['Operating cash flow'])}",
            f"AssetsCurrent {shown(row['AssetsCurrent'])}", f"LiabilitiesCurrent {shown(row['LiabilitiesCurrent'])}",
            f"Liabilities {shown(row['Liabilities'])}", f"Equity {shown(row['Equity'])}",
            f"Current ratio {shown(row['Current ratio'], 2)}", f"Liabilities / equity {shown(row['Liabilities / equity'], 2)}",
        ]))
    for investor, checks in report["checks_by_investor"].items():
        print(f"\n{investor} checks ({report['verdicts'][investor]})")
        for check, result in checks.items():
            print(f"- {check}: {result}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lab_19 investor panel")
    parser.add_argument("ticker")
    parser.add_argument("--user-agent", required=True)
    parser.add_argument("--graham-current-ratio-threshold", type=float, default=2.0)
    parser.add_argument("--memo", type=Path)
    args = parser.parse_args()
    if "@" not in args.user_agent:
        parser.error("Provide a name-and-email SEC User-Agent.")
    try:
        report = build_panel_report(args.ticker, args.user_agent, args.graham_current_ratio_threshold)
        print_panel_report(report)
        if args.memo:
            flags = memo_unprinted_numbers(args.memo, report)
            print("\nMemo number check: " + ("all memo numbers were printed" if not flags else "FLAGGED: " + ", ".join(flags)))
            return 0 if not flags else 1
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
