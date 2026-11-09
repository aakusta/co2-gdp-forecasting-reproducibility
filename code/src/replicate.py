"""Rolling-origin replication using the five archived imputations."""
import argparse
import os
from pathlib import Path

os.environ.setdefault("TF_NUM_INTEROP_THREADS", "2")
os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "2")
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet, Ridge
from sklearn.preprocessing import StandardScaler

from .metrics import compute_metrics
from .modeling import _set_seed, build_mt_gru_model, build_st_gru_model, require_tensorflow

TARGETS = ["co2_emissions", "gdp_growth"]
FEATURES = [
    "energy_use_pc", "renewable_share", "trade_gdp_lagged_1",
    "fdi_gdp_lagged_1", "inflation_lagged_1", "unemployment_lagged_1",
]
POLICY = ["ETS policy dummy", "stage_underdev_dummy", "stage_implemented_dummy"]
FEATURES += POLICY
MODELS = ["MT-GRU", "ST-GRU", "Ridge", "ElasticNet", "RandomForest", "LastValue", "MovingAverage3"]
METRICS = ["RMSE", "MAE", "MSE", "MAPE", "nRMSE", "Bias", "R2", "DA"]
KEY = ["Country Code", "Year"]


def load_panel(path):
    raw = pd.read_csv(path, dtype={"Country Code": str})
    raw = raw.loc[raw["Country Name"].ne("European Union") & raw.Year.between(1990, 2023)]
    return raw.set_index(KEY, verify_integrity=True).sort_index()


def load_histories(raw, paths):
    if len(paths) != 5:
        raise ValueError("Expected the five archived imputation panels")
    histories = []
    for path in paths:
        history = load_panel(path)
        if not history.index.equals(raw.index):
            raise ValueError(f"{path}: country-year keys differ from the archived raw panel")
        if not history[POLICY].equals(raw[POLICY]):
            raise ValueError(f"{path}: policy fields differ from the reproduced V3 coding")
        numeric = history[FEATURES + TARGETS]
        if numeric.isna().any().any():
            raise ValueError(f"{path}: incomplete archived model inputs")
        histories.append(numeric)
    return histories


def historical_slice(history, origin):
    return history.loc[history.index.get_level_values("Year") < origin]


def make_split(raw, history, features, origin, lookback=3, horizon=1):
    countries = sorted(raw.index.get_level_values(0).unique())
    historical = raw.loc[raw.index.get_level_values("Year") < origin, TARGETS]
    target_available = historical.notna().groupby(level=0).any().reindex(countries, fill_value=False)
    years = range(1990, origin)
    idx = pd.MultiIndex.from_product([countries, years], names=KEY)
    x = history[features].reindex(idx).to_numpy().reshape(len(countries), len(years), len(features))
    y = history[TARGETS].reindex(idx).to_numpy().reshape(len(countries), len(years), len(TARGETS))
    y = np.where(target_available.to_numpy()[:, None, :], y, np.nan)
    windows = range(lookback, len(years) - horizon + 1)
    x_train = np.stack([x[:, end - lookback:end, :] for end in windows], axis=1)
    y_train = np.stack([y[:, end + horizon - 1, :] for end in windows], axis=1)
    x_test = x[:, -lookback:, :]
    eligible = np.isfinite(x_test).all(axis=(1, 2))
    train_rows = np.isfinite(x_train).all(axis=(2, 3))
    target_year = origin + horizon - 1
    actual_idx = pd.MultiIndex.from_product([countries, [target_year]], names=KEY)
    actual = raw[TARGETS].reindex(actual_idx).to_numpy()
    return np.array(countries), x_train, y_train, x_test, actual, y[:, -3:, :], train_rows, eligible


def standardize(x, y, test, train_rows, features):
    x = x.copy()
    y = y.copy()
    test = test.copy()
    y_center = np.zeros((len(x), y.shape[-1]))
    y_scale = np.ones_like(y_center)
    for i, (inputs, targets, rows) in enumerate(zip(x, y, train_rows)):
        if rows.any():
            scaler = StandardScaler().fit(inputs[rows].reshape(-1, len(features)))
            for col in POLICY:
                if col in features:
                    k = features.index(col)
                    scaler.mean_[k], scaler.scale_[k] = 0, 1
            x[i] = scaler.transform(inputs.reshape(-1, len(features))).reshape(inputs.shape)
            test[i] = scaler.transform(test[i])
        for j in range(y.shape[-1]):
            observed = rows & np.isfinite(targets[:, j])
            if observed.any():
                scaler_y = StandardScaler().fit(targets[observed, j, None])
                y_center[i, j], y_scale[i, j] = scaler_y.mean_[0], scaler_y.scale_[0]
                y[i, :, j] = (targets[:, j] - y_center[i, j]) / y_scale[i, j]
    return x, y, test, y_center, y_scale


def fit_predict(split, features, model_names, seed, epochs, pfi_repeats=0, warm=None, shuffle=False, units=32, learning_rate=0.001, reuse=None):
    countries, x, y, test, actual, previous, train_rows, eligible = split
    predicts = {}
    results_pfi = []
    if "LastValue" in model_names:
        predicts["LastValue"] = previous[:, -1, :]
    if "MovingAverage3" in model_names:
        predicts["MovingAverage3"] = np.mean(previous, axis=1)
    learners = {
        "Ridge": lambda: Ridge(alpha=1.0),
        "ElasticNet": lambda: ElasticNet(alpha=0.001, l1_ratio=0.5, random_state=42),
        "RandomForest": lambda: RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=2),
    }
    for name in model_names:
        if name not in learners:
            continue
        pred = np.full(actual.shape, np.nan)
        for j in range(len(TARGETS)):
            mask = train_rows & np.isfinite(y[:, :, j])
            train = x[mask].reshape(mask.sum(), -1)
            to_predict = test[eligible].reshape(eligible.sum(), -1)
            pred[eligible, j] = learners[name]().fit(train, y[:, :, j][mask]).predict(to_predict)
        predicts[name] = pred
    if not any(name in {"MT-GRU", "ST-GRU"} for name in model_names):
        return predicts, results_pfi
    tf = require_tensorflow()
    sx, sy, stest, center, scale = standardize(x, y, test, train_rows, features)
    nx = stest[eligible].astype("float32")
    lookback = x.shape[2]
    builders = {"MT-GRU": build_mt_gru_model, "ST-GRU": build_st_gru_model}
    for name in model_names:
        if name not in builders:
            continue
        pred = np.full(actual.shape, np.nan)
        tasks = [None] if name == "MT-GRU" else range(len(TARGETS))
        for task in tasks:
            _set_seed(tf, seed + (0 if task is None else task + 1))
            key = (name, task)
            saved_warm = warm.get(key) if warm is not None else None
            if saved_warm is None or isinstance(saved_warm, tuple):
                fresh = builders[name](tf, lookback, len(features), units, 16, 0.10, learning_rate)
                reuse_key = (name, task, lookback, len(features), units, learning_rate)
                if reuse is not None and warm is None and reuse_key in reuse:
                    model = reuse[reuse_key]
                    for var, initial in zip(model.variables, fresh.variables, strict=True):
                        var.assign(initial)
                    for var in model.optimizer.variables:
                        if var.name != "learning_rate":
                            var.assign(tf.zeros_like(var))
                else:
                    model = fresh
                    if reuse is not None and warm is None:
                        reuse[reuse_key] = model
                if task is None and model is fresh:
                    def masked_loss(truth, predicted):
                        finite = tf.math.is_finite(truth)
                        clean = tf.where(finite, truth, tf.zeros_like(truth))
                        errors = tf.where(finite, tf.square(clean - predicted), tf.zeros_like(predicted))
                        return tf.reduce_sum(errors, axis=-1) / tf.maximum(
                            tf.reduce_sum(tf.cast(finite, predicted.dtype), axis=-1), 1
                        )
                    model.compile(optimizer=model.optimizer, loss=masked_loss)
                if isinstance(saved_warm, tuple):
                    model.optimizer.build(model.trainable_variables)
                    for var, saved in zip(model.variables, saved_warm[0], strict=True):
                        var.assign(saved)
                    for var, saved in zip(model.optimizer.variables, saved_warm[1], strict=True):
                        var.assign(saved)
                if warm is not None:
                    warm[key] = model
            else:
                model = saved_warm
            targets = sy if task is None else sy[:, :, task:task + 1]
            mask = train_rows & np.isfinite(targets).any(axis=2)
            train_y = targets[mask].astype("float32")
            if shuffle and task is None:
                valid = np.isfinite(train_y[:, 1])
                train_y[valid, 1] = np.random.default_rng(seed).permutation(train_y[valid, 1])
            dataset = tf.data.Dataset.from_tensor_slices((sx[mask].astype("float32"), train_y))
            options = tf.data.Options()
            options.threading.private_threadpool_size = 2
            dataset = dataset.shuffle(len(train_y), seed=seed).batch(32).with_options(options)
            model.fit(dataset, epochs=epochs, verbose=0, callbacks=[
                tf.keras.callbacks.EarlyStopping(monitor="loss", patience=3, restore_best_weights=True)
            ])
            standardized = model(nx, training=False).numpy()
            if task is None:
                pred[eligible] = standardized * scale[eligible] + center[eligible]
                if pfi_repeats:
                    rng = np.random.default_rng(seed + 10000)
                    for k, feature in enumerate(features):
                        permuted = []
                        for _ in range(pfi_repeats):
                            altered = nx.copy()
                            altered[:, :, k] = nx[rng.permutation(len(nx)), :, k]
                            permuted.append(model(altered, training=False).numpy() * scale[eligible] + center[eligible])
                        for j, target in enumerate(TARGETS):
                            valid = np.isfinite(actual[eligible, j]) & np.isfinite(previous[eligible, -1, j])
                            truth = actual[eligible, j][valid]
                            base = np.square(pred[eligible, j][valid] - truth).sum()
                            perturb = np.mean([np.square(p[valid, j] - truth).sum() for p in permuted])
                            results_pfi.append((feature, target, base, perturb, len(truth)))
            else:
                pred[eligible, task] = standardized[:, 0] * scale[eligible, task] + center[eligible, task]
        predicts[name] = pred
    if warm is None and reuse is None:
        tf.keras.backend.clear_session()
    return predicts, results_pfi


def trace_predictions(split, predictions, origin, imp, lookback, horizon, variant):
    countries, _, _, _, actual, previous, _, eligible = split
    use = eligible[:, None] & np.isfinite(actual) & np.isfinite(previous[:, -1, :])
    for model, pred in predictions.items():
        if not np.isfinite(pred[use]).all():
            raise ValueError(f"{model}, {origin}: incomplete forecasts on common evaluation sample")
        for j, target in enumerate(TARGETS):
            for i, country in enumerate(countries):
                yield (variant, model, target, imp, origin, origin + horizon - 1, country,
                       lookback, horizon, np.isfinite(actual[i, j]), use[i, j], actual[i, j],
                       pred[i, j], previous[i, -1, j])


TRACE_COLUMNS = ["variant", "model", "target", "imputation", "origin", "target_year", "country",
                 "lookback", "horizon", "target_observed", "used_for_metric", "actual", "prediction", "previous"]


def score_trace(trace, keys):
    rows = []
    for group, frame in trace.loc[trace.used_for_metric].groupby(keys, sort=True):
        values = compute_metrics(*(frame[c].to_numpy() for c in ["actual", "prediction", "previous"]))
        values["DA"] *= 100
        rows.append(dict(zip(keys, group), **values))
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--mode", choices=["smoke", "primary", "appendix"], required=True)
    parser.add_argument("--imputed", type=Path, nargs=5, required=True)
    args = parser.parse_args()
    from .runner import run
    run(args.panel, args.imputed, args.out, args.mode)


if __name__ == "__main__":
    main()
