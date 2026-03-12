# PDF Reading & Analysis

> ⚠️ **Before using this document**: Read this document in full before processing any PDF file, so you can choose the most appropriate tool and method. Do not attempt to process a PDF without reading this first.

Methods for extracting text, tables, and metadata from PDF files.

## Quick Decision Table

| Scenario | Recommended Tool | Reason | Command / Code Example |
|----------|-----------------|--------|------------------------|
| Plain text extraction (most common) | pdftotext command | Fastest and simplest | `pdftotext input.pdf output.txt` |
| Preserve layout | pdftotext -layout | Retains original formatting | `pdftotext -layout input.pdf output.txt` |
| Extract tables | pdfplumber | Strong table recognition | `page.extract_tables()` |
| Extract metadata | pypdf | Lightweight | `reader.metadata` |
| Scanned PDF (image-based) | OCR (pytesseract) | No other option | Convert to image first, then OCR |

## Text Extraction Priority

**Recommended priority (highest to lowest)**:
1. **pdftotext command-line tool** (fastest, works for most PDFs)
2. pdfplumber (when layout preservation or table extraction is needed)
3. pypdf (lightweight, for simple extraction)
4. OCR (only for scanned PDFs or when direct text extraction is not possible)

## Quick Start: Using pdftotext (Recommended)

> ⚠️ **Important**: Always save output to a file — do NOT print to stdout/terminal, as that consumes a large number of tokens!

```bash
# ✅ Correct: extract text to file (fastest and simplest)
pdftotext input.pdf output.txt

# ✅ Correct: preserve layout and save to file
pdftotext -layout input.pdf output.txt

# ✅ Correct: extract specific pages to file
pdftotext -f 1 -l 5 input.pdf output.txt  # pages 1–5

# ❌ Wrong: do NOT use stdout (consumes many tokens)
# pdftotext input.pdf -
```

**Workflow**:
1. Use pdftotext to extract text into a temporary file
2. Use grep or the Read tool to search within the generated text file
3. Read only the relevant context around matches, not the full text

If you need to process in Python:

```python
from pypdf import PdfReader

# Open PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf — Basic Text Extraction

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")

# Extract all text
for page in reader.pages:
    text = page.extract_text()
    print(text)

# Extract metadata
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

### pdfplumber — Text and Table Extraction with Layout

#### Extract Text (preserving layout)

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables

```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction (convert to DataFrame)

```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # check table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

#### Precise Text Extraction with Coordinates

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]

    # Extract all characters with their coordinates
    chars = page.chars
    for char in chars[:10]:  # first 10 characters
        print(f"Char: '{char['text']}' at x:{char['x0']:.1f} y:{char['y0']:.1f}")

    # Extract text within a bounding box (left, top, right, bottom)
    bbox_text = page.within_bbox((100, 100, 400, 200)).extract_text()
```

#### Advanced Settings for Complex Tables

```python
import pdfplumber

with pdfplumber.open("complex_table.pdf") as pdf:
    page = pdf.pages[0]

    # Custom table extraction settings
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "intersection_tolerance": 15
    }
    tables = page.extract_tables(table_settings)

    # Visual debugging
    img = page.to_image(resolution=150)
    img.save("debug_layout.png")
```

### pypdfium2 — Fast Rendering and Text Extraction

```python
import pypdfium2 as pdfium

# Load PDF
pdf = pdfium.PdfDocument("document.pdf")

# Extract text
for i, page in enumerate(pdf):
    text = page.get_text()
    print(f"Page {i+1} text length: {len(text)} chars")
```

#### Render PDF Pages as Images

```python
import pypdfium2 as pdfium
from PIL import Image

pdf = pdfium.PdfDocument("document.pdf")

# Render a single page
page = pdf[0]  # first page
bitmap = page.render(
    scale=2.0,   # high resolution
    rotation=0   # no rotation
)

# Convert to PIL Image
img = bitmap.to_pil()
img.save("page_1.png", "PNG")

# Process multiple pages
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.5)
    img = bitmap.to_pil()
    img.save(f"page_{i+1}.jpg", "JPEG", quality=90)
```

## Command-Line Tools

### pdftotext (poppler-utils)

> ⚠️ **Performance tip**: Always output to a file to avoid consuming tokens.

```bash
# ✅ Extract text to file
pdftotext input.pdf output.txt

# ✅ Preserve layout and save to file
pdftotext -layout input.pdf output.txt

# ✅ Extract specific pages to file
pdftotext -f 1 -l 5 input.pdf output.txt  # pages 1–5

# ✅ Extract text with coordinates to XML file (for structured data)
pdftotext -bbox-layout document.pdf output.xml

# ❌ Avoid: do not omit the output filename (prints to stdout)
# pdftotext input.pdf
```

### Advanced Image Conversion (pdftoppm)

```bash
# Convert to PNG at specified resolution
pdftoppm -png -r 300 document.pdf output_prefix

# Convert specific page range at high resolution
pdftoppm -png -r 600 -f 1 -l 3 document.pdf high_res_pages

# Convert to JPEG at specified quality
pdftoppm -jpeg -jpegopt quality=85 -r 200 document.pdf jpeg_output
```

### Extract Embedded Images (pdfimages)

```bash
# Extract all images
pdfimages -j input.pdf output_prefix

# List image info without extracting
pdfimages -list document.pdf

# Extract in original format
pdfimages -all document.pdf images/img
```

## OCR Extraction (Scanned PDFs)

```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

## Handling Encrypted PDFs

```python
from pypdf import PdfReader

try:
    reader = PdfReader("encrypted.pdf")
    if reader.is_encrypted:
        reader.decrypt("password")

    # Extract text normally after decryption
    for page in reader.pages:
        text = page.extract_text()
        print(text)
except Exception as e:
    print(f"Failed to decrypt: {e}")
```

```bash
# Decrypt using qpdf (password required)
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf

# Check encryption status
qpdf --show-encryption encrypted.pdf
```

## Batch Processing

```python
import os
import glob
from pypdf import PdfReader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def batch_extract_text(input_dir):
    """Batch extract text from all PDFs in a directory."""
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))

    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            output_file = pdf_file.replace('.pdf', '.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.info(f"Extracted text from: {pdf_file}")

        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_file}: {e}")
            continue
```

## Performance Tips

1. **File output first**: Always save pdftotext output to a file, then search with grep/Read — avoid printing to terminal to save tokens
2. **Large PDFs**: Process page by page in a streaming fashion; avoid loading the entire file at once
3. **Text extraction**: `pdftotext` is fastest; pdfplumber is better for structured data and tables
4. **Image extraction**: `pdfimages` is much faster than rendering pages
5. **Memory management**: Process large files page by page or in chunks

## Quick Reference

| Task | Best Tool | Command / Code |
|------|-----------|----------------|
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Command-line extraction | pdftotext | `pdftotext -layout input.pdf` |
| OCR scanned PDF | pytesseract | Convert to image first, then OCR |
| Extract metadata | pypdf | `reader.metadata` |
| PDF to image | pypdfium2 | `page.render()` |

## Available Packages

- **pypdf** — basic operations (BSD license)
- **pdfplumber** — text and table extraction (MIT license)
- **pypdfium2** — fast rendering and extraction (Apache/BSD license)
- **pytesseract** — OCR (Apache license)
- **pdf2image** — PDF to image conversion
- **poppler-utils** — command-line tools (GPL-2 license)
