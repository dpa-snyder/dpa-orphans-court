# Client Questions

## Decision Order

1. [ ] KC/SC: Where are the final container list sources with Location IDs?
2. [ ] SC: Are the 7 chancery-type Miscellaneous Orphans Court Minors Files out of scope?
3. [ ] SC: What should happen to the 5 unaccounted Miscellaneous Orphans Court Minors Files records?
4. [ ] SC: Should Death Names become separate/skeleton records linked to matching orphan records?
5. [ ] SC: How should the single `Paste Errors.csv` row be handled?
6. [ ] NCC: Where should the NCC container list come from?
7. [ ] NCC: Is `work to be done1.xlsx` still relevant?

## Confirmed/Mostly Settled

- KC uses `Adults` as authoritative, then adds the 28 records found only in `Copy of Adults`.
- KC and SC oversize barcode lists should stay as separate oversize records, with barcode cross-references back to the related Adults records.
- KC and SC should keep `000` as the SubGr default where source data has no SubGr.
- Deleted folder records should be ignored for final output unless a later exception is approved.
- Deleted folders tables should be treated as QA/suppression/rename references, not direct AE import sources.
- Output should use repeated `Description` and `Notes` headers.
- KC mapping and SC metadata normalization are already implemented enough to discuss remaining source decisions.
