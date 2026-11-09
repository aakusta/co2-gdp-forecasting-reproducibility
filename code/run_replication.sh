#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python_bin="${PYTHON_BIN:-python3}"
data="$root/public_data"
run="$root/replication_run"
out="$run/outputs"
if [[ -n "${C40_OPENMP_DIR:-}" ]]; then
  export DYLD_LIBRARY_PATH="$C40_OPENMP_DIR${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"
fi
cd "$root/code"
mkdir -p "$out"
panel="$data/analysis_panel_pre_imputation_1990_2023.csv"
"$python_bin" reproduce_v3_policy.py --merged-wdi "$data/wdi_macro_energy_clean_1990_2023.xlsx" \
  --inventory "$data/policy_source_inventory_2024.csv" --v3-panel "$panel" \
  --out "$out/policy_country_year_v3_reproduced.csv"
common=(--panel "$panel" --imputed "$data"/analysis_panel_imputed_m{1,2,3,4,5}_1990_2023.csv)
if [[ "${1:-all}" == smoke ]]; then
  "$python_bin" -m src.replicate "${common[@]}" --out "$out/smoke" --mode smoke
  "$python_bin" verify_trace.py "$out/smoke" --out "$out/smoke/trace_rmse_audit.csv"
else
  "$python_bin" -m src.replicate "${common[@]}" --out "$out" --mode primary
  "$python_bin" verify_trace.py "$out" --out "$out/trace_rmse_audit.csv"
  "$python_bin" -m src.replicate "${common[@]}" --out "$out" --mode appendix
  "$python_bin" make_figures.py --panel "$panel" --out "$out" --figures "$run/generated_figures"
fi
