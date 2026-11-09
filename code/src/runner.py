"""Execute and persist fold-level outputs."""
import numpy as np
import pandas as pd

from .replicate import (
    FEATURES, MODELS, TARGETS, TRACE_COLUMNS, fit_predict, historical_slice, load_histories,
    load_panel, make_split, score_trace, trace_predictions,
)


def run(panel, imputed, out, mode):
    raw = load_panel(panel)
    histories = load_histories(raw, imputed)
    out.mkdir(parents=True, exist_ok=True)
    smoke = mode == "smoke"
    origins = [2005, 2014, 2023] if smoke else list(range(2005, 2024))
    imputations = 1 if smoke else 5
    models = MODELS
    features = FEATURES
    if mode == "appendix":
        from .appendix import run_appendix
        run_appendix(raw, histories, out, features)
        return
    trace, pfi, inventory = [], [], []
    for origin in origins:
        for imp, archived in enumerate(histories[:imputations], 1):
            history = historical_slice(archived, origin)
            split = make_split(raw, history, features, origin)
            seed = 42 + 100 * origin + imp
            predictions, importance = fit_predict(split, features, models, seed, 18, 0 if smoke else 10)
            trace.extend(trace_predictions(split, predictions, origin, imp, 3, 1, "primary"))
            pfi.extend((origin, imp, *row) for row in importance)
            countries, _, targets, _, _, _, valid_inputs, _ = split
            for j, target in enumerate(TARGETS):
                eligible = valid_inputs & np.isfinite(targets[:, :, j])
                inventory.append((origin, imp, "V3 archive", origin - 1, target,
                                  int(eligible.any(axis=1).sum()), int(eligible.sum()),
                                  ",".join(countries[~eligible.any(axis=1)])))
        print(f"{mode}: completed {origin}", flush=True)
    trace = pd.DataFrame(trace, columns=TRACE_COLUMNS)
    verify_common_sample(trace, models, origins, imputations)
    trace.to_csv(out / "observed_target_eval_trace.csv", index=False)
    pd.DataFrame(inventory, columns=["origin", "imputation", "imputation_source", "history_max_year",
                                    "target", "training_countries", "training_rows", "excluded_countries"]).to_csv(
        out / "training_inventory.csv", index=False
    )
    write_headlines(trace, out)
    if pfi:
        importance = pd.DataFrame(pfi, columns=["origin", "imputation", "feature", "target",
                                                "base_sse", "permuted_sse", "observations"])
        importance.to_csv(out / "pfi_fold_details.csv", index=False)
        total = importance.groupby(["feature", "target"])[["base_sse", "permuted_sse", "observations"]].sum()
        total["pfi_percent"] = 100 * (total.permuted_sse - total.base_sse) / total.base_sse.replace(0, np.nan)
        total.reset_index().pivot(index="feature", columns="target", values="pfi_percent").add_prefix("pfi_").to_csv(
            out / "table7_permutation_feature_importance.csv"
        )


def verify_common_sample(trace, models, origins, imputations):
    used = trace.loc[trace.used_for_metric]
    keys = ["target", "origin", "imputation", "country"]
    counts = used.groupby(keys)["model"].nunique()
    if not counts.eq(len(models)).all() or used.duplicated(keys + ["model"]).any():
        raise ValueError("Models differ in scored country-years or contain duplicate forecasts")
    for target in TARGETS:
        rows = used.loc[used.target.eq(target)]
        if set(rows.origin) != set(origins) or len(rows.groupby(["origin", "imputation"])) != len(origins) * imputations:
            raise ValueError(f"{target}: incomplete origin/imputation coverage")
        samples = rows.groupby(["origin", "imputation"]).country.agg(frozenset)
        if samples.groupby(level=0).nunique().ne(1).any():
            raise ValueError(f"{target}: scored sample varies across imputations")


def write_headlines(trace, out):
    folds = score_trace(trace, ["target", "model", "origin", "imputation"])
    folds.to_csv(out / "fold_metrics.csv", index=False)
    from .replicate import METRICS
    summary = folds.groupby(["target", "model"])[METRICS].mean()
    for target, filename in zip(TARGETS, ["table5_co2_model_performance.csv", "table6_gdp_model_performance.csv"]):
        summary.loc[target].rename_axis("Model").to_csv(out / filename)
