# Findings - SC

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
