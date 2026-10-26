"""Reproduce manually checked observations and arithmetic. Original scans are unchanged."""
from pathlib import Path
from collections import Counter
import json
import sys
import os
os.environ['MPLCONFIGDIR'] = str(Path(__file__).resolve().parents[2]/'tmp/deep_dive/mplconfig')
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'tmp/deep_dive/python_deps'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
def save(name, data):
    (OUT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

# Occupation descriptions in columns 20a/20b only; NOT a full labor-force transcription.
rows=[]
def add(sheet, line, description, sector, status='worked', note=''):
    image = sheet+1 if sheet<9 else 10
    rows.append(dict(sheet=sheet,line=line,occupation_normalized=description,sector=sector,
                     status_reading=status,note=note,
                     source=f'sources/03_census/1950_manuscripts/ed_10-6/43290879-New_Mexico-180130-{image:04d}.jpg'))
for sheet,lines in {1:[1,3,4,6,7,10,15,16,21,23,25],2:[1,5,17],4:[2,29],5:[16],7:[11,24,28,29],8:[4,5,13,19,25],71:[2,4]}.items():
    for line in lines:add(sheet,line,'Ranch work','Ranching')
for line in [4,27,29]:
    add(2,line,'Store clerk','Retail','has_job_not_worked' if line==27 else 'worked',
        'First word overwritten; clerk clear; retail classification provisional.' if line==4 else '')
add(2,8,'Cement finisher; contract building','Construction')
add(3,3,'Livestock inspector','Government inspection')
for line in [6,8]:add(4,line,'School teacher','Education / instruction')
add(4,10,'Railroad work','Railroad')
add(4,17,'Railroad agent','Railroad')
add(4,19,'Store clerk','Retail')
add(4,22,'Railroad work','Railroad','looking_for_work','Last occupation, not evidence of current employment.')
for line,description,sector in [(2,'Postmaster; post office','Postal'),(8,'Bookkeeper','Bookkeeping'),
    (9,'General merchandise manager; store manager','Retail'),(10,'Store clerk','Retail'),
    (14,'Service station','Fuel service'),(15,'Cafe manager','Food / drink'),
    (20,'Railroad work','Railroad'),(21,'Bartender; bar','Food / drink'),(23,'Mail carrier','Postal')]:
    add(5,line,description,sector,note='Keeping house in item 15, but Yes to work in item 16.' if line==15 else '')
add(6,1,'Railroad foreman','Railroad')
add(6,3,'Cafe waitress','Food / drink')
add(6,11,'Railroad worker','Railroad')
add(6,29,'Railroad work','Railroad','looking_for_work','Last occupation, not evidence of current employment.')
add(7,4,'Railroad telegraph role (abbreviated)','Railroad',note='Written Railroad Tele.; expansion inferred, not a verbatim title.')
add(7,5,'Beautician; beauty shop','Personal service','has_job_not_worked','Yes in item 18; occupation lies on printed row boundary.')
add(7,6,'Railroad signal role (abbreviated)','Railroad',note='Written Railroad Signal M.; exact full job title not expanded.')
add(8,21,'Veterans instructor','Education / instruction',note='Government class; not automatically a schoolteacher.')
rows.sort(key=lambda r:(r['sheet'],r['line']))
assert len(rows)==56 and len({(r['sheet'],r['line']) for r in rows})==56
assert Counter(r['sector'] for r in rows)['Ranching']==28
assert Counter(r['status_reading'] for r in rows)=={'worked':52,'has_job_not_worked':2,'looking_for_work':2}
save('cuervo_1950_occupation_readings.json',{'method':'Manual visual reading of main occupation fields on all nine population sheets. Normalized descriptions, not diplomatic transcription. Residence is not workplace. Blank occupations and sample-only prior occupations are outside this inventory. Not a labor-force denominator.', 'entries':rows,'counts':dict(Counter(r['sector'] for r in rows))})
person_rows={1:list(range(1,26))+[29,30],2:list(range(1,6))+list(range(8,31)),3:list(range(1,19))+list(range(21,30)),4:list(range(1,31)),5:list(range(1,11))+list(range(14,19))+list(range(20,27)),6:list(range(1,10))+list(range(11,17))+list(range(20,31)),7:list(range(1,9))+list(range(11,23))+list(range(24,31)),8:[1]+list(range(3,16))+list(range(19,23))+[25],71:[1,2,3,4]}
assert sum(map(len,person_rows.values()))==210
save('cuervo_1950_person_count.json',{'method':'Count named occupied person rows once; exclude vacant / absent placeholders; include four callback persons on sheet 71. Not a full name/age transcription. Washington cover total 211 and one ICR remain administratively unresolved.','named_rows_by_sheet':person_rows,'counts_by_sheet':{k:len(v) for k,v in person_rows.items()},'total':210})

retail={
 'Guadalupe County':dict(population_1930=7027,stores=67,proprietors=72,full_time_employees=109,net_sales=1415000,stocks=248000,payroll=112000),
 'Santa Rosa':dict(population_1930=1127,stores=23,proprietors=25,full_time_employees=48,net_sales=629000,stocks=117000,payroll=58000),
 'Rest of Guadalupe County':dict(population_1930=5900,stores=44,proprietors=47,full_time_employees=61,net_sales=786000,stocks=131000,payroll=54000),
 'Tucumcari':dict(population_1930=4143,stores=88,proprietors=87,full_time_employees=213,net_sales=3038000,stocks=447000,payroll=242000),
 'Quay County':dict(population_1930=10828,stores=157,proprietors=169,full_time_employees=240,net_sales=3966000,stocks=605000,payroll=270000)}
for key in retail['Santa Rosa']:
 assert retail['Santa Rosa'][key]+retail['Rest of Guadalupe County'][key]==retail['Guadalupe County'][key]
save('retail_1929_table13.json',{'source':'1930 Retail Distribution Part I chapter 3, PDF 124 / printed 166, Table 13','units':'Sales, stocks and payroll converted from printed $1,000 units to nominal dollars. Sales/payroll year 1929; population 1930. Employment count averages reported dates where available, otherwise enumeration-visit count. Proprietors exclude those on payroll.','data':retail})
types=[
 ('Grocery stores, without meat',14,2,12,27000,None,None),
 ('Combination grocery and meat',3,1,2,74000,None,None),
 ('General stores',19,6,13,769000,316000,453000),
 ('Motor-vehicle sales',4,2,2,248000,None,None),
 ('Filling stations',11,5,6,38000,33000,5000),
 ('Garages and repair shops',4,2,2,53000,None,None),
 ('Restaurants and lunch rooms',4,2,2,85000,None,None),
 ('Other eating places',1,0,1,None,0,None),
 ('Lumber yards and building materials',2,1,1,None,None,None),
 ('Electrical shops, without radios',1,1,0,None,None,0),
 ('Drug stores',3,1,2,38000,None,None),
 ('All other stores',1,0,1,12000,0,12000)]
assert sum(t[1] for t in types)==67 and sum(t[2] for t in types)==23 and sum(t[3] for t in types)==44
save('retail_1929_table14.json',{'source':'Part I chapter 7, PDF 17-18 / printed 642-643, Table 14 rows 26-28. Only categories with a county establishment are listed. All-food subtotal: 17/3/14 stores, $102,000/$42,000/$60,000 sales.','null':'Suppressed (x), not zero. Printed money rounded independently; subtotals need not add exactly.','columns':['category','county_stores','santa_rosa_stores','rest_stores','county_sales','santa_rosa_sales','rest_sales'],'rows':types})
population=[
 dict(year=1910,cuervo_precinct=545,santa_rosa_precinct=1031,santa_rosa_place=None,guadalupe_county=10927),
 dict(year=1920,cuervo_precinct=438,santa_rosa_precinct=1390,santa_rosa_place=None,guadalupe_county=8015),
 dict(year=1930,cuervo_precinct=287,santa_rosa_precinct=1381,santa_rosa_place=1127,guadalupe_county=7027),
 dict(year=1940,cuervo_precinct=188,santa_rosa_precinct=2527,santa_rosa_place=2310,guadalupe_county=8646),
 dict(year=1950,cuervo_precinct=210,santa_rosa_precinct=2548,santa_rosa_place=2199,guadalupe_county=6772),
 dict(year=1960,cuervo_precinct=None,santa_rosa_precinct=None,santa_rosa_place=2220,guadalupe_county=5610,santa_rosa_division=3380,tucumcari_city=8143),
 dict(year=1970,cuervo_precinct=None,santa_rosa_precinct=None,santa_rosa_place=2483,guadalupe_county=4969,santa_rosa_division=3221,tucumcari_city=7189)]
save('population_observations.json',{'notes':['1910-1920 precinct comparability not established; county lost territory in 1917.','Santa Rosa incorporated 1920 discrepancy: 1920 compendium read as 1003, 1930 Tables 4 and 5 print 1093. Keep unresolved.','1960/1970 divisions are not earlier precincts. Municipality and precinct must remain separate.','1970 Table 10 Guadalupe footnote records town-to-city and village-to-town designations; no Guadalupe annexation stated. Quay footnote records boundary changes.'],'data':population})
pct=lambda a,b:(b-a)/a*100
sr=retail['Santa Rosa']; gc=retail['Guadalupe County']; rest=retail['Rest of Guadalupe County']
calcs={'santa_rosa_county_shares_pct':{k:100*sr[k]/gc[k] for k in sr},
 'sales_per_resident_santa_rosa':sr['net_sales']/sr['population_1930'],
 'sales_per_resident_rest':rest['net_sales']/rest['population_1930'],
 'general_store_sales_share_santa_rosa_pct':100*316/629,
 'filling_station_sales_county_share_santa_rosa_pct':100*33/38,
 'filling_station_sales_share_santa_rosa_total_pct':100*33/629,
 'tucumcari_quay_sales_share_pct':100*3038/3966,
 'tucumcari_quay_population_share_pct':100*4143/10828,
 '1930_1940':{'cuervo_change':188-287,'cuervo_pct':pct(287,188),'santa_rosa_change':2310-1127,'santa_rosa_pct':pct(1127,2310),'county_change':8646-7027,'county_pct':pct(7027,8646),'rest_county_change':(8646-2310)-(7027-1127),'hypothetical_99_of_1183_pct':100*99/1183},
 '1940_1950':{'cuervo_pct':pct(188,210),'santa_rosa_pct':pct(2310,2199),'county_pct':pct(8646,6772)},
 '1960_1970':{'santa_rosa_change':263,'santa_rosa_pct':pct(2220,2483),'county_change':-641,'county_pct':pct(5610,4969),'rest_county_1960':5610-2220,'rest_county_1970':4969-2483,'rest_county_change':-904,'rest_county_pct':pct(3390,2486),'division_outside_place_1960':3380-2220,'division_outside_place_1970':3221-2483,'division_outside_place_pct':pct(1160,738),'tucumcari_pct':pct(8143,7189)},
 '1920_1930_santa_rosa_sensitivity':{'using_1003_pct':pct(1003,1127),'using_1093_pct':pct(1093,1127)}}
save('calculations.json',calcs)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.titleweight':'bold','figure.facecolor':'white'})
teal='#116466'; ochre='#B26A32'; ink='#203344'
fig,ax=plt.subplots(figsize=(8.6,4.6),layout='constrained')
keys=['population_1930','stores','full_time_employees','net_sales','stocks','payroll']
labels=['Population (1930)','Retail establishments','Full-time employees','Net sales (1929)','Stocks at year end','Salaries and wages']
values=[calcs['santa_rosa_county_shares_pct'][k] for k in keys]
ax.barh(labels,values,color=[ochre]+[teal]*5,height=.64)
ax.invert_yaxis();ax.set_xlim(0,60);ax.set_xlabel('Santa Rosa share of Guadalupe County (%)')
for i,v in enumerate(values):ax.text(v+.7,i,f'{v:.1f}%',va='center',color=ink)
ax.set_title('A commercial center before the 1930s population surge',loc='left',pad=18)
ax.xaxis.grid(True,alpha=.15);ax.set_axisbelow(True)
fig.savefig(OUT/'retail_shares.png',dpi=180);plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(9,3.9),layout='constrained')
for ax,title,vals,col in zip(axes,['Cuervo precinct','Santa Rosa municipality','Guadalupe County'],[[287,188,210],[1127,2310,2199],[7027,8646,6772]],[ochre,teal,ink]):
 ax.plot([1930,1940,1950],vals,marker='o',color=col,lw=2)
 ax.set_xticks([1930,1940,1950]);ax.set_title(title,fontsize=10,pad=12)
 ax.set_ylim(0,max(vals)*1.3);ax.yaxis.grid(True,alpha=.15)
 for x,y in zip([1930,1940,1950],vals):ax.annotate(f'{y:,}',(x,y),xytext=(0,9),textcoords='offset points',ha='center',fontsize=9)
axes[0].set_ylabel('Persons; each panel has its own scale')
fig.savefig(OUT/'population_1930_1950.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.3,4.3),layout='constrained')
x=[0,1]; a=[2220,2483];b=[3390,2486]
ax.bar(x,a,color=teal,label='Santa Rosa municipality',width=.52)
ax.bar(x,b,bottom=a,color='#CCD8DB',label='Rest of Guadalupe County',width=.52)
for i in x:
 ax.text(i,a[i]/2,f'{a[i]:,}',ha='center',va='center',color='white',fontweight='bold')
 ax.text(i,a[i]+b[i]/2,f'{b[i]:,}',ha='center',va='center',color=ink)
 ax.text(i,a[i]+b[i]+90,f'Total {a[i]+b[i]:,}',ha='center',color=ink)
ax.set_xticks(x,['1960','1970']);ax.set_ylim(0,6700);ax.set_ylabel('Persons');ax.legend(loc='upper right',frameon=False,fontsize=9)
ax.set_title('Municipal growth within a shrinking county',loc='left',pad=15)
fig.savefig(OUT/'population_1960_1970.png',dpi=180);plt.close(fig)

audit=['# Cuervo 1950: row-level occupation reading log','',
 'All nine population sheets of ED 10-6 were visually reviewed. This inventory covers main occupation fields only. Descriptions are normalized. It is not a complete demographic or labor-force transcription. One clerk classification is provisional. Residence does not locate an employer.','',
 '| Sheet | Line | Occupation / industry reading | Status | Note |','|---|---:|---|---|---|']
for r in rows:audit.append(f"| {r['sheet']} | {r['line']} | {r['occupation_normalized']} | {r['status_reading']} | {r['note']} |")
audit+=['','## Named-person count by sheet','','| Sheet | Named rows counted |','|---|---:|']
for sh,rr in person_rows.items():audit.append(f'| {sh} | {len(rr)} |')
audit+=['| **Total** | **210** |','','The cover has a field total of 210, a Washington-office total of 211, and an ICR entry of 1. The visible named rows corroborate 210; the administrative difference remains unresolved. Sheet 71 is the callback sheet, not evidence of 62 missing sheets.']
(OUT/'cuervo_1950_reading_log.md').write_text('\n'.join(audit)+'\n',encoding='utf-8')
print(json.dumps({'occupation_entries':len(rows),'named_persons':210,'sector_counts':dict(Counter(r['sector'] for r in rows)),'calculations':calcs},indent=2))
