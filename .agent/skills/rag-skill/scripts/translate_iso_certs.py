"""
translate_iso_certs.py
----------------------
Extract text from image-based ISO certificate PDFs using Claude Vision (OCR),
translate any non-English content to English, and save structured .md files
to an en-US/ subfolder alongside the source PDFs.

Usage:
    python translate_iso_certs.py <pdf_folder>

    If no folder is given, defaults to the current working directory.

Requirements:
    pip install anthropic pymupdf

Environment:
    ANTHROPIC_API_KEY must be set.

Output:
    <pdf_folder>/en-US/<original_filename>_en-US.md
    - Skips files already translated (incremental runs safe).
"""

import os
import sys
import io
import base64
import anthropic
import fitz  # PyMuPDF

# Fix Windows console encoding for filenames with non-ASCII characters (e.g. Japanese, Chinese)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

MAX_IMG_BYTES = 4_800_000  # Stay under the 5 MB API image limit


def page_to_base64(page, zoom=1.5):
    """Render a PDF page to PNG base64, reducing zoom if the image is too large."""
    for z in [zoom, 1.2, 1.0, 0.8]:
        mat = fitz.Matrix(z, z)
        pix = page.get_pixmap(matrix=mat)
        data = pix.tobytes("png")
        if len(data) <= MAX_IMG_BYTES:
            return base64.standard_b64encode(data).decode()
    # Last resort: JPEG at lower quality
    data = page.get_pixmap(matrix=fitz.Matrix(0.8, 0.8)).tobytes("jpeg", jpg_quality=75)
    return base64.standard_b64encode(data).decode()


def call_vision(client, images_b64, filename, page_desc=""):
    """Send one or more page images to Claude and return extracted + translated text."""
    content = []
    for img in images_b64:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": img,
            },
        })
    content.append({
        "type": "text",
        "text": (
            f"The above image(s) show {page_desc}of an ISO certification certificate: '{filename}'.\n\n"
            "Please:\n"
            "1. Extract ALL text visible in the certificate (OCR), preserving the logical structure "
            "(title, issuing body, certificate number, company name, scope, standard, issue date, "
            "expiry date, authorised signatures, accreditation body, etc.).\n"
            "2. Translate any non-English text to English.\n"
            "3. Format the output as a clean structured Markdown document with labelled fields.\n"
            "4. Do NOT omit any information — include all visible text, codes, dates, "
            "and descriptions of logos/seals.\n\n"
            "Output format example:\n"
            "# CERTIFICATE OF REGISTRATION\n\n"
            "**Field**: Value\n"
            "..."
        ),
    })
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )
    return msg.content[0].text.strip()


def extract_and_translate(client, pdf_path):
    """OCR + translate all pages of a PDF; falls back to per-page calls if needed."""
    doc = fitz.open(pdf_path)
    filename = os.path.basename(pdf_path)
    pages_b64 = [page_to_base64(page) for page in doc]

    if len(pages_b64) == 1:
        return call_vision(client, pages_b64, filename)

    # Multi-page: try sending all pages together first
    try:
        return call_vision(client, pages_b64, filename, f"all {len(pages_b64)} pages ")
    except anthropic.BadRequestError:
        # Fall back to one page at a time
        parts = []
        for i, img_b64 in enumerate(pages_b64):
            parts.append(
                call_vision(client, [img_b64], filename, f"page {i + 1} of {len(pages_b64)} ")
            )
        return "\n\n---\n\n".join(parts)


def process_folder(src_dir):
    """Translate all PDFs in src_dir that don't already have an en-US output."""
    out_dir = os.path.join(src_dir, "en-US")
    os.makedirs(out_dir, exist_ok=True)

    client = anthropic.Anthropic()

    pdfs = sorted(f for f in os.listdir(src_dir) if f.lower().endswith(".pdf"))
    if not pdfs:
        print(f"No PDF files found in: {src_dir}")
        return

    for filename in pdfs:
        out_name = os.path.splitext(filename)[0] + "_en-US.md"
        out_path = os.path.join(out_dir, out_name)

        if os.path.exists(out_path):
            print(f"Skipping (already done): {filename}")
            continue

        print(f"Processing: {filename} ...", flush=True)
        pdf_path = os.path.join(src_dir, filename)
        text = extract_and_translate(client, pdf_path)

        header = (
            f"[Source: {filename}]\n"
            f"[Translated to: English (en-US)]\n"
            f"[Model: claude-sonnet-4-6]\n\n"
            f"{'=' * 60}\n\n"
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(header + text + "\n")

        print(f"  -> Saved : en-US/{out_name}")
        print(f"  -> Chars : {len(text)}\n")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    folder = os.path.abspath(folder)
    print(f"Source folder : {folder}")
    process_folder(folder)
