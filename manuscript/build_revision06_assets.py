"""Rebuild changed scholarly figures from their recorded source data."""
from pathlib import Path
import sys, os, json, textwrap, hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
OUT=ROOT/'manuscript/figures/book-revision06';OUT.mkdir(parents=True,exist_ok=True)
NAVY,TAUPE,INK,GRAY,RULE='#1b3558','#9c7151','#242528','#756e65','#d8d2c9'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.unicode_minus':False})
manifest={}
def save(fig,key,provenance):
    for ext in ['png','svg']:fig.savefig(OUT/f'{key}.{ext}',dpi=300,facecolor='white')
    plt.close(fig);manifest[key]=provenance

# Use the intact archival JPEG2000; the earlier JPEG derivative is damaged.
source=ROOT/'sources/06_maps/sanborn_santa_rosa_1908_sheet_01.jp2'
with Image.open(source) as im:
    im.load();im.save(OUT/'santa-rosa-full.png')
    boxes={'warehouse':(410,300,1830,870),'station':(5050,40,6040,470),'bank':(3710,2620,4520,3010)}
    for key,box in boxes.items():im.crop(box).save(OUT/f'santa-rosa-{key}.png')
manifest['santa-rosa-map']={'source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop_boxes':boxes,'treatment':'Full overview and separately labeled crops; no retouching. Intact JP2 replaces corrupted JPEG derivative.'}

age_source='research_evidence/chapter05_2026-09-28/calculations.json'
age={int(y):v for y,v in json.loads((ROOT/age_source).read_text(encoding='utf-8'))['age'].items()}
fig,axes=plt.subplots(2,1,figsize=(6.9,6.3),layout='constrained');ys=list(age)
for ax in axes:
    ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color('#c9c2b8')
    ax.tick_params(length=0,pad=7,colors=INK,labelsize=11);ax.grid(axis='y',color='#e8e4df',linewidth=.7);ax.set_axisbelow(True)
    ax.set_xticks(ys);ax.set_xlim(1906,1954)
axes[0].scatter(ys,[age[y]['population'] for y in ys],color=NAVY,s=45)
for y in ys:axes[0].annotate(str(age[y]['population']),(y,age[y]['population']),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12,color=NAVY)
axes[0].set_ylim(0,650);axes[0].set_ylabel('People');axes[0].set_title('Population in the named Cuervo precinct',loc='left',fontsize=13,color=NAVY,pad=12)
for y in ys:
    lo,hi=age[y]['median_bounds'];mid=(lo+hi)/2
    if lo!=hi:axes[1].errorbar(y,mid,yerr=(hi-lo)/2,fmt='none',color=TAUPE,capsize=5,linewidth=2)
    else:axes[1].scatter([y],[mid],color=TAUPE,s=38)
    label=f'{lo:g}–{hi:g}' if lo!=hi else f'{lo:g}'
    axes[1].annotate(label,(y,hi),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12,color=TAUPE)
axes[1].set_ylim(0,35);axes[1].set_yticks([0,10,20,30]);axes[1].set_ylabel('Years');axes[1].set_title('Median age, allowing for unread entries',loc='left',fontsize=13,color=NAVY,pad=12)
save(fig,'population-and-age',{'source':age_source,'age':age,'change':'En dashes in age ranges; source values unchanged.'})

regional=json.loads((ROOT/'research_evidence/census_deep_dive_2026-09-18/population_housing_observations.json').read_text(encoding='utf-8'))
sr=regional['Santa Rosa city'];years=[1980,1990,2000,2010,2020]
hp=[sr[str(y)]['household_population'] for y in years];gq=[sr[str(y)]['group_quarters'] for y in years]
fig,ax=plt.subplots(figsize=(6.9,4.5),layout='constrained')
ax.bar(years,hp,width=5,color=NAVY,label='Household residents');ax.bar(years,gq,bottom=hp,width=5,color=TAUPE,label='Group-quarters residents')
for y,a,b in zip(years,hp,gq):ax.text(y,a+b+70,f'{a+b:,}',ha='center',fontsize=11)
ax.set_xticks(years);ax.set_ylim(0,4050);ax.set_ylabel('People');ax.spines[['top','right']].set_visible(False)
ax.legend(frameon=False,fontsize=10,loc='upper left');ax.set_title('Santa Rosa: population by living arrangement',loc='left',fontsize=13,color=NAVY,pad=18)
save(fig,'regional-households',{'source':'research_evidence/census_deep_dive_2026-09-18/population_housing_observations.json','years':years,'household_population':hp,'group_quarters':gq,'change':'Santa Rosa panel only; Los Lunas is discussed in Chapter 7.'})

old=json.loads((ROOT/'manuscript/figures/book-revision03/sources.json').read_text(encoding='utf-8'))
events=next(x['events'] for x in old['figures'] if x['key']=='functional-chronology')
events.insert(5,{'date':'1952','function':'ROAD ALIGNMENT','text':'The highway southwest of Cuervo moved to a new course.','reference':'1993 National Register nomination, sections 7–10; Chapter 6.'})
for row in events:row['date']=row['date'].replace('1963-65','1963–1965')
fig=plt.figure(figsize=(8,9.5));ax=fig.add_axes([.015,.045,.97,.90]);ax.set_xlim(0,1);ax.set_ylim(-.9,10.7);ax.axis('off')
fig.text(.045,.983,'SELECTED OBSERVATIONS / 1903–2026',color=GRAY,fontsize=11,va='top')
ax.plot([.245,.245],[0,10],color=RULE,lw=1.4)
for i,row in enumerate(events):
    y=10-i;ax.scatter(.245,y,s=27,color=NAVY)
    ax.text(.215,y+.1,row['date'],ha='right',va='top',color=NAVY,fontsize=11.5,weight='bold')
    ax.text(.285,y+.23,row['function'],va='top',color=TAUPE,fontsize=9,weight='bold')
    ax.text(.285,y-.025,textwrap.fill(row['text'],width=59),va='top',color=INK,fontsize=10.6,linespacing=1.3)
fig.text(.045,.02,'Equal row spacing shows sequence, not elapsed time or continuous operation.',color=GRAY,fontsize=9)
save(fig,'functional-chronology',{'source':'manuscript/figures/book-revision03/sources.json','events':events,'added':'1952 southwest highway realignment'})

events6=[('Southwest highway',1952,1952,'1952 / Route relocated','point'),
 ('Local passenger stops',1958+117/365,1958+299/365,'Apr–Oct 1958 / Stops disappear','bracket'),
 ('Train-order office',1956+273/366,1958+299/365,'Sep 1956–Oct 1958 / Designation disappears','bracket'),
 ('Nearby interstate project',1963,1965,'1963–1965 / Recorded construction interval','construction'),
 ('Through Golden State',1968,1968,'March 1968 / Golden State discontinued','point'),
 ('Freight administration',1974+348/365,1974+348/365,'Dec 1974 / No agent; billing at Tucumcari','point')]
fig,axes=plt.subplots(6,1,figsize=(7.1,7.35),sharex=True)
fig.subplots_adjust(left=.04,right=.96,top=.955,bottom=.075,hspace=.85)
for ax,(title,start,end,label,kind) in zip(axes,events6):
    ax.set_xlim(1950,1978);ax.set_ylim(-.2,1);ax.set_yticks([]);ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color(RULE);ax.tick_params(length=0,pad=9,labelsize=10)
    ax.text(1950,.95,title,fontsize=11.3,color=NAVY,va='top',weight='bold')
    if kind=='point':ax.scatter([start],[.2],color=NAVY,s=32)
    else:
        ax.plot([start,end],[.2,.2],color=TAUPE if kind=='bracket' else NAVY,lw=4,solid_capstyle='butt')
        ax.scatter([start,end],[.2,.2],s=18,facecolors='white' if kind=='bracket' else NAVY,edgecolors=TAUPE if kind=='bracket' else NAVY,zorder=3)
    ax.text(1950,-.45,label,fontsize=9.7,color=INK,va='top')
axes[-1].set_xticks([1950,1955,1960,1965,1970,1975]);axes[-1].spines['bottom'].set_visible(False);axes[-1].tick_params(pad=27)
save(fig,'chronology',{'source':'manuscript/build_chapter06_assets.py','events':events6,'change':'Name the Golden State and standardize ranges.'})
(OUT/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Built 5 revised figures and 3 Sanborn details.')
