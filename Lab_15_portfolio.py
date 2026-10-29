"""Lab 14 portfolio engine plus reusable search and price-estimate functions."""

from pathlib import Path

import numpy as np
import pandas as pd

from lab_14_portfolio import (
    CORRELATION as LAB14_CORRELATION,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    covariance_matrix,
    expected_return,
    main,
    portfolio_volatility,
    reserve_eligible_weight,
    validate_correlation,
)

# Kept here so the app uses this file as the single editable Meridian input source.
CORRELATION = {name: row.copy() for name, row in LAB14_CORRELATION.items()}


def lowest_risk_mix(
    sleeves, correlation, objective_return, reserve_eligible, minimum_reserve
):
    """Return the lowest-volatility feasible long-only allocation in 5% steps."""
    validate_correlation(correlation, sleeves)
    if not 0 <= minimum_reserve <= 1:
        raise ValueError("minimum_reserve must be between 0 and 1.")

    names = list(sleeves)
    covariance = covariance_matrix(sleeves, correlation)
    best = None

    def try_weights(position, remaining, weights):
        nonlocal best
        if position == len(names) - 1:
            candidate = {**weights, names[position]: remaining / 100}
            candidate_return = expected_return(candidate, sleeves)
            candidate_reserve = reserve_eligible_weight(candidate, reserve_eligible)
            if candidate_return < objective_return or candidate_reserve < minimum_reserve:
                return
            candidate_volatility = portfolio_volatility(candidate, covariance)
            result = {
                "weights": candidate,
                "return": candidate_return,
                "volatility": candidate_volatility,
                "reserve_weight": candidate_reserve,
            }
            if best is None or result["volatility"] < best["volatility"]:
                best = result
            return

        for weight in range(0, remaining + 1, 5):
            try_weights(position + 1, remaining - weight, {**weights, names[position]: weight / 100})

    try_weights(0, 100, {})
    return best


def estimates_from_prices(prices_or_csv, last_36_months=False):
    """Estimate annualized returns, volatilities, and correlations from monthly prices."""
    if isinstance(prices_or_csv, pd.DataFrame):
        prices = prices_or_csv.copy()
    else:
        prices = pd.read_csv(Path(prices_or_csv))
    if prices.shape[1] < 2 or prices.columns[0] != "Date":
        raise ValueError("CSV must have Date first and at least one ticker column.")

    prices["Date"] = pd.to_datetime(prices["Date"])
    if not prices["Date"].is_monotonic_increasing:
        raise ValueError("Dates must be oldest first.")
    if prices["Date"].duplicated().any() or prices.isna().any().any():
        raise ValueError("Prices must have unique dates and no missing values.")

    monthly_returns = prices.set_index("Date").pct_change().dropna()
    if last_36_months:
        monthly_returns = monthly_returns.tail(36)
    if len(monthly_returns) < 2:
        raise ValueError("At least three monthly prices are required.")

    sleeves = {
        ticker: {
            "return": float(monthly_returns[ticker].mean() * 12),
            "volatility": float(monthly_returns[ticker].std() * np.sqrt(12)),
        }
        for ticker in monthly_returns.columns
    }
    correlation_frame = monthly_returns.corr()
    correlation = {
        left: {right: float(correlation_frame.loc[left, right]) for right in sleeves}
        for left in sleeves
    }
    return sleeves, correlation


if __name__ == "__main__":
    main()
