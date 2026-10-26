"""Compare the final rendered body pages with the prior Letter print copy."""
from pathlib import Path
import json
from PIL import Image,ImageChops,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/monograph-print-letter'
PRIOR=ROOT/'tmp/pdfs/revision10-print-letter'
assert len(list(QA.glob('page-*.png')))==148
comparisons=[]
for n in range(3,146):
    with Image.open(QA/f'page-{n:03d}.png') as a,Image.open(PRIOR/f'letter-{n:03d}.png') as b:
        assert a.size==b.size
        # The removed proof footer is below y=1040. The main content, top
        # running heads, and rule above the footer remain within this crop.
        crop=(0,0,a.width,1040)
        diff=ImageChops.difference(a.convert('RGB').crop(crop),b.convert('RGB').crop(crop))
        comparisons.append({'page':n,'body_pixels_identical':diff.getbbox() is None})

def sheet(name,pages,columns=3):
    rows=(len(pages)+columns-1)//columns
    canvas=Image.new('RGB',(columns*380,rows*530),'#dddddd');draw=ImageDraw.Draw(canvas)
    for j,n in enumerate(pages):
        with Image.open(QA/f'page-{n:03d}.png') as im:
            im=im.convert('RGB');im.thumbnail((360,495))
            x=(j%columns)*380+(380-im.width)//2;y=(j//columns)*530+25
            canvas.paste(im,(x,y));draw.text(((j%columns)*380+12,(j//columns)*530+8),f'Page {n}',fill='black')
    canvas.save(QA/name)

sheet('changed-pages.png',[1,2,146,147,148,3])
sheet('representative-pages.png',[8,9,48,108,109,110,121,137,142])
different=[x['page'] for x in comparisons if not x['body_pixels_identical']]
for i in range(0,len(different),9):sheet(f'comparison-differences-{i//9+1}.png',different[i:i+9])
result={'rendered_pages':148,'body_comparison_pages':143,'pixel_identical_body_pages':sum(x['body_pixels_identical'] for x in comparisons),'body_pages_with_differences':different,'comparison_excludes_removed_footer':True,'pages':comparisons}
(QA/'raster-comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='pages'},indent=2))
