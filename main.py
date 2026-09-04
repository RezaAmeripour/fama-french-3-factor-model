"""
Runs the full pipeline: load stock + factor data -> fit 3-factor regression
-> print/save results -> plot actual vs fitted returns.

Usage:
    python main.py
    python main.py --ticker MSFT --start 2018-01-01
"""
import argparse
import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_loader import build_dataset
from regression import fit_three_factor_model, results_table

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")


def main(ticker: str, start: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading data for {ticker} and Fama-French factors...")
    data = build_dataset(ticker=ticker, start=start)
    print(f"Matched {len(data)} trading days.")

    print("Fitting 3-factor regression...")
    results = fit_three_factor_model(data)

    print(results.summary())

    table = results_table(results)
    table_path = os.path.join(OUTPUT_DIR, "results.csv")
    table.to_csv(table_path, index=False)

    r_squared = results.rsquared
    print(f"\nR-squared: {r_squared:.4f}")
    with open(os.path.join(OUTPUT_DIR, "r_squared.txt"), "w") as f:
        f.write(f"{r_squared:.4f}\n")

    fitted = results.fittedvalues
    actual = data["excess_return"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(fitted, actual, alpha=0.3, s=10)
    lims = [min(fitted.min(), actual.min()), max(fitted.max(), actual.max())]
    ax.plot(lims, lims, color="red", linewidth=1, label="Perfect fit")
    ax.set_xlabel("Fitted excess return")
    ax.set_ylabel("Actual excess return")
    ax.set_title(f"Fama-French 3-Factor Model Fit: {ticker}")
    ax.legend()
    fig.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "actual_vs_fitted.png")
    fig.savefig(plot_path, dpi=150)
    plt.close(fig)

    print(f"\nSaved results table to {table_path}")
    print(f"Saved plot to {plot_path}")
    print("\nCopy the numbers from results.csv and r_squared.txt into the "
          "Results table in README.md.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", default="AAPL", help="Yahoo Finance ticker")
    parser.add_argument("--start", default="2015-01-01", help="Start date YYYY-MM-DD")
    args = parser.parse_args()

    main(args.ticker, args.start)
