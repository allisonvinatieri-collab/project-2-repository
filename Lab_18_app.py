"""Streamlit interface for the Legend Investor SEC EDGAR skill."""

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

SCRIPT_DIR = Path(__file__).parent / ".codex" / "skills" / "Lab_18_legend_investor" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from Lab_18_edgar_buffett import build_report, memo_unprinted_numbers  # noqa: E402

st.set_page_config(page_title="Legend Investor", layout="wide")
st.title("Legend Investor as Skill")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    ticker = st.text_input("Ticker", "COST").strip().upper()
    contact = st.text_input("SEC User-Agent (your name and email)", value="FIN43900 Student student@example.com")
    memo_file = st.text_input("Memo file", value=f"Lab_18_{ticker}_buffett_memo.md")

if st.button("Run SEC EDGAR review", type="primary"):
    if "@" not in contact:
        st.error("Enter a User-Agent with your name and email, e.g. Jane Doe jane@example.com.")
        st.stop()
    try:
        report = build_report(ticker, contact)
    except Exception as error:
        st.error(f"SEC EDGAR request failed: {error}")
        st.stop()
    rows = report["rows"]
    if len(rows) < 5:
        st.warning(f"SEC EDGAR returned only {len(rows)} qualifying 10-K fiscal years.")
    frame = pd.DataFrame(rows)
    chart = frame.set_index("fiscal_year_end")[["Owner earnings", "Net income"]]
    st.subheader("Owner earnings and net income ($ millions)")
    st.line_chart(chart)

    st.subheader("10-K table ($ millions)")
    display = frame[["fiscal_year_end", "Revenue", "Revenue tag", "Net income", "Net income tag", "Operating cash flow", "Operating cash flow tag", "Capital spending", "Capital spending tag", "Equity", "Equity tag", "ROE", "Owner earnings"]].copy()
    display["ROE"] = display["ROE"].map(lambda value: "not known" if pd.isna(value) else f"{value:.1f}%")
    for column in ["Revenue", "Net income", "Operating cash flow", "Capital spending", "Equity", "Owner earnings"]:
        display[column] = display[column].map(lambda value: "not found" if pd.isna(value) else f"{value:,.0f}")
    st.dataframe(display, use_container_width=True, hide_index=True)

    st.subheader("Buffett checks (computed in code)")
    st.table(pd.DataFrame(report["checks"].items(), columns=["Check", "Result"]))

    st.subheader("Buffett memo")
    memo_path = Path(memo_file)
    if memo_path.exists():
        memo = memo_path.read_text(encoding="utf-8")
        st.markdown(memo)
        flags = memo_unprinted_numbers(memo_path, report)
        if flags:
            st.error("Numbers in the memo not printed by the script: " + ", ".join(flags))
        else:
            st.success("Every number in this memo was printed by the script.")
    else:
        st.info(f"No memo found at `{memo_path}`. Create it with the legend-investor skill after reviewing the printed facts.")
