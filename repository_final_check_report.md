# Repository Final Check Report

## 1. Summary of fixes made

- Kept final public output filenames aligned with final revised manuscript numbering.
- Synchronized the public and reviewer-facing appendix-output semantics for A6, A7, A10, A11, and A13 without changing headline manuscript values.
- Updated public documentation for Tables 5-7, Appendix Tables A1-A14, and Figures 1-3 plus Appendix Figures A1-A2.
- Refreshed the public-output safety audit so it explicitly covers A9-A14 in addition to the previously released outputs.
- Regenerated checksums after the output-surface and documentation updates.

## 2. Public outputs audit result

Public outputs are aggregate metrics, aggregate diagnostics, or figure assets. No country-year restricted ICAP-derived row-level panel records are included.

## 3. Output mapping status

`output_mapping.md` maps Table 5, Table 6, Table 7, Appendix Tables A1-A14, and Figures 1-3 / Appendix Figures A1-A2 to the final public output filenames and their synchronized semantics.

## 4. README status

`README.md` states that the public repository provides public-source preprocessing/input-check entry points, aggregate outputs, and documentation, while full restricted-input reproduction remains confidential.

## 5. Restricted-data framing status

`restricted_data_notice.md` remains aligned with the public/restricted boundary: full reproduction involving restricted ICAP-derived inputs is available only in confidential reviewer materials.

## 6. Checksums status

`checksums.txt` was regenerated with one file per line, excluding `.git/`, `checksums.txt`, `__pycache__/`, `.venv/`, and `.DS_Store`.

## 7. Final parity status

- Final A1-A14 naming in `public_outputs/`: yes.
- Final Figure 1-3 and Appendix Figure A1-A2 naming in `public_outputs/`: yes.
- Public restricted-data leakage: no.
- A6/A7/A10/A11/A13 surface labels synchronized across public outputs and public docs: yes.
- Public-output safety audit updated through A14: yes.
- Remaining critical issues: 0.
- Remaining major issues: 0.
