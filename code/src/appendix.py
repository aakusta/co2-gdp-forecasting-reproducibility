"""Regenerate supplementary diagnostics from fold inputs and primary traces."""
from functools import partial
import hashlib
from pathlib import Path
import tempfile
import warnings

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, combine_pvalues, mannwhitneyu

from .replicate import (
    FEATURES, POLICY, TARGETS, TRACE_COLUMNS, fit_predict, historical_slice, make_split, score_trace,
    trace_predictions,
)

PFI_COLUMNS = ["origin", "imputation", "feature", "target", "base_sse", "permuted_sse", "observations"]
MT = ["MT-GRU"]
GRU = ["MT-GRU", "ST-GRU"]
SHORT_ORIGINS = {2005, 2014, 2023}
NAMES = {
    1: "country_list_58_national_units", 2: "no_imputation_robustness",
    3: "warm_start_from_scratch", 4: "multi_horizon_diagnostics",
    5: "imputation_variance_summary", 6: "lookback_sensitivity",
    7: "hyperparameter_sensitivity", 8: "classical_econometric_diagnostics",
    9: "missingness_mechanism_diagnostics", 10: "mnar_sensitivity",
    11: "imputation_effect_on_key_results", 12: "prediction_interval_summary",
    13: "gru_ablation_mapping", 14: "gru_ablation_numerical_summary",
}


def save(frame, out, number):
    frame.to_csv(out / f"appendix_table_a{number}_{NAMES[number]}.csv", index=False)


def add_variant(rows, raw, history, features, origin, imp, variant, models=MT, lookback=3,
                horizon=1, epochs=18, warm=None, shuffle=False, units=32, learning_rate=0.001, pfi=None, reuse=None):
    split = make_split(raw, history, features, origin, lookback, horizon)
    predictions, importance = fit_predict(
        split, features, models, 42 + 100 * origin + imp, epochs, pfi_repeats=10 if pfi is not None else 0,
        warm=warm, shuffle=shuffle, units=units, learning_rate=learning_rate, reuse=reuse
    )
    if pfi is not None:
        pfi.extend((origin, imp, *row) for row in importance if row[0] in POLICY)
    rows.extend(trace_predictions(split, predictions, origin, imp, lookback, horizon, variant))


def run_appendix(raw, histories, out, features):
    primary = pd.read_csv(out / "observed_target_eval_trace.csv")
    rows = []
    add = partial(add_variant, rows, reuse={})
    warm_models = {}
    state_root = checkpoint_directory(raw, histories, out)
    for origin in range(2005, 2024):
        stage = state_root / str(origin)
        if stage.is_dir():
            rows.extend(pd.read_csv(stage / "forecasts.csv").itertuples(index=False, name=None))
            warm_models = read_warm_state(stage / "warm.npz")
            print(f"appendix: restored {origin}", flush=True)
            continue
        row_start = len(rows)
        for imp, archived in enumerate(histories, 1):
            history = historical_slice(archived, origin)
            for lookback in [2, 4, 5]:
                add(raw, history, features, origin, imp, "lookback", lookback=lookback)
            for horizon in [2, 3]:
                if origin + horizon - 1 <= 2023:
                    add(raw, history, features, origin, imp, "horizon", models=GRU, horizon=horizon)
            add(raw, history, features, origin, imp, "warm", models=GRU,
                        warm=warm_models.setdefault(imp, {}), epochs=18 if origin == 2005 else 8)
            if imp != 1:
                continue
            observed = raw.loc[raw.index.get_level_values(1) < origin, features + TARGETS]
            add(raw, observed, features, origin, imp, "complete_case", models=GRU)
            if (origin - 2005) % 3 == 0:
                for units in [24, 32]:
                    for rate in [0.001, 0.003]:
                        add(raw, history, features, origin, imp, f"grid_{units}_{rate}",
                                    epochs=10, units=units, learning_rate=rate)
                for sign in [-1, 1]:
                    shifted = history.copy()
                    for target in TARGETS:
                        aligned = raw[target].reindex(shifted.index)
                        missing = aligned.isna()
                        shifted.loc[missing, target] += sign * 0.25 * aligned.std()
                        if target == "co2_emissions":
                            shifted[target] = shifted[target].clip(lower=0)
                    add(raw, shifted, features, origin, imp, f"mnar_{sign:+d}")
            if origin in SHORT_ORIGINS:
                add(raw, history, features, origin, imp, "ablation_reference", models=GRU, epochs=5)
                add(raw, history, features, origin, imp, "ablation_shuffled_gdp", epochs=5, shuffle=True)
                add(raw, history, [c for c in features if c not in POLICY], origin, imp,
                    "ablation_without_policy", epochs=5)
        with tempfile.TemporaryDirectory(dir=state_root) as tmp:
            pending = Path(tmp) / "complete"
            pending.mkdir()
            pd.DataFrame(rows[row_start:], columns=TRACE_COLUMNS).to_csv(pending / "forecasts.csv", index=False)
            write_warm_state(warm_models, pending / "warm.npz")
            pending.rename(stage)
        print(f"appendix: completed {origin}", flush=True)
    extra = pd.DataFrame(rows, columns=TRACE_COLUMNS)
    extra.to_csv(out / "appendix_forecast_trace.csv", index=False)
    report_appendix(raw, primary, extra, out)


def checkpoint_directory(raw, histories, out):
    fingerprint = hashlib.sha256(pd.util.hash_pandas_object(raw, index=True).values.tobytes())
    for history in histories:
        fingerprint.update(pd.util.hash_pandas_object(history, index=True).values.tobytes())
    fingerprint.update(Path(__file__).read_bytes())
    fingerprint.update(Path(__file__).with_name("replicate.py").read_bytes())
    fingerprint.update((out / "observed_target_eval_trace.csv").read_bytes())
    directory = out / ".appendix_checkpoints" / fingerprint.hexdigest()[:16]
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def write_warm_state(warm_models, path):
    arrays = {}
    for imp, models in warm_models.items():
        for (model_name, task), model in models.items():
            for label, variables in [("model", model.variables), ("optimizer", model.optimizer.variables)]:
                for i, variable in enumerate(variables):
                    arrays[f"{imp}/{model_name}/{task}/{label}/{i:03}"] = variable.numpy()
    np.savez_compressed(path, **arrays)


def read_warm_state(path):
    warm_models = {}
    with np.load(path, allow_pickle=False) as saved:
        for name in sorted(saved.files):
            imp, model, task, label, _ = name.split("/")
            task = None if task == "None" else int(task)
            weights, optimizer = warm_models.setdefault(int(imp), {}).setdefault((model, task), ([], []))
            (weights if label == "model" else optimizer).append(saved[name])
    return warm_models


def report_appendix(raw, primary, extra, out):
    save(raw.reset_index()[["Country Code", "Country Name"]].drop_duplicates(), out, 1)
    keys = ["target", "model", "origin", "imputation", "country"]
    complete = extra.loc[extra.variant.eq("complete_case") & extra.used_for_metric]
    matched = primary.merge(complete[keys], on=keys).assign(variant="imputed_on_complete_case_sample")
    variants = pd.concat([primary, extra, matched], ignore_index=True)
    folds = score_trace(variants, ["variant", "target", "model", "lookback", "horizon", "origin", "imputation"])
    metrics = ["RMSE", "MAE", "nRMSE", "Bias", "DA"]
    summary = folds.groupby(["variant", "target", "model", "lookback", "horizon"])[metrics].mean().reset_index()
    coverage = variants.loc[variants.used_for_metric].groupby(
        ["variant", "target", "model", "lookback", "horizon"]
    ).agg(scored_rows=("country", "size"), countries=("country", "nunique"),
          origins=("origin", "nunique"), imputations=("imputation", "nunique")).reset_index()
    summary = summary.merge(coverage, on=["variant", "target", "model", "lookback", "horizon"])
    save(summary.loc[summary.variant.isin(["complete_case", "imputed_on_complete_case_sample"])], out, 2)
    save(summary.loc[summary.model.isin(GRU) & summary.variant.isin(["warm", "primary"])], out, 3)
    save(summary.loc[summary.model.isin(GRU) & summary.variant.isin(["horizon", "primary"])], out, 4)

    main = folds.loc[folds.variant.eq("primary")]
    pooled = main.groupby(["target", "model", "imputation"]).RMSE.agg(["mean", "var", "size"])
    pooled["within_mean_variance"] = pooled["var"] / pooled["size"]
    variance = pooled.groupby(level=[0, 1]).agg(
        rmse=("mean", "mean"), within_imputation_variance=("within_mean_variance", "mean"),
        between_imputation_variance=("mean", "var"), imputations=("mean", "size"),
    ).reset_index()
    variance["total_variance"] = variance.within_imputation_variance + (
        1 + 1 / variance.imputations
    ) * variance.between_imputation_variance
    save(variance, out, 5)

    save(summary.loc[summary.model.eq("MT-GRU") & summary.variant.isin(["lookback", "primary"])], out, 6)
    save(summary.loc[summary.variant.str.startswith("grid_")], out, 7)
    save(classical_diagnostic(raw), out, 8)
    save(missingness_diagnostic(raw), out, 9)
    local_main = main.loc[main.imputation.eq(1) & main.origin.sub(2005).mod(3).eq(0) & main.model.eq("MT-GRU")]
    base = local_main.groupby(["target", "model"])[metrics].mean().reset_index().assign(variant="mnar_baseline")
    save(pd.concat([base, summary.loc[summary.variant.str.startswith("mnar_")]], ignore_index=True), out, 10)

    pooled_rows = score_trace(primary, ["target", "model", "imputation"])
    pooled_rows["rmse_rank"] = pooled_rows.groupby(["target", "imputation"]).RMSE.rank(method="min")
    pooled_rows = pooled_rows.merge(
        main.groupby(["target", "model"]).RMSE.mean().rename("headline_mean_fold_rmse").reset_index(),
        on=["target", "model"],
    )
    save(pooled_rows, out, 11)
    save(prediction_intervals(primary), out, 12)
    ablations = summary.loc[summary.variant.str.startswith("ablation_")]
    mapping = ablations[["variant", "model", "imputations", "origins"]].drop_duplicates().copy()
    mapping["reference"] = "ablation_reference"
    save(mapping, out, 13)
    save(ablations, out, 14)


def missingness_diagnostic(raw):
    rows = []
    for variable in FEATURES + TARGETS:
        missing = raw[variable].isna()
        counts = pd.crosstab(raw.index.get_level_values(0), missing)
        country_p = chi2_contingency(counts, correction=False).pvalue if counts.shape[1] == 2 else np.nan
        covariates = {}
        for other in FEATURES + TARGETS:
            if other == variable:
                continue
            x, y = raw.loc[missing, other].dropna(), raw.loc[~missing, other].dropna()
            if len(x) >= 5 and len(y) >= 5:
                covariates[other] = mannwhitneyu(x, y, alternative="two-sided").pvalue
        strongest = min(covariates, key=covariates.get) if covariates else None
        omnibus = combine_pvalues(list(covariates.values())).pvalue if covariates else np.nan
        rows.append((variable, 100 * missing.mean(), country_p, omnibus, strongest,
                     covariates.get(strongest, np.nan)))
    return pd.DataFrame(rows, columns=["variable", "missing_percent", "country_association_p",
                                       "fisher_descriptive_p", "strongest_covariate", "covariate_p"])


def prediction_intervals(primary):
    rows = []
    predictions = primary.loc[primary.used_for_metric].groupby(
        ["target", "model", "origin", "country"], as_index=False
    ).agg(actual=("actual", "first"), prediction=("prediction", "mean"))
    predictions["residual"] = predictions.actual - predictions.prediction
    for (target, model), group in predictions.groupby(["target", "model"]):
        for nominal in [0.8, 0.95]:
            hits, widths = [], []
            for origin, evaluation in group.groupby("origin"):
                previous = group.loc[group.origin.lt(origin), "residual"]
                if len(previous) < 30:
                    continue
                alpha = (1 - nominal) / 2
                lo, hi = previous.quantile([alpha, 1 - alpha])
                hits.extend(evaluation.residual.between(lo, hi))
                widths.extend([hi - lo] * len(evaluation))
            rows.append((target, model, nominal, np.mean(hits), np.mean(widths), len(hits)))
    return pd.DataFrame(rows, columns=["target", "model", "nominal_coverage", "empirical_coverage",
                                       "mean_width", "scored_rows"])


def classical_diagnostic(raw):
    from statsmodels.tsa.api import VAR
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.statespace.dynamic_factor import DynamicFactor
    from statsmodels.tsa.statespace.structural import UnobservedComponents

    exog = ["energy_use_pc", "renewable_share"]
    fully_observed = raw[TARGETS].notna().groupby(level=0).all().all(axis=1)
    countries = sorted(fully_observed[fully_observed].index)[:4]
    rows = []
    for origin in range(2005, 2024):
        for target in TARGETS:
            for name in ["ARIMA", "ARIMAX", "VAR", "DFM", "StateSpace_UCM"]:
                errors = []
                for country in countries:
                    frame = raw.loc[country].sort_index()
                    past = frame.loc[frame.index < origin]
                    truth = frame.at[origin, target]
                    try:
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            if name == "ARIMA":
                                pred = ARIMA(past[target].to_numpy(), order=(1, 1, 0)).fit().forecast()[0]
                            elif name == "ARIMAX":
                                joined = pd.concat([past[target], past[exog].shift()], axis=1).dropna()
                                next_exog = past[exog].iloc[[-1]].to_numpy()
                                if len(joined) < 12 or not np.isfinite(next_exog).all():
                                    continue
                                pred = ARIMA(joined[target].to_numpy(), exog=joined[exog].to_numpy(),
                                             order=(1, 0, 0)).fit().forecast(
                                    exog=next_exog)[0]
                            elif name == "VAR":
                                data = past[TARGETS].to_numpy()
                                pred = VAR(data).fit(maxlags=1).forecast(data[-1:], steps=1)[0, TARGETS.index(target)]
                            elif name == "DFM":
                                pred = DynamicFactor(past[TARGETS].to_numpy(), k_factors=1, factor_order=1).fit(
                                    disp=False, maxiter=100).forecast()[0, TARGETS.index(target)]
                            else:
                                pred = UnobservedComponents(past[target].to_numpy(), level="local linear trend").fit(
                                    disp=False).forecast()[0]
                        if np.isfinite(pred):
                            errors.append((truth - pred) ** 2)
                    except (ValueError, np.linalg.LinAlgError, IndexError, RuntimeError):
                        continue
                rows.append((name, target, origin, ",".join(countries), len(errors),
                             np.sqrt(np.mean(errors)) if errors else np.nan, len(errors) >= 10))
    return pd.DataFrame(rows, columns=["model", "target", "origin", "country_scope", "scored_rows", "rmse",
                                       "meets_minimum_10_observations"])
