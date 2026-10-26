from pathlib import Path
import json,sys,os
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tmp/deep_dive/python_deps'))
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/matplotlib_config')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})
data=json.loads((OUT/'agriculture_transcription.json').read_text())['series']; years=[r['year'] for r in data]
fig,axs=plt.subplots(2,2,figsize=(12,10));fig.subplots_adjust(top=.82,bottom=.24,left=.10,right=.96,hspace=.62,wspace=.25)
for ax,field,title,color in zip(axs.flat,['cattle_head','sheep_lambs_head','all_farms','land_in_farms_acres'],['Cattle and calves • head','Sheep and lambs • head','All census farms • number','Land in census farms • acres'],['#b56930','#346d76','#644b7b','#598151']):
 vals=[r[field] for r in data];ax.plot(years,vals,'o-',color=color,lw=1.8,ms=7);ax.set_title(title,loc='left',pad=13);ax.set_ylim(0,max(vals)*1.23);ax.set_xticks(years);ax.tick_params(axis='x',rotation=40);ax.grid(axis='y',alpha=.18);ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:,.0f}'))
 for i in [0,4,6]:ax.annotate(f'{vals[i]:,}',(years[i],vals[i]),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10,color=color)
fig.suptitle('Ranching persisted; its composition and scale changed',x=.10,ha='left',fontsize=20,fontweight='bold')
fig.text(.10,.905,'Guadalupe County, New Mexico | Seven agricultural-census snapshots, 1930–1959',fontsize=12,color='#444')
fig.text(.10,.075,'County context, not Cuervo totals. Lines only connect observed census snapshots.\nInventory seasons differ; 1930 cattle exclude animals under 3 months. Farm definitions and coverage change.\nLand is assigned by farm headquarters and can cross county lines. Sheep and cattle heads are not equivalent output units.\nSources: USDA Census of Agriculture, 1935, 1945, 1950 and 1959; page-level transcription in the accompanying JSON.',fontsize=9.5,linespacing=1.6,color='#444')
fig.savefig(OUT/'guadalupe_agriculture_1930_1959.png',dpi=170);plt.close(fig)
old=json.loads((ROOT/'research_evidence/origins_followup_2026-09-23/financial_transcription.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(12,5.7));fig.subplots_adjust(top=.77,bottom=.22,wspace=.28,left=.07,right=.97)
for tab,col,label,color in [('table_32',1,'Merchandise inventory','#346d76'),('table_34',1,'Sheep investment','#b56930')]:
 rows=old[tab]['rows'];axs[0].plot([r[0] for r in rows],[r[col] for r in rows],'o-',label=label,color=color,lw=1.7,ms=4)
axs[0].set_title('Changing asset mix',loc='left');axs[0].legend(frameon=False,fontsize=9);axs[0].set_ylim(bottom=0)
rows=old['table_35']['rows'];axs[1].bar([r[0] for r in rows],[r[1] for r in rows],color='#644b7b',width=.7);axs[1].set_title('Company net profit',loc='left');axs[1].set_ylim(0,23)
for ax in axs:ax.set_ylabel('Nominal dollars, thousands');ax.grid(axis='y',alpha=.18);ax.set_xticks([1904,1907,1911,1915])
fig.suptitle('Bond & Wiest: a changing business with recurring profits',x=.07,ha='left',fontsize=18,fontweight='bold')
fig.text(.07,.85,'Cuervo firm accounts reconstructed by Grubbs (1958) | Original ledgers not yet audited',fontsize=11,color='#444')
fig.text(.07,.055,'Balances are not sales; company net profit is not merchandise gross profit or town income.\nNo inflation adjustment or return-on-capital calculation. Source: Grubbs, Tables 32, 34 and 35, pp. 106, 111–112.\nThe 1910–1911 profit trough was followed by recovery; it cannot be read as the firm’s closure.',fontsize=9.5,linespacing=1.6,color='#444')
fig.savefig(OUT/'bond_wiest_assets_and_profit.png',dpi=170);plt.close(fig)
metrics={'1940_1950_cattle_pct':(41276/19227-1)*100,'1940_1950_sheep_pct':(56412/67765-1)*100,'1930_1959_sheep_pct':(44426/99296-1)*100,'1950_1959_cattle_pct':(31020/41276-1)*100,'1950_1959_sheep_pct':(44426/56412-1)*100,'1954_1959_farms_drop':333-297,'1959_farm_definition_exclusions':10,'1959_reported_pasture_acres':1562499+12409+1337,'1959_pasture_share_of_land_in_farms':(1562499+12409+1337)/1588274,'1959_truck_reporting_share_sample':250/299,'1954_truck_reporting_share_sample':285/328}
(OUT/'derived_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
print(json.dumps(metrics,indent=2))
