"""Public-source preprocessing entry point.

This entry point is intentionally limited to public WDI/World Bank inputs. Full headline reproduction requires restricted ICAP-derived policy inputs supplied only for confidential review.
"""

from pathlib import Path

PUBLIC_DATA_DIR = Path(__file__).resolve().parents[1] / "public_data"


def main():
    required = [
        PUBLIC_DATA_DIR / "wdi_macro_energy_raw_1990_2023.xlsx",
        PUBLIC_DATA_DIR / "wdi_macro_energy_metadata_1990_2023.xlsx",
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(path)
    print("Public-source inputs are present. Full model reproduction requires restricted policy inputs.")


if __name__ == "__main__":
    main()
