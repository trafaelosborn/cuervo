"""Chapter 6: descriptive figures and unretouched station-book excerpts."""
from pathlib import Path
import os,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
OUT=ROOT/'manuscript/figures/book-revision10';OUT.mkdir(parents=True,exist_ok=True)

NAVY='#1b3558';TAUPE='#9c7151';INK='#242528';PALE='#ece8e2'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})
manifest=[]
def source(relative,role):
    p=ROOT/relative;manifest.append({'file':relative,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':role});return p
def save(fig,name):
    for ext in ['png','svg']:fig.savefig(OUT/f'{name}.{ext}',dpi=300,facecolor='white')
    plt.close(fig)
table=source('research_evidence/deep_dive_2026-09-17/retail_1929_table13.json','Previously checked retail transcription; arithmetic recomputed')
d=json.loads(table.read_text())['data'];sr=d['Santa Rosa'];cty=d['Guadalupe County']
shares={key:100*sr[key]/cty[key] for key in ['population_1930','stores','net_sales','stocks','payroll']}
for key in sr:assert sr[key]+d['Rest of Guadalupe County'][key]==cty[key]
source('research_evidence/deep_dive_2026-09-17/retail_1929_table14.json','Classification ratios and establishment counts')
trip={'Cuervo-Tucumcari':{'departure':420,'arrival':500,'return_departure':1185,'return_arrival':1260},
      'Cuervo-Santa Rosa':{'departure':1260,'arrival':1295,'return_departure':1820,'return_arrival':1860}}
# Correct return arrival: 7:00 next day = 1,860 minutes. All times Mountain Time.
trip['Cuervo-Santa Rosa']['return_arrival']=1860
assert trip['Cuervo-Tucumcari']['return_departure']-trip['Cuervo-Tucumcari']['arrival']==685
assert trip['Cuervo-Santa Rosa']['arrival']-trip['Cuervo-Santa Rosa']['departure']==35
assert trip['Cuervo-Santa Rosa']['return_arrival']-trip['Cuervo-Santa Rosa']['return_departure']==40
source('sources/01_railroad/rock_island_public_timetable_1926-01.pdf','Table 2 p.18, notes p.19; four advertised journeys')
fig,axes=plt.subplots(2,1,figsize=(7.1,5.8),sharex=True)
fig.subplots_adjust(left=.09,right=.97,top=.9,bottom=.16,hspace=.55)
labels=[('Tucumcari / 68 km (42 mi) by rail','Cuervo-Tucumcari','7:00 a.m.','8:20 a.m.','7:45 p.m.','9:00 p.m.'),
        ('Santa Rosa / 27 km (17 mi) by rail','Cuervo-Santa Rosa','9:00 p.m.','9:35 p.m.','6:20 a.m.','7:00 a.m.')]
for ax,(title,key,a,b,c,e) in zip(axes,labels):
    r=trip[key];v=[r[x]/60 for x in ['departure','arrival','return_departure','return_arrival']]
    ax.set_xlim(5.8,32.2);ax.set_ylim(-1,1);ax.set_yticks([])
    ax.spines[['top','left','right']].set_visible(False);ax.spines['bottom'].set_color('#c9c2b8')
    ax.axvspan(24,32.2,color='#f6f3ee',zorder=0)
    ax.plot(v[:2],[0,0],lw=7,color=NAVY,solid_capstyle='butt')
    ax.plot(v[1:3],[0,0],lw=7,color=TAUPE,solid_capstyle='butt')
    ax.plot(v[2:],[0,0],lw=7,color=NAVY,solid_capstyle='butt')
    ax.scatter(v,[0]*4,s=22,color=NAVY,zorder=3)
    ax.set_title(title,loc='left',color=NAVY,fontsize=13,pad=14)
    ax.text(v[0],-.24,a+'\nLeave Cuervo',ha='left',va='top',fontsize=9.4)
    ax.text(v[1],.2,b+'\nArrive',ha='left',va='bottom',fontsize=9.4)
    ax.text(v[2],.2,c+'\nLeave',ha='right',va='bottom',fontsize=9.4)
    ax.text(v[3],-.24,e+'\nBack in Cuervo',ha='right',va='top',fontsize=9.4)
    ax.tick_params(length=0,pad=10,labelsize=9)
axes[0].text(14.04,-.78,'11 hr 25 min in Tucumcari',ha='center',va='top',fontsize=10,color=TAUPE)
axes[1].text(25.95,-.78,'Overnight in Santa Rosa',ha='center',va='top',fontsize=10,color=TAUPE)
axes[1].set_xticks([6,12,18,24,30],['6 a.m.','Noon','6 p.m.','Midnight','6 a.m.\nNext day'])
fig.text(.09,.035,'NAVY  Train journey     BROWN  Time at destination',fontsize=10,color=NAVY)
save(fig,'journeys')
(OUT/'journey-sources.json').write_text(json.dumps({'date':'2026-10-02','inputs':manifest,'journey_minutes':trip,'kilometers_per_mile':1.609344,'distance_rounding':'Nearest whole kilometer; original whole-mile distances retained'},indent=2),encoding='utf-8')
