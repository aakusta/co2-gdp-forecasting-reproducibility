# Repository Manifest

| File | Folder | Public/Restricted/Internal | Purpose | Used in manuscript? | Notes |
|---|---|---|---|---|---|
| README.md | root | Public | Overview of data availability and reproducibility package | Yes | Explains public vs restricted materials. |
| data_sources.md | root | Public | Source-level data documentation | Yes | Describes WDI, World Bank, and ICAP sources. |
| variable_dictionary.csv | root | Public | Variable definitions and source status | Yes | Policy variables marked restricted. |
| restricted_data_notice.md | root | Public | Explains non-public ICAP-derived materials | Yes | Does not include restricted data. |
| reproducibility_notes.md | root | Public | Reproducibility workflow notes | Yes | Explains public and internal/reviewer modes. |
| output_mapping.md | root | Public | Maps manuscript tables/figures to output files | Yes | Links aggregate outputs to manuscript items. |
| public_outputs_audit.md | root | Public | Documents public-output safety audit | Yes | Confirms aggregate-output status. |
| repository_final_check_report.md | root | Public | Final repository audit report | Yes | Summarizes checks and remaining issues. |
| checksums.txt | root | Public | SHA256 checksums for repository files | No | Excludes .git and checksums.txt. |
| config_public_reproducibility.yaml | code/ | Public | Public reproducibility configuration documenting public-source mode and restricted-input limitations | No | Does not include restricted inputs or full model-training logic. |
| public_preprocessing_entrypoint.py | code/ | Public | Public-source preprocessing entry point / input-presence check | No | Not the full restricted-input model-training pipeline. |
| requirements.txt | code/ | Public | Python requirements | No | For reproducibility environment. |
| wdi_macro_energy_raw_1990_2023.xlsx | public_data/ | Public | Raw WDI macro/energy component | Yes | Public-source data component. |
| wdi_macro_energy_clean_1990_2023.xlsx | public_data/ | Public | Clean WDI macro/energy component | Yes | Public-source data component. |
| wdi_macro_energy_metadata_1990_2023.xlsx | public_data/ | Public | WDI metadata | Yes | Public-source metadata. |
| table5_co2_model_performance.csv | public_outputs/ | Public aggregate output | CO2 model performance table | Yes | Aggregate output only. |
| table6_gdp_model_performance.csv | public_outputs/ | Public aggregate output | GDP model performance table | Yes | Aggregate output only. |
| table7_permutation_feature_importance.csv | public_outputs/ | Public aggregate output | PFI table | Yes | Aggregate output only. |
| appendix_table_a1_country_list_58_national_units.csv | public_outputs/ | Public aggregate output | Appendix A1 58-country national sample list | Yes | Aggregate output only. |
| appendix_table_a2_no_imputation_robustness.csv | public_outputs/ | Public aggregate output | Appendix A2 no-imputation robustness diagnostics | Yes | Aggregate output only. |
| appendix_table_a3_warm_start_from_scratch.csv | public_outputs/ | Public aggregate output | Appendix A3 warm-start versus from-scratch diagnostics | Yes | Aggregate output only. |
| appendix_table_a4_multi_horizon_diagnostics.csv | public_outputs/ | Public aggregate output | Appendix A4 multi-horizon diagnostics | Yes | Aggregate output only. |
| appendix_table_a7_hyperparameter_sensitivity.csv | public_outputs/ | Public aggregate output | Appendix A7 hyperparameter-sensitivity diagnostics | Yes | Aggregate output only. |
| appendix_table_a8_classical_econometric_diagnostics.csv | public_outputs/ | Public aggregate output | Appendix A8 limited classical-econometric diagnostics | Yes | Aggregate output only. |
| figure2_cross_imputation_stability.png | public_outputs/ | Public figure output | Figure 2 cross-imputation stability diagnostic | Yes | Manuscript figure asset. |
| figure3_metric_normalized_model_comparison.png | public_outputs/ | Public figure output | Figure 3 metric-normalized model-comparison summary | Yes | Manuscript figure asset. |
| appendix_table_a5_imputation_variance_summary.csv | public_outputs/ | Public aggregate output | Appendix A5 imputation-variance diagnostics | Yes | Aggregate diagnostics only; no row-level ICAP-derived data. |
| appendix_table_a6_lookback_sensitivity.csv | public_outputs/ | Public aggregate output | Appendix A6 lookback-sensitivity diagnostics | Yes | Aggregate diagnostics only; primary specification remains lookback=3. |
| figure1_missing_values_heatmap.png | public_outputs/ | Public figure output | Figure 1 missing-values heatmap | Yes | Manuscript figure asset. |
| appendix_figure_a1_missingness_correlation_matrix.png | public_outputs/ | Public figure output | Appendix Figure A1 missingness correlation matrix | Yes | Manuscript appendix figure asset. |
| appendix_figure_a2_missingness_country_pattern.png | public_outputs/ | Public figure output | Appendix Figure A2 missingness country pattern | Yes | Manuscript appendix figure asset. |
