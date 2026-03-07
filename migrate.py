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
    "subgr": "SubGr",
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

# ArchivERA output header parts. Description/Notes are repeated (no numbering).
HEADER_PREFIX = [
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
]
HEADER_SUFFIX = [
    "Container Type",
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


def build_header(description_count, notes_count=2):
    """Build output header with repeated Description/Notes columns."""
    return (
        HEADER_PREFIX
        + (["Description"] * description_count)
        + ["Material Types"]
        + (["Notes"] * notes_count)
        + HEADER_SUFFIX
    )


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


def format_child_line(child, index):
    """Format a single child entry for description output."""
    first = child.get("first_name", "")
    middle = child.get("middle_name", "")
    last = child.get("last_name", "")
    suffix = child.get("suffix", "")
    child_id = clean_float_str(child.get("child_record_id", ""))
    comments = (child.get("comments", "") or "").strip()

    name = format_person_name(first, middle, last)
    if suffix:
        suffix = suffix.strip()
        if name:
            name = f"{name} {suffix}"
        else:
            name = suffix

    base = f"{index}."
    if name:
        base = f"{base} {name}"

    parts = [base]
    if child_id:
        parts.append(f"Child ID: {child_id}")
    if comments:
        parts.append(f"Comment: {comments}")

    return " - ".join(parts).strip()


def build_children_lines(children_list):
    """Return a list of numbered child lines."""
    lines = []
    for idx, child in enumerate(children_list, 1):
        line = format_child_line(child, idx)
        if line:
            lines.append(line)
    return lines


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
                "child_record_id": get(row, CHILD_COLUMNS, "child_record_id"),
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


def build_description_fields(adult_row, children_list, children_format, description_count=6):
    """
    Build Description values in column order.
    Returns (desc_values_list, notes_extra, overflow_flag).
    """
    deceased = get(adult_row, ADULT_COLUMNS, "deceased")
    dod = get(adult_row, ADULT_COLUMNS, "dod")
    num_sheets = get(adult_row, ADULT_COLUMNS, "num_sheets")
    comments = get(adult_row, ADULT_COLUMNS, "comments")

    # Clean DOD — strip ".0" from float representation
    dod = clean_float_str(dod)

    result = [""] * max(description_count, 1)
    notes_extra = ""
    overflow = False

    if is_foundling(adult_row):
        # Foundling pattern:
        #   Description (col 1): comment (e.g. "Foundling, parents unknown")
        #   Description (col 2): Deceased: Yes/No
        #   Description (col 3): (empty)
        #   Description (col 4): (empty)
        #   Description (col 5): child comment (e.g. "no last name listed")
        #   Description (col 6): Number of sheets: N
        cap_comments = comments[0].upper() + comments[1:] if comments else ""
        result[0] = cap_comments
        if len(result) > 1:
            result[1] = f"Deceased: {deceased}" if deceased else ""

        # Child comment in desc4
        if children_list:
            child_comments = [c["comments"] for c in children_list if c["comments"]]
            if child_comments:
                if len(result) > 4:
                    result[4] = child_comments[0]

        if len(result) > 5:
            result[5] = f"Number of sheets: {num_sheets}" if num_sheets else ""
    else:
        # Standard pattern
        if children_format == "single":
            if len(result) > 1:
                result[1] = f"Deceased: {deceased}" if deceased else ""
            if len(result) > 2:
                result[2] = f"Date of death: {dod}" if dod else ""

        # Only list children in Description when there IS a deceased parent.
        # When Deceased=No and children are used as the Title, don't repeat them.
        if deceased and deceased.lower() == "yes":
            child_lines = build_children_lines(children_list)
            if not child_lines:
                if children_format == "single":
                    if len(result) > 3:
                        result[3] = "Children: none"
                else:
                    if result:
                        result[0] = "Children: none"
            else:
                if children_format == "single":
                    if len(result) > 3:
                        result[3] = "\n".join(child_lines)
                else:
                    # One child per Description column (as many as provided).
                    for idx, line in enumerate(child_lines):
                        if idx < len(result):
                            result[idx] = line
                        else:
                            overflow = True
                            extra = "\n".join(child_lines[idx:])
                            if result:
                                if result[-1]:
                                    result[-1] = f"{result[-1]}\n{extra}"
                                else:
                                    result[-1] = extra
                            break
                    if len(child_lines) > len(result):
                        overflow = True
        if children_format == "single":
            if len(result) > 5:
                result[5] = f"Number of sheets: {num_sheets}" if num_sheets else ""
        else:
            notes_bits = []
            if deceased:
                notes_bits.append(f"Deceased: {deceased}")
            if dod:
                notes_bits.append(f"Date of death: {dod}")
            if num_sheets:
                notes_bits.append(f"Number of sheets: {num_sheets}")
            notes_extra = " | ".join(notes_bits)

    return result, notes_extra, overflow


def build_record(adult_row, children_list, container_lookup, defaults=None, children_format="single", description_count=6):
    """
    Transform one adult record + its children into an ArchivERA output row.
    Returns (output_dict, description_values, notes_values, flags_list).
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
    subgr = pad_series(get(adult_row, ADULT_COLUMNS, "subgr") or defaults.get("subgr", "0"))
    dept_org = get(adult_row, ADULT_COLUMNS, "dept_org") or defaults.get("dept_org", "")
    series_name = get(adult_row, ADULT_COLUMNS, "series_name") or defaults.get("series_name", "")

    # Title
    title = build_title(adult_row, children_list)

    # FullDate
    full_date = ""
    if begin_year and end_year:
        full_date = f"01/01/{begin_year} - 12/31/{end_year}"

    # Description fields
    desc_values, notes_extra, overflow = build_description_fields(
        adult_row, children_list, children_format, description_count
    )
    if overflow:
        flags.append(
            f"Record {rid}: {len(children_list)} children; "
            f"only first {description_count} in separate Description columns, remainder appended to last Description column"
        )

    # Notes
    notes_oversize = f"Oversize: {oversized}" if oversized else ""
    notes_size = ""
    if oversized and oversized.lower() == "yes" and size_of_container:
        # Normalize case: "16 X 20" → "16 x 20"
        notes_size = f"Size of container: {size_of_container.replace(' X ', ' x ').replace(' x ', ' x ')}"
    notes_primary = notes_oversize
    if notes_size:
        notes_primary = f"{notes_primary} | {notes_size}" if notes_primary else notes_size

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

    container_note = ""
    if lookup_last:
        barcode, location = container_lookup.find(lookup_last, lookup_first)
    else:
        barcode, location = None, None
        flags.append(f"Record {rid}: No last name available for container lookup")
        container_note = "Container lookup: no last name"

    if barcode is None and lookup_last:
        flags.append(f"Record {rid}: No container match for '{lookup_last}'")

    if container_note:
        if notes_extra:
            notes_extra = f"{notes_extra} | {container_note}"
        else:
            notes_extra = container_note

    notes_values = [notes_primary, notes_extra]

    # Build output row
    output = {
        "Record Type": "file/item",
        "Record Level Name": "file",
        "RG": rg,
        "SubGr": subgr,
        "Series": series,
        "Dept_Organization": dept_org,
        "Series_Name": series_name,
        "Title": title,
        "FullDate": full_date,
        "Record_ID": rid,
        "Material Types": "Document",
        "Container Type": "",
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

    return output, desc_values, notes_values, flags


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
    parser.add_argument(
        "--default-subgr", default="",
        help="Default SubGr value when source is empty (3-digit, e.g. 000)"
    )
    parser.add_argument(
        "--children-format", default="single",
        choices=["single", "columns", "both"],
        help="Children formatting: single (newline list), columns (one per Description column), both"
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
    max_children = max((len(v) for v in children_index.values()), default=0)
    description_count_columns = max(max_children, 6)

    # Defaults for records with missing metadata
    defaults = {
        "rg": args.default_rg,
        "series": args.default_series,
        "subgr": args.default_subgr,
        "dept_org": args.default_dept_org,
        "series_name": args.default_series_name,
    }

    # Auto-fill missing defaults for these headers only:
    # RG, Series, SubGr, Dept_Organization, Series_Name
    auto_cols = {
        "rg": ADULT_COLUMNS["rg"],
        "series": ADULT_COLUMNS["series"],
        "subgr": ADULT_COLUMNS["subgr"],
        "dept_org": ADULT_COLUMNS["dept_org"],
        "series_name": ADULT_COLUMNS["series_name"],
    }
    auto_keys = [k for k in auto_cols if not defaults.get(k)]
    if auto_keys:
        counts = {k: {} for k in auto_keys}
        with open(args.adults, newline="", encoding="utf-8-sig") as f_in:
            reader = csv.DictReader(f_in)
            for row in reader:
                for key in auto_keys:
                    col = auto_cols[key]
                    val = (row.get(col) or "").strip()
                    if not val:
                        continue
                    counts[key][val] = counts[key].get(val, 0) + 1
        for key in auto_keys:
            if counts[key]:
                defaults[key] = max(counts[key].items(), key=lambda x: x[1])[0]

    print(f"Processing adults from: {args.adults}")

    def output_path_with_suffix(path, suffix):
        base, ext = os.path.splitext(path)
        return f"{base}_{suffix}{ext}"

    def review_path_for(path):
        base, ext = os.path.splitext(path)
        return f"{base}_review{ext}"

    if args.children_format == "both":
        output_specs = [
            ("single", output_path_with_suffix(args.output, "children_single"), 6),
            ("columns", output_path_with_suffix(args.output, "children_columns"), description_count_columns),
        ]
    else:
        desc_count = description_count_columns if args.children_format == "columns" else 6
        output_specs = [(args.children_format, args.output, desc_count)]

    from contextlib import ExitStack
    notes_count = 2
    flags_by_format = {fmt: [] for fmt, *_ in output_specs}
    records_written = 0

    with ExitStack() as stack, open(args.adults, newline="", encoding="utf-8-sig") as f_in:
        reader = csv.DictReader(f_in)
        writers = {}
        headers_by_fmt = {}
        for fmt, out_path, desc_count in output_specs:
            f_out = stack.enter_context(open(out_path, "w", newline="", encoding="utf-8"))
            header = build_header(desc_count, notes_count)
            writer = csv.writer(f_out)
            writer.writerow(header)
            writers[fmt] = writer
            headers_by_fmt[fmt] = header

        for adult_row in reader:
            rid = clean_float_str(get(adult_row, ADULT_COLUMNS, "record_id"))
            children_list = children_index.get(rid, [])

            for fmt, _, desc_count in output_specs:
                output, desc_values, notes_values, flags = build_record(
                    adult_row,
                    children_list,
                    container_lookup,
                    defaults,
                    children_format=fmt,
                    description_count=desc_count,
                )
                header = headers_by_fmt[fmt]
                row = []
                desc_idx = 0
                notes_idx = 0
                for col in header:
                    if col == "Description":
                        row.append(desc_values[desc_idx] if desc_idx < len(desc_values) else "")
                        desc_idx += 1
                    elif col == "Notes":
                        row.append(notes_values[notes_idx] if notes_idx < len(notes_values) else "")
                        notes_idx += 1
                    else:
                        row.append(output.get(col, ""))
                writers[fmt].writerow(row)
                flags_by_format[fmt].extend(flags)

            records_written += 1

    for fmt, out_path, _desc_count in output_specs:
        all_flags = flags_by_format[fmt]
        review_path = review_path_for(out_path)
        if all_flags:
            with open(review_path, "w", newline="", encoding="utf-8") as f_review:
                review_writer = csv.writer(f_review)
                review_writer.writerow(["Flag"])
                for flag in all_flags:
                    review_writer.writerow([flag])
            print(f"\nReview file written: {review_path} ({len(all_flags)} flags)")

        print(f"\nDone. {records_written} records written to: {out_path}")
        if all_flags:
            print(f"Flags ({len(all_flags)}):")
            for flag in all_flags:
                print(f"  - {flag}")


if __name__ == "__main__":
    main()
