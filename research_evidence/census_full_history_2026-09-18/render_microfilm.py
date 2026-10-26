"""Render selected one-based microfilm PDF pages, or a header contact sheet."""
from pathlib import Path
import argparse
import pypdfium2 as pdfium
from PIL import Image, ImageDraw

p=argparse.ArgumentParser()
p.add_argument('pdf');p.add_argument('output');p.add_argument('pages', help='start:end:step or comma-separated pages')
p.add_argument('--headers',action='store_true');p.add_argument('--scale',type=float,default=2.0)
a=p.parse_args()
if ':' in a.pages:
    x=[int(v) for v in a.pages.split(':')]; pages=list(range(x[0],x[1]+1,x[2] if len(x)>2 else 1))
else: pages=[int(v) for v in a.pages.split(',')]
doc=pdfium.PdfDocument(a.pdf)
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
if a.headers:
    strips=[]
    for n in pages:
        im=doc[n-1].render(scale=a.scale).to_pil().convert('RGB')
        im=im.crop((0,0,im.width,int(im.height*.19)))
        im.thumbnail((1800,1800))
        strip=Image.new('RGB',(1880,im.height+12),'#dddddd');strip.paste(im,(70,6))
        ImageDraw.Draw(strip).text((5,20),str(n),fill='black');strips.append(strip)
    sheet=Image.new('RGB',(1880,sum(x.height for x in strips)),'white');y=0
    for im in strips:sheet.paste(im,(0,y));y+=im.height
    sheet.save(out)
else:
    out.mkdir(parents=True,exist_ok=True)
    for n in pages:
        im=doc[n-1].render(scale=a.scale).to_pil().convert('RGB')
        im.save(out/f'pdf{n}.jpg',quality=96)
print(str(out))
