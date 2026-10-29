"""Interactive Lab 15 portfolio app."""

import pandas as pd
import streamlit as st

from Lab_15_portfolio import (
    CORRELATION,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimates_from_prices,
    lowest_risk_mix,
)


def show_answer(label, result):
    """Display a search result or the required no-solution message."""
    st.subheader(label)
    if result is None:
        st.warning("No mix meets the objective.")
        return
    weights = pd.DataFrame.from_dict(result["weights"], orient="index", columns=["Weight"])
    st.dataframe(weights.style.format("{:.0%}"), width="stretch")
    one, two, three = st.columns(3)
    one.metric("Return", f"{result['return']:.2%}")
    two.metric("Volatility", f"{result['volatility']:.2%}")
    three.metric("Reserve-eligible", f"{result['reserve_weight']:.2%}")


st.set_page_config(page_title="Lab 15 Portfolio App", layout="wide")
st.title("Lab 15 Portfolio App")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

st.sidebar.header("Mandate controls")
objective = st.sidebar.number_input("Objective", 0.0, 1.0, float(OBJECTIVE_RETURN), 0.005, format="%.3f")
reserve_minimum = st.sidebar.number_input("Minimum reserve-eligible weight", 0.0, 1.0, 0.03, 0.01, format="%.2f")
uploaded_file = st.sidebar.file_uploader("Your Lab_15_prices.csv", type="csv")
last_36 = st.sidebar.toggle("Use last 36 months", value=False)

try:
    if uploaded_file is None:
        loaded_sleeves = {name: values.copy() for name, values in SLEEVES.items()}
        loaded_correlation = CORRELATION
        source_label = "Meridian inputs as loaded"
    else:
        uploaded_prices = pd.read_csv(uploaded_file)
        loaded_sleeves, loaded_correlation = estimates_from_prices(uploaded_prices)
        source_label = "CSV estimates on all months"
    current_sleeves, current_correlation = (
        estimates_from_prices(uploaded_prices, last_36) if uploaded_file is not None else (loaded_sleeves, loaded_correlation)
    )
except ValueError as error:
    st.error(str(error))
    st.stop()

st.subheader("Expected-return estimates")
edited_sleeves = {name: values.copy() for name, values in current_sleeves.items()}
return_columns = st.columns(len(edited_sleeves))
for column, (name, values) in zip(return_columns, edited_sleeves.items()):
    values["return"] = column.number_input(
        name, -1.0, 1.0, float(values["return"]), 0.005, format="%.3f"
    )

st.subheader("Reserve-eligible assets")
reserve_columns = st.columns(len(edited_sleeves))
selected_reserves = {
    name
    for column, name in zip(reserve_columns, edited_sleeves)
    if column.checkbox(name, value=name in RESERVE_ELIGIBLE, key=f"reserve_{name}")
}

loaded_result = lowest_risk_mix(
    loaded_sleeves, loaded_correlation, objective, selected_reserves, reserve_minimum
)
current_result = lowest_risk_mix(
    edited_sleeves, current_correlation, objective, selected_reserves, reserve_minimum
)

left, right = st.columns(2)
with left:
    show_answer("Current controls", current_result)
with right:
    show_answer(source_label, loaded_result)

if current_result is not None and loaded_result is not None:
    largest_change = max(
        abs(current_result["weights"][name] - loaded_result["weights"][name])
        for name in edited_sleeves
    )
    st.info(f"Largest weight change: {largest_change:.0%} points.")
