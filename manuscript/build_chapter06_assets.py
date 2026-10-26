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
OUT=ROOT/'manuscript/figures/chapter06';OUT.mkdir(parents=True,exist_ok=True)
EV=ROOT/'research_evidence/chapter06_2026-09-28';EV.mkdir(parents=True,exist_ok=True)
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
labels=[('Tucumcari / 42 railway miles','Cuervo-Tucumcari','7:00 a.m.','8:20 a.m.','7:45 p.m.','9:00 p.m.'),
        ('Santa Rosa / 17 railway miles','Cuervo-Santa Rosa','9:00 p.m.','9:35 p.m.','6:20 a.m.','7:00 a.m.')]
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
fig,ax=plt.subplots(figsize=(7.1,5.7));fig.subplots_adjust(left=.31,right=.9,top=.9,bottom=.17)
keys=list(shares);names=['Population (1930)','Establishments','Retail sales','Stocks at year end','Retail payroll']
values=[shares[k] for k in keys];bars=ax.barh(range(5),values,color=[TAUPE]+[NAVY]*4,height=.5)
ax.set_yticks(range(5),names);ax.invert_yaxis();ax.set_xlim(0,60)
ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color('#c9c2b8');ax.tick_params(length=0,pad=8)
ax.set_xticks([0,20,40,60],['0%','20%','40%','60%']);ax.grid(axis='x',color=PALE);ax.set_axisbelow(True)
for bar,val in zip(bars,values):ax.text(val+1,bar.get_y()+bar.get_height()/2,f'{val:.1f}%',va='center',fontsize=12,color=NAVY)
ax.set_xlabel('Santa Rosa share of Guadalupe County',labelpad=14,fontsize=11)
fig.text(.05,.96,'Retail activity, 1929 / Population, 1930',fontsize=13,color=NAVY)
save(fig,'retail')

original=source('sources/01_railroad/local_functions_2026-09-20/ri_station_book.pdf','December 15, 1974; C 15 / PDF 67')
view=source('research_evidence/rail_local_functions_2026-09-20/ri_station_book_page_67.png','Prior page render; complete page visually rechecked')
for name,box in [('station-headings',(85,143,1380,291)),('station-rows',(85,474,1380,644)),('station-legend',(95,858,1040,914))]:
    with Image.open(view) as im:im.crop(box).save(OUT/f'{name}.png')
    manifest.append({'output':name+'.png','source_render':str(view.relative_to(ROOT)),'crop_pixels':box,'treatment':'Crop only, no retouching; omissions identified in caption'})

events=[('Southwest highway',1952,1952,'1952 / Route relocated','point'),
 ('Local passenger stops',1958+117/365,1958+299/365,'Apr-Oct 1958 / Stops disappear','bracket'),
 ('Train-order office',1956+273/366,1958+299/365,'Sep 1956-Oct 1958 / Designation disappears','bracket'),
 ('Nearby interstate project',1963,1965,'1963-1965 / Recorded construction interval','construction'),
 ('Through Golden State',1968,1968,'1968 / Through passenger service ends','point'),
 ('Freight administration',1974+348/365,1974+348/365,'Dec 1974 / No agent; billing at Tucumcari','point')]
fig,axes=plt.subplots(6,1,figsize=(7.1,7.35),sharex=True)
fig.subplots_adjust(left=.04,right=.96,top=.955,bottom=.075,hspace=.85)
for ax,(title,start,end,label,kind) in zip(axes,events):
    ax.set_xlim(1950,1978);ax.set_ylim(-.2,1);ax.set_yticks([])
    ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color(PALE)
    ax.tick_params(length=0,pad=9,labelsize=10)
    ax.text(1950,.95,title,fontsize=11.3,color=NAVY,va='top',weight='bold')
    if kind=='point':ax.scatter([start],[.2],color=NAVY,s=32,zorder=3)
    else:
        ax.plot([start,end],[.2,.2],color=TAUPE if kind=='bracket' else NAVY,lw=4,solid_capstyle='butt')
        ax.scatter([start,end],[.2,.2],s=18,facecolors='white' if kind=='bracket' else NAVY,edgecolors=TAUPE if kind=='bracket' else NAVY,zorder=3)
    ax.text(1950,-.45,label,fontsize=9.7,color=INK,va='top')
axes[-1].set_xticks([1950,1955,1960,1965,1970,1975])
axes[-1].spines['bottom'].set_visible(False)
axes[-1].tick_params(pad=27)
save(fig,'chronology')
for f in ['research_evidence/rail_local_functions_2026-09-20.md','research_evidence/cuervo_freight_accounting_1974_2026-09-20.md',
 'sources/04_highways/nrhp_abandoned_route_66_cuervo_to_nm_156_1993.pdf','sources/04_highways/ntsb_cuervo_2002_highway_factors_factual_report.pdf',
 'research_evidence/rail_service_2026-09-19.md']:
    source(f,'Chronology source; chart intervals retain observational limits')
calc={'retail_shares_pct':shares,'ratios':{'general_stores_share_pct':100*316/629,'filling_station_counted_sales_share_pct':100*33/38,
 'filling_station_share_of_santa_rosa_sales_pct':100*33/629,'tucumcari_to_santa_rosa_sales':3038/629},'journey_minutes':trip,
 'tucumcari_time_at_destination_minutes':685,'chronology':events,
 'limits':['Travel opportunities, not passenger counts or purchases.','Retail measures 1929; population measures 1930.',
 'Passenger and office spans bracket disappearance between inspected documents; they are not event durations.',
 'Freight-accounting identities do not establish actual shipments.']}
(EV/'calculations.json').write_text(json.dumps(calc,indent=2),encoding='utf-8')
(OUT/'sources.json').write_text(json.dumps({'created':'2026-09-28','inputs':manifest,'calculations':str(EV/'calculations.json')},indent=2),encoding='utf-8')
print('Three descriptive graphics and three source excerpts prepared; ratios and journey arithmetic checked.')
