from pathlib import Path
import argparse
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--pages',required=True,help='Comma-separated physical PDF page numbers; ranges with colon are inclusive.')
args=parser.parse_args()
pages=[]
for part in args.pages.split(','):
    if ':' in part:
        a,b=map(int,part.split(':')); pages.extend(range(a,b+1))
    else: pages.append(int(part))
doc=pdfium.PdfDocument(ROOT/'sources/origins_followup_2026-09-23/grubbs_bond_thesis_1958.pdf')
out=ROOT/'research_evidence/origins_followup_2026-09-23/thesis_page_renders'
out.mkdir(parents=True,exist_ok=True)
for n in pages:
    target=out/f'thesis_pdf{n:03d}.png'
    if not target.exists(): doc[n-1].render(scale=2.5).to_pil().save(target)
print('Rendered',len(pages),'requested pages.')
