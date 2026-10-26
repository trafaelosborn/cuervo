"""Extract faithful engineering plates and add plan approval to the timeline."""
from pathlib import Path
import sys,os,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/pdfs/matplotlib-config'))
import pypdfium2 as pdfium
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=ROOT/'manuscript/figures/book-revision08';OUT.mkdir(exist_ok=True)
source=ROOT/'sources/DOT/I-040-5(13)291-AS-BUILT.pdf'
doc=pdfium.PdfDocument(source)
manifest={'source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'treatment':'PDF rendering and rectangular cropping only. Original marks retained; no generative restoration, erasure or contrast reconstruction.','plates':{}}
pages={}
for n in [151,137,114]:
 p=doc[n-1];im=p.render(scale=6000/max(p.get_size())).to_pil();pages[n]=im;p.close()
def crop(key,n,box=None):
 im=pages[n]
 if box:
  # Coordinates refer to the checked 3401 x 2628 reference rendering.
  b=tuple(round(v*(im.width/3401 if i%2==0 else im.height/2628)) for i,v in enumerate(box))
  result=im.crop(b)
 else:b=None;result=im
 result.save(OUT/f'{key}.png')
 manifest['plates'][key]={'pdf_page':n,'render_pixels':list(im.size),'crop_pixels':b,'output_pixels':list(result.size)}
crop('dot-town',151,(100,330,3260,2350))
crop('dot-north',151,(1770,390,3240,970))
crop('dot-south',151,(1230,930,3260,1630))
crop('dot-interchange',137,(175,600,3250,1870))
crop('dot-signs',114,(1825,410,2390,1480))
doc.close()

NAVY,TAUPE,INK,GRAY,RULE='#1b3558','#9c7151','#242528','#756e65','#d8d2c9'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.unicode_minus':False})
events=[('Southwest highway',1952,1952,'1952 / Route relocated','point'),
 ('Local passenger stops',1958+117/365,1958+299/365,'Apr–Oct 1958 / Stops disappear','bracket'),
 ('Train-order office',1956+273/366,1958+299/365,'Sep 1956–Oct 1958 / Designation disappears','bracket'),
 ('Cuervo interchange plan',1963+195/365,1963+195/365,'15 Jul 1963 / State approval; opening date unestablished','approval'),
 ('Nearby interstate project',1963,1965,'1963–1965 / Recorded construction interval','construction'),
 ('Through Golden State',1968,1968,'Mar 1968 / Golden State discontinued','point'),
 ('Freight administration',1974+348/365,1974+348/365,'Dec 1974 / No agent; billing at Tucumcari','point')]
fig,axes=plt.subplots(7,1,figsize=(7.1,8.5),sharex=True)
fig.subplots_adjust(left=.025,right=.97,top=.97,bottom=.08,hspace=.80)
for ax,(title,start,end,label,kind) in zip(axes,events):
 ax.set_xlim(1950,1976);ax.set_ylim(-.9,1);ax.spines[:].set_visible(False);ax.set_yticks([]);ax.tick_params(axis='x',length=0,labelsize=10,colors=GRAY)
 ax.text(1950,.82,title,fontsize=11,color=NAVY,weight='bold',va='top')
 ax.axhline(.15,color=RULE,lw=.7)
 if start==end:ax.scatter([start],[.15],marker='D' if kind=='approval' else 'o',s=39,facecolors='white' if kind=='approval' else NAVY,edgecolors=NAVY,zorder=3)
 else:
  ax.plot([start,end],[.15,.15],color=TAUPE if kind=='bracket' else NAVY,lw=3.5,solid_capstyle='butt')
  ax.scatter([start,end],[.15,.15],s=18,facecolors='white' if kind=='bracket' else NAVY,edgecolors=TAUPE if kind=='bracket' else NAVY,zorder=3)
 ax.text(1950,-.45,label,fontsize=9.2,color=INK,va='top')
axes[-1].set_xticks([1950,1955,1960,1965,1970,1975]);axes[-1].tick_params(pad=30)
for ext in ['png','svg']:fig.savefig(OUT/f'chronology.{ext}',dpi=300,facecolor='white')
plt.close(fig)
manifest['chronology']={'base':'manuscript/figures/book-revision06/sources.json','events':events,'addition':'State approval of project I-040-5(13)291; separate from nearby construction interval.'}
(OUT/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Five engineering excerpts and revised chronology generated.')
