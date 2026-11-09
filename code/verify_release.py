"""Validate coverage, appendix pairing and manuscript assets in the V5 release."""
import argparse
import hashlib
from pathlib import Path

import pandas as pd

from src.replicate import FEATURES, MODELS, TARGETS
from src.runner import verify_common_sample


def verify(root):
    run = root / "replication_run"
    out = run / "outputs"
    for line in (root / "documentation/archive_imputation_sha256.txt").read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        assert hashlib.sha256((root / "public_data" / name).read_bytes()).hexdigest() == expected, name
    policy = pd.read_csv(out / "policy_country_year_v3_reproduced.csv")
    assert len(policy) == 2004
    trace = pd.read_csv(out / "observed_target_eval_trace.csv")
    verify_common_sample(trace, MODELS, range(2005, 2024), 5)
    scored = trace.loc[trace.used_for_metric]
    assert scored[["actual", "prediction"]].notna().all().all()
    assert scored.groupby("target").country.nunique().to_dict() == {"co2_emissions": 56, "gdp_growth": 58}
    inventory = pd.read_csv(out / "training_inventory.csv").fillna("")
    assert all({"LIE", "MNE"} <= set(c.split(",")) for c in inventory.loc[
        inventory.target.eq("co2_emissions"), "excluded_countries"])
    assert not any({"LIE", "MNE"} & set(c.split(",")) for c in inventory.loc[
        inventory.target.eq("gdp_growth"), "excluded_countries"])
    pfi = pd.read_csv(out / "pfi_fold_details.csv")
    assert set(pfi.feature) == set(FEATURES) and len(pfi) == 19 * 5 * len(FEATURES) * len(TARGETS)
    appendix = pd.read_csv(out / "appendix_forecast_trace.csv")
    keys = ["target", "origin", "imputation", "country"]
    def sample(frame):
        return set(frame.loc[frame.used_for_metric, keys].itertuples(index=False, name=None))

    main_mt = sample(trace.loc[trace.model.eq("MT-GRU")])
    for lookback in [2, 4, 5]:
        assert sample(appendix.loc[appendix.variant.eq("lookback") & appendix.lookback.eq(lookback)]) == main_mt
    variants = appendix.loc[appendix.variant.str.startswith("ablation_")]
    reference = sample(variants.loc[variants.variant.eq("ablation_reference") & variants.model.eq("MT-GRU")])
    assert set(variants.imputation) == {1} and set(variants.origin) == {2005, 2014, 2023}
    for variant, model in [("ablation_reference", "ST-GRU"), ("ablation_shuffled_gdp", "MT-GRU"),
                           ("ablation_without_policy", "MT-GRU")]:
        assert sample(variants.loc[variants.variant.eq(variant) & variants.model.eq(model)]) == reference
    for number in range(1, 15):
        assert len(list(out.glob(f"appendix_table_a{number}_*.csv"))) == 1
    assert {p.name for p in (run / "generated_figures").glob("*.png")} == {
        "figure1_missing_values_heatmap.png",
        "figure2_cross_imputation_stability.png",
        "figure3_metric_normalized_model_comparison.png",
        "appendix_figure_a1_missingness_correlation_matrix.png",
        "appendix_figure_a2_missingness_country_pattern.png",
    }
    print("Verified archival hashes, 19 origins × 5 panels, policy rows, target masks, PFI, A6 and A14 samples.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    verify(parser.parse_args().root)
