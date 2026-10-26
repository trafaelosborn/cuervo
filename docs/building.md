# Building the book

The supported entry point is `tools/build.py`. It typesets the current monograph from Revision 10 chapter text, places the included figures, and produces the US Letter print PDF. It does not rerun the historical research or change the working archive outside this checkout.

## Set up Python

Use Python 3.12 in a virtual environment:

```sh
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in Windows PowerShell or `source .venv/bin/activate` in a POSIX shell. Then install the tested dependencies:

```sh
python -m pip install -r requirements.txt
```

Jost and Playfair Display are included under their SIL Open Font Licenses. The current build uses those fonts. A compatibility fallback allows older style-registration code to initialize without Microsoft's Garamond, Baskerville, or Calibri fonts.

## Build the print edition

```sh
python tools/build.py
```

The stages are:

1. Typeset `manuscript/book-revision-10/chapters/` with the current publication title page and photograph credits.
2. Convert the typeset pages to US Letter with mirrored binding margins, embedded fonts, preserved links, and an intentional final blank page.
3. Check page count, title, annotations, and font embedding.

The result is `output/pdf/cuervo-monograph-print-letter.pdf`. Temporary pages and image caches are written under `tmp/`; generated PDFs are ignored by Git.

## Build the compact edition

```sh
python tools/build.py --compact
```

This also writes `output/pdf/cuervo-monograph-compact.pdf`. The release copy preserves all text, vector drawing commands, links, page dimensions, and chart pixels. Photographs use smaller pixel dimensions and JPEG compression; archival scans retain their full pixel dimensions. The size ceiling is 9,800,000 bytes.

## Check a published download

```sh
python tools/verify_release.py
```

This compares downloaded files against the SHA-256 values in `releases/v1.0.0-files.json`. A fresh build can have a different PDF hash because creation metadata and PDF object serialization can vary. A checksum mismatch in a rebuilt file is therefore different from a mismatch in a downloaded release asset.

To compare the rebuilt print PDF with a downloaded reference:

```sh
python tools/check_build.py --reference path/to/downloaded-print.pdf
```

The comparison checks text on every page, page geometry, link destinations, and embedded fonts. Inspect rendered pages when changing typography, layout, images, or the PDF toolchain.

## Research and historical scripts

Earlier build and research scripts remain alongside their dated outputs. Some expect the author's original directory structure, proprietary legacy fonts, or the external source archive. The current typesetting entry point is the supported path for this repository. Source acquisition scripts are not run automatically.

The archive catalog records original project-relative paths. Restoring those holdings under `sources/` or `Cuervo/` may satisfy historical script inputs, but individual scripts should be inspected before execution. The catalog is a finding aid, not a download script.
