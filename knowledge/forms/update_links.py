#!/usr/bin/env python3
"""
Update outdated HTTP links in all form CSV files.

Two categories of fixes:
  A. Changed URL  - both the domain/path and protocol changed
  B. Protocol only - just http:// -> https://, same URL

Run from the knowledge/forms/ directory:
    python update_links.py [--dry-run]
"""

import glob
import os
import sys

# ── Category A: Full URL replacements (old URL -> new URL) ──────────────────
CHANGED_URLS = {
    # UK Companies House
    "http://www.companieshouse.gov.uk":
        "https://find-and-update.company-information.service.gov.uk/",

    # UK HMRC -> GOV.UK
    "http://www.hmrc.gov.uk":
        "https://www.gov.uk/government/organisations/hm-revenue-customs",

    # UK Charity Commission -> GOV.UK
    "http://www.charitycommission.gov.uk":
        "https://www.gov.uk/government/organisations/charity-commission",

    # Spain CNAE (both casings of the same dead URL)
    "http://www.ine.es/jaxi/menu.do?type=pcaxis&path=%2Ft40%2Fclasrev%2F&file=inebase&L=1":
        "https://www.ine.es/uc/Z7rrBQPg",
    "http://www.ine.es/jaxi/menu.do?type=pcaxis&path=%2ft40%2fclasrev%2f&file=inebase&l=1":
        "https://www.ine.es/uc/Z7rrBQPg",

    # Belgium NACE-BEL (2025 edition now in force)
    "http://statbel.fgov.be/nl/statistieken/gegevensinzameling/nomenclaturen/nacebel/":
        "https://statbel.fgov.be/en/about-statbel/methodology/classifications/nace-bel-2025",

    # Netherlands SBI (CBS site redesigned)
    "http://www.cbs.nl/nl-NL/menu/methoden/classificaties/overzicht/sbi/default.htm":
        "https://www.cbs.nl/nl-nl/onze-diensten/methoden/classificaties/activiteiten/standaard-bedrijfsindeling--sbi--",
    "http://www.cbs.nl/nl-nl/menu/methoden/classificaties/overzicht/sbi/default.htm":
        "https://www.cbs.nl/nl-nl/onze-diensten/methoden/classificaties/activiteiten/standaard-bedrijfsindeling--sbi--",

    # Czech ARES (moved to new domain)
    "http://wwwinfo.mfcr.cz/ares/ares_es.html.cz":
        "https://ares.gov.cz/",

    # France NAF (INSEE site restructured)
    "http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/naf2008/naf2008.htm":
        "https://www.insee.fr/fr/information/2120875",

    # EU VIES VAT checker (path changed)
    "http://ec.europa.eu/taxation_customs/vies/vatResponse.html":
        "https://ec.europa.eu/taxation_customs/vies",

    # Italy ATECO (istat.it site restructured; ATECO 2025 in force)
    "http://en.istat.it/strumenti/definizioni/ateco/":
        "https://www.istat.it/en/classification/ateco-classification-of-economic-activity-2007/",

    # Singapore ACRA SSIC search (app subdomain retired)
    "http://app.acra.gov.sg/SSIC_Search.asp":
        "https://www.acra.gov.sg/ssic-search",
    "http://app.acra.gov.sg/ssic_search.asp":
        "https://www.acra.gov.sg/ssic-search",

    # Philippines PSIC (nap subdomain -> psa.gov.ph)
    "http://nap.psa.gov.ph/activestats/psic/":
        "https://psa.gov.ph/classification/psic",

    # Malaysia SSM (path changed)
    "http://www.ssm.com.my/en":
        "https://www.ssm.com.my/",

    # Vietnam GSO (site fully redesigned)
    "http://www.gso.gov.vn/default.aspx?tabid=728":
        "https://www.gso.gov.vn/en/homepage/",

    # Portugal company portal (moved to gov.pt)
    "http://www.portaldaempresa.pt/CVE/en":
        "https://www2.gov.pt/espaco-empresa/empresa-online",

    # Romania CAEN (moved to main insse.ro; CAEN Rev.3 in force Jan 2025)
    "http://colectaredate.insse.ro/senin/classifications.htm?selectedClassification=CAEN_Rev.2&action=structure":
        "https://insse.ro/cms/ro/caen",
}


def process_file(path, dry_run=False):
    with open(path, encoding="utf-8-sig") as f:
        original = f.read()

    updated = original

    # ── Category A: apply specific URL replacements ──────────────────────────
    for old, new in CHANGED_URLS.items():
        updated = updated.replace(old, new)

    # ── Category B: flip all remaining http:// to https:// ──────────────────
    updated = updated.replace("http://", "https://")

    if updated == original:
        return 0  # no changes

    if not dry_run:
        # Write back without BOM (utf-8 is fine; utf-8-sig only on read)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(updated)

    return 1


def main():
    dry_run = "--dry-run" in sys.argv

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_files = sorted(glob.glob(os.path.join(script_dir, "*.csv")))

    if not csv_files:
        print("No CSV files found.")
        sys.exit(1)

    changed = 0
    for path in csv_files:
        n = process_file(path, dry_run=dry_run)
        if n:
            tag = "[DRY RUN] would update" if dry_run else "Updated"
            print(f"  {tag}: {os.path.basename(path)}")
            changed += 1

    mode = "(dry run)" if dry_run else ""
    print(f"\nDone {mode}: {changed}/{len(csv_files)} files updated.")


if __name__ == "__main__":
    main()
