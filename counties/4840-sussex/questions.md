# Questions - 4840 Sussex County

- Should RG `4848` be normalized to `4840`, or kept as-is for that record?
- Should Series outliers (e.g., `03`, `03'5`, `035'`, `oo9`) be normalized to `009` or `035`, or left as-is?
- SubGr is mostly `000` with 90 blanks and one `009`. Do we auto-fill blanks with `000`?
- Dept_Organization and Series_Name have small outliers (e.g., "Orphans Court" vs "Orphans Court, Sussex County", "Case File" vs "Case Files"). Normalize or preserve?
- How should we handle the single record in `Paste Errors.csv`?
- Should "Sussex County Deleted" be used to suppress/rename imports or only as a QA reference?
- Are `4840-002 Death Names` and `4840-000-009 Miscellaneous Orphans Court Minors Files` in scope for AE import or separate collections?
- Where should the Sussex container list come from (separate export/source for barcode/location lookups)?
