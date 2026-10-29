"""Streamlit preview: lowest-risk mix meeting the Project 2 mandate."""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).with_name("Lab_15_prices.csv")
RESERVE_TICKER = "BIL"


@st.cache_data
def load_prices() -> pd.DataFrame:
    """Load adjusted monthly prices from the project data file."""
    return pd.read_csv(DATA_FILE, parse_dates=["Date"], index_col="Date")


def lowest_risk_mix(
    annual_returns: np.ndarray,
    annual_covariance: np.ndarray,
    target: float,
    minimum_reserve: float,
):
    """Search 1-percentage-point long-only allocations for the lowest volatility mix."""
    choices = []
    reserve_floor = int(np.ceil(minimum_reserve * 100 - 1e-9))
    for bil in range(reserve_floor, 101):
        for ief in range(101 - bil):
            for lqd in range(101 - bil - ief):
                vt = 100 - bil - ief - lqd
                weights = np.array([bil, ief, lqd, vt], dtype=float) / 100
                portfolio_return = float(weights @ annual_returns)
                if portfolio_return >= target:
                    volatility = float(np.sqrt(weights @ annual_covariance @ weights))
                    choices.append((volatility, portfolio_return, weights))
    return min(choices, key=lambda choice: choice[0]) if choices else None


def show_result(label: str, result, tickers: list[str]) -> None:
    st.subheader(label)
    if result is None:
        st.error("No 1% allocation meets this target and reserve constraint.")
        return
    volatility, portfolio_return, weights = result
    mix = pd.DataFrame({"Ticker": tickers, "Weight": weights}).set_index("Ticker")
    st.dataframe(mix.style.format({"Weight": "{:.0%}"}), width="stretch")
    left, right = st.columns(2)
    left.metric("Annualized historical return", f"{portfolio_return:.2%}")
    right.metric("Annualized volatility", f"{volatility:.2%}")


st.set_page_config(page_title="Project 2 Portfolio Engine", layout="centered")
st.title("Project 2 Portfolio Engine")
st.caption("Lowest-risk 1% allocation that meets the historical return objective.")

prices = load_prices()
returns = prices.pct_change().dropna()
tickers = list(prices.columns)
if tickers != ["BIL", "IEF", "LQD", "VT"]:
    st.error("Lab_15_prices.csv must contain BIL, IEF, LQD, and VT in that order.")
    st.stop()

annual_returns = returns.mean().to_numpy() * 12
annual_covariance = returns.cov().to_numpy() * 12
st.sidebar.header("Mandate controls")
target = st.sidebar.slider("Annualized return objective", 0.02, 0.12, 0.06, 0.005)
reserve_floor = st.sidebar.slider("Minimum BIL reserve", 0.00, 0.50, 0.10, 0.01)
shock_ticker = st.sidebar.selectbox("One-point estimate test", tickers, index=tickers.index("VT"))
shock_direction = st.sidebar.radio("Estimate change", ("Decrease by 1 point", "Increase by 1 point"))

st.write(f"Using {len(prices)} monthly adjusted-close observations from {prices.index.min():%b %Y} through {prices.index.max():%b %Y}.")
base_result = lowest_risk_mix(annual_returns, annual_covariance, target, reserve_floor)
show_result("Base mandate", base_result, tickers)

st.divider()
shock = -0.01 if shock_direction.startswith("Decrease") else 0.01
shocked_returns = annual_returns.copy()
shocked_returns[tickers.index(shock_ticker)] += shock
one_point_result = lowest_risk_mix(shocked_returns, annual_covariance, target, reserve_floor)
show_result(
    f"One-point test: {shock_ticker} return estimate {shock:+.0%}",
    one_point_result,
    tickers,
)
if one_point_result is None:
    st.warning("No feasible 1% allocation survives this one-point estimate change.")
else:
    st.success("A feasible allocation survives this one-point estimate change.")

with st.expander("What happens when a control moves?"):
    st.write("Streamlit reruns this script from top to bottom. The changed widget value is used to recalculate the feasible allocations and refresh the result.")
