from pathlib import Path
import json
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
audit=json.loads((ROOT/'sources/02_newspapers/cuervo_clipper/full_scan_audit_2026-09-17.json').read_text(encoding='utf-8'))
issues={r['issue_date']:r for r in audit['issues']}
# Relative page rectangles, after inspection of each complete front page.
for date,box in [('1910-10-07',(.47,.32,.63,.46)),('1910-11-18',(.73,.24,.9,.34)),
                 ('1911-01-27',(.73,.16,.92,.30)),('1912-02-08',(.37,.70,.54,.79))]:
    doc=pdfium.PdfDocument(str(ROOT/issues[date]['file']))
    page=doc[1];im=page.render(scale=5).to_pil()
    w,h=im.size
    im.crop(tuple(int(n*size) for n,size in zip(box,(w,h,w,h)))).save(HERE/'page_renders'/f'clipper_{date}_detail.png')
    page.close();doc.close()
print('Four source details rendered.')
