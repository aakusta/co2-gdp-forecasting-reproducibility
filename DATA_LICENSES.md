# Data sources and licenses

## World Development Indicators

Source: [World Bank, World Development Indicators](https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators), archived export reporting a database update of 15 April 2025. The accompanying `wdi_macro_energy_metadata_1990_2023.xlsx` retains the source and license notices for each series. The [World Bank data terms](https://data.worldbank.org/summary-terms-of-use) require attribution and preservation of indicator-specific conditions.

The nine WDI series in the study panels are marked [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) in the archived indicator metadata.

| Panel variable | WDI series | Data provider identified in the archive |
|---|---|---|
| `co2_emissions` | `EN.GHG.CO2.MT.CE.AR5` | EDGAR (European Commission JRC and IEA) |
| `gdp_growth` | `NY.GDP.MKTP.KD.ZG` | World Bank and OECD national accounts |
| `energy_use_pc` | `EG.USE.PCAP.KG.OE` | [IEA Energy Statistics Data Browser](https://www.iea.org/data-and-statistics/data-tools/energy-statistics-data-browser), CC BY 4.0 |
| `renewable_share` | `EG.FEC.RNEW.ZS` | WDI, with source attribution to IEA, IRENA, UNSD, World Bank, and WHO, *Tracking SDG 7: The Energy Progress Report* (2023) |
| `trade_gdp_lagged_1` | `NE.TRD.GNFS.ZS` | World Bank and OECD national accounts |
| `fdi_gdp_lagged_1` | `BX.KLT.DINV.WD.GD.ZS` | IMF, World Bank, and OECD |
| `inflation_lagged_1` | `FP.CPI.TOTL.ZG` | IMF International Financial Statistics |
| `unemployment_lagged_1` | `SL.UEM.TOTL.ZS` | ILO modelled estimates, ILOSTAT |
| `carbon_intensity` | `EN.GHG.CO2.RT.GDP.KD` | EDGAR (European Commission JRC and IEA) |

The WDI renewable-energy series carries its own CC BY 4.0 notice. The cited *Tracking SDG 7* report has a separate CC BY-NC 3.0 IGO license.

The distributed raw and joined WDI workbooks preserve the original row order, series labels and source notes. The authors removed numeric observations for 12 unused indicators whose archived metadata refers to separate IEA terms. The joined workbook retains the original `Type` and `Status` fields used to audit the policy coding.

## Carbon Pricing Dashboard

Source: [World Bank, Carbon Pricing Dashboard](https://datacatalog.worldbank.org/search/dataset/0042051/carbon-pricing-dashboard), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The archived workbook records the 1 April 2024 update on the `Compliance_Gen Info` sheet. The inventory CSV extracts columns A–E and retains the original worksheet row numbers. The authors derived three country-year indicators from the archived instrument type, stage, and year and provide the linked source records in the policy coding CSV.

## Author transformations and attribution

The analysis panel selects study series and country-years, lags trade, FDI, inflation, and unemployment by one year, and joins the derived policy indicators. The five archived completed panels contain author-imputed values as well as the original observations. Forecast traces and reported results are author calculations. Personal file-location metadata was removed from the distributed Excel copies without changing their analysis or Dashboard data.

When reusing the data, credit the World Bank datasets and original providers named in the metadata, link the applicable license, and indicate modifications. Cite this study for the derived coding and panels. The IEA-sourced open material is credited above and covered by the [IEA Notice for CC-licensed Content](https://www.iea.org/terms/creative-commons-cc-licenses).

This is a work derived by the study authors from IEA material and the study authors are solely liable and responsible for this derived work. The derived work is not endorsed by the IEA or its Member countries in any manner.

See `LICENSE` for the code and documentation notice.
