# Public Outputs Audit

| file | public_status | reason | action_taken |
|---|---|---|---|
| public_outputs/appendix_classical_benchmark_full.csv | keep_public | Contains aggregate benchmark diagnostics by model/target/fold year and reliability flags; no country-year rows or raw/imputed panel values. | Kept public. |
| public_outputs/appendix_hyperparameter_grid_full.csv | removed_from_public_package | Stale pre-correction hyperparameter grid (panel_v9_mi1, include_eu=True) inconsistent with final corrected chain. | Removed from public package. |
| public_outputs/table5_co2_model_performance.csv | keep_public | Contains aggregate model performance metrics; no country-year raw or imputed values. | Kept public. |
| public_outputs/table6_gdp_model_performance.csv | keep_public | Contains aggregate model performance metrics; no country-year raw or imputed values. | Kept public. |
| public_outputs/appendix_table_a1_warm_start_from_scratch.csv | keep_public | Contains aggregate warm-start versus from-scratch RMSE comparisons only. | Kept public. |
| public_outputs/appendix_table_a2_multistep_no_imputation.csv | keep_public | Contains aggregate multi-step and no-imputation diagnostics only; no country-year panel records. | Kept public. |
| public_outputs/appendix_table_a3_classical_benchmark_diagnostics.csv | keep_public | Contains aggregate diagnostic schema/header for classical benchmark appendix output; no row-level restricted panel data. | Kept public. |
| public_outputs/appendix_table_a4_hyperparameter_sensitivity.csv | keep_public | Contains aggregate hyperparameter sensitivity summary values only. | Kept public. |
| public_outputs/appendix_table_a5_imputation_variance_summary.csv | keep_public | Contains aggregate imputation-variance diagnostics only (metric-level pooled/within/between/total variance summaries); no country/year or row-level ICAP-derived data. | Kept public. |
| public_outputs/appendix_table_a6_lookback_sensitivity.csv | keep_public | Contains aggregate MT-GRU lookback-sensitivity diagnostics only (target-level/lookup-level summary metrics) with no country-year rows or row-level ICAP-derived panel values. | Kept public. |
| public_outputs/table7_permutation_feature_importance.csv | keep_public | Contains aggregate manuscript-level PFI values only; no row-level restricted data. | Kept public. |
| public_outputs/figure1_missing_values_heatmap.png | keep_public | Figure output image; no extractable row-level panel table embedded in repository file format. | Kept public. |
| public_outputs/figure2_co2_mtgru_error_metrics.png | keep_public | Figure output image with aggregate metric visualization. | Kept public. |
| public_outputs/figure3_gdp_mtgru_error_metrics.png | keep_public | Figure output image with aggregate metric visualization. | Kept public. |
| public_outputs/appendix_figure_a1_missingness_correlation_matrix.png | keep_public | Figure output image for missingness correlation pattern. | Kept public. |
| public_outputs/appendix_figure_a2_missingness_country_pattern.png | keep_public | Figure output image for missingness country pattern. | Kept public. |

Public outputs are aggregate manuscript outputs only. No restricted ICAP-derived row-level files are included.
