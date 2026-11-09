# C40 forecasting replication

The public repository and the reviewer package provide the pre-imputation panel, the five archived completed panels used for the reported forecasts, the dated World Bank Carbon Pricing Dashboard workbook and source extract, country-year policy coding, analysis code, forecast traces, and reported outputs. See [Data sources and licenses](DATA_LICENSES.md) for source versions, attribution, and transformations.

## Run the reported analysis

Use Python 3.12 and install the pinned forecast dependencies.

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r code/requirements.txt
bash code/run_replication.sh
```

For a short test, run `bash code/run_replication.sh smoke`. It writes the short-run results and the trace-to-table check to `replication_run/outputs/smoke/`. The full run writes tables and traces to `replication_run/outputs/` and figures to `replication_run/generated_figures/`. After the full run, use `python code/verify_release.py .` to verify the archived panel hashes, evaluation coverage, appendix samples and figure count.

The run reads the five archived panels in numerical order. The script first reconstructs the three historical policy columns from the archived joined workbook and checks all values against the raw reference. The raw panel also supplies the country-year keys and observed targets. The release check verifies the five completed panels against the original submission's SHA-256 values in `documentation/archive_imputation_sha256.txt`.

The one-year forecast uses the three preceding annual input rows. The headline training sample expands through the year before each origin. GRU scalers are fitted separately for each country and origin using the training inputs and available target labels. The three binary policy inputs retain their original 0/1 values. GRU predictions are returned to the target's original units. Each headline GRU is freshly initialized using deterministic seeds with base 42. The V3 architecture, optimizer, learning rate, batch size, epoch limit and early stopping settings are preserved. Ridge, ElasticNet and Random Forest retain the V3 estimator settings. All seven headline models use 2005–2023 and the same observed target rows within an origin and imputation. Countries with no observed training target contribute no labels to the corresponding training loss.

The Dashboard source workbook is `public_data/world_bank_carbon_pricing_dashboard_2024-04-01.xlsx`. Its `Compliance_Gen Info` sheet gives 1 April 2024 as the update date and matches all 128 rows of the bundled inventory extract. See `documentation/V3_POLICY_REPRODUCTION.md` for the direct workbook verification command.

## Recreate the five archived MICE panels

Use a separate Python 3.11 environment. On macOS, LightGBM requires OpenMP. Set `DYLD_LIBRARY_PATH` to the directory containing `libomp.dylib` if needed.

```sh
python3.11 -m venv .venv-mice
. .venv-mice/bin/activate
python -m pip install -r code/requirements-mice.txt
OMP_NUM_THREADS=2 python code/impute_archival_panel.py \
  --panel public_data/analysis_panel_pre_imputation_1990_2023.xlsx \
  --out replication_run/mice_regenerated
```

The command follows the original notebook. It fits miceforest 5.7.0 with LightGBM 4.5.0 on the numeric columns of the workbook's `Panel` sheet, using five iterations, five datasets and seed 123. It checks that observed values are preserved and exports the 1990–2023 rows in the same format as the archived inputs. The verification results are in `documentation/mice_archive_comparison.txt`. The forecast command reads the supplied archived panels directly.

## Check the input sources

```sh
mkdir -p replication_run
python code/wdi_preprocess.py --raw public_data/wdi_macro_energy_raw_1990_2023.xlsx \
  --panel public_data/analysis_panel_pre_imputation_1990_2023.csv \
  --out replication_run/wdi_input_audit.csv
```

See [policy reconstruction](documentation/V3_POLICY_REPRODUCTION.md) for the dated source records and the command that reproduces the 6,012 policy indicator values. The supplied analysis panels are the inputs for the forecast run. The WDI command audits the mapped WDI series against those inputs.

## Output map

| Output | Generator |
|---|---|
| Historical policy coding and source rows | code/reproduce_v3_policy.py |
| Tables 5–6 and fold metrics | code/src/runner.py, primary mode |
| Table 7 and fold-level permutation errors | code/src/replicate.py and code/src/runner.py |
| Tables A1–A14 and appendix forecast trace | code/src/appendix.py |
| Figures 1–3 and Appendix Figures A1–A2 | code/make_figures.py |
| Independent trace-to-table RMSE audit | code/verify_trace.py |

Table 7 uses ten permutations per feature, origin and imputation. A feature's three-year history is permuted as a block across countries. PFI compares pooled squared errors in the original target units. A6 varies only the lookback. A14 uses the first imputation, forecast years 2005, 2014 and 2023 and a five-epoch cap for each reference and variant. The policy-omission row is a local ablation. For A11, RMSE is pooled within each imputation. Tables 5 and 6 average the origin-level RMSEs across the five imputations.

The public reference tables and figures are in `public_outputs/` and the forecast and validation records are in `public_traces/`. See [output locations](output_mapping.md) for both distributions.
