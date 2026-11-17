"""Project 2 portfolio mandate and stress-test decision system.

Run locally with ``python -m streamlit run app.py``. The application uses the
included historical monthly-price sample; it does not download or trade assets.
"""

from pathlib import Path

import altair as alt
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


def run_search(sleeves, correlation, objective, reserve_floor, annual_cost):
    """Find a gross allocation that clears the stated net objective after cost."""
    result = lowest_risk_mix(sleeves, correlation, objective + annual_cost, {"BIL"}, reserve_floor)
    if result is None:
        return None
    return {**result, "gross_return": result["return"], "net_return": result["return"] - annual_cost}


def portfolio_row(name, weights, sleeves, correlation, objective, reserve_floor, annual_cost):
    """Create a comparable baseline or constrained-portfolio mandate verdict."""
    gross_return = expected_return(weights, sleeves)
    net_return = gross_return - annual_cost
    reserve_weight = reserve_eligible_weight(weights, {"BIL"})
    failed_rules = []
    if net_return < objective:
        failed_rules.append("net return objective")
    if reserve_weight < reserve_floor:
        failed_rules.append("BIL reserve floor")
    return {
        "Portfolio": name,
        "Net historical return": net_return,
        "Annualized volatility": portfolio_volatility(weights, covariance_matrix(sleeves, correlation)),
        "BIL reserve weight": reserve_weight,
        "Mandate verdict": "Pass" if not failed_rules else f"Fail: {', '.join(failed_rules)}",
    }


def allocation_text(result):
    """Render a compact allocation label for a decision table or heat map."""
    if result is None:
        return "No feasible mix"
    return " / ".join(f"{ticker} {result['weights'][ticker]:.0%}" for ticker in TICKERS if result["weights"][ticker])


def largest_weight_change(first, second):
    """Return the largest allocation change between two feasible search results."""
    if first is None or second is None:
        return None
    return max(abs(first["weights"][ticker] - second["weights"][ticker]) for ticker in TICKERS)


def render_mix(result):
    """Display weights and decision-relevant metrics for an optimizer result."""
    if result is None:
        st.error("No 5% long-only allocation meets both mandate rules.")
        return
    weights = pd.DataFrame.from_dict(result["weights"], orient="index", columns=["Weight"])
    st.dataframe(weights.style.format("{:.0%}"), width="stretch")
    return_col, risk_col, reserve_col = st.columns(3)
    return_col.metric("Net historical return", f"{result['net_return']:.2%}")
    risk_col.metric("Annualized volatility", f"{result['volatility']:.2%}")
    reserve_col.metric("BIL reserve weight", f"{result['reserve_weight']:.0%}")


def scenario_rows(prices, objective, reserve_floor, annual_cost):
    """Run the pre-specified estimate, window, cost, and constraint stresses."""
    all_sleeves, all_correlation = estimates_from_prices(prices)
    recent_sleeves, recent_correlation = estimates_from_prices(prices, last_36_months=True)
    vt_stress = {ticker: values.copy() for ticker, values in all_sleeves.items()}
    vt_stress["VT"]["return"] -= 0.01
    definitions = [
        ("Base case", all_sleeves, all_correlation, objective, reserve_floor, annual_cost),
        ("VT return estimate -1.0 point", vt_stress, all_correlation, objective, reserve_floor, annual_cost),
        ("Last 36 monthly returns", recent_sleeves, recent_correlation, objective, reserve_floor, annual_cost),
        ("Annual cost +0.50 points", all_sleeves, all_correlation, objective, reserve_floor, annual_cost + 0.005),
        ("BIL floor raised to 20%", all_sleeves, all_correlation, objective, max(reserve_floor, 0.20), annual_cost),
    ]
    rows = []
    for name, sleeves, correlation, scenario_objective, scenario_floor, scenario_cost in definitions:
        result = run_search(sleeves, correlation, scenario_objective, scenario_floor, scenario_cost)
        rows.append(
            {
                "Scenario": name,
                "Allocation": allocation_text(result),
                "Net historical return": result["net_return"] if result else None,
                "Volatility": result["volatility"] if result else None,
                "Result": "Feasible" if result else "Stop / committee review",
            }
        )
    return pd.DataFrame(rows)


def robustness_map(prices, annual_cost):
    """Return sensitivity of selected allocation to objective and BIL-floor combinations."""
    sleeves, correlation = estimates_from_prices(prices)
    rows = []
    for objective in [0.045, 0.05, 0.055, 0.06, 0.065, 0.07]:
        for reserve_floor in [0.0, 0.10, 0.20, 0.30, 0.40]:
            result = run_search(sleeves, correlation, objective, reserve_floor, annual_cost)
            rows.append(
                {
                    "Net objective": objective,
                    "BIL minimum": reserve_floor,
                    "Volatility": result["volatility"] if result else None,
                    "Allocation": allocation_text(result),
                    "Status": "Feasible" if result else "No feasible mix",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    st.set_page_config(page_title="Project 2: Portfolio Mandate & Stress-Test Decision System", layout="wide")
    st.title("Project 2: Portfolio Mandate & Stress-Test Decision System")
    st.caption(
        "AI announcement: Generative AI assisted with code and documentation; the student verified the reported calculations "
        "and owns the analysis and decision. Education, not investment advice."
    )
    st.warning(
        "This is a classroom decision-support prototype. Historical estimates are not forecasts and do not establish that "
        "any allocation will meet its objective."
    )

    prices = load_prices()
    if list(prices.columns) != ["Date", *TICKERS]:
        st.error("Lab_15_prices.csv must contain Date, BIL, IEF, LQD, and VT in that order.")
        st.stop()

    st.sidebar.header("Mandate controls")
    objective = st.sidebar.number_input(
        "Net annualized historical-return objective", 0.0, 0.20, DEFAULT_OBJECTIVE, 0.005, format="%.3f"
    )
    reserve_floor = st.sidebar.number_input(
        "Minimum BIL reserve weight", 0.0, 1.0, DEFAULT_RESERVE, 0.05, format="%.2f"
    )
    annual_cost = st.sidebar.number_input(
        "Annual implementation-cost assumption", 0.0, 0.05, 0.0, 0.001, format="%.3f"
    )
    use_last_36 = st.sidebar.toggle("Use last 36 monthly returns", value=False)
    vt_shock = st.sidebar.slider("Interactive stress: reduce VT return estimate", 0.0, 0.05, 0.01, 0.005, format="%.1f%%")
    view = st.radio("View", ["Committee view", "Technical detail"], horizontal=True)

    sleeves, correlation = estimates_from_prices(prices, last_36_months=use_last_36)
    optimized = run_search(sleeves, correlation, objective, reserve_floor, annual_cost)
    base_sleeves, base_correlation = estimates_from_prices(prices)
    base_case = run_search(base_sleeves, base_correlation, DEFAULT_OBJECTIVE, DEFAULT_RESERVE, 0.0)

    if view == "Committee view":
        st.subheader("Committee decision")
        if optimized is None:
            st.error("Action: stop and return to committee review. No feasible allocation meets the active mandate.")
        else:
            change = largest_weight_change(base_case, optimized)
            action = "Hold pilot; no investable allocation or rebalancing authorization."
            if change is not None and change >= 0.20:
                action = "Hold pilot and return to committee review before any rebalance: allocation differs materially from the base case."
            st.success(f"Action: {action}")
            st.caption(
                "Reversal triggers: an infeasible stress, a material allocation shift across approved windows, a BIL-floor breach, "
                "or a failed point-in-time data control."
            )

        st.subheader("Base-case portfolio comparison")
        comparison_rows = [
            portfolio_row("Equal weight", equal_weight_weights(sleeves), sleeves, correlation, objective, reserve_floor, annual_cost),
            portfolio_row("Inverse volatility", inverse_volatility_weights(sleeves), sleeves, correlation, objective, reserve_floor, annual_cost),
        ]
        if optimized is not None:
            comparison_rows.append(
                portfolio_row("Constrained search", optimized["weights"], sleeves, correlation, objective, reserve_floor, annual_cost)
            )
        comparison = pd.DataFrame(comparison_rows)
        st.dataframe(
            comparison.style.format(
                {
                    "Net historical return": "{:.2%}",
                    "Annualized volatility": "{:.2%}",
                    "BIL reserve weight": "{:.0%}",
                }
            ),
            width="stretch",
            hide_index=True,
        )
        st.bar_chart(comparison.set_index("Portfolio")[["Net historical return", "Annualized volatility"]], width="stretch")

        left, right = st.columns(2)
        with left:
            st.subheader("Active allocation")
            render_mix(optimized)
        with right:
            st.subheader("Interactive VT-return stress")
            shocked_sleeves = {ticker: values.copy() for ticker, values in sleeves.items()}
            shocked_sleeves["VT"]["return"] -= vt_shock
            stressed = run_search(shocked_sleeves, correlation, objective, reserve_floor, annual_cost)
            st.caption(f"VT historical-return estimate reduced by {vt_shock:.1%}; all other active inputs unchanged.")
            render_mix(stressed)
            change = largest_weight_change(optimized, stressed)
            if stressed is None:
                st.error("Stop condition met: no feasible allocation remains under this stress.")
            elif change is not None:
                st.info(f"Largest allocation change from active case: {change:.0%} points.")

        st.subheader("Pre-specified stress scenarios")
        scenarios = scenario_rows(prices, objective, reserve_floor, annual_cost)
        st.dataframe(
            scenarios.style.format({"Net historical return": "{:.2%}", "Volatility": "{:.2%}"}),
            width="stretch",
            hide_index=True,
        )
        st.caption("The scenario table tests an estimate, sample window, cost, and constraint. “Stop / committee review” is the process stop condition.")

    else:
        st.subheader("Mandate and data")
        st.write(
            "**Objective:** at least the selected net annualized historical-return estimate after the displayed cost assumption. "
            "**Universe:** BIL, IEF, LQD, and VT. **Hard constraint:** at least the selected weight in BIL."
        )
        st.caption(
            f"Price sample: {pd.to_datetime(prices['Date']).min():%B %Y} through "
            f"{pd.to_datetime(prices['Date']).max():%B %Y}; {len(prices) - 1} monthly returns."
        )

        st.subheader("Allocation robustness map")
        robustness = robustness_map(prices, annual_cost)
        chart = (
            alt.Chart(robustness)
            .mark_rect()
            .encode(
                x=alt.X("BIL minimum:O", title="Minimum BIL reserve weight", axis=alt.Axis(format="%")),
                y=alt.Y("Net objective:O", title="Net historical-return objective", axis=alt.Axis(format="%")),
                color=alt.Color("Volatility:Q", title="Volatility", scale=alt.Scale(scheme="blues")),
                tooltip=[
                    alt.Tooltip("Net objective:Q", format=".1%"),
                    alt.Tooltip("BIL minimum:Q", format=".0%"),
                    alt.Tooltip("Allocation:N"),
                    alt.Tooltip("Volatility:Q", format=".2%"),
                    alt.Tooltip("Status:N"),
                ],
            )
            .properties(height=330)
        )
        st.altair_chart(chart, width="stretch")
        st.caption("Each cell shows the lowest-volatility feasible allocation under the stated objective and BIL floor; blank cells have no feasible mix.")
        st.dataframe(robustness, width="stretch", hide_index=True)

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


if __name__ == "__main__":
    main()
