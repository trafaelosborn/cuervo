"""Make explicitly bounded reading crops, retaining original full scans separately."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse
p=argparse.ArgumentParser();p.add_argument('year');p.add_argument('pages');p.add_argument('--box',default=None)
a=p.parse_args();root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
cfg={
 '1910':('1910_cuervo_pages/pdf{}.jpg',(.25,.145,.371,.944)),
 '1920':('1920_cuervo_pages/pdf{}.jpg',(.248,.14,.374,.936)),
 '1930':('1930_cuervo_highres/pdf{}.jpg',(.32,.14,.383,.94)),
 '1940':('../../sources/03_census/1940_manuscripts/ed_10-6/m-t0627-02445-00{}.jpg',(.25,.14,.36,.8))
}
pattern,box=cfg[a.year]
if a.box:box=tuple(float(x) for x in a.box.split(','))
pages=[int(x) for x in a.pages.split(',')];panels=[]
for n in pages:
 im=Image.open(here/pattern.format(n));w,h=im.size
 im=im.crop(tuple(int(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
 im=im.resize((round(im.width*1900/im.height),1900))
 panel=Image.new('RGB',(im.width+20,1940),'white');panel.paste(im,(10,35))
 ImageDraw.Draw(panel).text((10,10),f'{a.year}: PDF/image {n}',fill='black')
 panels.append(panel)
out=Image.new('RGB',(sum(im.width for im in panels),1940),'#e0e0e0');x=0
for im in panels:out.paste(im,(x,0));x+=im.width
dest=root/'tmp/census_full_history'/f'{a.year}_ages_{a.pages.replace(",","_")}.png';out.save(dest);print(dest)
