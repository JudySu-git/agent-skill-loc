#!/usr/bin/env python3
"""
Grammar and typo checker for all forms CSVs.
Checks the 'en' column (or any text column) for common issues.
"""

import csv
import os
import re
import sys
from pathlib import Path

FORMS_DIR = Path(__file__).parent

# ── Text column names to check ───────────────────────────────────────────────
TEXT_COLS = {"en", "uk_ua"}

# ── Skip response options (country lists etc) – too many false positives ──────
SKIP_FIELDS_PREFIXES = ("responseOption",)

# ── Typo dictionary: (pattern, replacement, note) ─────────────────────────────
# Use regex patterns for flexibility. $WORD$ means surrounded by word boundaries.
TYPOS = [
    # Common misspellings
    (r"\brecieve\b", "receive", "Misspelling"),
    (r"\brecieved\b", "received", "Misspelling"),
    (r"\brecieving\b", "receiving", "Misspelling"),
    (r"\boccured\b", "occurred", "Misspelling"),
    (r"\boccurence\b", "occurrence", "Misspelling"),
    (r"\boccurences\b", "occurrences", "Misspelling"),
    (r"\bseperate\b", "separate", "Misspelling"),
    (r"\bseparetely\b", "separately", "Misspelling"),
    (r"\bseperation\b", "separation", "Misspelling"),
    (r"\badress\b", "address", "Misspelling"),
    (r"\badresses\b", "addresses", "Misspelling"),
    (r"\bsubmittal\b", "submission", "Non-standard; prefer 'submission'"),
    (r"\bdefinately\b", "definitely", "Misspelling"),
    (r"\bdefinatly\b", "definitely", "Misspelling"),
    (r"\bexistance\b", "existence", "Misspelling"),
    (r"\bgoverment\b", "government", "Misspelling"),
    (r"\bgovernement\b", "government", "Misspelling"),
    (r"\bresponsable\b", "responsible", "Misspelling"),
    (r"\bsupervison\b", "supervision", "Misspelling"),
    (r"\bsupervison\b", "supervision", "Misspelling"),
    (r"\bsubcontactor\b", "subcontractor", "Misspelling"),
    (r"\bsubconractor\b", "subcontractor", "Misspelling"),
    (r"\bcontacter\b", "contactor", "Misspelling"),
    (r"\bpriorty\b", "priority", "Misspelling"),
    (r"\bpriority\b", "priority", "Check: verify correct"),
    (r"\bconpany\b", "company", "Misspelling"),
    (r"\bcomapny\b", "company", "Misspelling"),
    (r"\bcomapnies\b", "companies", "Misspelling"),
    (r"\binsurrance\b", "insurance", "Misspelling"),
    (r"\binsurnace\b", "insurance", "Misspelling"),
    (r"\bcertifcate\b", "certificate", "Misspelling"),
    (r"\bcertificate's\b", "certificate's", "Check apostrophe"),
    (r"\bproceedure\b", "procedure", "Misspelling"),
    (r"\bprocedure's\b", "procedure's", "Check apostrophe"),
    (r"\bproccedure\b", "procedure", "Misspelling"),
    (r"\bpolicies's\b", "policies'", "Incorrect apostrophe"),
    (r"\bemploy ee\b", "employee", "Spacing"),
    (r"\b(teh) \b", "the", "Misspelling"),
    (r"\bthier\b", "their", "Misspelling"),
    (r"\byour'e\b", "you're", "Misspelling"),
    (r"\bits'\b", "its'", "Check: possessive vs contraction"),
    (r"\bcompaines\b", "companies", "Misspelling"),
    (r"\bsubmited\b", "submitted", "Misspelling"),
    (r"\bsubmiting\b", "submitting", "Misspelling"),
    (r"\bemployeed\b", "employed", "Misspelling"),
    (r"\bemployeed\b", "employed", "Misspelling"),
    (r"\batleast\b", "at least", "Should be two words"),
    (r"\baleast\b", "at least", "Should be two words"),
    (r"\balot\b", "a lot", "Should be two words"),
    (r"\baccording\b", "according", "Verify usage"),
    (r"\battatch\b", "attach", "Misspelling"),
    (r"\battatched\b", "attached", "Misspelling"),
    (r"\battatching\b", "attaching", "Misspelling"),
    (r"\bverifyication\b", "verification", "Misspelling"),
    (r"\bverificaiton\b", "verification", "Misspelling"),
    (r"\bverificaton\b", "verification", "Misspelling"),
    (r"\bindivdual\b", "individual", "Misspelling"),
    (r"\bindivduals\b", "individuals", "Misspelling"),
    (r"\bcontarctor\b", "contractor", "Misspelling"),
    (r"\bcontarcor\b", "contractor", "Misspelling"),
    (r"\bcontractor s\b", "contractors", "Spacing"),
    (r"\bsaftey\b", "safety", "Misspelling"),
    (r"\bsafety and health\b", "Safety and Health", "Check capitalization"),
    (r"\bhealth and safety\b", "Health and Safety", "Check capitalization"),
    (r"\bworplace\b", "workplace", "Misspelling"),
    (r"\bworkpalce\b", "workplace", "Misspelling"),
    (r"\bworkpace\b", "workplace", "Misspelling"),
    (r"\bregualtion\b", "regulation", "Misspelling"),
    (r"\bregulations'\b", "regulations'", "Check apostrophe"),
    (r"\bcompiance\b", "compliance", "Misspelling"),
    (r"\bcomplaince\b", "compliance", "Misspelling"),
    (r"\btraning\b", "training", "Misspelling"),
    (r"\btraiing\b", "training", "Misspelling"),
    (r"\bhazadous\b", "hazardous", "Misspelling"),
    (r"\bhazardous\b", "hazardous", "Verify"),
    (r"\binformation\b", "information", "Verify"),
    (r"\bincident s\b", "incidents", "Spacing"),
    (r"\bregistartion\b", "registration", "Misspelling"),
    (r"\bregistation\b", "registration", "Misspelling"),
    (r"\bregistraion\b", "registration", "Misspelling"),
    (r"\borganisation\b", "organization", "UK vs US spelling (if US context)"),
    (r"\borganisations\b", "organizations", "UK vs US spelling (if US context)"),
    (r"\blicence\b", "license", "UK vs US spelling (if US context)"),
    (r"\blicenced\b", "licensed", "UK vs US spelling (if US context)"),
    (r"\bauthorise\b", "authorize", "UK vs US spelling (if US context)"),
    (r"\bauthorised\b", "authorized", "UK vs US spelling (if US context)"),
    (r"\brecognise\b", "recognize", "UK vs US spelling (if US context)"),
    (r"\brecognised\b", "recognized", "UK vs US spelling (if US context)"),
    # Specific known issues
    (r"\bEDPROU\b", "EDRPOU", "Acronym typo (seen in English source text)"),
    (r"\bEdprou\b", "EDRPOU", "Acronym typo"),
]

# Remove false positives from TYPOS (patterns that match too broadly)
REAL_TYPOS = [
    (r"\brecieve\b", "receive", "Misspelling"),
    (r"\brecieved\b", "received", "Misspelling"),
    (r"\brecieving\b", "receiving", "Misspelling"),
    (r"\boccured\b", "occurred", "Misspelling"),
    (r"\boccurence\b", "occurrence", "Misspelling"),
    (r"\boccurences\b", "occurrences", "Misspelling"),
    (r"\bseperate\b", "separate", "Misspelling"),
    (r"\bseparetely\b", "separately", "Misspelling"),
    (r"\bseperation\b", "separation", "Misspelling"),
    (r"\bdefinately\b", "definitely", "Misspelling"),
    (r"\bdefinatly\b", "definitely", "Misspelling"),
    (r"\bexistance\b", "existence", "Misspelling"),
    (r"\bgoverment\b", "government", "Misspelling"),
    (r"\bgovernement\b", "government", "Misspelling"),
    (r"\bresponsable\b", "responsible", "Misspelling"),
    (r"\bsupervison\b", "supervision", "Misspelling"),
    (r"\bsubcontactor\b", "subcontractor", "Misspelling"),
    (r"\bsubconractor\b", "subcontractor", "Misspelling"),
    (r"\binsurrance\b", "insurance", "Misspelling"),
    (r"\binsurnace\b", "insurance", "Misspelling"),
    (r"\bcertifcate\b", "certificate", "Misspelling"),
    (r"\bproceedure\b", "procedure", "Misspelling"),
    (r"\bproccedure\b", "procedure", "Misspelling"),
    (r"\bthier\b", "their", "Misspelling"),
    (r"\bcompaines\b", "companies", "Misspelling"),
    (r"\bsubmited\b", "submitted", "Misspelling"),
    (r"\bsubmiting\b", "submitting", "Misspelling"),
    (r"\battatch\b", "attach", "Misspelling"),
    (r"\battatched\b", "attached", "Misspelling"),
    (r"\battatching\b", "attaching", "Misspelling"),
    (r"\bverifyication\b", "verification", "Misspelling"),
    (r"\bverificaiton\b", "verification", "Misspelling"),
    (r"\bverificaton\b", "verification", "Misspelling"),
    (r"\bindivdual\b", "individual", "Misspelling"),
    (r"\bindivduals\b", "individuals", "Misspelling"),
    (r"\bcontarctor\b", "contractor", "Misspelling"),
    (r"\bcontarcor\b", "contractor", "Misspelling"),
    (r"\bsaftey\b", "safety", "Misspelling"),
    (r"\bworplace\b", "workplace", "Misspelling"),
    (r"\bworkpalce\b", "workplace", "Misspelling"),
    (r"\bworkpace\b", "workplace", "Misspelling"),
    (r"\bregualtion\b", "regulation", "Misspelling"),
    (r"\bcompiance\b", "compliance", "Misspelling"),
    (r"\bcomplaince\b", "compliance", "Misspelling"),
    (r"\btraning\b", "training", "Misspelling"),
    (r"\btraiing\b", "training", "Misspelling"),
    (r"\bhazadous\b", "hazardous", "Misspelling"),
    (r"\bregistartion\b", "registration", "Misspelling"),
    (r"\bregistation\b", "registration", "Misspelling"),
    (r"\bregistraion\b", "registration", "Misspelling"),
    (r"\batleast\b", "at least", "Should be two words"),
    (r"\baleast\b", "at least", "Should be two words"),
    (r"\balot\b", "a lot", "Should be two words"),
    # Acronym issues
    (r"\bEDPROU\b", "EDRPOU", "Acronym typo"),
    (r"\bEdprou\b", "EDRPOU", "Acronym typo"),
    # "a" before vowel sound
    (r"\ba employee\b", "an employee", "Article: 'a' → 'an' before vowel"),
    (r"\ba employer\b", "an employer", "Article: 'a' → 'an' before vowel"),
    (r"\ba organization\b", "an organization", "Article: 'a' → 'an' before vowel"),
    (r"\ba incident\b", "an incident", "Article: 'a' → 'an' before vowel"),
    (r"\ba activity\b", "an activity", "Article: 'a' → 'an' before vowel"),
    (r"\ba additional\b", "an additional", "Article: 'a' → 'an' before vowel"),
    (r"\ba individual\b", "an individual", "Article: 'a' → 'an' before vowel"),
    (r"\ba original\b", "an original", "Article: 'a' → 'an' before vowel"),
    (r"\ba applicable\b", "an applicable", "Article: 'a' → 'an' before vowel"),
    (r"\ba example\b", "an example", "Article: 'a' → 'an' before vowel"),
    (r"\ba error\b", "an error", "Article: 'a' → 'an' before vowel"),
    (r"\ba existing\b", "an existing", "Article: 'a' → 'an' before vowel"),
    (r"\ba authorized\b", "an authorized", "Article: 'a' → 'an' before vowel"),
    (r"\ba official\b", "an official", "Article: 'a' → 'an' before vowel"),
    (r"\ba update\b", "an update", "Article: 'a' → 'an' before vowel"),
]

# Punctuation checks (applied to plain text, avoid inside URLs)
def check_double_spaces(text, filename, avetta_id, field):
    issues = []
    # Look for 2+ consecutive spaces (not in markdown links or after \n)
    segments = re.split(r'\[.*?\]\(.*?\)', text)  # remove link syntax
    full_text = ' '.join(segments)
    # Find double spaces outside of newline sequences
    matches = re.finditer(r'(?<!\n)  +(?!\n)', full_text)
    for m in matches:
        context_start = max(0, m.start() - 20)
        context_end = min(len(full_text), m.end() + 20)
        context = full_text[context_start:context_end]
        issues.append({
            "filename": filename,
            "avettaId": avetta_id,
            "field": field,
            "old": repr(context),
            "new": repr(re.sub(r'  +', ' ', context)),
            "note": "Double space"
        })
        break  # report once per cell
    return issues


def check_space_before_punctuation(text, filename, avetta_id, field):
    issues = []
    # Space before comma or period (not decimal or abbreviation)
    # Avoid matching in URLs
    text_no_links = re.sub(r'\[.*?\]\(https?://\S+\)', '', text)
    text_no_links = re.sub(r'https?://\S+', '', text_no_links)

    for pat, desc in [
        (r'\w +,', "Space before comma"),
        (r'\w +\.(?!\d)', "Space before period"),
    ]:
        m = re.search(pat, text_no_links)
        if m:
            issues.append({
                "filename": filename,
                "avettaId": avetta_id,
                "field": field,
                "old": m.group(),
                "new": re.sub(r' +([,.])', r'\1', m.group()),
                "note": desc
            })
    return issues


def check_missing_space_after_comma(text, filename, avetta_id, field):
    issues = []
    # comma not followed by space, newline, or end-of-string (ignore inside URLs)
    text_no_links = re.sub(r'\[.*?\]\(https?://\S+\)', '', text)
    text_no_links = re.sub(r'https?://\S+', '', text_no_links)

    m = re.search(r',[^\s\n"\'\])]', text_no_links)
    if m:
        context = text_no_links[max(0, m.start()-5):m.end()+10]
        issues.append({
            "filename": filename,
            "avettaId": avetta_id,
            "field": field,
            "old": context.strip(),
            "new": re.sub(r',([^\s])', r', \1', context.strip()),
            "note": "Missing space after comma"
        })
    return issues


def is_english(text):
    """Skip non-English (e.g. Ukrainian) cells."""
    if not text:
        return False
    # If >30% chars are non-ASCII, assume non-English
    non_ascii = sum(1 for c in text if ord(c) > 127)
    return non_ascii / max(len(text), 1) < 0.3


def truncate(s, max_len=80):
    s = s.replace('\n', '\\n').replace('\r', '')
    if len(s) > max_len:
        return s[:max_len] + "…"
    return s


def check_cell(text, filename, avetta_id, field):
    findings = []

    if not text or not is_english(text):
        return findings

    # ── Typo checks ───────────────────────────────────────────────────────────
    for pat, replacement, note in REAL_TYPOS:
        if re.search(pat, text, re.IGNORECASE):
            m = re.search(pat, text, re.IGNORECASE)
            old_word = m.group()
            # Preserve case pattern for replacement suggestion
            if old_word.isupper():
                new_word = replacement.upper()
            elif old_word[0].isupper():
                new_word = replacement.capitalize()
            else:
                new_word = replacement
            findings.append({
                "filename": filename,
                "avettaId": avetta_id,
                "field": field,
                "old": truncate(text),
                "new": f'Replace "{old_word}" → "{new_word}"',
                "note": note
            })

    # ── Double spaces ─────────────────────────────────────────────────────────
    # Check for double spaces (not preceded by newline marker)
    if re.search(r'(?<!\n)(?<!\\n)  +', text):
        m = re.search(r'(?<!\n)(?<!\\n)  +', text)
        context_start = max(0, m.start() - 15)
        context_end = min(len(text), m.end() + 15)
        context = text[context_start:context_end]
        findings.append({
            "filename": filename,
            "avettaId": avetta_id,
            "field": field,
            "old": truncate(context),
            "new": "Remove extra space(s)",
            "note": "Double/triple space"
        })

    # ── Space before punctuation ───────────────────────────────────────────────
    # Avoid matching URLs
    text_no_urls = re.sub(r'https?://\S+', 'URL', text)
    text_no_urls = re.sub(r'\[.*?\]\(URL\)', 'LINK', text_no_urls)

    m = re.search(r'\w +[,](?!\d)', text_no_urls)
    if m:
        findings.append({
            "filename": filename,
            "avettaId": avetta_id,
            "field": field,
            "old": truncate(m.group()),
            "new": m.group().rstrip().rstrip() + ',',
            "note": "Space before comma"
        })

    # ── Missing space after comma ───────────────────────────────────────────────
    text_no_urls2 = re.sub(r'https?://[^\s\]"]+', 'URL', text)
    m = re.search(r',[a-zA-Z]', text_no_urls2)
    if m:
        context = text_no_urls2[max(0, m.start()-5):m.end()+10]
        findings.append({
            "filename": filename,
            "avettaId": avetta_id,
            "field": field,
            "old": context.strip(),
            "new": context.strip().replace(m.group(), m.group()[0] + ' ' + m.group()[1]),
            "note": "Missing space after comma"
        })

    return findings


def main():
    all_findings = []

    csv_files = sorted(FORMS_DIR.glob("formId_*.csv"))

    for csv_path in csv_files:
        filename = csv_path.name
        try:
            with open(csv_path, encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames or []

                # Find the text column
                text_col = None
                for col in TEXT_COLS:
                    if col in fieldnames:
                        text_col = col
                        break

                if not text_col:
                    continue

                for row in reader:
                    field = row.get("field", "")
                    avetta_id = row.get("avettaId", "")
                    text = row.get(text_col, "")

                    # Skip response options (country lists, etc.)
                    if any(field.startswith(p) for p in SKIP_FIELDS_PREFIXES):
                        continue

                    if text:
                        findings = check_cell(text, filename, avetta_id, field)
                        all_findings.extend(findings)

        except Exception as e:
            print(f"ERROR reading {filename}: {e}", file=sys.stderr)

    # ── Output ────────────────────────────────────────────────────────────────
    if not all_findings:
        print("No issues found.")
        return

    # Deduplicate by (filename, avettaId, field, note)
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f["filename"], f["avettaId"], f["field"], f["note"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    print(f"Found {len(unique_findings)} issue(s):\n")
    print(f"{'#':<4} {'File':<50} {'Field':<20} {'Old value':<50} {'Corrected value / Action':<50} {'Notes'}")
    print("-" * 240)

    for i, f in enumerate(unique_findings, 1):
        print(f"{i:<4} {f['filename']:<50} {f['field']:<20} {f['old']:<50} {f['new']:<50} {f['note']}")

    # Also write a simple TSV for easier processing
    tsv_path = FORMS_DIR / "grammar_issues.tsv"
    with open(tsv_path, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=["#", "filename", "avettaId", "field", "old", "new", "note"],
                                delimiter="\t")
        writer.writeheader()
        for i, f in enumerate(unique_findings, 1):
            writer.writerow({"#": i, **f})
    print(f"\nResults saved to: {tsv_path}")


if __name__ == "__main__":
    main()
