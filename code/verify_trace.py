"""Recompute fold-average RMSE independently of the training implementation."""
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("directory", type=Path)
parser.add_argument("--legacy", action="store_true")
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
folds = defaultdict(list)
with (args.directory / "observed_target_eval_trace.csv").open() as f:
    for row in csv.DictReader(f):
        if row["used_for_metric"] != "True":
            continue
        if args.legacy:
            if any(row[k] != v for k, v in {
                "include_eu": "False", "warm_start": "False", "lookback": "3",
                "horizon": "1", "imputation_mode": "imputed",
            }.items()):
                continue
            origin, imp = row["origin_year"], row["imputation_id"]
            truth, pred = row["y_true"], row["y_pred"]
        else:
            origin, imp = row["origin"], row["imputation"]
            truth, pred = row["actual"], row["prediction"]
        folds[row["target"], row["model"], origin, imp].append((float(truth) - float(pred)) ** 2)

rmse = defaultdict(list)
origins = defaultdict(set)
for (target, model, origin, imp), errors in folds.items():
    rmse[target, model].append(math.sqrt(mean(errors)))
    origins[target, model].add(origin)
with args.out.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["target", "model", "origins", "fold_imputations", "trace_rmse", "table_rmse", "absolute_difference"])
    for target, filename in [
        ("co2_emissions", "table5_co2_model_performance.csv"),
        ("gdp_growth", "table6_gdp_model_performance.csv"),
    ]:
        with (args.directory / filename).open() as reported:
            for row in csv.DictReader(reported):
                key = (target, row["Model"])
                computed, saved = mean(rmse[key]), float(row["RMSE"])
                difference = abs(computed - saved)
                writer.writerow([*key, len(origins[key]), len(rmse[key]), computed, saved, difference])
                if difference > (5e-4 if args.legacy else 1e-8):
                    raise ValueError(f"{key}: trace RMSE does not match table")
