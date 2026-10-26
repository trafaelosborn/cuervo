"""Compare all rendered pages and prepare image-quality review sheets."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageStat
import json
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/monograph-compact'
MASTER=ROOT/'tmp/pdfs/monograph-print-letter'
assert len(list(QA.glob('page-*.png')))==148
changes=[];same=[]
for n in range(1,149):
    with Image.open(QA/f'page-{n:03d}.png') as a,Image.open(MASTER/f'page-{n:03d}.png') as b:
        assert a.size==b.size
        diff=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
        box=diff.getbbox()
        if box:changes.append({'page':n,'mean_absolute_difference':sum(ImageStat.Stat(diff).mean)/3,'bounding_box':box})
        else:same.append(n)
expected={r['page'] for r in json.loads((ROOT/'manuscript/monograph/compact/compression.json').read_text())['images'] if r['kind'] in ['photograph','source scan']}
assert {r['page'] for r in changes}<=expected
for i in range(0,len(changes),9):
    pages=[r['page'] for r in changes[i:i+9]]
    sheet=Image.new('RGB',(1140,1590),'#dddddd');draw=ImageDraw.Draw(sheet)
    for j,n in enumerate(pages):
        with Image.open(QA/f'page-{n:03d}.png') as im:
            im=im.convert('RGB');im.thumbnail((360,495))
            sheet.paste(im,((j%3)*380+(380-im.width)//2,(j//3)*530+25))
            draw.text(((j%3)*380+12,(j//3)*530+8),f'Page {n}',fill='black')
    sheet.save(QA/f'image-review-{i//9+1}.png')
result={'rendered_pages':148,'pixel_identical_pages':same,'changed_pages':changes,'differences_only_on_image_pages':True}
(QA/'raster-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'rendered_pages':148,'pixel_identical_pages':len(same),'changed_pages':[r['page'] for r in changes]},indent=2))
