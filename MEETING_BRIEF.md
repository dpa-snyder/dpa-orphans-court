# Meeting Brief - Lindsay Findings and Questions

Purpose: walk through the remaining decisions in the order they unblock migration work.

## Dashboard Workflow

- Use the HTML dashboard checklist as the live view.
- A checked box means the matching GitHub issue is closed.
- To check off an open item, open the linked issue, paste/add the meeting note, and close it in GitHub.
- Items without a matching issue get a prefilled "New issue" link from the dashboard.

## Recommended Discussion Order

1. [x] **Decisions already recorded**
   - KC: use `Adults` as the authoritative table, then add the 28 records found only in `Copy of Adults`.
   - KC/SC: keep SubGr default as `000` where source data has no SubGr.
   - KC/SC: do not merge oversize barcode lists into Adults by name match; create separate oversize records and cross-reference the barcode.
   - KC: source barcodes are preserved. For oversized source-barcoded records, add a letter-size companion row using the Legal Upright name-range barcode when it differs from the source barcode.
   - Deleted folders: ignore these folders for final output unless a later exception is approved.

2. [ ] **SC extra dataset scope**
   - Death Names: import like any other AE import; container data is already in AE export/report and should use the same name-range lookup treatment.
   - Miscellaneous Orphans Court Minors Files: confirm whether the 7 chancery-type records are out of scope and decide what to do with the 5 unaccounted records.
   - Clarify which extra dataset is covered by the note: "Nothing to be done, ignore this data set."
   - `Paste Errors.csv`: confirm whether the single row belongs in final output or manual exception handling.

3. [x] **Container source strategy**
   - Source blocker is resolved for all three counties.
   - Find items by name range and plug the container barcode.

4. [x] **County metadata defaults and normalization**
   - SC: confirm normalization of obvious RG/Series/Dept_Organization/Series_Name outliers to dominant values.

5. [ ] **Data completeness and review flags**
   - Compare extracted row counts against Access if needed.
   - Review missing-name and container-matching flags in `_review.csv`.

6. [ ] **AE import validation**
   - Confirm repeated `Description` and `Notes` headers are accepted.
   - Validate final Description column count covers the max children per county.

## Client Questions

1. [ ] SC: Which extra dataset is covered by "Nothing to be done, ignore this data set"?
2. [ ] SC: Are the 7 chancery-type Miscellaneous Orphans Court Minors Files out of scope?
3. [ ] SC: What should happen to the 5 unaccounted Miscellaneous Orphans Court Minors Files records?
4. [ ] SC: How should the single `Paste Errors.csv` row be handled?
5. [ ] Row counts: should counts be compared to CSV counts, or should Lindsay exclude review rows first?
6. [ ] NCC: What manual review decisions remain after processing?
7. [ ] NCC: Is `work to be done1.xlsx` still relevant?

## Evidence By County

### New Castle County
- Adults: 10,853; Children: 25,540; Deleted folders: 807.
- Max children for one adult: 23.
- Adults with Barcode present: 39.
- Deleted folders match existing adult/child/renamed records often enough to use as QA/reference.
- Container list is not in the NCC Access database.

### Kent County
- Adults: 6,251; Children: 17,135; Copy of Adults: 6,261; Deleted folders: 722.
- Max children for one adult: 36.
- `Adults` vs `Copy of Adults`: 28 IDs only in copy, 18 only in Adults, and 3,094 shared IDs with at least one differing value.
- Decision recorded: use `Adults` as authoritative, then add the 28 records found only in `Copy of Adults`.
- September 3 workbook update: `KC Copy of Adults Missing from Adults.xlsx` supplies the 28 copy-only records. Two of those 28 have source barcodes, and both already match their Legal Upright name range.
- Zip-original output evidence: 143 KC Adults rows already had source barcodes; 129 are marked oversized and 14 are not.
- Output rule: keep every source barcode. For the 129 oversized source-barcoded rows, add a same-Record_ID letter-size companion row when the Legal Upright range barcode differs from the source barcode; 128 companion rows are added and 3 source barcodes already match the range.
- Oversize barcode list has 1,378 rows; 1,145 match KC Adults by last+first name.
- Decision recorded: do not merge oversize rows into Adults by name match; create separate oversize records and cross-reference barcode.
- No KC container list or Location ID source found in exports.
- September 3 update: container source blocker is resolved; use name ranges and plug container barcode.

### Sussex County
- Adults: 7,510; Children: 16,909; Paste Errors: 1; Death Names: 626; Deleted folders: 927; Misc minors: 37.
- Max children for one adult: 20.
- One child record has no matching Adult.
- Metadata has apparent outliers/typos, especially Series values.
- Oversize barcode list has 2,351 rows; 1,975 match SC Adults by last+first name.
- Decision recorded: do not merge oversize rows into Adults by name match; create separate oversize records and cross-reference barcode.
- Death Names direction: import like any other AE import; file/item info is in the SC Death Names MDB and container data comes from the AE export/report.
- Misc minors still need client decision: 7 chancery-type records and 5 unaccounted records.
- No SC container list or Location ID source found in exports.
- September 3 update: container source blocker is resolved; use name ranges and plug container barcode.

## Current Issue Status

- Closed: KC authoritative table, oversize barcode handling, SubGr default, deleted folder handling, container source identification.
- Still open for meeting: SC extra dataset scope, row count confirmation, review flags, Description column count, AE import validation, final delivery.

## Recently Resolved Issue Notes

### #11 - Container list sources
- Status: resolved September 3.
- Current note: source blocker is done for all three counties.
- Treatment: find item by name range and plug container barcode.

## Remaining Open Issues And Close Conditions

### #10 - SC extra dataset scope
- Current evidence: Death Names should be imported like any other AE import; container data is already in AE export/report and should use name-range lookup.
- Current evidence: Miscellaneous Orphans Court Minors Files has 7 chancery-type records and 5 unaccounted records that need Brittany/Lindsay direction.
- Current evidence: `Paste Errors.csv` has one row that needs manual disposition.
- Open question: which extra dataset is covered by "Nothing to be done, ignore this data set"?
- Close when: client confirms which SC extra datasets/rows are ignored or imported, and how Misc minors/Paste Errors should be represented.

### #14 - Row count confirmation
- Current evidence from findings: NCC Adults 10,853 / Children 25,540; KC Adults 6,251 / Children 17,135 / Copy of Adults 6,261; SC Adults 7,510 / Children 16,909 plus supplemental tables.
- Current note: counts may be skewed by review rows, e.g. NCC 329.
- Close when: CSV counts are accepted as comparison target, or Lindsay confirms excluded review rows before final comparison.

### #15 - Review flags
- Current note: KC and SC are clear enough to process.
- Current note: NCC has review work because it was processed already.
- Next step: process KC and SC to create review files for Lindsay.
- Close when: KC/SC review files exist and NCC manual review dispositions are recorded.

### #17 - Description column count
- Current evidence: max children per adult are NCC 23, KC 36, and SC 20.
- Close when: final output schema is verified to include enough repeated `Description` columns for each county, with KC's 36-child maximum as the current high-water mark.

### #18 - AE import validation
- Close when: ArchivERA accepts a test import using the final repeated `Description`/`Notes` schema, or any required schema corrections are documented and applied.

### #19 - Final delivery
- Close when: final CSVs plus county findings/report package are delivered after AE import validation is complete.
