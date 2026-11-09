"""Reconstruct the WDI-only analysis series and optionally audit the input panel."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook

SERIES = {
    "co2_emissions": ("EN.GHG.CO2.MT.CE.AR5", 0),
    "gdp_growth": ("NY.GDP.MKTP.KD.ZG", 0),
    "energy_use_pc": ("EG.USE.PCAP.KG.OE", 0),
    "renewable_share": ("EG.FEC.RNEW.ZS", 0),
    "trade_gdp_lagged_1": ("NE.TRD.GNFS.ZS", 1),
    "fdi_gdp_lagged_1": ("BX.KLT.DINV.WD.GD.ZS", 1),
    "inflation_lagged_1": ("FP.CPI.TOTL.ZG", 1),
    "unemployment_lagged_1": ("SL.UEM.TOTL.ZS", 1),
}
KEY = ["Country Code", "Year"]


def reconstruct(source):
    sheet = load_workbook(source, read_only=True, data_only=True).worksheets[0]
    records = sheet.values
    header = next(records)
    position = {str(value): i for i, value in enumerate(header) if value}
    variables = {code: (name, lag) for name, (code, lag) in SERIES.items()}
    rows = []
    for row in records:
        code = row[position["Series Code"]]
        if code not in variables:
            continue
        name, lag = variables[code]
        country = row[position["Country Code"]]
        for year in range(1990, 2024):
            source_year = year - lag
            i = position[f"{source_year} [YR{source_year}]"]
            rows.append((country, year, name, row[i] if source_year >= 1990 else None))
    data = pd.DataFrame(rows, columns=KEY + ["variable", "value"])
    data["value"] = pd.to_numeric(data.value, errors="coerce")
    return data.pivot(index=KEY, columns="variable", values="value").reset_index()


def audit(panel, wdi):
    original = pd.read_csv(panel)
    original = original.loc[original.Year.between(1990, 2023)]
    merged = original.merge(wdi, on=KEY, suffixes=("_panel", "_wdi"), how="left", validate="one_to_one")
    rows = []
    for name, (code, lag) in SERIES.items():
        a, b = merged[f"{name}_panel"], merged[f"{name}_wdi"]
        paired = a.notna() & b.notna()
        diff = (a[paired] - b[paired]).abs()
        close = np.isclose(a[paired], b[paired], atol=1e-5, rtol=1e-5)
        rows.append((name, code, lag, paired.sum(), (a.notna() & b.isna()).sum(),
                     (a.isna() & b.notna()).sum(), (~close).sum(), diff.max()))
    return pd.DataFrame(rows, columns=["variable", "wdi_series", "lag_years", "paired_numeric",
                                       "panel_only", "wdi_only", "outside_rounding_tolerance", "max_abs_diff"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--panel", type=Path, help="Optional confidential panel to audit")
    args = parser.parse_args()
    data = reconstruct(args.raw)
    if args.panel:
        data = audit(args.panel, data)
    data.to_csv(args.out, index=False)
