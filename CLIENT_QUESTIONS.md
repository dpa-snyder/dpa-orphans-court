# Client Questions

## Decision Order

1. [ ] KC: Which table should be authoritative for Adults, `Adults` or `Copy of Adults`?
2. [ ] KC/SC: Where are the final container list sources with Location IDs?
3. [ ] KC/SC: Should oversize barcode lists be merged into Adults by last+first name match?
4. [ ] SC: Are `4840-002 Death Names` and `4840-000-009 Miscellaneous Orphans Court Minors Files` in scope for AE import?
5. [ ] SC: How should the single `Paste Errors.csv` row be handled?
6. [ ] NCC: Where should the NCC container list come from?
7. [ ] NCC: Is `work to be done1.xlsx` still relevant?

## Confirmed/Mostly Settled

- Deleted folders tables should be treated as QA/suppression/rename references, not direct AE import sources.
- Output should use repeated `Description` and `Notes` headers.
- KC mapping and SC metadata normalization are already implemented enough to discuss remaining source decisions.
