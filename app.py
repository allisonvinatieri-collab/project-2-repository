"""Project 2 investment-management application.

Run locally with ``streamlit run app.py``.  The app uses the included monthly
adjusted-price sample; it does not download or trade securities.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from Lab_15_portfolio import estimates_from_prices, lowest_risk_mix
from lab_14_portfolio import (
    covariance_matrix,
    equal_weight_weights,
    expected_return,
    inverse_volatility_weights,
    portfolio_volatility,
    reserve_eligible_weight,
)


DATA_FILE = Path(__file__).with_name("Lab_15_prices.csv")
CPI_FILE = Path(__file__).with_name("ALFRED_CPIAUCSL_vintages.csv")
TICKERS = ["BIL", "IEF", "LQD", "VT"]
DEFAULT_OBJECTIVE = 0.06
DEFAULT_RESERVE = 0.10


@st.cache_data
def load_prices() -> pd.DataFrame:
    """Load the fixed historical monthly price sample."""
    return pd.read_csv(DATA_FILE)


@st.cache_data
def load_cpi_vintages() -> pd.DataFrame:
    """Load CPI observations with their recorded publication dates."""
    frame = pd.read_csv(CPI_FILE)
    frame["Month measured"] = pd.to_datetime(frame["Month measured"])
    frame["Published on"] = pd.to_datetime(frame["Published on"])
    return frame


def portfolio_row(name, weights, sleeves, correlation, objective, reserve_assets, reserve_floor):
    """Create the comparable baseline/portfolio table row."""
    result_return = expected_return(weights, sleeves)
    result_reserve = reserve_eligible_weight(weights, reserve_assets)
    failed_rules = []
    if result_return < objective:
        failed_rules.append("return objective")
    if result_reserve < reserve_floor:
        failed_rules.append("BIL reserve floor")
    return {
        "Portfolio": name,
        "Annualized historical return": result_return,
        "Annualized volatility": portfolio_volatility(weights, covariance_matrix(sleeves, correlation)),
        "BIL reserve weight": result_reserve,
        "Mandate verdict": "Pass" if not failed_rules else f"Fail: {', '.join(failed_rules)}",
    }


def render_mix(result):
    """Display weights and decision-relevant metrics for an optimizer result."""
    if result is None:
        st.error("No 5% long-only allocation meets both mandate rules.")
        return
    weights = pd.DataFrame.from_dict(result["weights"], orient="index", columns=["Weight"])
    st.dataframe(weights.style.format("{:.0%}"), width="stretch")
    return_col, risk_col, reserve_col = st.columns(3)
    return_col.metric("Annualized historical return", f"{result['return']:.2%}")
    risk_col.metric("Annualized volatility", f"{result['volatility']:.2%}")
    reserve_col.metric("BIL reserve weight", f"{result['reserve_weight']:.0%}")


def main() -> None:
    st.set_page_config(page_title="Meridian Portfolio Decision System", layout="wide")
    st.title("Meridian Portfolio Decision System")
    st.caption(
        "AI announcement: Generative AI assisted with code and documentation; the student must verify "
        "all results and owns the analysis and decision. Education, not investment advice."
    )
    st.warning(
        "This is a classroom decision-support prototype. Historical estimates are not forecasts and do not "
        "establish that any allocation will meet its objective."
    )

    prices = load_prices()
    if list(prices.columns) != ["Date", *TICKERS]:
        st.error("Lab_15_prices.csv must contain Date, BIL, IEF, LQD, and VT in that order.")
        st.stop()

    st.sidebar.header("Mandate controls")
    objective = st.sidebar.number_input(
        "Annualized historical-return objective", 0.0, 0.20, DEFAULT_OBJECTIVE, 0.005, format="%.3f"
    )
    reserve_floor = st.sidebar.number_input(
        "Minimum BIL reserve weight", 0.0, 1.0, DEFAULT_RESERVE, 0.05, format="%.2f"
    )
    use_last_36 = st.sidebar.toggle("Use last 36 monthly returns", value=False)
    shock = st.sidebar.slider("Stress: reduce VT return estimate", 0.0, 0.05, 0.01, 0.005, format="%.1f%%")

    sleeves, correlation = estimates_from_prices(prices, last_36_months=use_last_36)
    optimized = lowest_risk_mix(sleeves, correlation, objective, {"BIL"}, reserve_floor)

    st.subheader("Mandate and data")
    st.write(
        "**Objective:** at least the selected annualized historical-return estimate. "
        "**Universe:** BIL, IEF, LQD, and VT. **Hard constraint:** at least the selected weight in BIL."
    )
    st.caption(
        f"Price sample: {pd.to_datetime(prices['Date']).min():%B %Y} through "
        f"{pd.to_datetime(prices['Date']).max():%B %Y}; {len(prices) - 1} monthly returns."
    )

    st.subheader("Two baselines and constrained portfolio")
    baseline_rows = [
        portfolio_row("Equal weight", equal_weight_weights(sleeves), sleeves, correlation, objective, {"BIL"}, reserve_floor),
        portfolio_row("Inverse volatility", inverse_volatility_weights(sleeves), sleeves, correlation, objective, {"BIL"}, reserve_floor),
    ]
    if optimized is not None:
        baseline_rows.append(
            portfolio_row("Constrained search", optimized["weights"], sleeves, correlation, objective, {"BIL"}, reserve_floor)
        )
    st.dataframe(
        pd.DataFrame(baseline_rows).style.format(
            {
                "Annualized historical return": "{:.2%}",
                "Annualized volatility": "{:.2%}",
                "BIL reserve weight": "{:.0%}",
            }
        ),
        width="stretch",
        hide_index=True,
    )
    st.caption("A pass means only that the displayed historical-estimate and reserve rules pass; it is not a forecast or approval.")

    left, right = st.columns(2)
    with left:
        st.subheader("Recommended constrained allocation")
        render_mix(optimized)
    with right:
        st.subheader("Stress run")
        shocked_sleeves = {ticker: values.copy() for ticker, values in sleeves.items()}
        shocked_sleeves["VT"]["return"] -= shock
        stressed = lowest_risk_mix(shocked_sleeves, correlation, objective, {"BIL"}, reserve_floor)
        st.caption(f"VT annualized historical-return estimate reduced by {shock:.1%}; all other inputs unchanged.")
        render_mix(stressed)
        if stressed is None:
            st.error("Stop condition met: no feasible allocation remains under this stress.")
        elif optimized is not None:
            largest_change = max(abs(optimized["weights"][ticker] - stressed["weights"][ticker]) for ticker in TICKERS)
            st.info(f"Largest allocation change from base: {largest_change:.0%} points.")

    st.subheader("Point-in-time inflation monitoring signal")
    cpi = load_cpi_vintages()
    as_of = st.date_input("Decision date for CPI availability", value=pd.Timestamp("2026-09-30").date())
    available = cpi.loc[cpi["Published on"].dt.date <= as_of].sort_values("Published on")
    if available.empty:
        st.warning("No recorded CPI vintage is available for this decision date.")
    else:
        latest = available.iloc[-1]
        st.write(
            f"As of **{as_of:%B %d, %Y}**, the latest recorded CPI vintage is "
            f"**{latest['Month measured']:%B %Y} = {latest['Value']:.3f}**, published {latest['Published on']:%B %d, %Y}."
        )
        st.caption(
            "Rule: do not use a CPI observation until its recorded publication date. CPI is a monitoring signal here, not an optimizer input."
        )
        st.dataframe(available.tail(6), width="stretch", hide_index=True)

    st.subheader("Committee recommendation")
    st.write(
        "**Recommendation: pilot, not adopt.** Use no allocation until the mandate-approved return objective, reserve definition, "
        "cost assumptions, and broader robustness tests are approved. A pilot should be stopped or returned to committee review if "
        "the stressed search becomes infeasible, the allocation shifts materially across reasonable windows, or point-in-time data controls fail."
    )


if __name__ == "__main__":
    main()
