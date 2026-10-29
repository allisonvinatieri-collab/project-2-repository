"""Compute portfolio return, risk, reserves, and objective status."""

# Editable course inputs
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160},
}

CORRELATION = {
    "Treasury bills": {
        "Treasury bills": 1.00, "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10, "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05, "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00, "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_correlation(correlation, sleeves):
    """Raise ValueError when the correlation table is invalid."""
    names = set(sleeves)
    if set(correlation) != names:
        raise ValueError("Correlation table must contain every sleeve exactly once.")

    for left in names:
        if set(correlation[left]) != names:
            raise ValueError(f"Correlation row for {left} must contain every sleeve.")
        for right in names:
            value = correlation[left][right]
            if not -1 <= value <= 1:
                raise ValueError(f"Correlation for {left} and {right} must be between -1 and 1.")
            if value != correlation[right][left]:
                raise ValueError(f"Correlation table is not symmetric for {left} and {right}.")


def covariance_matrix(sleeves, correlation):
    """Return covariance values as a nested dictionary."""
    return {
        left: {
            right: correlation[left][right]
            * sleeves[left]["volatility"]
            * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def expected_return(weights, sleeves):
    """Return the weighted expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariance):
    """Return portfolio volatility from weights and covariance values."""
    variance = sum(
        weights[left] * weights[right] * covariance[left][right]
        for left in weights
        for right in weights
    )
    return variance ** 0.5


def reserve_eligible_weight(weights, reserve_eligible):
    """Return the combined reserve-eligible portfolio weight."""
    return sum(weights[name] for name in reserve_eligible)


def meets_objective(portfolio_return, objective_return):
    """Return whether the expected return meets the objective."""
    return portfolio_return >= objective_return


def benchmark_weights(sleeves):
    """Return the 40% investment-grade bond and 60% equity benchmark."""
    return {
        name: 0.40 if name == "Investment-grade bond fund"
        else 0.60 if name == "Global equity index fund"
        else 0.0
        for name in sleeves
    }


def equal_weight_weights(sleeves):
    """Return equal weights across all sleeves."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_weights(sleeves):
    """Return weights proportional to inverse volatility."""
    inverse_volatilities = {
        name: 1 / values["volatility"] for name, values in sleeves.items()
    }
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def print_portfolio(name, weights, sleeves, covariance):
    """Print required portfolio metrics."""
    portfolio_return = expected_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariance)
    reserve_weight = reserve_eligible_weight(weights, RESERVE_ELIGIBLE)
    print(f"\n{name}")
    for sleeve in sleeves:
        print(f"  {sleeve}: {weights[sleeve]:.1%}")
    print(f"  Expected return: {portfolio_return:.2%}")
    print(f"  Volatility: {volatility:.2%}")
    print(f"  Reserve-eligible weight: {reserve_weight:.1%}")
    print(f"  Meets {OBJECTIVE_RETURN:.1%} objective: {'yes' if meets_objective(portfolio_return, OBJECTIVE_RETURN) else 'no'}")


def main():
    """Validate inputs and print the three portfolios."""
    validate_correlation(CORRELATION, SLEEVES)
    covariance = covariance_matrix(SLEEVES, CORRELATION)
    portfolios = {
        "Benchmark": benchmark_weights(SLEEVES),
        "Equal weight": equal_weight_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance)


if __name__ == "__main__":
    main()
