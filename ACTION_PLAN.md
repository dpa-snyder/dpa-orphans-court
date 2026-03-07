# Action Plan

## Phase 1: Scope and Decisions
- [ ] Confirm how to use deleted folders tables for NCC, KC, and SC (suppress, rename, or QA only).
- [ ] Decide whether KC should use `Adults` or `Copy of Adults` as the authoritative table.
- [ ] Confirm scope for SC extra datasets: `4840-002 Death Names`, `4840-000-009 Miscellaneous Orphans Court Minors Files`, and `Paste Errors`.
- [ ] Identify container list sources for KC and SC (barcode/location lookup files).

## Phase 2: Schema and Mapping
- [ ] Define KC-specific column mapping (or a pre-rename step) to match the NCC schema.
- [ ] Decide SubGr defaults for KC and SC (likely `000`).
- [ ] Decide how to normalize SC RG/Series/Dept_Organization/Series_Name outliers (keep vs fold into dominant values).
- [ ] Confirm Notes column policy (two `Notes` columns) and what goes in each for all counties.

## Phase 3: Extraction QA
- [ ] Verify all Access tables are exported for KC and SC (Adults/Children + supplemental tables).
- [ ] Validate leading-zero handling for RG/Series/SubGr and decide if padding should be enforced at export or in script.
- [ ] Compare extracted row counts against Access to ensure completeness.

## Phase 4: Generate AE Outputs
- [ ] Run NCC exports with current script and defaults; produce both `single` and `columns` outputs.
- [ ] Implement KC mapping and generate KC outputs once decisions are finalized.
- [ ] Implement SC normalization rules and generate SC outputs.

## Phase 5: Review and Cleanup
- [ ] Review `_review.csv` flags and resolve container-matching and missing-name cases.
- [ ] Apply deleted folder suppression/rename rules where approved.
- [ ] Confirm Description column counts cover maximum children per county.

## Phase 6: Handoff
- [ ] Validate an AE import using the final output schema.
- [ ] Deliver final CSVs plus findings/report for each county.
