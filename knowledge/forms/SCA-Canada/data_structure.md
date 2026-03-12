# SCA-Canada Forms

This folder contains SCA (Specific Client Audit) localization source files for
Canadian provinces. Files provide occupational health and safety requirements
structured by topic category, regulatory reference, and help text — used as
source material for localization into 38 target languages.

## File Index

| File | Sheet(s) | Description | Province | Region |
|------|----------|-------------|----------|--------|
| British Columbia_For Localization.xlsx | BC Topics, British Columbia, BC Mapping | Safety audit requirements for British Columbia, organized by topic (e.g. Abrasive Blasting, Confined Spaces, Fall Protection). Columns: Category, Requirement (col B), Help Text (col C), Regulatory Reference (col D), URL. Covers 278 requirements across ~60 safety topics mapped to BC OHS Regulation parts and sections. | British Columbia | NORAM |

## Excel File Structure

`British Columbia_For Localization.xlsx` contains three sheets:

| Sheet | Rows | Columns | Purpose |
|-------|------|---------|---------|
| BC Topics | ~1537 | 3 | Full list of all safety topics used in BC audit forms |
| British Columbia | ~279 | 14 | Main localization source: Category / Requirement / Help Text / Regulatory Reference / URL |
| BC Mapping | ~77 | 4 | Maps regulation names to topic names with citation and comments |

### British Columbia Sheet Columns
- **Column A – Category**: Safety topic group (e.g. Abrasive Blasting and High Pressure Washing, Confined Spaces)
- **Column B – Requirement**: Short title of the specific safety requirement *(primary term-mining target)*
- **Column C – Help Text**: Explanatory text describing what the requirement means and how to comply *(primary term-mining target)*
- **Column D – Regulatory Reference**: Citation to BC OHS Regulation part and section
- **Column E – URL**: Link to the relevant WorkSafeBC regulation page
