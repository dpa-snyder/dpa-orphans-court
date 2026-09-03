# Client Questions

## Decision Order

1. [ ] SC: Which extra dataset is covered by "Nothing to be done, ignore this data set"?
2. [ ] SC: Are the 7 chancery-type Miscellaneous Orphans Court Minors Files out of scope?
3. [ ] SC: What should happen to the 5 unaccounted Miscellaneous Orphans Court Minors Files records?
4. [ ] SC: How should the single `Paste Errors.csv` row be handled?
5. [ ] Row counts: should counts be compared to CSV counts, or should Lindsay exclude review rows first?
6. [ ] NCC: What manual review decisions remain after processing?
7. [ ] NCC: Is `work to be done1.xlsx` still relevant?

## Confirmed/Mostly Settled

- KC uses `Adults` as authoritative, then adds the 28 records found only in `Copy of Adults`.
- KC `Copy of Adults` supplemental workbook has been applied: 28 records, including 2 source-barcoded records that already match their Legal Upright name ranges.
- KC source-barcoded Adults rows are preserved: 129 oversized and 14 regular. Oversized source-barcoded rows now get same-Record_ID letter-size companion rows when the source barcode differs from the Legal Upright range barcode.
- KC and SC oversize barcode lists should stay as separate oversize records, with barcode cross-references back to the related Adults records.
- KC and SC should keep `000` as the SubGr default where source data has no SubGr.
- Deleted folder records should be ignored for final output unless a later exception is approved.
- Deleted folders tables should be treated as QA/suppression/rename references, not direct AE import sources.
- Container lookup source blocker is resolved for all three counties; use name ranges and plug container barcode.
- SC Death Names should be imported like any other AE import, using name-range container lookup from the AE export/report.
- Output should use repeated `Description` and `Notes` headers.
- KC mapping and SC metadata normalization are already implemented enough to discuss remaining source decisions.
