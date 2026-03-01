#!/usr/bin/env python3
"""
Query a forms CSV file and render its content in a readable structure.

Each CSV contains Avetta PQF (Pre-Qualification Form) data with:
  - questionGroup rows (sections/headers)
  - question rows (question text, descriptions, and response options)

Usage:
    python query_form.py <csv_path> [options]

Options:
    --groups            Show only question group names (quick overview)
    --questions         Show groups + question texts only (no response options)
    --search KEYWORD    Show all rows where 'en' column contains KEYWORD (case-insensitive)
    --full              Show everything: groups, questions, descriptions, and all response options
    (default)           Show groups + questions + descriptions (no response options)

Examples:
    python query_form.py knowledge/forms/formId_20115_en_20260223_143543.csv --groups
    python query_form.py knowledge/forms/formId_20042_en_20260223_165924.csv --questions
    python query_form.py knowledge/forms/formId_20042_en_20260223_165924.csv --search "VAT"
    python query_form.py knowledge/forms/formId_40415_en_20260223_165924.csv --full
"""

import csv
import sys
import argparse


def load_csv(path):
    rows = []
    with open(path, encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)
    return rows


def is_response_option(field):
    return field.startswith("responseOption") or field.startswith("link")


def render_form(rows, mode="default", search=None):
    """
    Render form rows according to the selected mode.
    Modes: groups | questions | default | full | search
    """
    if search:
        kw = search.lower()
        matches = [r for r in rows if kw in r["en"].lower()]
        if not matches:
            print(f"No rows found containing '{search}'")
            return
        print(f"=== {len(matches)} rows matching '{search}' ===\n")
        for r in matches:
            print(f"[{r['mongoObject']} / {r['field']}]  {r['en'][:200]}")
        return

    current_group = None
    current_question = None

    for row in rows:
        obj = row["mongoObject"]
        field = row["field"]
        text = row["en"].strip().replace("\\n", "\n")

        if obj == "questionGroup" and field == "questionGroupText":
            current_group = text
            if mode in ("groups", "questions", "default", "full"):
                print(f"\n## {text}")
            current_question = None

        elif obj == "question":
            if field == "questionText":
                current_question = text
                if mode in ("questions", "default", "full"):
                    print(f"  Q: {text[:150]}")

            elif field == "description":
                if mode in ("default", "full"):
                    print(f"     (desc) {text[:150]}")

            elif is_response_option(field):
                if mode == "full":
                    print(f"       - [{field}] {text[:100]}")


def main():
    parser = argparse.ArgumentParser(description="Query a forms CSV file")
    parser.add_argument("csv_path", help="Path to the CSV file")
    parser.add_argument("--groups", action="store_true", help="Show only question group names")
    parser.add_argument("--questions", action="store_true", help="Show groups + question texts")
    parser.add_argument("--full", action="store_true", help="Show everything including response options")
    parser.add_argument("--search", metavar="KEYWORD", help="Search for keyword in all row text")
    args = parser.parse_args()

    try:
        rows = load_csv(args.csv_path)
    except FileNotFoundError:
        print(f"Error: File not found: {args.csv_path}")
        sys.exit(1)

    # Determine mode
    if args.search:
        mode = "search"
    elif args.groups:
        mode = "groups"
    elif args.questions:
        mode = "questions"
    elif args.full:
        mode = "full"
    else:
        mode = "default"

    # Print header
    form_id = None
    form_name = None
    for r in rows:
        if r["mongoObject"] == "questionGroup" and r["field"] == "questionGroupText":
            form_name = r["en"].strip()
            form_id = r.get("formDisplayId", "")
            break

    print(f"Form ID : {form_id or 'unknown'}")
    print(f"Name    : {form_name or 'unknown'}")
    print(f"Mode    : {mode}")
    print(f"Rows    : {len(rows)}")
    print("=" * 60)

    render_form(rows, mode=mode, search=args.search)


if __name__ == "__main__":
    main()
