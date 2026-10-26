"""Prepare faithful archival details and a cattle chart sized for the reading proof."""
from pathlib import Path
import json
import hashlib
import sys
import os
import subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'manuscript/figures/revision-2026-09-28'
OUT.mkdir(parents=True,exist_ok=True)
TMP=ROOT/'tmp/pdfs/rewrite-2026-09-28'
TMP.mkdir(parents=True,exist_ok=True)
POP=Path('C:/Users/Clem/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
sources={
 '1911-09-14':ROOT/'sources/02_newspapers/cuervo_clipper/full_scans/The Cuervo Clipper, 09-14-1911 - The Cuervo Clipper 09-14-1911.pdf',
 '1910-03-04':ROOT/'sources/02_newspapers/cuervo_clipper/full_scans/The Cuervo Clipper, 03-04-1910 - The Cuervo Clipper 03-04-1910.pdf',
 'cuervo-map':ROOT/'Cuervo/Cuervo/Parcel Map/City of Cuervo.pdf'}
records=[]
for key,src in sources.items():
    page=1 if key=='cuervo-map' else 2
    target=TMP/f'{key}.png'
    if not target.exists():
        subprocess.run([str(POP),'-f',str(page),'-singlefile','-scale-to','4000','-png',str(src),str(target.with_suffix(''))],check=True,capture_output=True)
    records.append({'id':key,'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'pdf_page':page,'render':str(target)})

crops={
 '1911-masthead':('1911-09-14',(364,79,1006,187)),
 '1911-depot':('1911-09-14',(516,786,691,839)),
 '1911-lumber':('1911-09-14',(518,1299,693,1370)),
 '1911-school':('1911-09-14',(693,1366,869,1638)),
 '1910-sheep':('1910-03-04',(477,458,649,508)),
 '1910-supplies':('1910-03-04',(486,888,658,971)),
 '1910-advertisement':('1910-03-04',(333,1278,842,1648))}
for name,(key,box) in crops.items():
    with Image.open(TMP/f'{key}.png') as im:
        # Coordinates recorded against the inspected 1376 x 1780 page view.
        actual=tuple(round(v*(im.width/1376 if i%2==0 else im.height/1780)) for i,v in enumerate(box))
        im.crop(actual).save(OUT/f'{name}.png')
    records.append({'output':name+'.png','source_id':key,'pixel_crop':actual,'treatment':'Crop only; no restoration or retouching.'})

with Image.open(TMP/'cuervo-map.png') as im:
    im.save(OUT/'cuervo-map-overview.png')
# This inspected detail preserves the source orientation and ownership coloring.
detail=OUT/'cuervo-rail-corridor-master.png'
with Image.open(detail) as im: im.crop((410,140,1070,480)).save(OUT/'cuervo-rail-detail.png')
records.append({'output':'cuervo-rail-detail.png','source_id':'cuervo-map','derived_from':str(detail),
                'pixel_crop_from_derivative':[410,140,1070,480],
                'treatment':'Enlargement of depot and warehouse; retained original orientation and ownership marks.'})

sys.path.insert(0,str(ROOT/'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
source=ROOT/'research_evidence/real_cattle_prices_2026-09-19/annual_prices_and_cpi.json'
data=json.loads(source.read_text(encoding='utf-8'))
rows=sorted(data['observations'],key=lambda r:r['year'])
assert [r['year'] for r in rows]==list(range(1913,1979))
base=next(r['real_1950_usd_per_cwt'] for r in rows if r['year']==1951)
values=[r['real_1950_usd_per_cwt']/base*100 for r in rows]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.unicode_minus':False})
fig,ax=plt.subplots(figsize=(7,4.9),layout='constrained')
ax.plot([r['year'] for r in rows],values,color='#1b3558',linewidth=2)
ax.set_xlim(1912,1980);ax.set_ylim(0,118)
ax.set_xticks([1920,1930,1940,1950,1960,1970,1978]);ax.set_yticks([0,25,50,75,100])
ax.set_ylabel('Consumer purchasing power; 1951 = 100',fontsize=11,labelpad=10)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#c9c2b8')
ax.tick_params(length=0,pad=7,labelsize=11,colors='#242528')
ax.grid(axis='y',color='#e8e4df',linewidth=.7);ax.set_axisbelow(True)
for year,offset,align in [(1951,(-12,15),'right'),(1956,(7,-24),'left'),(1973,(0,15),'center')]:
    value=values[year-1913]
    ax.scatter([year],[value],s=22,color='#1b3558',zorder=3)
    ax.annotate(f'{year}: {value:.0f}',(year,value),xytext=offset,textcoords='offset points',
                ha=align,fontsize=11,color='#1b3558',bbox={'facecolor':'white','edgecolor':'none','pad':2})
for ext in ['png','svg']:fig.savefig(OUT/f'cattle-price-cycle.{ext}',dpi=300,facecolor='white')
plt.close(fig)
records.append({'output':'cattle-price-cycle.png / .svg','source':str(source),
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'method':'100 * (price / CPI) / (1951 price / 1951 CPI)','observations':len(rows),
 'scope':'New Mexico beef cattle, excluding calves; annual price per 100 lb liveweight.',
 'limits':'Consumer purchasing power, not ranch profit; no population overlay or causal estimate.'})
(OUT/'sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Prepared archival details and 66-observation price chart.')
