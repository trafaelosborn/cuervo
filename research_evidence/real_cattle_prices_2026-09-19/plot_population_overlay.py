"""Plot the overlapping price/population record without inventing annual people counts."""
from pathlib import Path
import json
import os
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'output' / 'charts'
OUT.mkdir(parents=True, exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(ROOT / 'tmp' / 'matplotlib_config')
sys.path.insert(0, str(ROOT / 'tmp' / 'deep_dive' / 'python_deps'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, FuncFormatter

source = json.loads((HERE / 'annual_prices_and_cpi.json').read_text(encoding='utf-8'))
price_rows = {r['year']: r for r in source['observations']}
pop_file = ROOT / 'research_evidence/census_full_history_2026-09-18/published_population_series.json'
pop = {int(k): v for k,v in json.loads(pop_file.read_text(encoding='utf-8'))['series']['Cuervo precinct 6'].items()}
nominal = {y:r['nominal_usd_per_cwt'] for y,r in price_rows.items()}
# Additional early annual observations: visually checked USDA bulletin 265,
# table 43, printed/PDF p. 46. BLS CPI-U begins in 1913, so these stay nominal.
nominal.update({1910:5.70,1911:4.25,1912:5.60})
real = {y:r['real_1950_usd_per_cwt'] for y,r in price_rows.items()}

shared_real_years = sorted(set(real) & set(pop))
shared_nominal_years = sorted(set(nominal) & set(pop))
assert shared_real_years == [1920,1930,1940,1950]
assert shared_nominal_years == [1910,1920,1930,1940,1950]
assert all(y in real for y in range(1920,1951))
assert all(y in nominal for y in range(1910,1951))

TEAL='#146879'
RUST='#af542e'
INK='#22323e'
MUTED='#596772'
BG='#fcfbf8'
GRID='#e1e4e4'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11,
    'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':MUTED,
    'svg.fonttype':'none','savefig.facecolor':BG})

def frame(start, end, subtitle, title='Cuervo population and cattle prices'):
    fig, ax = plt.subplots(figsize=(12,7.7))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    fig.subplots_adjust(left=.095,right=.91,bottom=.25,top=.73)
    fig.text(.095,.955,title,fontsize=23,fontweight='bold',va='top')
    fig.text(.095,.892,subtitle,fontsize=12,color=MUTED,va='top')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#b8bfc2')
    ax.grid(axis='y',color=GRID,lw=.8)
    ax.set_axisbelow(True)
    ax.set_xlim(start-1,end+1)
    ax.set_xticks(list(range(start,end+1,10)))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.tick_params(which='both',length=0,pad=8)
    ax.set_xlabel('Year',labelpad=10)
    return fig,ax

def legend(fig, price_label):
    handles=[Line2D([0],[0],color=TEAL,lw=2.8,label=price_label),
             Line2D([0],[0],ls='',marker='o',ms=9,color=RUST,
                    markeredgecolor=BG,markeredgewidth=1.5,
                    label='Cuervo precinct population · census observations')]
    fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.095,.835),
               frameon=False,ncol=1,handlelength=2.6,borderaxespad=0,labelspacing=.6,fontsize=10.5)

def footer(fig, first, last):
    fig.text(.095,.135,first,fontsize=10,color=INK,va='top')
    fig.text(.095,.099,'Sources: USDA Bulletin 265, table 43 (p. 46); published Cuervo census precinct counts'+
             ('; BLS annual CPI-U.' if 'nominal' not in last.lower() else '.'),fontsize=8.7,color=MUTED,va='top')
    fig.text(.095,.069,last,fontsize=8.7,color=MUTED,va='top')
    fig.text(.095,.041,'Precinct boundaries are not assumed constant. Annual prices include months after census dates.',
             fontsize=8.7,color=MUTED,va='top')

def save(fig,stem):
    for suffix in ['png','svg']:
        fig.savefig(OUT/f'{stem}.{suffix}',dpi=200)
    plt.close(fig)

# Recommended overlay: a shared baseline creates a percentage-change comparison
# on one y axis. Labels on population markers remain the actual person counts.
fig,ax=frame(1920,1950,'1920–1950  |  Inflation-adjusted New Mexico cattle prices  |  Both series: 1920 = 100')
legend(fig,'Real cattle price · annual average')
years=list(range(1920,1951))
pi=[100*real[y]/real[1920] for y in years]
py=[100*pop[y]/pop[1920] for y in shared_real_years]
ax.plot(years,pi,color=TEAL,lw=2.8,zorder=3)
ax.scatter(shared_real_years,py,s=100,color=RUST,edgecolor=BG,lw=2,zorder=5)
for y,v in zip(shared_real_years,py):
    ax.annotate(f'{pop[y]:,} residents',(y,v),xytext=(7,16) if y==1920 else (-5,16) if y==1950 else (0,-24) if y==1930 else (0,16),
                textcoords='offset points',ha='left' if y==1920 else 'right' if y==1950 else 'center',
                color=RUST,fontsize=11,fontweight='bold')
ax.set_ylim(0,270)
ax.set_yticks([0,50,100,150,200,250])
ax.axhline(100,color='#aeb8bb',ls=(0,(3,4)),lw=1,zorder=1)
ax.set_ylabel('Index (1920 = 100)',labelpad=12)
ax.annotate(f'Real price: {pi[-1]:.0f}\n+{pi[-1]-100:.0f}% since 1920',
    xy=(1950,pi[-1]),xytext=(1941.8,233),color=TEAL,fontsize=11,fontweight='bold',
    arrowprops={'arrowstyle':'-','color':TEAL,'lw':1.0},ha='left',va='center')
footer(fig,'100 = the 1920 level; 50 = half that level; 200 = twice that level. Dots are labeled with resident counts.',
       'Prices: live beef cattle, excluding calves; deflated with annual CPI-U. Population is observed only at the four dots.')
save(fig,'cuervo_cattle_population_real_index_1920_1950')

# Companion in original units; two explicit, zero-based axes. Line crossings and
# vertical distances between the series have no meaning on different units.
fig,ax=frame(1920,1950,'1920–1950  |  Real cattle prices and observed population, shown in their own units')
legend(fig,'Real cattle price · annual average · left axis')
ax.plot(years,[real[y] for y in years],color=TEAL,lw=2.8,zorder=3)
ax.set_ylim(0,27)
ax.set_yticks([0,5,10,15,20,25])
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,_:f'${x:g}'))
ax.set_ylabel('1950 dollars per 100 lb liveweight',color=TEAL,labelpad=12)
ax.tick_params(axis='y',colors=TEAL)
ap=ax.twinx()
ap.set_ylim(0,500)
ap.set_yticks([0,100,200,300,400,500])
ap.spines[['top','left']].set_visible(False)
ap.spines['right'].set_color('#b8bfc2')
ap.spines['bottom'].set_visible(False)
ap.tick_params(axis='y',colors=RUST,length=0,pad=8)
ap.set_ylabel('Cuervo precinct residents',color=RUST,labelpad=12)
ap.scatter(shared_real_years,[pop[y] for y in shared_real_years],s=100,color=RUST,edgecolor=BG,lw=2,zorder=5)
for y in shared_real_years:
    ap.annotate(f'{pop[y]:,}',(y,pop[y]),xytext=(0,-23) if y==1940 else (0,12),textcoords='offset points',ha='center',color=RUST,fontweight='bold')
footer(fig,'Teal line: left price axis. Orange dots: right population axis. Crossings between series have no numerical meaning.',
       'Prices: live beef cattle, excluding calves; deflated with annual CPI-U. Population is observed only at the four dots.')
save(fig,'cuervo_cattle_population_real_units_1920_1950')

# Complete shared record, including the 1910 census; explicitly nominal because
# this project's verified CPI-U series has no pre-1913 observations.
fig,ax=frame(1910,1950,'1910–1950  |  Full shared record using nominal New Mexico cattle prices  |  Both series: 1910 = 100')
legend(fig,'Nominal cattle price · annual average · no inflation adjustment')
years_nom=list(range(1910,1951))
pn=[100*nominal[y]/nominal[1910] for y in years_nom]
pp=[100*pop[y]/pop[1910] for y in shared_nominal_years]
ax.plot(years_nom,pn,color=TEAL,lw=2.8,zorder=3)
ax.scatter(shared_nominal_years,pp,s=100,color=RUST,edgecolor=BG,lw=2,zorder=5)
for y,v in zip(shared_nominal_years,pp):
    ax.annotate(f'{pop[y]:,} residents',(y,v),xytext=(7,16) if y==1910 else (-5,16) if y==1950 else (0,-24) if y==1920 else (0,-15) if y==1930 else (0,14),
        textcoords='offset points',ha='left' if y==1910 else 'right' if y==1950 else 'center',
        color=RUST,fontweight='bold',fontsize=11)
ax.set_ylim(0,480)
ax.set_yticks([0,100,200,300,400])
ax.axhline(100,color='#aeb8bb',ls=(0,(3,4)),lw=1,zorder=1)
ax.set_ylabel('Index (1910 = 100)',labelpad=12)
ax.annotate(f'Nominal price: {pn[-1]:.0f}\n+{pn[-1]-100:.0f}% since 1910',
    xy=(1950,pn[-1]),xytext=(1938.5,420),color=TEAL,fontsize=11,fontweight='bold',
    arrowprops={'arrowstyle':'-','color':TEAL,'lw':1.0},ha='left',va='center')
footer(fig,'100 = the 1910 level. Dots are labeled with resident counts. This version includes all five census observations.',
       'Nominal prices include inflation. The verified CPI-U series starts in 1913. Redistricting limits the 1910–1920 comparison.')
save(fig,'cuervo_cattle_population_nominal_index_1910_1950')

observations=[]
for y in range(1910,1951):
    observations.append(dict(year=y,nominal_usd_per_cwt=nominal[y],
        real_1950_usd_per_cwt=real.get(y),cuervo_precinct_population=pop.get(y),
        real_price_index_1920_100=100*real[y]/real[1920] if y in real and y>=1920 else None,
        population_index_1920_100=100*pop[y]/pop[1920] if y in pop and y>=1920 else None,
        nominal_price_index_1910_100=100*nominal[y]/nominal[1910],
        population_index_1910_100=100*pop[y]/pop[1910] if y in pop else None))
manifest=dict(real_overlap=[1920,1950],nominal_overlap=[1910,1950],
    real_census_years=shared_real_years,nominal_census_years=shared_nominal_years,
    price_frequency='annual',population_frequency='observed census years only; no interpolation',
    deflator='BLS annual CPI-U; real dollars refer to 1950 purchasing power',
    indexed_method='Value divided by same series base-year value, multiplied by 100',
    caveats=['Statewide cattle prices, Cuervo precinct population; differing geographic scales.',
             'Population reporting units are not assumed to have constant boundaries; 1910-1920 redistricting is documented.',
             'Annual prices include months following census enumeration.',
             'No annual population estimates or correlation/regression have been inferred.',
             'The indexed plots compare proportional changes; the dual-axis plot compares levels in different units.'],
    sources=source['sources'][:1]+source['sources'][2:]+[
        {'path':str(pop_file.relative_to(ROOT)),'locators':'research_evidence/population_series_verified.md'},
        {'additional_nominal_years':{'1910':5.70,'1911':4.25,'1912':5.60},'locator':'USDA bulletin 265, table 43, printed/PDF p.46'}],
    observations=observations,outputs=sorted(p.name for p in OUT.glob('cuervo_cattle_population_*')))
(HERE/'population_overlay_data.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'real_overlap':manifest['real_overlap'],'nominal_overlap':manifest['nominal_overlap'],
    'real_population_points':len(shared_real_years),'nominal_population_points':len(shared_nominal_years),
    'real_price_change_1920_1950_pct':pi[-1]-100,'population_change_1920_1950_pct':py[-1]-100,
    'outputs':manifest['outputs']},indent=2))
