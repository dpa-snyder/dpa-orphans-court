# DPA Orphans Court Migration

Automated migration of Delaware Public Archives Orphans Court case records from Access database exports into ArchivERA-ready import CSVs.

## Overview

Orphans Court records consist of adult (deceased parent) records linked to child records, each assigned to physical containers organized by alphabetical name ranges. This project provides a Python script that:

1. Links parent records to child records by `Record_ID`
2. Matches each record to the correct container (Barcode + Location ID) via alphabetical surname lookup
3. Transforms everything into ArchivERA's import format using repeated `Description`/`Notes` headers (no numbering)
4. Flags edge cases (foundlings, missing data) for manual review

## Quick Start

```bash
python3 migrate.py \
  --adults "NCC Adults.csv" \
  --children "NCCChildren.csv" \
  --containers "NCC Orphans Court Containers.csv" \
  --output "output.csv" \
  --default-rg 2840 \
  --default-series 39 \
  --default-dept-org "Orphans Court, New Castle County" \
  --default-series-name "Case Files" \
  --profile ncc
```

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)

## Input Files

| File | Description |
|------|-------------|
| Adults CSV | Deceased parent records from Access database |
| Children CSV | Child records linked by `Record_ID` |
| Containers CSV | 431 containers with Barcode/Location, organized by alphabetical name ranges |

## Output

- **`output.csv`** — ArchivERA-ready import file (repeated `Description`/`Notes` headers, counts vary)
- **`output_review.csv`** — Flagged records requiring manual review
If `--children-format both` is used, two files are written:
- `output_children_single.csv` (children as a numbered list in one Description field)
- `output_children_columns.csv` (one child per Description column)
Each output gets its own `_review.csv`.

Both formats emit two `Notes` columns labeled `Notes` (no numbering). The first stores oversize/size info; the second stores metadata such as Deceased/DOD/Number of sheets (for `columns`) and container lookup notes.
For `--children-format columns`, the output uses **repeated** `Description` headers (no numbering) with as many columns as needed for the maximum number of children in the dataset (minimum 6). Deceased/DOD/Number of sheets move to the second `Notes` column for that format.

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--adults` | `NCC Adults.csv` | Path to adults CSV |
| `--children` | `NCCChildren.csv` | Path to children CSV |
| `--containers` | `NCC Orphans Court Containers.csv` | Path to containers CSV |
| `--no-containers` | (false) | Skip container lookup (barcode/location left blank unless present in source) |
| `--output` | `output.csv` | Output file path |
| `--default-rg` | (empty) | Fallback RG when source is empty (4-digit) |
| `--default-series` | (empty) | Fallback Series when source is empty (3-digit) |
| `--default-subgr` | (empty) | Fallback SubGr when source is empty (3-digit) |
| `--default-dept-org` | (empty) | Fallback Dept_Organization |
| `--default-series-name` | (empty) | Fallback Series_Name |
| `--children-format` | `single` | Children formatting: `single`, `columns`, or `both` |
| `--profile` | `ncc` | Column mapping profile: `ncc`, `kc`, or `sc` |

If any of `--default-rg`, `--default-series`, `--default-subgr`, `--default-dept-org`, or
`--default-series-name` are omitted, the script auto-fills missing values from the most common
non-empty value in the Adults CSV for those fields.

## Number Formatting

- **RG**: 4 digits with leading zeros (e.g. `2840`, `0042`)
- **SubGr / Series / SubSeries**: 3 digits with leading zeros (e.g. `039`, `000`)

## Record Types

| Type | Example | Title Source |
|------|---------|-------------|
| Deceased parent with children | Katie Bell (5 children) | Parent name |
| Deceased parent, no children | George Bell | Parent name |
| No parent, children listed | Emily Joan Agoos, Susan Julia Agoos | Children names joined with "and" |
| Foundling | Sarah (no last name) | Child first name only |

## Reference Files

| File | Purpose |
|------|---------|
| `NCC Orphans Court - Edited.csv` | Gold standard — manually mapped ArchivERA import |
| `NCC Orphans Court Combined.csv` | Intermediate combined parent-child records |
| `NCC Orphans Court.csv` | Less cleaned-up parent-child version |
| `CONTEXT.md` | Full project context and field mapping documentation |
| `QUESTIONS.md` | Resolved decisions and open items |
| `notes.md` | Original working notes (KC, NCC, SC counties) |

## Counties

The notes reference three counties with container counts:
- **NCC** (New Castle County) — 431 containers (current dataset)
- **KC** (Kent County) — 211 containers
- **SC** (Sussex County) — 289 containers

The script is designed to handle all three by adjusting input files and default CLI args per county.
