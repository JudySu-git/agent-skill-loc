---
name: forms-kb
description: "Retrieves and answers questions about Avetta PQF (Pre-Qualification Form) content stored in knowledge/forms/ as CSV files. 96 forms covering company information for 70+ countries plus client-specific forms (SOLV Energy, Vantage Data Centers, Caterpillar, etc.). Each CSV contains question groups, questions, descriptions, and response options in English. Use when users ask: what questions are in a specific form, what response options exist, which forms cover a topic (VAT, tax ID, company seal, safety, industry codes), what a country-specific form asks, or any question about PQF form content."
---

# Forms Knowledge Base (forms-kb)

## Data Overview

- **Location**: `knowledge/forms/` (96 CSV files)
- **Naming**: `formId_{ID}_en_{date}.csv`
- **Index**: `knowledge/forms/data_structure.md` — complete table of all 96 forms with ID, name, and description

### CSV Schema

| Column | Values | Purpose |
|--------|--------|---------|
| `mongoObject` | `questionGroup` / `question` | Row type |
| `field` | `questionGroupText` / `questionText` / `description` / `responseOption*` | Content type |
| `formDisplayId` | e.g. `20115` | Matches the ID in the filename |
| `en` | text | English content |

## Retrieval Workflow

### Step 1: Identify target form(s)

Read `knowledge/forms/data_structure.md` to match the user query to form IDs by:
- Country name (e.g. "UK" -> formId 20115, "Brazil" -> formId 20177 or 20042)
- Client name (e.g. "SOLV Energy" -> formId 40415, "Vantage" -> formId 47567/47569/47570)
- Topic keywords in the description column (e.g. "safety" -> formId 14000)

### Step 2a: Single-form content query

Run `scripts/query_form.py` with the appropriate mode:

```bash
# Quick overview of sections
python3 .agent/skills/forms-kb/scripts/query_form.py knowledge/forms/formId_20115_en_20260223_143543.csv --groups

# All questions (no response options) -- good for "what does this form ask?"
python3 .agent/skills/forms-kb/scripts/query_form.py knowledge/forms/formId_20115_en_20260223_143543.csv --questions

# Search for specific topic within one form
python3 .agent/skills/forms-kb/scripts/query_form.py knowledge/forms/formId_20042_en_20260223_165924.csv --search "legal name"

# Full content including all response options -- use for "what are the options for X?"
python3 .agent/skills/forms-kb/scripts/query_form.py knowledge/forms/formId_40415_en_20260223_165924.csv --full
```

### Step 2b: Cross-form search (topic appears in multiple forms)

Use Grep across all CSVs when the user asks "which forms ask about X" or "find all forms that mention Y":

- Use the Grep tool: pattern=KEYWORD, path="knowledge/forms", glob="*.csv", output_mode="files_with_matches"
- Then for each matching file, run `query_form.py --search KEYWORD` to see context

### Step 3: Answer the user

Summarize findings with:
- Form ID and name as source reference
- Relevant question text and response options
- If cross-form: list which forms contain the topic and what they ask

## Common Query Patterns

| User asks | Strategy |
|-----------|----------|
| "What questions are in the [country] form?" | Find form in data_structure.md, run --questions |
| "What response options does [question] have?" | Find form, run --full or --search [topic] |
| "Which forms ask about VAT?" | Grep across CSVs, then --search VAT per match |
| "What does form 20042 cover?" | --groups for overview, then --questions |
| "List all question groups in the Brazil form?" | Find formId 20177, run --groups |
| "What does the safety form ask?" | formId 14000, run --full (only 4 rows) |

## Finding the Right CSV File

Given a form ID from `data_structure.md`, find the exact filename with:

```bash
ls knowledge/forms/formId_{ID}_*.csv
```

If multiple files exist for the same ID (different dates), use the most recent date.

## Notes

- The `en` column may contain HTML tags and backslash-n -- treat as plain text
- `responseOption` keys use country codes (e.g. `responseOptionUS`) or numbers (`responseOption1`)
- Form 20042 (General Company Information) is the largest with 63 questions -- prefer --questions over --full
- Always read `data_structure.md` first instead of scanning filenames -- it has all form IDs, names, and descriptions pre-indexed
