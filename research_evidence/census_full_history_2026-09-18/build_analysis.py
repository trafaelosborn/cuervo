"""Expand the manual readings into source-addressable observations and age summaries."""
from pathlib import Path
import json, statistics, re, sys, os
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
raw=json.loads((HERE/'age_transcriptions.json').read_text(encoding='utf-8'))
observations=[]
expected={1910:545,1920:438,1930:287,1940:188,1950:210}
page_starts={1910:924,1920:39,1930:454,1940:652}
for year in [1910,1920,1930,1940]:
    item=raw[str(year)]
    for page,sequence in item['pages'].items():
        page=int(page);offset=page-page_starts[year]
        half=40 if year==1940 else 50
        printed_start=(offset%2)*half+1
        for i,token in enumerate(sequence.split()):
            if token=='-':continue
            assert re.fullmatch(r'[MF](?:\d{1,3}|\?)',token),token
            observations.append(dict(year=year,source=item['source'],pdf_page=page if year!=1940 else None,
                image=f'm-t0627-02445-00{page}.jpg' if year==1940 else None,
                sheet=f'{offset//2+1}{"A" if offset%2==0 else "B"}',line=printed_start+i,
                sex_recorded=token[0],age_completed_years=None if token[1:]=='?' else int(token[1:]),
                age_status='unknown' if token[1:]=='?' else 'manual-reading'))

old=ROOT/'research_evidence/census_deep_dive_2026-09-18'
ages=json.loads((old/'cuervo_1950_age_transcription.json').read_text(encoding='utf-8'))
inventory=json.loads((ROOT/'research_evidence/deep_dive_2026-09-17/cuervo_1950_person_count.json').read_text(encoding='utf-8'))['named_rows_by_sheet']
for sheet,seq in ages['sheets'].items():
    assert len(seq.split())==len(inventory[sheet])
    suffix=int(sheet)+1 if sheet!='71' else 10
    for line,token in zip(inventory[sheet],seq.split()):
        observations.append(dict(year=1950,source='sources/03_census/1950_manuscripts/ed_10-6/',pdf_page=None,
            image=f'43290879-New_Mexico-180130-{suffix:04}.jpg',sheet=sheet,line=line,
            sex_recorded=token[0],age_completed_years=int(token[1:]),age_status='manual-reading'))

def save(name,data):
    (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
save('person_age_observations.json',observations)
summaries={}
bins=[('0-4',0,4),('5-17',5,17),('18-34',18,34),('35-49',35,49),('50-64',50,64),('65+',65,130)]
for year in expected:
    records=[x for x in observations if x['year']==year]
    assert len(records)==expected[year],(year,len(records),expected[year])
    assert len({(x['sheet'],x['line']) for x in records})==len(records)
    vals=[r['age_completed_years'] for r in records if r['age_completed_years'] is not None]
    missing=len(records)-len(vals)
    assert all(0<=v<=110 for v in vals)
    under=sum(x<18 for x in vals);older=sum(x>=65 for x in vals)
    med_bounds=[statistics.median(vals+[0]*missing),statistics.median(vals+[110]*missing)]
    summaries[year]={
        'named_persons':len(records),'published_population':expected[year],'read_ages':len(vals),'unknown_ages':missing,
        'median_read_ages':statistics.median(vals),'median_all_possible_bounds':med_bounds,
        'mean_read_ages':statistics.mean(vals),'under18_read':under,
        'under18_possible_bounds':[under,under+missing],'under18_percent_lower':under/len(records)*100,
        'under18_percent_upper':(under+missing)/len(records)*100,
        'age65plus_read':older,'age65plus_possible_bounds':[older,older+missing],
        'recorded_sex_counts':dict(Counter(r['sex_recorded'] for r in records)),
        'age_bins_known':{label:sum(lo<=v<=hi for v in vals) for label,lo,hi in bins},
        'men_18_to_44_read':sum(r['sex_recorded']=='M' and r['age_completed_years'] is not None and 18<=r['age_completed_years']<=44 for r in records),
        'boys_12_to_17_read':sum(r['sex_recorded']=='M' and r['age_completed_years'] is not None and 12<=r['age_completed_years']<=17 for r in records),
        'unknown_records':[{'sheet':r['sheet'],'line':r['line'],'page_or_image':r['pdf_page'] or r['image']} for r in records if r['age_completed_years'] is None]
    }
save('age_summary.json',summaries)

published={
 'Cuervo precinct 6':dict(zip([1910,1920,1930,1940,1950],[545,438,287,188,210])),
 'Santa Rosa precinct 8':dict(zip([1910,1920,1930,1940,1950],[1031,1390,1381,2527,2548])),
 'Santa Rosa municipality':{1920:None,1930:1127,1940:2310,1950:2199},
 'Guadalupe County':dict(zip([1900,1910,1920,1930,1940,1950],[5429,10927,8015,7027,8646,6772]))
}
modern=json.loads((old/'population_housing_observations.json').read_text(encoding='utf-8'))
for name,records in modern.items():
    series_name='Santa Rosa municipality' if name=='Santa Rosa city' else name
    for year,rec in records.items():
        if 'population' in rec:published.setdefault(series_name,{})[int(year)]=rec['population']
save('published_population_series.json',{'method':'Observations on contemporary reporting units. Not constant boundaries. See report and prior source locators. Santa Rosa 1920 municipality unresolved: 1003 vs 1093.','series':published})

sys.path.insert(0,str(ROOT/'tmp/deep_dive/python_deps'))
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/census_full_history/matplotlib_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','figure.facecolor':'white','savefig.facecolor':'white'})
years=list(expected);ink='#203344';teal='#116466';gold='#B26A32'
fig,axes=plt.subplots(1,2,figsize=(10.7,4.1))
ax=axes[0]
counts=[expected[y] for y in years]
ax.bar(years,counts,width=5,color=teal)
for y,n in zip(years,counts):ax.text(y,n+10,str(n),ha='center',color=ink,fontweight='bold')
ax.set(title='Fewer residents',ylabel='Cuervo precinct: published persons',xticks=years,ylim=(0,610))
ax=axes[1]
med=[summaries[y]['median_read_ages'] for y in years]
ax.bar(years,med,width=5,color=gold)
for y,m in zip(years,med):
    low,high=summaries[y]['median_all_possible_bounds']
    ax.plot([y,y],[low,high],color=ink,lw=3)
    label=f'{low:g}' if low==high else f'{low:g}-{high:g}'
    ax.text(y,high+.6,label,ha='center',color=ink,fontweight='bold')
ax.set(title='No steady rise in median age',ylabel='Median recorded age (years)',xticks=years,ylim=(0,30))
fig.subplots_adjust(bottom=.22,wspace=.32,top=.86)
fig.text(.06,.06,'Manual manuscript readings. Median labels span all possible values of unread ages.\n1910-1920 precinct boundaries require reconstruction; named units are not fixed territory.',fontsize=8.5,color='#52636e')
fig.savefig(HERE/'population_and_age.png',dpi=190);plt.close(fig)

fig,ax=plt.subplots(figsize=(10,4.8));bottom=[0]*5
palette=['#8AC4B7','#277E78','#42677D','#7B94A2','#BC9B70','#865D3C','#D2D2D2']
for i,(label,lo,hi) in enumerate(bins):
    heights=[summaries[y]['age_bins_known'][label]/expected[y]*100 for y in years]
    ax.bar([str(y) for y in years],heights,bottom=bottom,label=label,color=palette[i],width=.58)
    bottom=[a+b for a,b in zip(bottom,heights)]
unknown=[summaries[y]['unknown_ages']/expected[y]*100 for y in years]
ax.bar([str(y) for y in years],unknown,bottom=bottom,label='Unread',color=palette[-1],width=.58)
ax.set(title='The precinct continued to contain many children',ylabel='Percent of all named residents',ylim=(0,100))
ax.legend(ncol=7,loc='upper center',bbox_to_anchor=(.5,-.11),frameon=False,fontsize=9)
fig.subplots_adjust(bottom=.24,top=.87,left=.08,right=.98)
fig.text(.08,.025,'Age composition of each census population, not a panel tracking the same people. Geography caveats apply.',fontsize=8.5,color='#52636e')
fig.savefig(HERE/'age_composition.png',dpi=190);plt.close(fig)

save('validation.json',{
 'named_person_observations':len(observations),'unique_people_across_years':None,
 'known_ages':sum(s['read_ages'] for s in summaries.values()),'unknown_ages':sum(s['unknown_ages'] for s in summaries.values()),
 'year_totals_match_published':True,'record_keys_unique_within_year':True,
 'independent_double_entry_transcription':False,
 'note':'These are 1668 census appearances, not 1668 distinct people. Source count reconciliation is not independent validation of every digit. No family or person linkage has yet been asserted.'
})
print(json.dumps(summaries,indent=2))
