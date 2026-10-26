from pathlib import Path
import json, re
import pdfplumber, pypdfium2 as pdfium
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SRC=ROOT/'sources/regional_functions_2026-09-21'
source=SRC/'nmed_all_storage_tanks_2020-11-19.pdf'
targets=[(14,'1927'),(74,'30531'),(83,'31151')]
out=[]
with pdfplumber.open(source) as pdf:
    doc=pdfium.PdfDocument(source)
    for page,fid in targets:
        pg=pdf.pages[page-1]
        words=pg.extract_words()
        word=next(w for w in words if w['text']==fid and w['x0']<200)
        y=word['top'];im=doc[page-1].render(scale=2).to_pil()
        hy=next(w['top'] for w in words if w['text']=='FID')
        header=im.crop((180,int(max(0,hy-45)*2),im.width-180,int((hy+26)*2)))
        row=im.crop((180,int((y-4)*2),im.width-180,int((y+25)*2)))
        view=Image.new('RGB',(header.width,header.height+row.height+40),'white')
        view.paste(header,(0,0));view.paste(row,(0,header.height+25))
        ImageDraw.Draw(view).text((5,header.height+4),f'2020-11-19 inventory | PDF page {page} | FID {fid}',fill='black')
        view.save(HERE/f'nmed_2020_fid_{fid}.png')
        text=pg.crop((0,y-4,pg.width,min(pg.height,y+31))).extract_text()
        out.append({'fid':fid,'pdf_page':page,'source':source.relative_to(ROOT).as_posix(),
                    'row_area_text':text,'view':f'nmed_2020_fid_{fid}.png'})
(HERE/'nmed_facility_reading_locators.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
