# Reproduction of the original V3 policy indicators

The V3 analysis used three indicators derived from the `Type` and `Status` fields in the archived workbook that joined World Development Indicators with policy metadata. The archived `World_Development_Indicators (1).xlsx` is byte-identical to `wdi_macro_energy_clean_1990_2023.xlsx` in the V3 confidential submission.

The script selects the first nonblank `Type` and `Status` for each country code, independently and in worksheet order. It matches the selected pair and jurisdiction to the World Bank Carbon Pricing Dashboard inventory dated 1 April 2024 and records the instrument ID and the original worksheet row. The country-to-record selection is inherited from the archived joined workbook.

| V3 column | Reproduction rule |
|---|---|
| `ETS policy dummy` | 1 for a selected ETS record, including the regional EU ETS record. 0 for a selected carbon tax or undecided instrument. The value is fixed across years for each V3 unit. |
| `stage_underdev_dummy` | 1 from the year in “Under development since YYYY” or “Under consideration since YYYY”. 0 otherwise. |
| `stage_implemented_dummy` | 1 from the year in “Implemented in YYYY” or “Launched in YYYY”. 0 otherwise. |

For France, the selected record is `Tax_FR` (Dashboard worksheet row 32), with type `National Carbon tax` and status `Implemented in 2014`. The V3 type indicator is 0 throughout, while the implementation indicator moves from 0 to 1 in 2014. The EU aggregate has its own selected regional ETS record.

## Verify against the original Dashboard workbook

From the extracted V5 package root, with the pinned dependencies installed:

```sh
python code/reproduce_v3_policy.py \
  --merged-wdi public_data/wdi_macro_energy_clean_1990_2023.xlsx \
  --inventory public_data/world_bank_carbon_pricing_dashboard_2024-04-01.xlsx \
  --v3-panel public_data/analysis_panel_pre_imputation_1990_2023.csv \
  --out /tmp/c40-v5-policy-from-dashboard.csv
cmp /tmp/c40-v5-policy-from-dashboard.csv public_data/policy_country_year_v3_reproduced.csv
```

The workbook identifies its update date as 1 April 2024 on the `Compliance_Gen Info` sheet. The 128 source records and their worksheet row numbers match `public_data/policy_source_inventory_2024.csv`. Using either source produces the same audit CSV. The check covers 2,004 country-years and all 6,012 V3 indicator values, including the EU aggregate in the archived panel.

Both distributions include the joined WDI workbook used for this audit. The distribution copy retains its row order and Type and Status cells. Numeric observations for 12 unused series carrying separate IEA terms in the archived metadata were removed. The original workbook remains in the local source archive.
