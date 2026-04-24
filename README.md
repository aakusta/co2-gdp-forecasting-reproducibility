# Reproducibility Package for “Forecasting CO2 Emissions and Economic Growth with Multitask Neural Networks and Expanding-Window Validation”

## Overview
This repository contains public data components, code, variable definitions, and reproducibility documentation for the manuscript.

## What is included
- Public WDI/World Bank-derived data components where redistribution appears permissible.
- Code and configuration notes for public-source preprocessing.
- Variable dictionary and source notes.
- Output mapping and reproducibility notes.
- Restricted data notice explaining non-public ICAP-derived materials.

## What is not included
- ICAP-derived raw data are not publicly redistributed.
- ICAP-derived cleaned, merged, and imputed files are not publicly redistributed.
- Full reproduction of policy-variable results requires access to ICAP-derived materials.
- Restricted ICAP-derived files were made available to the editor and reviewers for confidential peer-review purposes.

## Data sources
The analysis uses World Development Indicators / World Bank macroeconomic and energy data, World Bank carbon-pricing public material where applicable, and ICAP ETS/policy source material subject to access and redistribution restrictions.

## Reproducibility modes
Public reproducibility mode reproduces public-source preprocessing and documents the pipeline. Internal/reviewer mode reproduces full results using restricted ICAP-derived files.

## How to run
1. Install requirements from `code/requirements.txt` where applicable.
2. Use `code/config_public_reproducibility.yaml` for public-source preprocessing documentation.
3. Use the internal/reviewer configuration only if restricted ICAP-derived data are available under appropriate access terms.

## Citation / manuscript
Manuscript: “Forecasting CO2 Emissions and Economic Growth with Multitask Neural Networks and Expanding-Window Validation”.

## Contact / notes
This package distinguishes public reproducibility from confidential full-review reproduction because some source materials are subject to third-party access restrictions.
