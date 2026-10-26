"""Chapter 5 figures from held, corrected transcriptions; no source data overwritten."""
from pathlib import Path
import os,sys,json,hashlib,statistics
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
OUT=ROOT/'manuscript/figures/chapter05';OUT.mkdir(parents=True,exist_ok=True)
EVIDENCE=ROOT/'research_evidence/chapter05_2026-09-28';EVIDENCE.mkdir(parents=True,exist_ok=True)
NAVY='#1b3558';TAUPE='#9c7151';INK='#242528'
manifest=[]
def data(relative):
    path=ROOT/relative
    manifest.append({'file':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'role':'held transcription or analysis input'})
    return json.loads(path.read_text(encoding='utf-8'))
early=data('research_evidence/census_full_history_2026-09-18/person_age_observations.json')
revised=data('research_evidence/rebound_1940_1950_2026-09-19/people_name_age_readings.json')
people=[p for p in early if p['year']<1940]+revised
published=data('research_evidence/census_full_history_2026-09-18/published_population_series.json')['series']['Cuervo precinct 6']
households=data('research_evidence/rebound_1940_1950_2026-09-19/households.json')
regional=data('research_evidence/census_deep_dive_2026-09-18/population_housing_observations.json')
age={}
for year in [1910,1920,1930,1940,1950]:
    rows=[p for p in people if p['year']==year]
    known=[p['age_completed_years'] for p in rows if p['age_completed_years'] is not None]
    missing=len(rows)-len(known);under18=sum(a<18 for a in known)
    age[year]={'population':len(rows),'known_ages':len(known),'unknown_ages':missing,
               'median_bounds':[statistics.median(known+[0]*missing),statistics.median(known+[110]*missing)],
               'under18_bounds':[under18,under18+missing]}
    assert len(rows)==published[str(year)]
assert sum(x['population'] for x in age.values())==1668
assert sum(x['unknown_ages'] for x in age.values())==7
assert age[1950]['median_bounds']==[25.5,25.5]
hh={}
for year in [1940,1950]:
    groups=[r for r in households if r['year']==year]
    count=sum(g['count'] for g in groups)
    assert count==age[year]['population']
    hh[year]={'people':count,'groups':len(groups),'mean_size':count/len(groups),
              'one_or_two_people':sum(g['count']<=2 for g in groups),'three_or_more_people':sum(g['count']>=3 for g in groups)}
assert [hh[y]['groups'] for y in [1940,1950]]==[42,59]
sr=regional['Santa Rosa city'];ll=regional['Los Lunas village']
years=[1980,1990,2000,2010,2020]
for year in years:
    for place in [sr,ll]:
        r=place[str(year)];assert r['population']==r['household_population']+r['group_quarters']
calculations={'age':age,'household_groups':hh,'regional':{k:regional[k] for k in ['Santa Rosa city','Los Lunas village']},
  'derived':{'cuervo_1940_1950_population_pct':100*(210/188-1),'cuervo_household_group_pct':100*(59/42-1),
             'santa_rosa_1990_2020_net_total':2850-2263,'santa_rosa_1990_2020_net_household':2261-2240,
             'santa_rosa_1990_2020_net_group_quarters':589-23,
             'santa_rosa_group_quarters_share_of_net_gain_pct':100*(589-23)/(2850-2263),
             'los_lunas_1990_2020_household_population_pct':100*(16994/5936-1)},
  'limits':['Reporting units are not reconstructed constant boundaries.','Age bounds reflect unread values only, not all enumeration or transcription error.',
            'Head-listed groups are a manual grouping, not a count of dwellings or migrating families.','Group-quarters subtraction is descriptive, not a counterfactual without the institution.']}
(EVIDENCE/'calculations.json').write_text(json.dumps(calculations,indent=2),encoding='utf-8')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none'})
def style(ax):
    ax.spines[['top','right','left']].set_visible(False);ax.spines['bottom'].set_color('#c9c2b8')
    ax.tick_params(length=0,pad=7,colors=INK,labelsize=11);ax.grid(axis='y',color='#e8e4df',linewidth=.7);ax.set_axisbelow(True)
def save(fig,name):
    for ext in ['png','svg']:fig.savefig(OUT/f'{name}.{ext}',dpi=300,facecolor='white')
    plt.close(fig)
fig,axes=plt.subplots(2,1,figsize=(6.9,6.3),layout='constrained')
ys=list(age)
for ax in axes:style(ax);ax.set_xticks(ys);ax.set_xlim(1906,1954)
axes[0].scatter(ys,[age[y]['population'] for y in ys],color=NAVY,s=45)
for y in ys:axes[0].annotate(str(age[y]['population']),(y,age[y]['population']),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12,color=NAVY)
axes[0].set_ylim(0,650);axes[0].set_ylabel('People');axes[0].set_title('Population in the named Cuervo precinct',loc='left',fontsize=13,color=NAVY,pad=12)
for y in ys:
    lo,hi=age[y]['median_bounds'];mid=(lo+hi)/2
    if lo!=hi:axes[1].errorbar(y,mid,yerr=(hi-lo)/2,fmt='none',color=TAUPE,capsize=5,linewidth=2)
    else:axes[1].scatter([y],[mid],color=TAUPE,s=38)
    label=f'{lo:g}-{hi:g}' if lo!=hi else f'{lo:g}'
    axes[1].annotate(label,(y,hi),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12,color=TAUPE)
axes[1].set_ylim(0,35);axes[1].set_yticks([0,10,20,30]);axes[1].set_ylabel('Years');axes[1].set_title('Median age, allowing for unread entries',loc='left',fontsize=13,color=NAVY,pad=12)
save(fig,'population-and-age')
fig,axes=plt.subplots(2,1,figsize=(6.9,6.1),layout='constrained')
for ax in axes:style(ax);ax.set_xticks([0,1],['1940','1950']);ax.set_xlim(-.6,1.6)
axes[0].bar([0,1],[188,210],width=.48,color=NAVY)
for x,value in enumerate([188,210]):axes[0].text(x,value+6,str(value),ha='center',fontsize=13,color=NAVY)
axes[0].set_ylim(0,260);axes[0].set_ylabel('People');axes[0].set_title('A modest population increase',loc='left',fontsize=13,color=NAVY,pad=10)
small=[13,27];large=[29,32]
axes[1].bar([0,1],small,width=.48,color=TAUPE,label='One or two people')
axes[1].bar([0,1],large,bottom=small,width=.48,color=NAVY,label='Three or more people')
for x in [0,1]:
    axes[1].text(x,small[x]/2,str(small[x]),ha='center',va='center',color='white',fontsize=12)
    axes[1].text(x,small[x]+large[x]/2,str(large[x]),ha='center',va='center',color='white',fontsize=12)
    axes[1].text(x,small[x]+large[x]+2,str(small[x]+large[x]),ha='center',fontsize=13,color=NAVY)
axes[1].set_ylim(0,90);axes[1].set_ylabel('Head-listed groups');axes[1].set_title('More groups, especially smaller ones',loc='left',fontsize=13,color=NAVY,pad=10)
axes[1].legend(frameon=False,fontsize=10,ncol=2,loc='upper center')
save(fig,'people-and-households')
fig,axes=plt.subplots(2,1,figsize=(6.9,6.6),layout='constrained')
for ax in axes:style(ax);ax.set_xticks(years);ax.set_xlim(1975,2025)
hp=[sr[str(y)]['household_population'] for y in years];gq=[sr[str(y)]['group_quarters'] for y in years]
axes[0].bar(years,hp,width=5,color=NAVY,label='Households');axes[0].bar(years,gq,bottom=hp,width=5,color=TAUPE,label='Group quarters')
for y,a,b in zip(years,hp,gq):axes[0].text(y,a+b+60,f'{a+b:,}',ha='center',fontsize=10)
axes[0].set_ylim(0,4000);axes[0].set_ylabel('People');axes[0].set_title('Santa Rosa: total population by living arrangement',loc='left',fontsize=12.5,color=NAVY,pad=12)
axes[0].legend(frameon=False,fontsize=10,ncol=2,loc='upper left')
axes[1].plot(years,hp,color=NAVY,marker='o',markersize=4,linewidth=1.6,label='Santa Rosa')
axes[1].plot(years,[ll[str(y)]['household_population'] for y in years],color=TAUPE,marker='s',markersize=4,linewidth=1.6,label='Los Lunas')
axes[1].set_ylim(0,20500);axes[1].set_yticks([0,5000,10000,15000,20000],['0','5,000','10,000','15,000','20,000'])
axes[1].set_ylabel('People in households');axes[1].set_title('Two different household-population histories',loc='left',fontsize=12.5,color=NAVY,pad=12)
axes[1].legend(frameon=False,fontsize=10,loc='upper left')
axes[1].annotate('16,994',(2020,16994),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10,color=TAUPE)
axes[1].annotate('2,261',(2020,2261),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10,color=NAVY)
save(fig,'regional-households')

def crop(relative,name,box):
    source=ROOT/relative
    with Image.open(source) as im:im.crop(box).save(OUT/f'{name}.png')
    manifest.append({'output':name+'.png','derived_from':relative,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'crop_pixels':box,'treatment':'Crop only; no retouching. Adjacent panels omit intervening columns, identified in the caption.'})
higgins='research_evidence/pupil_links_and_holbrook_2026-09-21/crops/1950_higgins.png'
crop(higgins,'higgins-names',(415,0,1490,294));crop(higgins,'higgins-work',(2330,0,3300,294))
cafe='research_evidence/regional_functions_2026-09-21/census_views/10-8_0024.jpg'
crop(cafe,'cafe-names',(337,410,818,608));crop(cafe,'cafe-work',(1490,410,1940,608))
manifest.append({'census_source':'sources/03_census/1950_manuscripts/ed_10-6/43290879-New_Mexico-180130-0009.jpg','sheet':'8','lines':'19-22',
 'prior_crop_manifest':'research_evidence/pupil_links_and_holbrook_2026-09-21/crop_manifest.json'})
manifest.append({'census_source':'sources/03_census/1950_manuscripts/ed_10-8/43290879-New_Mexico-180132-0024.jpg','sheet':'71','lines':'1-5',
 'prior_view_manifest':'research_evidence/regional_functions_2026-09-21/census_view_manifest.json'})
for item in manifest:
    if 'census_source' in item:item['source_sha256']=hashlib.sha256((ROOT/item['census_source']).read_bytes()).hexdigest()
(OUT/'sources.json').write_text(json.dumps({'created':'2026-09-28','inputs':manifest,'calculation_file':str(EVIDENCE/'calculations.json')},indent=2),encoding='utf-8')
print('Three charts and four census details prepared; totals and corrected age values checked.')
