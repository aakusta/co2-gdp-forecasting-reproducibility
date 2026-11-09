# Replication output locations

Both distributions use the same `public_data/` inputs and `code/` entry points. Newly generated files are written to `replication_run/`.

| Material | Public repository | Reviewer package | Produced by |
|---|---|---|---|
| Imputation inputs and archived completed panels | `public_data/` | `public_data/` | Archived input and separate MICE command |
| Country-year policy coding and source links | `public_data/policy_country_year_v3_reproduced.csv` | Same, and reference copy in `outputs/` | `code/reproduce_v3_policy.py` |
| Tables 5–7 and Appendix Tables A1–A14 | `public_outputs/` | `outputs/` | Primary and appendix modes |
| Forecast traces, fold metrics, training inventory, permutation details and trace audit | `public_traces/` | `outputs/` | Primary, appendix and trace verification commands |
| Figures 1–3 and Appendix Figures A1–A2 | `public_outputs/` | `generated_figures/` | `code/make_figures.py` |
