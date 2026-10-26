"""Reproduce all headline counts from the dated transcription and observations."""
from pathlib import Path
from collections import Counter
import json, statistics, sys, os

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
people=json.loads((HERE/'people_name_age_readings.json').read_text())
hh=json.loads((HERE/'households.json').read_text())
assert len(people)==398 and len({p['id'] for p in people})==398
assert sorted(p['id'] for p in people)==sorted(i for h in hh for i in h['members'])
s={}
for year in [1940,1950]:
    pp=[p for p in people if p['year']==year]; h=[a for a in hh if a['year']==year]
    ages=[p['age_completed_years'] for p in pp if p['age_completed_years'] is not None]
    s[str(year)]={'people':len(pp),'head_listed_households':len(h),'mean_household_size':len(pp)/len(h),
        'size_distribution':dict(sorted(Counter(a['count'] for a in h).items())),
        'under10_known':sum(a<10 for a in ages),'under18_known':sum(a<18 for a in ages),
        'age0_19_known':sum(a<20 for a in ages),'age10_29_known':sum(10<=a<30 for a in ages),
        'age40_59_known':sum(40<=a<60 for a in ages),'age50_69_known':sum(50<=a<70 for a in ages),
        'median_read_age':statistics.median(ages),'unread_ages':len(pp)-len(ages)}
assert s['1940']['people']==188 and s['1950']['people']==210
assert s['1940']['head_listed_households']==42 and s['1950']['head_listed_households']==59
assert s['1950']['under10_known']==51
s['cohort_accounting']={'baseline_1940':188,'age10_plus_in_1950':159,'under10_in_1950':51,'cohorts_alive_at_1940_census_net_difference':-29,'net_population_change':22}
occ=json.loads((ROOT/'research_evidence/deep_dive_2026-09-17/cuervo_1950_occupation_readings.json').read_text())['entries']
idx={(str(p['sheet']),p['line']):p for p in people if p['year']==1950}
ranch_hh={idx[(str(o['sheet']),o['line'])]['household'] for o in occ if o['sector']=='Ranching'}
rr=[h for h in hh if h['id'] in ranch_hh]
s['1950_ranch_affiliation']={'definition':'At least one main occupation description classified Ranching; descriptive current association, not household fertility or land ownership.',
    'households':len(rr),'people':sum(h['count'] for h in rr),'under10':sum(h['under10_known'] for h in rr),'under18':sum(h['under18_known'] for h in rr)}
mig=json.loads((HERE/'prior_residence_readings.json').read_text())['observations']
for label,rows in [('out_of_county', [r for r in mig if r['movement_type']=='out_of_county']),('all_prior_places',mig)]:
    hids={x['household'] for x in rows}
    s[label]={'sample_entries':len(rows),'households':len(hids),'all_1950_members_in_these_households':sum(h['count'] for h in hh if h['id'] in hids),
        'caution':'Household residents are not all proven migrants; observations are not a net migration estimate.'}
a=json.loads((HERE/'agriculture_observations.json').read_text())['observations']
def val(metric,year): return next(x['value'] for x in a if x['metric']==metric and x['reference_year']==year)
s['agriculture_changes_percent']={}
for metric,y0,y1 in [('cattle_and_calves_sold_alive',1939,1944),('cattle_and_calves_sold_alive',1944,1949),('cattle_and_calves_sold_alive',1939,1949),('cattle_and_calves_inventory',1940,1945),('cattle_and_calves_inventory',1945,1950),('farms',1945,1950)]:
    s['agriculture_changes_percent'][f'{metric}_{y0}_{y1}']=100*(val(metric,y1)/val(metric,y0)-1)
(HERE/'analysis_summary.json').write_text(json.dumps(s,indent=2),encoding='utf-8')

# Publication figure: two distinct scales, fully labelled; no causal trend fitting.
sys.path.insert(0,str(ROOT/'tmp/deep_dive/python_deps'))
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/rebound_1940_1950/matplotlib_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(10,3.8),gridspec_kw={'wspace':.35})
for ax,vals,labels,title,col in [
    (axes[0],[42,59],['1940','1950'],'Cuervo: head-listed households','#14666a'),
    (axes[1],[7399,19724,17595],['1939','1944','1949'],'Guadalupe County: cattle/calves sold','#b46e35')]:
    bars=ax.bar(labels,vals,color=col,width=.57); ax.set_title(title,loc='left',fontsize=11,pad=16)
    ax.set_ylim(0,max(vals)*1.22);ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True)
    for b,v in zip(bars,vals):ax.text(b.get_x()+b.get_width()/2,v+max(vals)*.035,f'{v:,}',ha='center',fontweight='bold')
axes[0].set_ylabel('Households (manual grouping)');axes[1].set_ylabel('Head sold during calendar year')
fig.text(.08,.02,'Different geographies and measures. Neither series alone identifies the cause of population change.',fontsize=8.5,color='#445563')
fig.subplots_adjust(bottom=.19,top=.86,left=.08,right=.98)
fig.savefig(HERE/'households_and_cattle.png',dpi=200,facecolor='white');plt.close(fig)
print(json.dumps(s,indent=2))
