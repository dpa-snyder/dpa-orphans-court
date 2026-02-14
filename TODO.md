# TODO

## Completed
- [x] Parse and link Adults + Children by Record_ID
- [x] Container matching via alphabetical surname lookup
- [x] ArchivERA 30-column output format
- [x] Foundling handling (alternate description pattern)
- [x] RG/Series zero-padding (4-digit / 3-digit)
- [x] CLI defaults for missing metadata
- [x] Review file generation for flagged records
- [x] Verified output against gold standard (NCC Orphans Court - Edited.csv)

## In Progress
- [ ] Test with full NCC dataset (thousands of records)
- [ ] Validate container matching accuracy at scale

## Pending
- [ ] Kent County (KC) migration — 211 containers
- [ ] Sussex County (SC) migration — 289 containers
- [ ] Foundling container matching — revisit with larger dataset (currently flagged for manual review)
- [ ] Oversized record handling — verify OS Barcode column mapping (see notes.md)
- [ ] Column mapping config for KC/SC if schemas differ from NCC
- [ ] Final ArchivERA import validation (confirm field names match import spec)
