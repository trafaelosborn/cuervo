from pathlib import Path
from PIL import Image,ImageDraw
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'tmp'/'rebound_1940_1950'/'agriculture'
OUT.mkdir(parents=True,exist_ok=True)
for filename in ['1950_nm_agriculture_counties.pdf','1945_nm_agriculture_full.pdf']:
    path=ROOT/'sources'/'03_census'/'agriculture_rebound_2026-09-19'/filename
    if not path.exists():continue
    doc=pdfium.PdfDocument(path)
    for first in range(0,len(doc),16):
        board=Image.new('RGB',(1600,1680),'#ddd')
        draw=ImageDraw.Draw(board)
        for n in range(first,min(first+16,len(doc))):
            page=doc[n]
            im=page.render(scale=1).to_pil().convert('RGB')
            crop=im.crop((0,0,im.width,min(im.height,int(im.height*.68))))
            crop.thumbnail((390,390))
            x=(n-first)%4*400;y=(n-first)//4*420
            board.paste(crop,(x,y+25))
            draw.text((x+8,y+5),f'{filename[:4]} PDF {n+1}',fill='black')
            page.close()
        board.save(OUT/f'{filename[:4]}_contact_{first+1}.jpg',quality=95)
    print(filename,len(doc))
    doc.close()
