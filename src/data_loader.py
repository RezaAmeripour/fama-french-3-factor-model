"""
Loads two things and merges them by date:
  1. A stock's daily returns (via yfinance)
  2. Fama-French 3-factor daily data (Mkt-RF, SMB, HML, RF), pulled directly
     from Kenneth French's data library at Dartmouth - the standard public
     source for this data.
"""
import io
import os
import zipfile

import numpy as np
import pandas as pd
import requests
import yfinance as yf

FF_FACTORS_URL = (
    "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
    "F-F_Research_Data_Factors_daily_CSV.zip"
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")


def load_stock_returns(ticker: str = "AAPL", start: str = "2015-01-01",
                        end: str = None) -> pd.Series:
    """Returns a Series of daily simple returns (not log returns - we're
    matching Fama-French's convention, which uses simple returns)."""
    raw = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if raw.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Check the symbol.")
    close = raw["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]  # collapse to a plain Series if needed
    returns = close.pct_change().dropna()
    returns = returns.rename("stock_return")
    return returns


def load_ff_factors(use_cache: bool = True) -> pd.DataFrame:
    """
    Downloads and parses the Fama-French daily 3-factor CSV.
    Returns a DataFrame indexed by date with columns: Mkt-RF, SMB, HML, RF
    (all as decimals, e.g. 0.01 = 1%, not 1.0).
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, "ff_factors_daily.csv")

    if use_cache and os.path.exists(cache_path):
        return pd.read_csv(cache_path, index_col=0, parse_dates=True)

    resp = requests.get(FF_FACTORS_URL, timeout=30)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        csv_name = [n for n in zf.namelist() if n.lower().endswith(".csv")][0]
        with zf.open(csv_name) as f:
            raw_text = f.read().decode("latin-1")

    lines = raw_text.splitlines()
    # find the header row (starts with a comma, followed by Mkt-RF etc.)
    header_idx = next(i for i, line in enumerate(lines) if "Mkt-RF" in line)

    data_lines = [lines[header_idx]]
    for line in lines[header_idx + 1:]:
        first_field = line.split(",")[0].strip()
        # data rows start with an 8-digit date (YYYYMMDD); stop at the
        # annual-data section or trailing notes, which break this pattern
        if first_field.isdigit() and len(first_field) == 8:
            data_lines.append(line)
        elif len(data_lines) > 1:
            break  # we've reached the end of the daily data block

    df = pd.read_csv(io.StringIO("\n".join(data_lines)))
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={df.columns[0]: "date"})
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df = df.set_index("date")

    for col in ["Mkt-RF", "SMB", "HML", "RF"]:
        df[col] = pd.to_numeric(df[col], errors="coerce") / 100.0  # % -> decimal

    df = df.dropna()
    df.to_csv(cache_path)
    return df


def build_dataset(ticker: str = "AAPL", start: str = "2015-01-01") -> pd.DataFrame:
    """
    Returns a merged DataFrame indexed by date with columns:
        stock_return, Mkt-RF, SMB, HML, RF, excess_return
    where excess_return = stock_return - RF.
    """
    stock = load_stock_returns(ticker=ticker, start=start)
    factors = load_ff_factors()

    merged = pd.concat([stock, factors], axis=1, join="inner")
    merged["excess_return"] = merged["stock_return"] - merged["RF"]
    return merged.dropna()


if __name__ == "__main__":
    data = build_dataset()
    print(data.head())
    print(f"\n{len(data)} matched trading days")
