"""Lab_19 Streamlit side-by-side Legend Investor panel."""

from pathlib import Path
import re

import pandas as pd
import streamlit as st

from Lab_19_edgar_panel import build_panel_report, memo_unprinted_numbers


def workbook_memo(ticker: str, investor: str) -> str | None:
    """Return the combined Lab_19 COST memo after standalone memo files are removed."""
    if ticker != "COST":
        return None
    workbook = Path("Lab_19_panel_workbook.md")
    if not workbook.exists():
        return None
    text = workbook.read_text(encoding="utf-8")
    match = re.search(
        rf"### {investor} memo\n\n(.*?)(?=\n### |\n## |\Z)",
        text,
        flags=re.DOTALL,
    )
    return match.group(1).strip() if match else None

st.set_page_config(page_title="Lab_19 Legend Panel", layout="wide")
st.title("Lab_19 — Legend Panel")
st.caption("Same SEC EDGAR 10-K facts, three investor rule sets. Educational use only; not investment advice.")
st.caption("Sources: [SEC EDGAR companyfacts](https://data.sec.gov/api/xbrl/companyfacts/), [FAskills](https://github.com/CinderZhang/FAskills), and [Streamlit docs](https://docs.streamlit.io/).")

with st.sidebar:
    ticker = st.text_input("Ticker", "COST").strip().upper()
    contact = st.text_input("SEC User-Agent (your name and email)", "FIN43900 Student student@example.com")
    threshold = st.number_input("Graham current-ratio threshold", min_value=0.0, value=2.0, step=0.1)

if st.button("Run Lab_19 panel", type="primary"):
    if "@" not in contact:
        st.error("Enter a User-Agent with your name and email.")
        st.stop()
    try:
        report = build_panel_report(ticker, contact, threshold)
    except Exception as error:
        st.error(f"SEC EDGAR request failed: {error}")
        st.stop()

    frame = pd.DataFrame(report["rows"])
    st.subheader("Same 10-K facts for every investor ($ millions)")
    display = frame[["fiscal_year_end", "Net income", "Operating cash flow", "AssetsCurrent", "LiabilitiesCurrent", "Liabilities", "Equity", "Current ratio", "Liabilities / equity"]].copy()
    for column in ["Current ratio", "Liabilities / equity"]:
        display[column] = display[column].map(lambda value: "not known" if pd.isna(value) else f"{value:.2f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    panel_rows = [
        {"Investor": investor, "Check": check, ticker: result}
        for investor, checks in report["checks_by_investor"].items()
        for check, result in checks.items()
    ]
    st.subheader("Panel checks")
    st.dataframe(pd.DataFrame(panel_rows), use_container_width=True, hide_index=True)

    st.subheader("Verdicts and memos")
    columns = st.columns(3)
    for column, investor in zip(columns, ["Buffett", "Graham", "Burry"]):
        with column:
            st.markdown(f"### {investor}: {report['verdicts'][investor]}")
            filename = f"Lab_19_{ticker}_{investor.lower()}_memo.md"
            memo_path = Path(filename)
            if memo_path.exists():
                memo = memo_path.read_text(encoding="utf-8")
                st.markdown(memo)
                flags = memo_unprinted_numbers(memo_path, report)
                if flags:
                    st.error("Unprinted-number flag: " + ", ".join(flags))
                else:
                    st.success("No unprinted-number flag.")
            elif memo := workbook_memo(ticker, investor):
                st.markdown(memo)
                st.success("Memo loaded from Lab_19_panel_workbook.md.")
            else:
                st.info(f"No memo for {ticker} yet. Add it to Lab_19_panel_workbook.md after running the panel.")
            if investor == "Graham":
                st.caption(f"Threshold kept: current ratio ≥ {threshold:.1f}. Reason: the Lab_19 default preserves Graham's conservative liquidity rule.")
