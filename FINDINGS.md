# Findings Summary

Combined findings for all counties.

## 2840 New Castle County
Source: /Users/bag/code/dpa-orphans-court/counties/2840-new-castle/findings.md

## Scope
- Focused on NCC only (Access Adults/Children + deleted folders).
- Exports are raw CSV dumps from Access using `mdbtools` (no transformation).
- AE import reference files were added to clarify headers/schema (see "AE import reference" below).

## Source files
- access-dbs/2840 New Castle County/2840-000-039 NC Orphans Court Case Files - current.mdb (5.3 MB)
- access-dbs/2840 New Castle County/NCC deleted folders.accdb (816.0 KB)
- access-dbs/2840 New Castle County/work to be done1.xlsx (32.2 KB)

## Tables (Access)
- 2840-000-039 NC Orphans Court Case Files - current.mdb: Adults, Children
- NCC deleted folders.accdb: NCC deleted folders

## Extracted CSVs
- counties/2840-new-castle/extracted/2840-000-039 NC Orphans Court Case Files - current/Adults.csv
- counties/2840-new-castle/extracted/2840-000-039 NC Orphans Court Case Files - current/Children.csv
- counties/2840-new-castle/extracted/NCC deleted folders/NCC deleted folders.csv

## Row counts
- Adults: 10,853
- Children: 25,540
- NCC deleted folders: 807

## Key field stats
- Adults with children: 9,329
- Adults with zero children: 1,524
- Max children for one adult: 23
- Adults missing last name: 1,885
- Adults missing first name: 1,889
- Children missing last name: 67
- Children missing first name: 7
- Adults flagged Oversized=Yes: 1,177
- Adults with DOD present: 2,040
- Adults with Barcode present: 39 (~0.4%)
- Foundling count (Comments contains "foundling"): 1

## Children per adult distribution
- 1 child: 3,957
- 2-3 children: 2,894
- 4-5 children: 1,376
- 6+ children: 1,102

## ID consistency
- Distinct Adults.Record_ID: 10,853
- Distinct Children.Record_ID: 9,329
- Children records with no matching Adult: 0
- Adults with no matching Children: 1,524

## Leading zeros / sorting
- Adults.RG is stored as numeric (Double) in Access, so leading zeros are not stored there.
- Adults.SubGr and Adults.Series are Text fields; leading zeros are preserved in the exported CSVs.
- Observed RG values: 2840
- Observed SubGr values: (blank), 000
- Observed Series values: 039
 - Constant-field check (Adults.csv):
 - RG: 1 distinct (2840), 0 missing
 - Series: 1 distinct (039), 0 missing
 - Dept_Organization: 1 distinct ("Orphans Court, New Castle County"), 2 missing
 - Series_Name: 1 distinct ("Case Files"), 1 missing
 - SubGr: 1 distinct (000), 2 missing

## Sparse columns (>=90% empty)
- Adults sparse columns: Field1 (1 non-empty), Barcode (39), Container_Type (88), Suffix (246)
- Children sparse columns: Suffix (607)

## Deleted folders analysis (value/usage)
- Rows: 807
- folder deleted values observed: yes (802), es (1), blank (4)
- folder now located populated: 804
- New dates populated: 801
- mergered populated: 800
- Minor name change populated: 11
- comments populated: 353
- Adult last name populated: 437
- Child last name populated: 654
- Exact name match to Adults (Adult last/first): 149
- Exact name match to Children (Child last/first): 125
- Exact name match to Adults (folder now located): 381
- Any exact name match (Adult/Child/Now located): 456
- Adult name + exact begin/end year match: 20

Interpretation:
- This table looks like a curation log of folders that were deleted/merged/renamed, with a "folder now located" replacement label and (often) updated dates.
- About 56.5% of entries (456/807) match an existing adult/child name or a "folder now located" name in the main dataset, which suggests it is useful as a QA/reference list for name corrections or merge suppression.
- Recommendation: do not import this into AE as-is; treat it as a review/mapping list to prevent importing deleted folders and to normalize names/dates where matches exist.

## Notes
- Primary DB appears to be the "current" .mdb file.
- "Deleted folders" .accdb is now exported and should be reviewed for suppression/mapping rules.
- The XLSX file looks like working notes; confirm if it is still in use.
- Container/holding list is not present in the NCC .mdb; it will need to come from a separate source.

## AE import reference (headers/schema)
Reference files are in `ae-import-reference--example-data/`:
- CKFA Migration Template.xlsx (Sheet1): 51 columns; appears to be the full AE header list.
- 3000-000-002 Kent County Slave Records.xlsx (Table1): 23 columns.
- 9200-D01-000 Dashiell Papers.xlsx (Sheet1): 35 columns.
- Naturalization Records.xlsx (Naturalization Records): 24 columns. Other sheets appear to be auxiliary (not import sheets).
- Private Accounts Collection.xlsx (Sheet1): 29 columns. Other sheets appear to be auxiliary (not import sheets).

Header pattern observations:
- Example imports use multiple "Description" columns **with the same header name** (no `.1` suffix).  
- Private Accounts uses two "Notes" columns both labeled "Notes".
- CKFA template uses a single "Description" and a single "Notes".

Implication for Orphans Court:
- The NCC gold standard CSV uses numbered headers, but AE references use duplicate header names.
- Orphans Court outputs should follow the AE examples: repeated `Description`/`Notes` headers with no numbering.

## 3840 Kent County
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

## 4840 Sussex County
Source: /Users/bag/code/dpa-orphans-court/counties/4840-sussex/findings.md

## Scope
- Focused on Sussex only (Access Adults/Children + deleted folders and related tables).
- Exports are raw CSV dumps from Access using `mdbtools` (no transformation).

## Source files
- access-dbs/4840 Sussex County/4840 SC Orphans Court Records - drh.mdb (108.6 MB)
- access-dbs/4840 Sussex County/4840 SC Orphans Court Records - drh.ldb (64 B)
- access-dbs/4840 Sussex County/4840-002 Death Names.mdb (208.0 KB)
- access-dbs/4840 Sussex County/Deleted orphans court folder listing.accdb (784.0 KB)
- access-dbs/4840-000-009 check list/4840-000-009 Miscellaneous Orphans Court  Minors Files.mdb (144.0 KB)

## Tables (Access)
- 4840 SC Orphans Court Records - drh.mdb: Adults, Children, Paste Errors
- 4840-002 Death Names.mdb: 4840-002 Death Names
- Deleted orphans court folder listing.accdb: Sussex County Deleted
- 4840-000-009 Miscellaneous Orphans Court  Minors Files.mdb: 4840-000-009 Miscellaneous Orphans Court  Minors Files

## Extracted CSVs
- counties/4840-sussex/extracted/4840 SC Orphans Court Records - drh/Adults.csv
- counties/4840-sussex/extracted/4840 SC Orphans Court Records - drh/Children.csv
- counties/4840-sussex/extracted/4840 SC Orphans Court Records - drh/Paste Errors.csv
- counties/4840-sussex/extracted/4840-002 Death Names/4840-002 Death Names.csv
- counties/4840-sussex/extracted/Deleted orphans court folder listing/Sussex County Deleted.csv
- counties/4840-sussex/extracted/4840-000-009 Miscellaneous Orphans Court  Minors Files/4840-000-009 Miscellaneous Orphans Court  Minors Files.csv

## Row counts
- Adults: 7,510
- Children: 16,909
- Paste Errors: 1
- Death Names: 626
- Sussex County Deleted: 927
- Miscellaneous Orphans Court Minors Files: 37

## Key field stats
- Adults with children: 5,205
- Adults with zero children: 2,305
- Max children for one adult: 20
- Adults missing last name: 377
- Adults missing first name: 400
- Children missing last name: 2
- Children missing first name: 1
- Adults flagged Oversized=Yes: 2,486
- Adults with DOD present: 2,361
- Adults with Barcode present: 500
- Foundling count (Comments contains "foundling"): 0

## Children per adult distribution
- 1 child: 1,623
- 2-3 children: 1,716
- 4-5 children: 975
- 6+ children: 892

## ID consistency
- Distinct Adults.Record_ID: 7,510
- Distinct Children.Record_ID: 5,206
- Children records with no matching Adult: 1
- Adults with no matching Children: 2,305

## Leading zeros / sorting
- Record_ID values do not appear to include leading zeros.
- RG values are mostly `4840`, with one `4848` record.
- SubGr values: `000` (7,419), blank (90), `009` (1).
- Series values: `009` (7,491) with small outliers: `035` (11), `018` (2), `03` (1), `03'5` (2), `035'` (2), `oo9` (1).
- Dept_Organization values: `Orphans Court, Sussex County` (7,507), `Orphans Court` (2), `Case Files` (1).
- Series_Name values: `Case Files` (7,497), `Case File` (11), `Guardian Accounts` (2).

Implications:
- RG/Series/Dept_Organization/Series_Name are not perfectly constant and include apparent typos.
- If we auto-fill or normalize these fields, we should decide whether to keep outliers or fold them into the dominant values.

## Sparse columns (>=90% empty)
- Adults sparse columns: Suffix (216 non-empty), Barcode (500), File_Num (580), Field1 (2).
- Children sparse columns: Suffix (140), Oversized (12), Size_of_Container (4).
- Children fields that are entirely empty: Begin_year, End_Year, Number_of_Sheets, Container_Type, Barcode, DOD, File_Num, Plot.

## Deleted folders analysis (value/usage)
- Rows: 927
- folder deleted populated: 923
- new folder name populated: 908
- new dates populated: 895
- merged populated: 907
- comments populated: 640
- deceased populated: 904
- minors changed name populated: 13
- Deceased last/first name populated: 789/787
- Minor last/first name populated: 161/161
- Exact name match to Adults (Deceased last/first): 370
- Exact name match to Children (Minor last/first): 31
- Adult name + exact begin/end date match: 131

Interpretation:
- This appears to be a curation log of deleted/merged folders with replacement labels and revised dates.
- It likely serves as a QA/suppression list rather than an import source.

## Paste Errors
- One-row table that looks like an import or paste anomaly. Needs review if we want to reconcile it back into Adults/Children.

## Death Names / Minors Files
- 4840-002 Death Names and 4840-000-009 Miscellaneous Orphans Court Minors Files look like separate series with different schemas.
- Confirm whether these are in scope for AE import or handled as separate collections.

## Notes
- Container list is not present in the Sussex exports; we need a separate container source for barcode/location lookups.
