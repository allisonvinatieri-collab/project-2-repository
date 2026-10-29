# Lab 14 — Portfolio Return, Risk, and Mandate Fit

## Illustrative portfolio estimates

The lab does not provide approved capital-market assumptions, so these are illustrative long-run estimates rather than a mandate test. Risk is annualized volatility.

| Portfolio | Expected annual return | Annual volatility (risk) | Meridian mandate verdict |
|---|---:|---:|---|
| A | 6.69% | 10.32% | Best candidate: passes every checkable rule, but full compliance cannot be confirmed. |
| B | 7.15% | 11.56% | Fails: inadequate reserve, liquidity, and issuer concentration. |
| C | 7.39% | 13.37% | Fails: inadequate reserve. |
| D | 3.95% | 1.66% | Passes the checker, but is unlikely to achieve CPI + 4% net. |

The estimates use illustrative returns and volatilities for cash, Treasuries, global equity, investment-grade bonds, private real estate, and Acme securities.

## Meridian mandate conclusion

The mandate objective is CPI + 4% net over rolling five-year periods. If inflation is 2%, the approximate nominal hurdle is 6% net. Candidate A is the only candidate that both passes the checkable constraints and has a plausible expected return above that hurdle.

No candidate can be confirmed as fully compliant yet. The mandate lacks the approved return model, cost assumptions, loss definition, and turnover data needed to test the objective and risk policy.

## Diversification

Diversification means combining investments whose returns do not move exactly together. It can lower portfolio risk without requiring every investment to be low risk.

When correlation is below +1, the sleeves are not perfectly synchronized. Some movement in one sleeve can be offset by different movement in another, so the combined portfolio has lower volatility than a simple weighted average of individual volatilities. The covariance term captures that co-movement.

### Benchmark volatility by hand

The benchmark is 40% investment-grade bonds (5.0% expected return, 6.0% volatility) and 60% global equity (8.0% expected return, 16.0% volatility), with a correlation of 0.25.

| Step | Rule | Benchmark calculation |
|---|---|---|
| Expected return | $\sum weight \times return$ | $0.40 \times 5.0\% + 0.60 \times 8.0\% = 6.80\%$ |
| Covariance, bonds–equity | $correlation \times vol \times vol$ | $0.25 \times 0.06 \times 0.16 = 0.0024$ |
| Variance | $w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2 \times covariance$ | $0.000576 + 0.009216 + 0.001152 = 0.010944$ |
| Volatility | $\sqrt{variance}$ | $\sqrt{0.010944} = 10.46\%$ |
| Without the correlation term | Classic error | $\sqrt{0.000576 + 0.009216} = 9.90\%$ |

The 9.90% result is incorrect because it omits the covariance term. Including it produces the correct 10.46% benchmark volatility.

### Inverse-volatility weight for Treasury bills

Inverse-volatility weighting assigns each sleeve a weight proportional to $1 \div volatility$. For Treasury bills:

$$
(1 \div 0.005) \div \sum(1 \div volatility) = 200 \div 237.2 = 84.3\%
$$

### Annualizing monthly data

For simple annualization of independent monthly data, multiply the mean return by 12 and the standard deviation by $\sqrt{12}$. This is simple scaling, not compounded growth.

- 0.6% per month becomes 7.2% per year.
- 4.0% monthly standard deviation becomes 13.9% annual volatility.
