# Repository Final Check Report

## 1. Summary of fixes made
- Audited all files under `public_outputs/` for potential restricted row-level data leakage.
- Added `public_outputs/table7_permutation_feature_importance.csv` using manuscript-level aggregate PFI values.
- Created `public_outputs_audit.md` with per-file public classification and actions.
- Cleaned `output_mapping.md` to remove local/internal path references and manual-missing notes, and aligned paths to `public_outputs/...`.
- Updated `code/config_public_reproducibility.yaml` paths to match repository structure.
- Strengthened `README.md` with explicit public vs restricted reproduction boundary text.
- Ran repository-wide leakage keyword scan and reviewed results.
- Regenerated `checksums.txt` after modifications.

## 2. Public outputs audit result
- Audit file: `public_outputs_audit.md`
- Result: audited files in `public_outputs/` are classified as aggregate manuscript outputs or figures and were kept public.
- No country-year analysis panel rows, raw/imputed panel records, or ICAP-derived row-level policy status tables were found in public outputs.

## 3. Table 7 PFI output status
- `public_outputs/table7_permutation_feature_importance.csv` was created.

## 4. output_mapping.md status
- Cleaned and updated.
- Internal/local path references were removed.
- Table 7 mapping now points to `public_outputs/table7_permutation_feature_importance.csv`.
- Appendix A3 now maps to both:
  - `public_outputs/appendix_table_a3_classical_benchmark_diagnostics.csv`
  - `public_outputs/appendix_classical_benchmark_full.csv`
- Added explicit note that full reconstruction involving policy variables requires restricted ICAP-derived inputs.

## 5. Public config path status
- `code/config_public_reproducibility.yaml` paths corrected to:
  - `../public_data`
  - `../public_outputs`
  - `../public_data/wdi_macro_energy_raw_1990_2023.xlsx`
  - `../public_data/wdi_macro_energy_metadata_1990_2023.xlsx`

## 6. README strengthening status
- README now explicitly states:
  - ICAP-derived raw data are not publicly redistributed.
  - ICAP-derived cleaned, merged, and imputed files are not publicly redistributed.
  - Full reproduction of policy-variable results requires ICAP-derived materials.
  - Restricted ICAP-derived files were made available to editor/reviewers for confidential peer review.
- Added paragraph clarifying public aggregate workflow vs confidential full-review reconstruction.

## 7. Restricted data leakage findings
- Keyword scan hits were found in:
  - `variable_dictionary.csv`
  - `code/config_public_reproducibility.yaml`
  - `public_outputs/table7_permutation_feature_importance.csv`
- These hits are expected documentation/config/aggregate-output references and do not constitute row-level restricted data leakage.
- No problematic public row-level restricted dataset was identified.

## 8. Checksums status
- `checksums.txt` regenerated using SHA256 for repository files (excluding `checksums.txt` itself).

## 9. Unresolved issues requiring manual review
- None identified from this targeted pass.

## 10. Final pre-submission cleanup (latest pass)
- README live update verified.
- checksums regenerated excluding `.git`, `checksums.txt`, `__pycache__`, `.venv`, and `.DS_Store`.
- `MANIFEST.md` and `data_sources.md` markdown table formatting verified/fixed (pipe-table format confirmed).
- `public_outputs/table5_co2_model_performance.csv` and `public_outputs/table6_gdp_model_performance.csv` public-output safety rechecked.

## 11. Final formatting and safety pass
- README rendered with proper Markdown section separation, lists, and heading structure.
- Markdown tables verified/fixed in `output_mapping.md`, `public_outputs_audit.md`, `data_sources.md`, and `MANIFEST.md` (pipe-table format with one row per line).
- `variable_dictionary.csv` parsed successfully as CSV after LF normalization and row/column validation.
- `code/config_public_reproducibility.yaml` parsed successfully as YAML after multi-line normalization.
- `checksums.txt` regenerated with one file per line and excludes `.git`, `checksums.txt`, `__pycache__`, `.venv`, and `.DS_Store`.
- `public_outputs/table5_co2_model_performance.csv`, `public_outputs/table6_gdp_model_performance.csv`, `public_outputs/appendix_classical_benchmark_full.csv`, and `public_outputs/appendix_hyperparameter_grid_full.csv` were rechecked for restricted row-level leakage.
- No restricted row-level data found in checked public outputs; files remain public.
