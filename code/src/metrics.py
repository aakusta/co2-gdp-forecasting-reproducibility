"""Forecast metrics in the original outcome units."""

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prev: np.ndarray) -> dict:
    eps = 1e-9
    err = y_true - y_pred
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    mae = float(mean_absolute_error(y_true, y_pred))
    mape = float(np.mean(np.abs(err / np.where(np.abs(y_true) < eps, eps, y_true))) * 100.0)
    nrmse = float(rmse / (np.mean(np.abs(y_true)) + eps))
    bias = float(np.mean(err))

    try:
        r2 = float(r2_score(y_true, y_pred))
    except Exception:
        r2 = float("nan")

    da = float(np.mean(np.sign(y_true - y_prev) == np.sign(y_pred - y_prev)))
    residual_variance = float(np.var(err, ddof=1)) if len(err) > 1 else float("nan")

    return {
        "RMSE": rmse,
        "MAE": mae,
        "MSE": mse,
        "MAPE": mape,
        "nRMSE": nrmse,
        "Bias": bias,
        "R2": r2,
        "DA": da,
        "residual_variance": residual_variance,
        "n_obs": int(len(y_true)),
    }
