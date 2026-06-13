# Action Plan

Summary: Migrate NCC, KC, and SC Orphans Court data into ArchivERA-ready CSVs using repeated Description/Notes headers, with county-specific mapping, QA, and final import validation.

## Meeting Focus
- [ ] Confirm SC extra dataset scope and `Paste Errors.csv` handling.
- [ ] Identify final container list sources with Location IDs for NCC, KC, and SC.
- [ ] Confirm manual handling for review flags and missing-name/container cases.
- [ ] Complete Bryan final-pass checks for row counts and Description column coverage.

## Phase 1: Scope and Decisions
- [x] Treat deleted folders tables as QA/suppression/rename references, not direct AE import sources.
- [x] Decide whether KC should use `Adults` or `Copy of Adults` as the authoritative table.
- [ ] Confirm scope for SC extra datasets: `4840-002 Death Names`, `4840-000-009 Miscellaneous Orphans Court Minors Files`, and `Paste Errors`.
- [ ] Identify container list sources for NCC, KC, and SC (barcode/location lookup files).
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
- [x] Implement SC normalization rules and generate SC outputs.

## Phase 5: Review and Cleanup
- [ ] Review `_review.csv` flags and resolve container-matching and missing-name cases.
- [x] Apply deleted folder suppression/rename rules where approved.
- [ ] Confirm Description column counts cover maximum children per county.

## Phase 6: Handoff
- [ ] Validate an AE import using the final output schema.
- [ ] Deliver final CSVs plus findings/report for each county.

## Open Issue Close Conditions

- #10 SC extra dataset scope: close after client confirms Death Names, Miscellaneous Orphans Court Minors Files, and `Paste Errors.csv` handling.
- #11 Container list sources: close after final barcode/location lookup source files are received, reviewed, and accepted.
- #14 Row count confirmation: close after Bryan verifies Access/source row counts, or raw sources are available and a fresh count check is rerun.
- #15 Review flags: close after manual dispositions are recorded for `_review.csv` flags and accepted corrections are applied or deferred.
- #17 Description column count: close after final output schema covers the current max children per county: NCC 23, KC 36, SC 20.
- #18 AE import validation: close after ArchivERA accepts a test import or required schema corrections are applied.
- #19 Final delivery: close after final CSVs and county findings/report package are delivered.
