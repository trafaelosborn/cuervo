from pathlib import Path
import argparse
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('pages');p.add_argument('--out',default='renders');p.add_argument('--scale',type=float,default=2.0);p.add_argument('--contact',action='store_true');a=p.parse_args()
pages=[]
for part in a.pages.split(','):
    if ':' in part:
        bits=list(map(int,part.split(':'))); pages.extend(range(bits[0],bits[1]+1,bits[2] if len(bits)>2 else 1))
    else: pages.append(int(part))
doc=pdfium.PdfDocument(ROOT/a.source)
out=Path(__file__).parent/a.out;out.mkdir(parents=True,exist_ok=True)
for n in pages:
    path=out/f'page_{n:03d}.png'
    if not path.exists(): doc[n-1].render(scale=a.scale).to_pil().save(path)
if a.contact:
    for start in range(0,len(pages),20):
        board=Image.new('RGB',(1600,1800),'#ddd');d=ImageDraw.Draw(board)
        for k,n in enumerate(pages[start:start+20]):
            im=Image.open(out/f'page_{n:03d}.png'); im.thumbnail((390,330));x=k%4*400;y=k//4*360
            board.paste(im,(x,y+25));d.text((x+5,y+5),f'PDF {n}',fill='black')
        board.save(out/f'contact_{start+1}.jpg')
print(f'Rendered {len(pages)} pages to {out}',flush=True)
