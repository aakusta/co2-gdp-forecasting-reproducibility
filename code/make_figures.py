"""Generate manuscript figures from the analysis input and aggregated fold evidence."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

from src.replicate import FEATURES, TARGETS, load_panel

LABEL = {"co2_emissions": "CO₂ emissions (Mt)", "gdp_growth": "GDP growth (percentage points)"}
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7"]
MARKERS = ["o", "s", "D", "^", "P"]


def heatmap(frame, out, label, maximum, minimum=0, cmap="Reds"):
    fig, ax = plt.subplots(figsize=(9, max(3.5, 0.21 * len(frame))))
    m = ax.imshow(frame, cmap=cmap, aspect="auto", vmin=minimum, vmax=maximum)
    ax.set_xticks(range(len(frame.columns)), frame.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(frame.index)), frame.index)
    fig.colorbar(m, ax=ax, label=label)
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)


def make_figures(panel, out, figures):
    figures.mkdir(parents=True, exist_ok=True)
    raw = load_panel(panel)
    labels = {
        "co2_emissions": "CO₂ emissions", "gdp_growth": "GDP growth",
        "energy_use_pc": "Energy use per capita", "renewable_share": "Renewable energy share",
        "trade_gdp_lagged_1": "Trade openness (lag 1)", "fdi_gdp_lagged_1": "FDI (lag 1)",
        "inflation_lagged_1": "Inflation (lag 1)", "unemployment_lagged_1": "Unemployment (lag 1)",
    }
    missing = raw[TARGETS + FEATURES].isna().rename(columns=labels)
    rate = 100 * missing.groupby(level=0).mean()
    heatmap(rate, figures / "figure1_missing_values_heatmap.png", "Missing observations (%)", 100)

    country_names = raw["Country Name"].groupby(level=0).first()
    country_rates = rate.div(100).rename(index=country_names)
    order = country_rates.mean(axis=1).sort_values(ascending=False, kind="stable").index
    heatmap(country_rates.loc[order], figures / "appendix_figure_a2_missingness_country_pattern.png",
            "Missing observations (proportion)", 1, cmap="YlGnBu")
    heatmap(missing.astype(float).corr(), figures / "appendix_figure_a1_missingness_correlation_matrix.png",
            "Correlation", 1, -1, "RdBu_r")

    folds = pd.read_csv(out / "fold_metrics.csv")
    mt = folds.loc[folds.model.eq("MT-GRU")]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True)
    for i, target in enumerate(TARGETS):
        for j, metric in enumerate(["RMSE", "MAE"]):
            ax = axes[i, j]
            for imp, frame in mt.loc[mt.target.eq(target)].groupby("imputation"):
                ax.plot(frame.origin, frame[metric], label=f"Imputation {imp}", color=PALETTE[imp - 1],
                        marker=MARKERS[imp - 1], markersize=3)
            ax.set_title(f"{LABEL[target]} · {metric}")
            ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=7))
            if i == 1:
                ax.set_xlabel("Forecast year")
            ax.grid(alpha=0.2)
    handles, names = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, names, loc="lower center", ncol=5, frameon=False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(figures / "figure2_cross_imputation_stability.png", dpi=220)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7), layout="constrained")
    metrics = ["RMSE", "MAE", "nRMSE", "Bias", "R2", "DA"]
    for target, ax in zip(TARGETS, axes):
        frame = folds.loc[folds.target.eq(target)].groupby("model")[metrics].mean()
        frame["Bias"] = frame.Bias.abs()
        frame[["R2", "DA"]] *= -1
        span = frame.max() - frame.min()
        score = (frame.max() - frame).divide(span.replace(0, np.nan)).fillna(1)
        matrix = ax.imshow(score, cmap="YlGnBu", vmin=0, vmax=1, aspect="auto")
        ax.set_title(LABEL[target])
        ax.set_yticks(range(len(score)), score.index)
        ax.set_xticks(range(len(metrics)), ["RMSE", "MAE", "nRMSE", "|Bias|", "R²", "DA"])
    fig.colorbar(matrix, ax=axes, label="Within-target score (1 = best)")
    fig.savefig(figures / "figure3_metric_normalized_model_comparison.png", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ["panel", "out", "figures"]:
        parser.add_argument(f"--{option}", required=True, type=Path)
    args = parser.parse_args()
    make_figures(args.panel, args.out, args.figures)
