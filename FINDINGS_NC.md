# Findings - NC

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
