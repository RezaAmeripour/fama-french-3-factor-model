"""
Fits the Fama-French 3-factor regression using OLS:

    excess_return = alpha + beta_mkt * Mkt-RF + beta_smb * SMB + beta_hml * HML + error
"""
import pandas as pd
import statsmodels.api as sm


def fit_three_factor_model(data: pd.DataFrame):
    """
    data must contain columns: excess_return, Mkt-RF, SMB, HML

    Returns the fitted statsmodels regression results object.
    """
    X = data[["Mkt-RF", "SMB", "HML"]]
    X = sm.add_constant(X)  # adds the alpha (intercept) term
    y = data["excess_return"]

    model = sm.OLS(y, X)
    results = model.fit()
    return results


def results_table(results) -> pd.DataFrame:
    """Turns the statsmodels results into a clean, CV/README-ready table."""
    coef_names = {"const": "Alpha", "Mkt-RF": "Mkt-RF beta",
                  "SMB": "SMB beta", "HML": "HML beta"}

    table = pd.DataFrame({
        "coefficient": [coef_names[name] for name in results.params.index],
        "estimate": results.params.values,
        "p_value": results.pvalues.values,
    })
    table["significant_5pct"] = table["p_value"] < 0.05
    return table
