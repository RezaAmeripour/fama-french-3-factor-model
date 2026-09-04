# Fama-French 3-Factor Model: Explaining Equity Returns

A classic asset-pricing regression: explaining a stock's daily returns using the
Fama-French 3-Factor model. Built and run as a single Jupyter notebook.

## What this is

The Capital Asset Pricing Model (CAPM) says a stock's return is explained by one
thing: how the overall market moved. Fama and French (1993) showed that two more
factors meaningfully improve on this:

- **Mkt-RF** — the market's excess return (market return minus the risk-free rate).
  Same idea as CAPM.
- **SMB** ("Small Minus Big") — the historical tendency for small-company stocks to
  outperform large-company stocks.
- **HML** ("High Minus Low") — the historical tendency for "value" stocks (high
  book-to-market ratio) to outperform "growth" stocks.

This project fits that model to a single stock's daily returns (Apple, `AAPL`)
using linear regression (OLS), and interprets the result.

## Data

- **Stock returns**: pulled via `yfinance`.
- **Factor returns** (Mkt-RF, SMB, HML, RF): pulled directly from Kenneth French's
  publicly available data library at Dartmouth — the standard source every academic
  and practitioner uses for this exact model.

## Method

1. Compute the stock's daily excess return: `stock_return - risk_free_rate`.
2. Regress that excess return on the three factors:

   `Excess Return = alpha + beta_mkt * Mkt-RF + beta_smb * SMB + beta_hml * HML + error`

3. Interpret the output — see Results below.

## Results

Fitted on AAPL, 2015–present (2,910 matched trading days):

| Coefficient | Estimate | p-value | Significant? |
|-------------|----------|---------|---------------|
| Alpha       | 0.0004 (0.04%) | 0.104   | No            |
| Mkt-RF beta | 1.16     | <0.001  | Yes           |
| SMB beta    | -0.29    | <0.001  | Yes           |
| HML beta    | -0.34    | <0.001  | Yes           |

**R-squared: 0.564**

**Interpretation:**
- **Beta of 1.16** — Apple is more volatile than the overall market (moves about
  16% more on average), consistent with it being a higher-beta tech stock.
- **Negative SMB (-0.29)** — Apple behaves like a large-cap stock, not a small-cap
  one — correctly picked up by the model given it's one of the largest companies
  in the world.
- **Negative HML (-0.34)** — Apple behaves like a growth stock, not a value stock —
  again consistent with its profile as a high-growth tech company.
- **Alpha not significant (p=0.104)** — no unexplained "extra" return once the
  three factors are accounted for, which is the expected result in an efficient
  market (a large, significant alpha would be the unusual finding).
- **R-squared of 0.564** — the three factors explain 56% of Apple's daily return
  variation, a solid result for a single-stock regression (noisier than a
  portfolio-level regression would be).

## Limitations

- Single-stock regression on daily data — factor models are more commonly applied
  to diversified portfolios, where idiosyncratic (stock-specific) noise averages
  out. A single stock's daily returns are noisier, so expect a lower R-squared than
  you'd see applying this to a portfolio or index.
- Only covers the original 3 factors — later research (Fama-French 5-Factor,
  momentum) adds more explanatory power.
- Uses daily rather than monthly data; the original Fama-French papers use monthly
  data, which is the more standard convention in academic work.

## Repository structure

- `fama_french_3factor.ipynb` — the full project: data loading, factor download,
  regression, interpretation, and plot, in one notebook
- `requirements.txt` — Python dependencies
- `README.md` — this file

## Running it

You can view results by opening the fama_french_3factor.ipynb on GitHub.
