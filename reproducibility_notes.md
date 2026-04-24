# Reproducibility Notes

## 1. Data construction overview
The analysis combines public macroeconomic and energy indicators with restricted policy-status information.

## 2. Public-source preprocessing
Public mode documents and preprocesses WDI/World Bank-derived inputs where redistribution is permitted.

## 3. Restricted-source policy variables
ICAP-derived policy variables are not redistributed publicly. These variables enter the full analysis through the restricted analysis panel.

## 4. Multiple imputation
The full analysis uses multiple imputation on the merged analysis panel. Imputed panels containing ICAP-derived values are restricted.

## 5. Expanding-window validation
Forecast evaluation follows the manuscript's expanding-window validation protocol.

## 6. Model training
Full model training requires restricted policy variables and is available only in internal/reviewer reproduction mode.

## 7. Benchmark models
Benchmark outputs are provided where available as aggregate manuscript outputs.

## 8. Classical benchmark diagnostics
Classical ARIMA/ARIMAX/VAR/DFM/UCM diagnostics are documented in Appendix Table A3 and the full diagnostic CSV.

## 9. Known limitations of public reproduction
The public package does not fully reproduce restricted policy-variable results because ICAP-derived materials are not publicly redistributed.

## 10. Full reviewer reproduction
Full reviewer reproduction uses the confidential restricted package supplied for peer-review purposes.
