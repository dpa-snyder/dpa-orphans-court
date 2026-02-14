# DPA Orphans Court Data Import Context

## Project Overview
Converting Access database records for Orphans Court cases into a format suitable for import into ArchivERA (cloud-based archives CMS). The data includes both adult (deceased) and child records that need to be linked and combined.

## Data Sources

### Original Input Files
1. **NCC Adults.xlsx / NCC Adults.csv** - Adult records (deceased parents) from Access database
   - 5 records total
   - Fields: Record_ID, RG, Series, Dept_Organization, Series_Name, Deceaseds_Last_name, Deceaseds_First_name, Deceaseds_Middle_name, Deceased, Suffix, Begin_Year, End_Year, Number_of_sheets, Comments, DOD, Oversized, Container_Type, size_of_container

2. **NCCChildren.xlsx / NCCChildren.csv** - Child records from Access database
   - 10 records total
   - Fields: Record_ID, Last_Name, First_Name, MiddleName, Suffix, Parents_Last_Name, Parents_First_Name, Childrens_Record_ID, Comments

3. **NCC Orphans Court Containers.csv** - Container information (431 containers)
   - Fields: Record Type, Title, FullDate, Barcode, Location ID
   - Containers organized alphabetically by name range (e.g., "? Sarah to Adamson, John F.")

### Generated Output Files
1. **NCC Orphans Court Combined.xlsx / NCC Orphans Court Combined.csv** - AUTO-GENERATED
   - Combined parent-child records similar to the "less cleaned-up" format
   - Includes automatically matched Barcode and Location ID
   - Ready for manual verification and additional cleanup

2. **Reference Files for Comparison**
   - NCC Orphans Court.xlsx / NCC Orphans Court.csv - Original less cleaned-up version you created
   - NCC Orphans Court - Edited.xlsx / NCC Orphans Court - Edited.csv - Original cleaned-up version you created

## Record Type Categories
The dataset includes the following relationship patterns:
- **1 parent, 1 child** - Record ID 584 (George Bell, no children listed)
- **1 parent, many children** - Record ID 587 (Katie Bell, 5 children)
- **Unknown parent, 1 child** - Record ID 2 (James H. Aaron, child Bertha E. Aaron)
- **Unknown parent, many children** - Record ID 1 (Sarah with no last name, 1 child; no last name)
- **1 parent, no children** - Record ID 38 (Unknown parent, 2 children: Emily Joan Agoos, Susan Julia Agoos)

## Container Matching Algorithm
- **For known parents**: Matches deceased's last name alphabetically to container name ranges
- **For unknown parents**: Matches first child's last name to container name ranges
- Example: "Bell" → Barcode 354198, Location L3.01378 (from container "Beeson, Henry to Bell, Katie")

## Output Format Options

### Option 1: Less Cleaned-Up Version (NCC Orphans Court Combined.csv)
- Adult and children data linked with separate Child 1, Child 2, ... Child 5 columns
- Maintains clear traceability of parent-child relationships
- Includes automatically matched Barcode/Location ID
- **Best for**: Verification and manual cleanup before import

### Option 2: Cleaned-Up Version (NCC Orphans Court - Edited format)
- Data nearly ready for direct import into ArchivERA
- Field mapping already applied
- Deceased name in Title field
- Children names in Description field

## Field Mapping for ArchivERA Import

### Title Field
- **For records with known parent**: Deceased parent's name (e.g., "George Bell", "Katie Bell")
- **For records with unknown parent**: Children's names (e.g., "Sarah", "Emily Joan Agoos and Susan Julia Agoos")

### Description Field
- Children's names (for records with known parent)
- Other relevant details from the original database

### Required ArchivERA Fields (Same Value for All Records)
- **Record Type**: file/item
- **Record Level Name**: file
- **SubGr**: 0
- **Material Types**: Document
- **Set Current Location**: Yes
- **Restrictions on Use**: The material is open for research use.
- **Contributing Institution**: Delaware Public Archives
- **Disposition**: Permanent
- **Status**: on shelf

### Container Information
- **Barcode** - Automatically matched based on deceased/children's last name
- **Location ID** - Automatically matched based on deceased/children's last name
- Can be manually verified/corrected if needed

### Data from Original Database
Most fields from the original Access database are mapped to:
- Description field (for context)
- Notes field (for additional metadata)
- Examples: Number of sheets, Oversized status, Container type, DOD (Date of Death)

## Data Cleanup Tasks (Recommended)
1. ✓ Link parent records to child records
2. ✓ Verify all relationships are correct (especially for unknown parent cases)
3. ✓ Add Barcode and Location ID from container records (automatically done)
4. ⚠ **Manual verification**: Check container matches are correct
5. ⚠ **If needed**: Correct mismatched containers
6. ⚠ Map database fields to final ArchivERA field structure
7. ⚠ Add standard field values for ArchivERA import fields
8. ⚠ Remove verification-only columns before final import

## Known Issues/Notes
- Record 584 (George Bell): Shows no children in both parents and children tables - verify if this is correct
- Record 2 (Aaron): Children table shows child with matching Record_ID but Aaron table has no children names - data appears incomplete
- Record 38: No deceased name in adults table (marked as "Deceased: No") - identified by children names "Emily Joan Agoos" and "Susan Julia Agoos"
- Container matching may need manual verification for edge cases
- Unknown parent records identified by missing last name in adults table

## File Format
- All files available in both **.xlsx** (spreadsheet) and **.csv** (comma-separated values) formats
- CSV files easier for data processing and verification
- Excel files better for manual editing and viewing
