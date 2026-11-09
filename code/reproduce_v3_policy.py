"""Reproduce and audit the historical V3 policy coding."""
import argparse
import csv
import re
import unicodedata
from pathlib import Path

from openpyxl import load_workbook


KEY = ("Country Code", "Year")
INDICATORS = ("ETS policy dummy", "stage_underdev_dummy", "stage_implemented_dummy")
ETS_TYPES = {"ETS", "National ETS", "Regional ETS", "Subnational ETS"}
OTHER_TYPES = {"National Carbon tax", "Subnational Carbon tax", "National Undecided"}
STATUS = re.compile(
    r"(Under development since|Under consideration since|Implemented in|Launched in) (\d{4})"
)
SOURCE = "World Bank Carbon Pricing Dashboard, 1 April 2024, Compliance_Gen Info"


def load_country_metadata(path):
    """Select the first nonblank Type and Status independently, in sheet order."""
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        rows = workbook["Data"].values
        headers = next(rows)
        code, name, kind, status = map(headers.index, ("Country Code", "Country Name", "Type", "Status"))
        countries = {}
        for row_number, row in enumerate(rows, 2):
            if not row[code]:
                continue
            entry = countries.setdefault(row[code], {"name": row[name]})
            for field, col in (("type", kind), ("status", status)):
                if row[col] not in (None, "") and field not in entry:
                    entry[field] = row[col]
                    entry[f"{field}_row"] = row_number
        return countries
    finally:
        workbook.close()


def name_key(name):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", name.casefold()))


def load_inventory(path):
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as source:
            return list(csv.DictReader(source))
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = workbook["Compliance_Gen Info"]
        rows = sheet.iter_rows(min_row=3, max_col=5, values_only=True)
        fields = ("record_id", "program", "type", "status", "jurisdiction")
        return [
            {**dict(zip(fields, row)), "source_row": str(number)}
            for number, row in enumerate(rows, 3) if row[0]
        ]
    finally:
        workbook.close()


def source_record(country, entry, inventory):
    jurisdiction = "EU" if country == "EUU" else entry["name"]
    matches = [
        row for row in inventory
        if row["type"] == entry["type"] and row["status"] == entry["status"]
        and row["jurisdiction"] and name_key(row["jurisdiction"]) == name_key(jurisdiction)
    ]
    identities = {(row["record_id"], row["program"]) for row in matches}
    if len(identities) != 1:
        raise ValueError(f"{country}: expected one Dashboard record, found {identities}")
    return matches[0], "|".join(str(row["source_row"]) for row in matches)


def reproduce(panel, metadata, inventory):
    country_codes = dict.fromkeys(row[KEY[0]] for row in panel)
    coding = {}
    for country in country_codes:
        entry = metadata[country]
        kind, status = entry.get("type"), entry.get("status")
        match = STATUS.fullmatch(status or "")
        if kind not in ETS_TYPES | OTHER_TYPES or match is None:
            raise ValueError(f"{country}: unsupported historical Type/Status: {kind!r}, {status!r}")
        stage, start = match.groups()
        source, source_rows = source_record(country, entry, inventory)
        coding[country] = (entry, kind, status, stage, int(start), source, source_rows)

    output = []
    keys = set()
    for row in panel:
        country, year = row[KEY[0]], int(row[KEY[1]])
        if (country, year) in keys:
            raise ValueError(f"Duplicate country-year: {country} {year}")
        keys.add((country, year))
        entry, kind, status, stage, start, source, source_rows = coding[country]
        values = (
            int(kind in ETS_TYPES),
            int(year >= start and stage.startswith("Under ")),
            int(year >= start and stage in {"Implemented in", "Launched in"}),
        )
        for column, actual in zip(INDICATORS, values):
            if actual != float(row[column]):
                raise ValueError(f"{country} {year} {column}: generated {actual}, V3 has {row[column]}")
        output.append({
            KEY[0]: country, KEY[1]: year, **dict(zip(INDICATORS, values)),
            "selected_type": kind, "selected_status": status, "status_start_year": start,
            "merged_wdi_type_row": entry["type_row"], "merged_wdi_status_row": entry["status_row"],
            "dashboard_record_id": source["record_id"], "dashboard_program": source["program"],
            "dashboard_sheet_rows": source_rows, "source": SOURCE,
        })
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--merged-wdi", type=Path, required=True, help="Archived WDI workbook with Type and Status")
    parser.add_argument("--inventory", type=Path, required=True, help="Original Dashboard XLSX or its transcribed CSV")
    parser.add_argument("--v3-panel", type=Path, required=True, help="Archived V3 pre-imputation CSV for keys and parity check")
    parser.add_argument("--out", type=Path, required=True, help="Output country-year audit CSV")
    args = parser.parse_args()
    with args.v3_panel.open(encoding="utf-8-sig", newline="") as source:
        panel = list(csv.DictReader(source))
    if not panel:
        raise ValueError("The V3 reference panel is empty.")
    rows = reproduce(panel, load_country_metadata(args.merged_wdi), load_inventory(args.inventory))
    with args.out.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Reproduced {len(rows):,} country-years and verified all {len(rows) * len(INDICATORS):,} V3 indicator values.")


if __name__ == "__main__":
    main()
