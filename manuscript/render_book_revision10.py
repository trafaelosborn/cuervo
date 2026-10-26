"""Render every final proof page for visual review."""
from pathlib import Path
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/book-revision10-verified';QA.mkdir(parents=True,exist_ok=True)
pdf=pdfium.PdfDocument(ROOT/'output/pdf/cuervo-complete-reading-proof-revision-10.pdf')
for n in range(len(pdf)):
    page=pdf[n];bitmap=page.render(scale=1.4);im=bitmap.to_pil()
    im.save(QA/f'page-{n+1:03d}.png');im.close();bitmap.close();page.close()
print(f'Rendered {len(pdf)} pages.')
pdf.close()
