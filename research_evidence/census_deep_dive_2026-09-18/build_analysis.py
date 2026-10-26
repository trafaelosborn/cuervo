"""Reproduce the September 18 census comparisons from saved primary-source readings."""
from pathlib import Path
import json, statistics, sys, os

sys.stdout.reconfigure(encoding='utf-8')
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tmp/deep_dive/python_deps'))
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/census_deep_dive/matplotlib_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

def save(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2)+'\n', encoding='utf-8')

# All older cells below were visually checked against the scanned tables.
# PDF page numbers are one-based. Modern records are extracted from official bulk files.
manual = {
 'Santa Rosa city': {
   1950: {'population':2199, 'source':'1950 Table 6, printed 31-8'},
   1960: {'population':2220, 'source':'1970 Table 10, printed 33-14 / PDF 24'},
   1970: {'population':2485, 'housing_units':724, 'source':'1970 Table 10, printed 33-14 / PDF 24; 1990 CPH-2 Table 9, printed 17 / PDF 30'},
   1980: {'population':2469, 'household_population':2467, 'group_quarters':2, 'households':811, 'housing_units':992, 'median_age':25.4, 'source':'1980 PC80-1-B33 Table 14, printed 33-8 / PDF 22; 1990 CPH-2 Table 9'},
   1990: {'population':2263, 'household_population':2240, 'group_quarters':23, 'households':810, 'housing_units':988, 'median_age':30.4, 'families':614, 'living_alone':180, 'land_sq_miles':2.8, 'source':'1990 CP-1-33 Tables 1 and 75, printed 2 and 248 / PDF 21 and 267; CPH-2 Table 9'},
   2000: {'population':2744, 'household_population':2241, 'group_quarters':503, 'households':898, 'housing_units':1024, 'vacant':126, 'land_sq_miles':4.25, 'source':'2000 PHC-1-33 Tables 9, 10, 11, 16, printed 63, 69, 72, 95 / PDF 76, 82, 85, 108'}
 },
 'Los Lunas village': {
   1970: {'population':973, 'housing_units':288, 'source':'1990 CPH-2-33 Table 9, printed 16 / PDF 29'},
   1980: {'population':3525, 'household_population':3158, 'group_quarters':367, 'households':1043, 'housing_units':1146, 'median_age':24.4, 'source':'1980 PC80-1-B33 Table 14, printed 33-7 / PDF 21; 1990 CPH-2 Table 9'},
   1990: {'population':6013, 'household_population':5936, 'group_quarters':77, 'households':2059, 'housing_units':2272, 'median_age':28.4, 'land_sq_miles':6.1, 'source':'1990 CP-1-33 Tables 1 and 2, printed 2 and 4 / PDF 21 and 23; household population = total minus group quarters; CPH-2 Table 9'},
   2000: {'population':10034, 'household_population':9920, 'group_quarters':114, 'households':3601, 'source':'2000 PHC-1-33 Table 10, printed 68 / PDF 81'}
 },
 'Guadalupe County': {
   1950: {'population':6772, 'median_age':21.0, 'percent_65_plus':5.2, 'source':'1950 PC volume II Table 12, printed 31-16 / PDF 14'},
   1960: {'population':5610, 'source':'1970 Table 10, printed 33-14 / PDF 24'},
   1970: {'population':4969, 'source':'1990 CPH-2-33 Table 8, printed 10 / PDF 23'},
   1980: {'population':4496, 'household_population':4494, 'group_quarters':2, 'households':1498, 'housing_units':2143, 'source':'1980 PC80-1-B33 Table 14, printed 33-8 / PDF 22; 1990 CPH-2 Table 8'},
   1990: {'population':4156, 'household_population':4133, 'group_quarters':23, 'households':1520, 'housing_units':2149, 'source':'1990 CP-1-33 Table 76, printed 249 / PDF 268; household population = total minus group quarters; CPH-2 Table 8'},
   2000: {'population':4680, 'household_population':4155, 'group_quarters':525, 'households':1655, 'housing_units':2160, 'vacant':505, 'source':'2000 PHC-1-33 Tables 9 and 11, printed 63 and 72 / PDF 76 and 85'}
 },
 'Tucumcari city': {
   1970: {'population':7189, 'source':'1990 CPH-2-33 Table 9, printed 17 / PDF 30'},
   1980: {'population':6765, 'source':'1990 CPH-2-33 Table 9'},
   1990: {'population':6831, 'source':'1990 CPH-2-33 Table 9'},
   2000: {'population':5989, 'source':'2000 PHC-1-33 Table 16, printed 95 / PDF 108'}
 },
 'Vaughn town': {
   1970: {'population':867, 'source':'1990 CPH-2-33 Table 9, printed 17 / PDF 30'},
   1980: {'population':737, 'source':'1990 CPH-2-33 Table 9'},
   1990: {'population':633, 'source':'1990 CPH-2-33 Table 9'},
   2000: {'population':539, 'household_population':539, 'group_quarters':0, 'households':232, 'housing_units':338, 'vacant':106, 'source':'2000 PHC-1-33 Tables 9, 11 and 16, printed 63, 72 and 95 / PDF 76, 85 and 108'}
 }
}
save('manual_published_readings.json',manual)
series = manual
for year in [2010,2020]:
    for rec in json.loads((HERE/f'modern_{year}_extract.json').read_text(encoding='utf-8')):
        g,v = rec['geography'],rec['values'];name=g['NAME']
        series.setdefault(name,{})
        if year==2010:
            fields={'population':'dpsf0010001','household_population':'dpsf0120002','group_quarters':'dpsf0120014','households':'dpsf0130001','families':'dpsf0130002','living_alone':'dpsf0130011','housing_units':'dpsf0180001','vacant':'dpsf0180003','seasonal_vacant':'dpsf0180008','other_vacant':'dpsf0180009','age_65_plus':'dpsf0070001'}
            vals={k:int(v[key]) for k,key in fields.items()}
            vals.update(median_age=float(v['dpsf0020001']),under_18=vals['population']-int(v['dpsf0040001']),source='2010 Census Demographic Profile bulk file; DPSF1,2,4,7,12,13,18')
        else:
            fields={'population':'P0010001','household_population':'P0150001','household_under_18':'P0150002','group_quarters':'P0180001','households':'P0160001','families':'P0160002','living_alone':'P0160008','housing_units':'H0010001','vacant':'H0030003'}
            vals={k:int(v[key]['value']) for k,key in fields.items()}
            vals.update(median_age=float(v['P0130001']['value']),source='2020 Census DHC bulk file; P1,12,13,15,16,18,H1,H3')
            vals['adult_correctional_facilities']=sum(int(x['value']) for k,x in v.items() if k.startswith('P018') and x['label']=='Correctional facilities for adults (101-106)')
            vals['age_65_plus']=sum(int(v[f'P012{i:04}']['value']) for i in list(range(20,26))+list(range(44,50)))
            vals['under_18']=sum(int(v[f'P012{i:04}']['value']) for i in list(range(3,7))+list(range(27,31)))
            assert vals['households']==int(v['H0030002']['value'])
        vals['land_sq_miles']=int(g['AREALAND'])/2589988.110336
        assert vals['population']==int(g['POP100'])
        assert vals['housing_units']==int(g['HU100'])
        series[name][year]=vals

for name,years in series.items():
    for y,row in years.items():
        if 'household_population' in row:
            assert row['household_population']+row['group_quarters']==row['population'],(name,y)
            row['average_household_size']=row['household_population']/row['households']
        if 'housing_units' in row and 'households' in row:
            row.setdefault('vacant',row['housing_units']-row['households'])
            assert row['vacant']+row['households']==row['housing_units'],(name,y)
            row['percent_vacant']=100*row['vacant']/row['housing_units']
save('population_housing_observations.json',series)

transcription=json.loads((HERE/'cuervo_1950_age_transcription.json').read_text(encoding='utf-8'))
ages=[int(p[1:]) for s in transcription['sheets'].values() for p in s.split()]
assert len(ages)==210
bins=[('0-4',0,4),('5-17',5,17),('18-34',18,34),('35-49',35,49),('50-64',50,64),('65+',65,130)]
age_counts={label:sum(lo<=a<=hi for a in ages) for label,lo,hi in bins}
assert sum(age_counts.values())==210
cuervo={'count':len(ages),'median_age':statistics.median(ages),'mean_age':statistics.mean(ages),'under_18':sum(a<18 for a in ages),'age_65_plus':sum(a>=65 for a in ages),'age_bins':age_counts,'sheet_person_counts':{k:len(v.split()) for k,v in transcription['sheets'].items()}}

def change(name,field,a,b):
    x,y=series[name][a][field],series[name][b][field]
    return {'from':x,'to':y,'difference':y-x,'percent_change':100*(y/x-1)}

changes={}
for name in manual:
    for field in ['population','household_population','households']:
        for a,b in [(1970,2020),(1980,2020),(1990,2000),(1990,2020),(2000,2020),(2010,2020)]:
            if field in series[name].get(a,{}) and field in series[name].get(b,{}):changes[f'{name};{field};{a}-{b}']=change(name,field,a,b)
calc={'cuervo_1950':cuervo,'changes':changes,'santa_rosa_1990_2020_share_of_net_growth_in_group_quarters':(589-23)/(2850-2263),'county_outside_santa_rosa_household_population':{y:series['Guadalupe County'][y]['household_population']-series['Santa Rosa city'][y]['household_population'] for y in [1980,1990,2000,2010,2020]},'county_outside_santa_rosa_total':{y:series['Guadalupe County'][y]['population']-series['Santa Rosa city'][y]['population'] for y in [1950,1960,1970,1980,1990,2000,2010,2020]}}
save('calculations.json',calc)

figs=HERE/'figures';figs.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#203344','text.color':'#203344','axes.titleweight':'bold','figure.facecolor':'white'})
teal,gold,gray='#116466','#B26A32','#879AAB'
years=[1980,1990,2000,2010,2020]
fig,ax=plt.subplots(figsize=(9,4.7))
hh=[series['Santa Rosa city'][y]['household_population'] for y in years]
gq=[series['Santa Rosa city'][y]['group_quarters'] for y in years]
ax.bar(years,hh,width=6.8,color=teal,label='People living in households')
ax.bar(years,gq,bottom=hh,width=6.8,color=gold,label='People living in group quarters')
for y,a,b in zip(years,hh,gq):
    ax.text(y,a/2,f'{a:,}',ha='center',va='center',color='white',fontweight='bold')
    ax.text(y,a+b+50,f'{a+b:,}',ha='center',va='bottom',fontsize=9)
    if b>100:ax.text(y,a+b/2,f'{b:,}',ha='center',va='center',color='white',fontsize=9)
ax.set(title='Santa Rosa: total growth, nearly flat household population',ylabel='Residents',xticks=years,ylim=(0,3350))
ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
ax.legend(loc='upper left',frameon=False,fontsize=8.7)
fig.text(.11,.015,'Published city boundaries in each census year. Group quarters include correctional facilities.',fontsize=8,color=gray)
fig.tight_layout(rect=(0,.05,1,1));fig.savefig(figs/'santa_rosa_households_group_quarters.png',dpi=200);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(9,4.4),sharey=True)
for ax,name,color in zip(axs,['Santa Rosa city','Los Lunas village'],[teal,gold]):
    nums=[series[name][y]['household_population'] for y in years]
    ax.plot(years,nums,'o-',color=color,lw=2.6)
    ax.set(title=name,xticks=years,xlim=(1976,2024),ylim=(0,19000));ax.tick_params(axis='x',labelsize=9)
    ax.grid(axis='y',alpha=.16)
    for i in [0,1,4]:ax.annotate(f'{nums[i]:,}',(years[i],nums[i]),xytext=(0,9),textcoords='offset points',ha='center',fontsize=9)
axs[0].set_ylabel('People living in households');axs[0].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
fig.suptitle('Household growth differs sharply, even after removing group quarters',fontsize=12,fontweight='bold')
fig.text(.09,.02,'Same vertical scale. Municipal boundaries changed; these are not constant-boundary growth estimates.',fontsize=8,color=gray)
fig.tight_layout(rect=(0,.06,1,.95));fig.savefig(figs/'household_population_comparison.png',dpi=200);plt.close(fig)

fig,ax=plt.subplots(figsize=(9,3.8))
ax.bar(age_counts.keys(),age_counts.values(),color=[gold,gold,teal,teal,teal,gray],width=.65)
for i,(label,count) in enumerate(age_counts.items()):ax.text(i,count+1,f'{count} ({100*count/210:.1f}%)',ha='center',fontsize=10)
ax.set(title='Cuervo in 1950: 85 of 210 residents were under 18',xlabel='Age in completed years',ylabel='People',ylim=(0,max(age_counts.values())+14))
fig.text(.1,.018,'Manual reading of every named person in ED 10-6. The district includes surrounding rural territory.',fontsize=8,color=gray)
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(figs/'cuervo_1950_age_profile.png',dpi=200);plt.close(fig)

print(json.dumps({'cuervo':cuervo,'sr_net_growth_gq_share':calc['santa_rosa_1990_2020_share_of_net_growth_in_group_quarters'],'outside_sr_hh':calc['county_outside_santa_rosa_household_population'],'key_changes':{k:v for k,v in changes.items() if k.endswith('1990-2020') or k.endswith('1970-2020')}},indent=2))
