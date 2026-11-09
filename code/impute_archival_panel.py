"""Recreate the archived 1990–2023 MICE panels from the original Excel input."""
import argparse
from pathlib import Path

import miceforest
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", type=Path, required=True, help="Original XLSX with the Panel worksheet")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    panel = pd.read_excel(args.panel, sheet_name="Panel")
    numeric = panel.select_dtypes(include="number")
    # Match the original notebook. Restrict the exported years after fitting.
    kernel = miceforest.ImputationKernel(
        numeric, datasets=5, save_all_iterations=True, random_state=123,
    )
    kernel.mice(5)

    args.out.mkdir(parents=True, exist_ok=True)
    observed = numeric.notna()
    years = panel["Year"].between(1990, 2023)
    for index in range(5):
        completed = kernel.complete_data(dataset=index, inplace=False)
        if completed.isna().any().any() or not completed.where(observed).equals(numeric.where(observed)):
            raise ValueError(f"Imputation {index + 1} has missing cells or changed observations")
        result = panel.loc[years].copy()
        result[completed.columns] = completed.loc[years]
        result.to_csv(args.out / f"analysis_panel_imputed_m{index + 1}_1990_2023.csv", index=False)
    print("Exported five MICE panels for 1990–2023.")


if __name__ == "__main__":
    main()
