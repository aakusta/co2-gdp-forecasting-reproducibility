# Data Availability and Reproducibility Package for "Forecasting CO2 Emissions and Economic Growth with Multitask Neural Networks and Expanding-Window Validation"

## Overview

This repository provides public data components, public-source preprocessing entry points, configuration files, variable definitions, aggregate manuscript outputs, output mapping, checksums, and reproducibility documentation associated with the manuscript.

It is designed to support public reproducibility where redistribution is permitted, while clearly distinguishing restricted ICAP-derived materials that cannot be publicly shared. Full model reproduction, including policy-variable construction and headline model estimation, requires restricted ICAP-derived materials supplied separately for confidential peer review.

## What is included

- Public WDI/World Bank-derived data components where redistribution is permitted by the source terms.
- Public-source preprocessing entry points and configuration files; these do not constitute the full restricted-input model-training pipeline.
- Variable dictionary and source notes.
- Aggregate manuscript outputs where redistribution is appropriate.
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

Public reproducibility mode documents the public-source preprocessing workflow and provides aggregate manuscript outputs where redistribution is appropriate.

Internal/reviewer mode reproduces the full analysis using restricted ICAP-derived files supplied separately for confidential peer review.

Full reconstruction of the merged analysis panel, imputed panels, and policy-variable results requires restricted ICAP-derived materials.

## How to run

1. Install requirements from `code/requirements.txt`, where applicable.
2. Use `code/config_public_reproducibility.yaml` for public-source preprocessing documentation.
3. Use internal/reviewer reproduction materials only where restricted ICAP-derived data are available under appropriate access terms.

## Citation / manuscript

Manuscript: "Forecasting CO2 Emissions and Economic Growth with Multitask Neural Networks and Expanding-Window Validation".

## Contact / notes

This repository distinguishes public data availability and reproducibility support from confidential full-review reproduction because some source materials are subject to third-party access restrictions.
