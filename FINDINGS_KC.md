# Findings - KC

Source: /Users/bag/code/dpa-orphans-court/counties/3840-kent/findings.md

## Scope
- Focused on KC only (Access Adults/Children + deleted folders).
- Exports are raw CSV dumps from Access using `mdbtools` (no transformation).

## Source files
- access-dbs/3840 Kent County/3840-000-006 KC Orphans Court Case Files current.mdb (6.5 MB)
- access-dbs/3840 Kent County/KC deleted folders.accdb (1.1 MB)
- access-dbs/3840 Kent County/Puzzle pieces.xlsx (13.5 KB)

## Tables (Access)
- 3840-000-006 KC Orphans Court Case Files current.mdb: Adults, Children, Copy of Adults
- KC deleted folders.accdb: KC orphans deleted folders

## Extracted CSVs
- counties/3840-kent/extracted/3840-000-006 KC Orphans Court Case Files current/Adults.csv
- counties/3840-kent/extracted/3840-000-006 KC Orphans Court Case Files current/Children.csv
- counties/3840-kent/extracted/3840-000-006 KC Orphans Court Case Files current/Copy of Adults.csv
- counties/3840-kent/extracted/KC deleted folders/KC orphans deleted folders.csv

## Row counts
- Adults: 6,251
- Children: 17,135
- Copy of Adults: 6,261
- KC deleted folders: 722

## Key field stats
- Adults with children: 5,098
- Adults with zero children: 1,153
- Max children for one adult: 36
- Adults missing last name: 264
- Adults missing first name: 267
- Children missing last name: 18
- Children missing first name: 4
- Adults flagged Oversized=Yes: 2,029
- Adults with DOD present: 5
- Adults with Barcode present: 143
- Foundling count (Comments contains "foundling"): 0

## Children per adult distribution
- 1 child: 1,663
- 2-3 children: 1,574
- 4-5 children: 911
- 6+ children: 950

## ID consistency
- Distinct Adults.Record ID: 6,251
- Distinct Children.Record ID: 5,098
- Children records with no matching Adult: 0
- Adults with no matching Children: 1,153

## Leading zeros / sorting
- Record Group Number: constant `3840` (2 missing).
- Series Number: constant `006` (1 missing), leading zeros preserved in the CSV.
- Department Name: constant `Orphans Court, Kent County` (1 missing).
- Series Name: constant `Case Files` (15 missing).
- No SubGr column present in the KC Adults table - will need a default (likely `000`) for AE import.

## Sparse columns (>=90% empty)
- Adults sparse columns: `Title: "Jr"` (171 non-empty), `Barcode` (143), `condition` (67), `DOD` (5), `Old code` (10).
- Children sparse columns: `Jr` (168), `Comments - Child` (7), `Oversize` (0).

## Copy of Adults comparison
- Copy of Adults has 6,261 rows and 18 columns (missing `condition`, `DOD`, `Old code`, `Plot`).
- Record IDs only in Adults: 18
- Record IDs only in Copy of Adults: 28
- Recommendation: treat `Adults` as the primary table unless you want a reconciliation step.

## Deleted folders analysis (value/usage)
- Rows: 722
- folder deleted populated: 721
- folder now located populated: 722
- mergered folders populated: 718
- dates populated: 720
- original date populated: 719
- deceased populated: 714
- minor name change populated: 20
- comments populated: 138
- Adult last/first name populated: 452/451
- Child last/first name populated: 479/480
- Exact name match to Adults (Adult last/first): 538
- Exact name match to Children (Child last/first): 177
- Adult name + exact begin/end date match: 223

Interpretation:
- This looks like a curation log of deleted/merged folders with replacement labels and revised dates.
- High match rate to Adults suggests it is useful as a QA/suppression list rather than an import source.

## Puzzle pieces (XLSX)
- Sheet "repair sheet" lists potential folder matches, fixes, and rescan needs; likely internal QA notes rather than import data.

## Schema/mapping differences vs NCC
- KC column names differ from NCC (e.g., `Record ID`, `Record Group Number`, `Series Number`, `Department Name`, `Deceased's Last name`).
- Children table uses `Child's Last Name`, `Children's Record ID`, `Comments - Child`, etc.
- For the migration script, we will need a KC-specific mapping or a renaming step before import.

## Notes
- Container list is not present in the KC .mdb export; we need a separate container source for barcode/location lookups.
