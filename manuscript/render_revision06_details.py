"""Selected large-scale renderings for the final visual review."""
from pathlib import Path
import json
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/pdfs/book-revision06-delivery-review';OUT.mkdir(parents=True,exist_ok=True)
document=pdfium.PdfDocument(ROOT/'output/pdf/cuervo-complete-reading-proof-revision-06.pdf')
manifest=json.loads((ROOT/'manuscript/book-revision-06/build-manifest.json').read_text(encoding='utf-8'))
keys={'2:santa-rosa-map','3:merchant-finance','4:school-staff-and-care','4:doctor-support','5:population-and-age','5:people-and-households','5:work-under-one-roof','5:regional-households','6:journeys','6:station-book','6:chronology','7:functional-chronology','7:support'}
pages=sorted({2,manifest['pages'],manifest['backmatter_pages']['bibliography'],manifest['backmatter_pages']['bibliography']+2,manifest['backmatter_pages']['credits']}|{r['page'] for r in manifest['figure_pages'] if r['figure'] in keys}|{r['source_notes_page'] for r in manifest['chapters'] if r['chapter'] in [4,6,7,8]})
for n in pages:
    page=document[n-1]
    page.render(scale=1.7).to_pil().save(OUT/f'detail-{n:03d}.png')
    page.close()
print('Rendered details:',pages)
