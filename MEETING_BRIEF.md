# Meeting Brief - Lindsay Findings and Questions

Purpose: walk through the remaining decisions in the order they unblock migration work.

## Dashboard Workflow

- Use the HTML dashboard checklist as the live view.
- A checked box means the matching GitHub issue is closed.
- To check off an open item, open the linked issue, paste/add the meeting note, and close it in GitHub.
- Items without a matching issue get a prefilled "New issue" link from the dashboard.

## Recommended Discussion Order

1. [ ] **Scope decisions**
   - KC: choose authoritative Adults table (`Adults` vs `Copy of Adults`).
   - SC: decide whether `4840-002 Death Names`, `4840-000-009 Miscellaneous Orphans Court Minors Files`, and `Paste Errors.csv` are in scope for AE import.

2. [ ] **Container and barcode strategy**
   - Identify county container list sources, especially KC and SC Location ID sources.
   - Decide whether to merge oversize barcode lists into county Adults records by last+first name match.

3. [ ] **Deleted folders policy**
   - Confirm deleted folder tables are QA/suppression/rename references, not direct AE import sources.
   - Decide who applies approved suppression/rename rules before final output.

4. [ ] **County metadata defaults and normalization**
   - KC and SC: confirm SubGr default of `000` where source data has no SubGr.
   - SC: confirm normalization of obvious RG/Series/Dept_Organization/Series_Name outliers to dominant values.

5. [ ] **Data completeness and review flags**
   - Compare extracted row counts against Access if needed.
   - Review missing-name and container-matching flags in `_review.csv`.

6. [ ] **AE import validation**
   - Confirm repeated `Description` and `Notes` headers are accepted.
   - Validate final Description column count covers the max children per county.

## Client Questions

1. [ ] KC: Which table should be authoritative for Adults, `Adults` or `Copy of Adults`?
2. [ ] KC/SC: Should oversize barcode lists be merged into Adults by last+first name match?
3. [ ] KC/SC: Where are the final container list sources with Location IDs?
4. [ ] SC: Are `4840-002 Death Names` and `4840-000-009 Miscellaneous Orphans Court Minors Files` in scope for AE import?
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
- Oversize barcode list has 1,378 rows; 1,145 match KC Adults by last+first name.
- No KC container list or Location ID source found in exports.

### Sussex County
- Adults: 7,510; Children: 16,909; Paste Errors: 1; Death Names: 626; Deleted folders: 927; Misc minors: 37.
- Max children for one adult: 20.
- One child record has no matching Adult.
- Metadata has apparent outliers/typos, especially Series values.
- Oversize barcode list has 2,351 rows; 1,975 match SC Adults by last+first name.
- No SC container list or Location ID source found in exports.

## Current Issue Status

- Closed: KC mapping, SC normalization, table exports, leading-zero handling, NCC output generation, deleted folders policy, Notes policy.
- Open: KC authoritative table, SC scope, container list sources, oversize barcode merge, SubGr defaults, row count confirmation, review flags, deleted folder rule application, Description column count, AE import validation, final delivery.
