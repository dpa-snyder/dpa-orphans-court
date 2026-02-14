#!/usr/bin/env python3
"""
DPA Orphans Court → ArchivERA Migration Script

Transforms Access database exports (Adults + Children + Containers CSVs)
into ArchivERA-ready import CSVs.

Usage:
    python migrate.py
    python migrate.py --adults "NCC Adults.csv" --children "NCCChildren.csv" \
                      --containers "NCC Orphans Court Containers.csv" --output "output.csv"
"""

import argparse
import csv
import os
import re
import sys
from bisect import bisect_right


# ---------------------------------------------------------------------------
# Column mapping config — edit these if source CSV column names differ
# ---------------------------------------------------------------------------

ADULT_COLUMNS = {
    "record_id": "Record_ID",
    "rg": "RG",
    "series": "Series",
    "dept_org": "Dept_Organization",
    "series_name": "Series_Name",
    "last_name": "Deceaseds_ Last_name",
    "first_name": "Deceaseds_First_name",
    "middle_name": "Deceaseds_Middle_name",
    "deceased": "Deceased",
    "suffix": "Suffix",
    "begin_year": "Begin_Year",
    "end_year": "End_Year",
    "num_sheets": "Number_of_sheets",
    "comments": "Comments",
    "dod": "DOD",
    "oversized": "Oversized",
    "container_type": "Container_Type",
    "size_of_container": "size_of_container",
}

CHILD_COLUMNS = {
    "record_id": "Record_ID",
    "last_name": "Last_Name",
    "first_name": "First_Name",
    "middle_name": "MiddleName",
    "suffix": "Suffix",
    "parent_last": "Parents_Last_Name",
    "parent_first": "Parents_First_Name",
    "child_record_id": "Childrens_Record_ID",
    "comments": "Comments",
}

CONTAINER_COLUMNS = {
    "title": "Title",
    "barcode": "Barcode",
    "location_id": "Location ID",
}

# ArchivERA output column header (30 columns, exact order)
OUTPUT_HEADER = [
    "Record Type",
    "Record Level Name",
    "RG",
    "SubGr",
    "Series",
    "Dept_Organization",
    "Series_Name",
    "Title",
    "FullDate",
    "Record_ID",
    "Description",
    "Description.1",
    "Description.2",
    "Description.3",
    "Description.4",
    "Description.5",
    "Material Types",
    "Notes",
    "Container Type",
    "Notes.1",
    "Notes.2",
    "Deceaseds_ Last_name",
    "Barcode",
    "Location ID",
    "Set Current Location",
    "Restrictions on Use",
    "Contributing Institution",
    "Disposition",
    "Status",
    "Import Hook",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get(row, mapping, key, default=""):
    """Safely get a value from a CSV row using the column mapping."""
    col = mapping.get(key, "")
    val = row.get(col, default)
    if val is None:
        return default
    return str(val).strip()


def clean_float_str(val):
    """Convert '2840.0' → '2840', leave non-numeric strings alone."""
    if not val:
        return val
    try:
        f = float(val)
        if f == int(f):
            return str(int(f))
        return val
    except ValueError:
        return val


def pad_rg(val):
    """Pad RG to 4 digits with leading zeros. E.g. '42' → '0042'."""
    val = clean_float_str(val)
    if not val:
        return val
    try:
        return str(int(val)).zfill(4)
    except ValueError:
        return val


def pad_series(val):
    """Pad Series/SubGr/SubSeries to 3 digits with leading zeros. E.g. '39' → '039'."""
    val = clean_float_str(val)
    if not val:
        return val
    try:
        return str(int(val)).zfill(3)
    except ValueError:
        return val


def format_middle(middle):
    """Format middle name: single letter gets a period, full words stay as-is."""
    if not middle:
        return ""
    middle = middle.strip()
    if len(middle) == 1:
        return middle + "."
    return middle


def format_person_name(first, middle, last):
    """Build 'First Middle Last' with proper middle formatting."""
    parts = []
    if first:
        parts.append(first.strip())
    mid = format_middle(middle)
    if mid:
        parts.append(mid)
    if last:
        parts.append(last.strip())
    return " ".join(parts)


def parse_container_range(title):
    """
    Parse a container title like 'Beeson, Henry to Bell, Katie'
    into (start_last, start_first, end_last, end_first).
    Handles the '?' prefix in the first container.
    """
    # Split on ' to ' (case-insensitive, but data uses 'to' and 'To')
    parts = re.split(r'\s+to\s+', title, maxsplit=1, flags=re.IGNORECASE)
    if len(parts) != 2:
        return None

    def parse_name(s):
        s = s.strip()
        # Handle "? Sarah" style entries
        if s.startswith("?"):
            s = s.lstrip("? ")
            return ("", s)  # empty last name sorts first
        comma_parts = s.split(",", 1)
        last = comma_parts[0].strip()
        first = comma_parts[1].strip() if len(comma_parts) > 1 else ""
        return (last, first)

    start = parse_name(parts[0])
    end = parse_name(parts[1])
    return (start, end)


def name_key(last, first=""):
    """Create a sortable key from last, first name."""
    return (last.lower().strip(), first.lower().strip())


# ---------------------------------------------------------------------------
# Container lookup
# ---------------------------------------------------------------------------

class ContainerLookup:
    """Binary-search based container lookup by alphabetical surname range."""

    def __init__(self, containers_path):
        self.ranges = []  # list of (end_key, barcode, location, title)
        self._load(containers_path)

    def _load(self, path):
        entries = []
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get(CONTAINER_COLUMNS["title"], "")
                barcode = row.get(CONTAINER_COLUMNS["barcode"], "")
                location = row.get(CONTAINER_COLUMNS["location_id"], "")
                parsed = parse_container_range(title)
                if parsed is None:
                    continue
                start, end = parsed
                start_key = name_key(start[0], start[1])
                end_key = name_key(end[0], end[1])
                entries.append((start_key, end_key, barcode, location, title))

        # Sort by start key
        entries.sort(key=lambda e: e[0])
        self.entries = entries
        # Build list of end keys for bisect
        self.end_keys = [e[1] for e in entries]
        self.start_keys = [e[0] for e in entries]

    def find(self, last_name, first_name=""):
        """
        Find the container for a given name.
        Returns (barcode, location) or (None, None) if not found.
        """
        if not last_name:
            return (None, None)

        lookup = name_key(last_name, first_name)

        # Linear scan: find the container whose range includes this name
        for start_key, end_key, barcode, location, title in self.entries:
            if start_key <= lookup <= end_key:
                return (barcode, location)

        # Fallback: check if name falls before the first range
        if self.entries and lookup <= self.entries[0][1]:
            return (self.entries[0][2], self.entries[0][3])

        return (None, None)


# ---------------------------------------------------------------------------
# Children index
# ---------------------------------------------------------------------------

def load_children(children_path):
    """Load children CSV, return dict keyed by Record_ID → list of child dicts."""
    children = {}
    with open(children_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid = get(row, CHILD_COLUMNS, "record_id")
            if not rid:
                continue
            rid = clean_float_str(rid)
            child = {
                "last_name": get(row, CHILD_COLUMNS, "last_name"),
                "first_name": get(row, CHILD_COLUMNS, "first_name"),
                "middle_name": get(row, CHILD_COLUMNS, "middle_name"),
                "suffix": get(row, CHILD_COLUMNS, "suffix"),
                "comments": get(row, CHILD_COLUMNS, "comments"),
            }
            children.setdefault(rid, []).append(child)
    return children


# ---------------------------------------------------------------------------
# Record transformation
# ---------------------------------------------------------------------------

def is_foundling(adult_row):
    """Detect foundling records (has comment indicating foundling/parents unknown)."""
    comments = get(adult_row, ADULT_COLUMNS, "comments")
    return bool(comments and "foundling" in comments.lower())


def build_title(adult_row, children_list):
    """Build the Title field based on record type."""
    last = get(adult_row, ADULT_COLUMNS, "last_name")
    first = get(adult_row, ADULT_COLUMNS, "first_name")
    middle = get(adult_row, ADULT_COLUMNS, "middle_name")
    deceased = get(adult_row, ADULT_COLUMNS, "deceased")

    # Case 1: Deceased parent with a name
    if deceased.lower() == "yes" and (last or first):
        return format_person_name(first, middle, last)

    # Case 2 & 3: No deceased parent — use children names
    if children_list:
        names = []
        for child in children_list:
            name = format_person_name(
                child["first_name"],
                child["middle_name"],
                child["last_name"],
            )
            if name:
                names.append(name)
        if names:
            return " and ".join(names)

    # Fallback
    return format_person_name(first, middle, last)


def format_children_description(children_list):
    """Format children list for Description.2 field."""
    if not children_list:
        return ""
    names = []
    for child in children_list:
        name = format_person_name(
            child["first_name"],
            child["middle_name"],
            child["last_name"],
        )
        if name:
            names.append(name)
    if not names:
        return ""
    return "Children: " + ", ".join(names)


def build_description_fields(adult_row, children_list):
    """
    Build Description through Description.5 fields.
    Returns a dict with keys: desc, desc1, desc2, desc3, desc4, desc5.
    """
    deceased = get(adult_row, ADULT_COLUMNS, "deceased")
    dod = get(adult_row, ADULT_COLUMNS, "dod")
    num_sheets = get(adult_row, ADULT_COLUMNS, "num_sheets")
    comments = get(adult_row, ADULT_COLUMNS, "comments")

    # Clean DOD — strip ".0" from float representation
    dod = clean_float_str(dod)

    result = {
        "desc": "",
        "desc1": "",
        "desc2": "",
        "desc3": "",
        "desc4": "",
        "desc5": "",
    }

    if is_foundling(adult_row):
        # Foundling pattern:
        #   Description:   comment (e.g. "Foundling, parents unknown")
        #   Description.1: Deceased: Yes/No
        #   Description.2: (empty)
        #   Description.3: (empty)
        #   Description.4: child comment (e.g. "no last name listed")
        #   Description.5: Number of sheets: N
        cap_comments = comments[0].upper() + comments[1:] if comments else ""
        result["desc"] = cap_comments
        result["desc1"] = f"Deceased: {deceased}" if deceased else ""

        # Child comment in desc4
        if children_list:
            child_comments = [c["comments"] for c in children_list if c["comments"]]
            if child_comments:
                result["desc4"] = child_comments[0]

        result["desc5"] = f"Number of sheets: {num_sheets}" if num_sheets else ""
    else:
        # Standard pattern:
        #   Description:   (empty)
        #   Description.1: Deceased: Yes/No
        #   Description.2: Date of death: YYYY (if present)
        #   Description.3: Children: ... (or "Children: none" if deceased but no children)
        #   Description.4: (empty)
        #   Description.5: Number of sheets: N
        result["desc1"] = f"Deceased: {deceased}" if deceased else ""
        result["desc2"] = f"Date of death: {dod}" if dod else ""

        # Only list children in Description.3 when there IS a deceased parent.
        # When Deceased=No and children are used as the Title, don't repeat them.
        if deceased and deceased.lower() == "yes":
            children_desc = format_children_description(children_list)
            if not children_desc:
                children_desc = "Children: none"
            result["desc3"] = children_desc

        result["desc5"] = f"Number of sheets: {num_sheets}" if num_sheets else ""

    return result


def build_record(adult_row, children_list, container_lookup, defaults=None):
    """
    Transform one adult record + its children into an ArchivERA output row.
    Returns (output_dict, flags_list).
    defaults: dict with fallback values for rg, series, dept_org, series_name
    """
    if defaults is None:
        defaults = {}
    flags = []

    rid = clean_float_str(get(adult_row, ADULT_COLUMNS, "record_id"))
    last_name = get(adult_row, ADULT_COLUMNS, "last_name")
    first_name = get(adult_row, ADULT_COLUMNS, "first_name")
    begin_year = clean_float_str(get(adult_row, ADULT_COLUMNS, "begin_year"))
    end_year = clean_float_str(get(adult_row, ADULT_COLUMNS, "end_year"))
    oversized = get(adult_row, ADULT_COLUMNS, "oversized")
    size_of_container = get(adult_row, ADULT_COLUMNS, "size_of_container")

    # RG: 4-digit padded; Series/SubGr: 3-digit padded
    rg = pad_rg(get(adult_row, ADULT_COLUMNS, "rg") or defaults.get("rg", ""))
    series = pad_series(get(adult_row, ADULT_COLUMNS, "series") or defaults.get("series", ""))
    dept_org = get(adult_row, ADULT_COLUMNS, "dept_org") or defaults.get("dept_org", "")
    series_name = get(adult_row, ADULT_COLUMNS, "series_name") or defaults.get("series_name", "")

    # Title
    title = build_title(adult_row, children_list)

    # FullDate
    full_date = ""
    if begin_year and end_year:
        full_date = f"01/01/{begin_year} - 12/31/{end_year}"

    # Description fields
    desc = build_description_fields(adult_row, children_list)

    # Notes
    notes_oversize = f"Oversize: {oversized}" if oversized else ""
    notes_size = ""
    if oversized and oversized.lower() == "yes" and size_of_container:
        # Normalize case: "16 X 20" → "16 x 20"
        notes_size = f"Size of container: {size_of_container.replace(' X ', ' x ').replace(' x ', ' x ')}"

    # Container lookup
    lookup_last = last_name
    lookup_first = first_name
    if not lookup_last and children_list:
        # Use first child's last name for container lookup
        for child in children_list:
            if child["last_name"]:
                lookup_last = child["last_name"]
                lookup_first = child["first_name"]
                break

    if lookup_last:
        barcode, location = container_lookup.find(lookup_last, lookup_first)
    else:
        barcode, location = None, None
        flags.append(f"Record {rid}: No last name available for container lookup")

    if barcode is None and lookup_last:
        flags.append(f"Record {rid}: No container match for '{lookup_last}'")

    # Build output row
    output = {
        "Record Type": "file/item",
        "Record Level Name": "file",
        "RG": rg,
        "SubGr": pad_series("0"),
        "Series": series,
        "Dept_Organization": dept_org,
        "Series_Name": series_name,
        "Title": title,
        "FullDate": full_date,
        "Record_ID": rid,
        "Description": desc["desc"],
        "Description.1": desc["desc1"],
        "Description.2": desc["desc2"],
        "Description.3": desc["desc3"],
        "Description.4": desc["desc4"],
        "Description.5": desc["desc5"],
        "Material Types": "Document",
        "Notes": notes_oversize,
        "Container Type": "",
        "Notes.1": notes_size,
        "Notes.2": "",
        "Deceaseds_ Last_name": last_name,
        "Barcode": barcode or "",
        "Location ID": location or "",
        "Set Current Location": "Yes",
        "Restrictions on Use": "The material is open for research use.",
        "Contributing Institution": "Delaware Public Archives",
        "Disposition": "Permanent",
        "Status": "on shelf",
        "Import Hook": "",
    }

    return output, flags


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Migrate Orphans Court records to ArchivERA import format."
    )
    parser.add_argument(
        "--adults", default="NCC Adults.csv",
        help="Path to adults CSV (default: NCC Adults.csv)"
    )
    parser.add_argument(
        "--children", default="NCCChildren.csv",
        help="Path to children CSV (default: NCCChildren.csv)"
    )
    parser.add_argument(
        "--containers", default="NCC Orphans Court Containers.csv",
        help="Path to containers CSV (default: NCC Orphans Court Containers.csv)"
    )
    parser.add_argument(
        "--output", default="output.csv",
        help="Path for output CSV (default: output.csv)"
    )
    parser.add_argument(
        "--default-rg", default="",
        help="Default RG value when source is empty (4-digit, e.g. 2840)"
    )
    parser.add_argument(
        "--default-series", default="",
        help="Default Series value when source is empty (3-digit, e.g. 039)"
    )
    parser.add_argument(
        "--default-dept-org", default="",
        help="Default Dept_Organization when source is empty"
    )
    parser.add_argument(
        "--default-series-name", default="",
        help="Default Series_Name when source is empty"
    )

    args = parser.parse_args()

    # Validate input files exist
    for path, label in [(args.adults, "Adults"), (args.children, "Children"),
                        (args.containers, "Containers")]:
        if not os.path.exists(path):
            print(f"Error: {label} file not found: {path}", file=sys.stderr)
            sys.exit(1)

    # Load data
    print(f"Loading containers from: {args.containers}")
    container_lookup = ContainerLookup(args.containers)
    print(f"  {len(container_lookup.entries)} containers loaded")

    print(f"Loading children from: {args.children}")
    children_index = load_children(args.children)
    total_children = sum(len(v) for v in children_index.values())
    print(f"  {total_children} children across {len(children_index)} records")

    # Defaults for records with missing metadata
    defaults = {
        "rg": args.default_rg,
        "series": args.default_series,
        "dept_org": args.default_dept_org,
        "series_name": args.default_series_name,
    }

    print(f"Processing adults from: {args.adults}")

    all_flags = []
    records_written = 0

    # Build review file path
    base, ext = os.path.splitext(args.output)
    review_path = f"{base}_review{ext}"

    with open(args.adults, newline="", encoding="utf-8-sig") as f_in, \
         open(args.output, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=OUTPUT_HEADER)
        writer.writeheader()

        for adult_row in reader:
            rid = clean_float_str(get(adult_row, ADULT_COLUMNS, "record_id"))
            children_list = children_index.get(rid, [])

            output, flags = build_record(adult_row, children_list, container_lookup, defaults)
            writer.writerow(output)
            records_written += 1
            all_flags.extend(flags)

    # Write review file if there are flags
    if all_flags:
        with open(review_path, "w", newline="", encoding="utf-8") as f_review:
            review_writer = csv.writer(f_review)
            review_writer.writerow(["Flag"])
            for flag in all_flags:
                review_writer.writerow([flag])
        print(f"\nReview file written: {review_path} ({len(all_flags)} flags)")

    print(f"\nDone. {records_written} records written to: {args.output}")
    if all_flags:
        print(f"Flags ({len(all_flags)}):")
        for flag in all_flags:
            print(f"  - {flag}")


if __name__ == "__main__":
    main()
