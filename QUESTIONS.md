# Migration Script — Resolved Decisions & Open Items

## Resolved Decisions

1. **Foundlings** are a defined record category with their own Description field pattern:
   - Description (col 1): foundling comment (e.g. "Foundling, parents unknown")
   - Description (col 2): Deceased status
   - Description (col 5): child comment
   - Description (col 6): Number of sheets

2. **Middle name formatting**: Full middle names preserved as-is (e.g. "Clay", "Joan"); single-letter initials get a period (e.g. "J" -> "J.").

3. **RG/Series/Dept_Org/Series_Name** vary per county/collection — always pulled from source data, with CLI defaults as fallback when source is empty.

4. **Number padding**: RG = 4 digits with leading zeros. SubGr, Series, SubSeries = 3 digits with leading zeros.

5. **Children in Description (single format)**: Only listed when Deceased=Yes. When Deceased=No and children appear in the Title, they are not repeated in Description.

6. **"Children: none"**: Shown in the children-list Description column (single format) when Deceased=Yes but no children are linked.

7. **Repeated header names**: AE reference files use duplicate `Description`/`Notes` header names (no numbering). Output headers should mirror that pattern.

## Open Items (revisit with larger dataset)

1. **Foundling container matching**: Records with no last name (e.g. Sarah) cannot be auto-matched to containers. Currently flagged for manual review. The "? Sarah to Adamson" container may be a pattern, but needs more data to confirm.

2. **Container matching edge cases**: Some names may fall between container ranges or match ambiguously. The script flags these for review.

3. **ArchivERA field name**: The target system is ArchivERA (cloud-based archives CMS). The gold standard CSV column header uses "Deceaseds_ Last_name" (with space) — verify this is the correct ArchivERA import field name.
