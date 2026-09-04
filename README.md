# Fama-French 3-Factor Model: Fitted to a Single Stock

A simple, classic asset-pricing regression: explaining a stock's returns using the
Fama-French 3-Factor model.

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

This project fits that model to a single stock's daily returns using linear
regression (OLS), and interprets the result.

## Data

- **Stock returns**: pulled via `yfinance` for a chosen ticker (default `AAPL`).
- **Factor returns** (Mkt-RF, SMB, HML, RF): pulled directly from Kenneth French's
  publicly available data library at Dartmouth — the standard source every academic
  and practitioner uses for this exact model.

## Method

1. Compute the stock's daily excess return: `stock_return - risk_free_rate`.
2. Regress that excess return on the three factors:

   `Excess Return = alpha + beta_mkt * Mkt-RF + beta_smb * SMB + beta_hml * HML + error`

3. Interpret the output:
   - **beta_mkt** — how sensitive the stock is to the overall market (close to 1 =
     moves with the market; higher = more aggressive than the market).
   - **beta_smb** — positive means the stock behaves more like a small-cap stock;
     negative means it behaves more like a large-cap stock.
   - **beta_hml** — positive means the stock behaves more like a value stock;
     negative means it behaves more like a growth stock.
   - **alpha** — the return left unexplained by the three factors. In an efficient
     market, alpha should be close to zero; a large, statistically significant alpha
     would be a notable (and rare) finding.
   - **R-squared** — how much of the stock's return variation the three factors
     explain overall.

## Results

*(Fill this in after running `main.py` locally — paste the actual regression output:
alpha, the three betas, R-squared, and which coefficients were statistically
significant.)*

| Coefficient | Estimate | p-value | Significant? |
|-------------|----------|---------|---------------|
| Alpha       | 0.0004 (0.04%)      | 0.104     | No           |
| Mkt-RF beta | 1.16      | <0.001     | Yes           |
| SMB beta    | -0.29      | <0.001     | Yes           |
| HML beta    | -0.34      | <0.001     | Yes           |

R-squared: 0.564

## Limitations

- Single-stock regression on daily data — factor models are more commonly applied
  to diversified portfolios, where idiosyncratic (stock-specific) noise averages out.
  A single stock's daily returns are noisier, so expect a lower R-squared than you'd
  see applying this to a portfolio or index.
- Only covers the original 3 factors — later research (Fama-French 5-Factor,
  momentum) adds more explanatory power.
- Uses daily rather than monthly data; the original Fama-French papers use monthly
  data, which is the more standard convention in academic work.

## Repository structure

- `src/data_loader.py` — pulls stock returns and Fama-French factor data
- `src/regression.py` — runs the OLS regression and formats results
- `main.py` — runs the full pipeline end to end
- `outputs/` — regression summary and a plot of actual vs. fitted returns

## Running it

```bash
pip install -r requirements.txt
python main.py
```
