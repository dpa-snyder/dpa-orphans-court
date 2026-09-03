# Action Plan

Summary: Migrate NCC, KC, and SC Orphans Court data into ArchivERA-ready CSVs using repeated Description/Notes headers, with county-specific mapping, QA, and final import validation.

## Meeting Focus
- [ ] Confirm SC extra dataset scope and `Paste Errors.csv` handling.
- [x] Identify final container list sources with Location IDs for NCC, KC, and SC.
- [ ] Confirm manual handling for review flags and missing-name/container cases.
- [ ] Complete Bryan final-pass checks for row counts and Description column coverage.

## Phase 1: Scope and Decisions
- [x] Treat deleted folders tables as QA/suppression/rename references, not direct AE import sources.
- [x] Decide whether KC should use `Adults` or `Copy of Adults` as the authoritative table.
- [ ] Confirm scope for SC extra datasets: `4840-002 Death Names`, `4840-000-009 Miscellaneous Orphans Court Minors Files`, and `Paste Errors`.
- [x] Identify container list sources for NCC, KC, and SC (barcode/location lookup files).
- [x] Decide whether to merge KC/SC oversize barcode lists into Adults by last+first name match.

## Phase 2: Schema and Mapping
- [x] Define KC-specific column mapping (or a pre-rename step) to match the NCC schema.
- [x] Decide SubGr defaults for KC and SC (likely `000`).
- [x] Decide how to normalize SC RG/Series/Dept_Organization/Series_Name outliers (keep vs fold into dominant values).
- [x] Confirm Notes column policy (two `Notes` columns) and what goes in each for all counties.

## Phase 3: Extraction QA
- [x] Verify all Access tables are exported for KC and SC (Adults/Children + supplemental tables).
- [x] Validate leading-zero handling for RG/Series/SubGr and decide if padding should be enforced at export or in script.
- [ ] Compare extracted row counts against Access to ensure completeness.

## Phase 4: Generate AE Outputs
- [x] Run NCC exports with current script and defaults; produce both single and columns outputs.
- [x] Implement KC mapping and generate KC outputs once decisions are finalized.
- [x] Add the 28 KC `Copy of Adults`-only records and preserve/duplicate KC source barcodes according to the oversized-folder rule.
- [x] Implement SC normalization rules and generate SC outputs.

## Phase 5: Review and Cleanup
- [ ] Review `_review.csv` flags and resolve container-matching and missing-name cases.
- [x] Apply deleted folder suppression/rename rules where approved.
- [ ] Confirm Description column counts cover maximum children per county.

## Phase 6: Handoff
- [ ] Validate an AE import using the final output schema.
- [ ] Deliver final CSVs plus findings/report for each county.

## Resolved Issue Notes

- #11 Container list sources: source blocker resolved for all three counties; use name-range lookup and plug container barcode.
- #20 Oversize barcode handling: do not merge oversize barcode lists by name. KC source barcodes stay on the source row; oversized source-barcoded records get a cross-referenced letter-size companion row when the Legal Upright range barcode differs.

## Open Issue Close Conditions

- #10 SC extra dataset scope: Death Names now in scope as a normal AE import using name-range container lookup; close after client confirms which extra dataset should be ignored and how Miscellaneous Minors/Paste Errors are handled.
- #14 Row count confirmation: counts may be skewed by review rows, e.g. NCC 329; close after CSV counts are accepted or Lindsay confirms excluded review rows.
- #15 Review flags: KC and SC clear enough to process; NCC still needs manual review. Close after KC/SC review files are generated and NCC review dispositions are recorded.
- #17 Description column count: close after final output schema covers the current max children per county: NCC 23, KC 36, SC 20.
- #18 AE import validation: close after ArchivERA accepts a test import or required schema corrections are applied.
- #19 Final delivery: close after final CSVs and county findings/report package are delivered.
