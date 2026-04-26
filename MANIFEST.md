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
| config_public_reproducibility.yaml | code/ | Public | Public reproducibility configuration | No | Does not include restricted inputs. |
| public_preprocessing_entrypoint.py | code/ | Public | Public-source preprocessing entrypoint | No | Documents public preprocessing mode. |
| requirements.txt | code/ | Public | Python requirements | No | For reproducibility environment. |
| wdi_macro_energy_raw_1990_2023.xlsx | public_data/ | Public | Raw WDI macro/energy component | Yes | Public-source data component. |
| wdi_macro_energy_clean_1990_2023.xlsx | public_data/ | Public | Clean WDI macro/energy component | Yes | Public-source data component. |
| wdi_macro_energy_metadata_1990_2023.xlsx | public_data/ | Public | WDI metadata | Yes | Public-source metadata. |
| table5_co2_model_performance.csv | public_outputs/ | Public aggregate output | CO2 model performance table | Yes | Aggregate output only. |
| table6_gdp_model_performance.csv | public_outputs/ | Public aggregate output | GDP model performance table | Yes | Aggregate output only. |
| table7_permutation_feature_importance.csv | public_outputs/ | Public aggregate output | PFI table | Yes | Aggregate output only. |
| appendix_classical_benchmark_full.csv | public_outputs/ | Public aggregate output | Full classical benchmark diagnostics | Yes | Aggregate diagnostics only. |
| appendix_table_a1_warm_start_from_scratch.csv | public_outputs/ | Public aggregate output | Appendix A1 warm-start vs from-scratch diagnostics | Yes | Aggregate diagnostics only. |
| appendix_table_a2_multistep_no_imputation.csv | public_outputs/ | Public aggregate output | Appendix A2 multi-step and no-imputation diagnostics | Yes | Aggregate diagnostics only. |
| appendix_table_a3_classical_benchmark_diagnostics.csv | public_outputs/ | Public aggregate output | Appendix A3 classical benchmark diagnostics | Yes | Aggregate diagnostics only. |
| appendix_table_a4_hyperparameter_sensitivity.csv | public_outputs/ | Public aggregate output | Appendix A4 hyperparameter sensitivity diagnostics | Yes | Aggregate diagnostics only. |
| appendix_table_a5_imputation_variance_summary.csv | public_outputs/ | Public aggregate output | Appendix A5 imputation-variance diagnostics | Yes | Aggregate diagnostics only; no row-level ICAP-derived data. |
| figure1_missing_values_heatmap.png | public_outputs/ | Public figure output | Figure 1 missing-values heatmap | Yes | Manuscript figure asset. |
| figure2_co2_mtgru_error_metrics.png | public_outputs/ | Public figure output | Figure 2 CO2 MT-GRU error metrics | Yes | Manuscript figure asset. |
| figure3_gdp_mtgru_error_metrics.png | public_outputs/ | Public figure output | Figure 3 GDP MT-GRU error metrics | Yes | Manuscript figure asset. |
| appendix_figure_a1_missingness_correlation_matrix.png | public_outputs/ | Public figure output | Appendix Figure A1 missingness correlation matrix | Yes | Manuscript appendix figure asset. |
| appendix_figure_a2_missingness_country_pattern.png | public_outputs/ | Public figure output | Appendix Figure A2 missingness country pattern | Yes | Manuscript appendix figure asset. |
