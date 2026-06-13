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
   - Deleted folders: ignore these folders for final output unless a later exception is approved.

2. [ ] **SC extra dataset scope**
   - Death Names: create separate/skeleton records connected to the matching orphan record where enough identifying data overlaps; do not merge into one record because they represent separate physical things.
   - Miscellaneous Orphans Court Minors Files: confirm whether the 7 chancery-type records are out of scope and decide what to do with the 5 unaccounted records.
   - `Paste Errors.csv`: confirm whether the single row belongs in final output or manual exception handling.

3. [ ] **Container source strategy**
   - Identify county container list sources, especially KC and SC Location ID sources.
   - Confirm whether NCC has a final container list outside the Access database.

4. [x] **County metadata defaults and normalization**
   - SC: confirm normalization of obvious RG/Series/Dept_Organization/Series_Name outliers to dominant values.

5. [ ] **Data completeness and review flags**
   - Compare extracted row counts against Access if needed.
   - Review missing-name and container-matching flags in `_review.csv`.

6. [ ] **AE import validation**
   - Confirm repeated `Description` and `Notes` headers are accepted.
   - Validate final Description column count covers the max children per county.

## Client Questions

1. [ ] KC/SC: Where are the final container list sources with Location IDs?
2. [ ] SC: Are the 7 chancery-type Miscellaneous Orphans Court Minors Files out of scope?
3. [ ] SC: What should happen to the 5 unaccounted Miscellaneous Orphans Court Minors Files records?
4. [ ] SC: Should Death Names become separate/skeleton records linked to matching orphan records?
5. [ ] SC: How should the single `Paste Errors.csv` row be handled?
6. [ ] NCC: Where should the NCC container list come from?
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
- Oversize barcode list has 1,378 rows; 1,145 match KC Adults by last+first name.
- Decision recorded: do not merge oversize rows into Adults by name match; create separate oversize records and cross-reference barcode.
- No KC container list or Location ID source found in exports.

### Sussex County
- Adults: 7,510; Children: 16,909; Paste Errors: 1; Death Names: 626; Deleted folders: 927; Misc minors: 37.
- Max children for one adult: 20.
- One child record has no matching Adult.
- Metadata has apparent outliers/typos, especially Series values.
- Oversize barcode list has 2,351 rows; 1,975 match SC Adults by last+first name.
- Decision recorded: do not merge oversize rows into Adults by name match; create separate oversize records and cross-reference barcode.
- Death Names direction: create separate/skeleton records linked to matching orphan records where identifiers overlap; do not merge them into the orphan record.
- Misc minors still need client decision: 7 chancery-type records and 5 unaccounted records.
- No SC container list or Location ID source found in exports.

## Current Issue Status

- Closed: KC authoritative table, oversize barcode handling, SubGr default, deleted folder handling.
- Still open for meeting: SC extra dataset scope, container list sources, row count confirmation, review flags, Description column count, AE import validation, final delivery.

## Remaining Open Issues And Close Conditions

### #10 - SC extra dataset scope
- Current evidence: Death Names should not be merged into orphan records; they likely need separate/skeleton records linked where identifiers overlap.
- Current evidence: Miscellaneous Orphans Court Minors Files has 7 chancery-type records and 5 unaccounted records that need Brittany/Lindsay direction.
- Current evidence: `Paste Errors.csv` has one row that needs manual disposition.
- Close when: client confirms which SC extra datasets/rows are in AE import scope and how Death Names, Misc minors, and Paste Errors should be represented.

### #11 - Container list sources
- Current evidence: no final NCC, KC, or SC Location ID source is present in the repo or Access-export findings.
- Current note: Lindsay is sending/resending source files and they need manual review.
- Close when: final barcode/location lookup source files are received, reviewed, and accepted for output generation.

### #14 - Row count confirmation
- Current evidence from findings: NCC Adults 10,853 / Children 25,540; KC Adults 6,251 / Children 17,135 / Copy of Adults 6,261; SC Adults 7,510 / Children 16,909 plus supplemental tables.
- Repo limitation: raw CSV/Access source files are not committed in this checkout, so final Access re-count cannot be independently rerun from this repo alone.
- Close when: Bryan verifies extracted row counts against Access/source files, or source files are available and a fresh count check is rerun.

### #15 - Review flags
- Current note: flagged missing-name/container-matching cases need manual disposition, not automated guessing.
- Close when: manual decisions are recorded for `_review.csv` flags and any accepted corrections are applied or explicitly deferred.

### #17 - Description column count
- Current evidence: max children per adult are NCC 23, KC 36, and SC 20.
- Close when: final output schema is verified to include enough repeated `Description` columns for each county, with KC's 36-child maximum as the current high-water mark.

### #18 - AE import validation
- Close when: ArchivERA accepts a test import using the final repeated `Description`/`Notes` schema, or any required schema corrections are documented and applied.

### #19 - Final delivery
- Close when: final CSVs plus county findings/report package are delivered after AE import validation is complete.
