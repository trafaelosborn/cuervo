"""Reproduce the cattle-price purchasing-power check from published annual columns."""
from pathlib import Path
import hashlib
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(ROOT / 'tmp' / 'matplotlib_config')
sys.path.insert(0, str(ROOT / 'tmp' / 'deep_dive' / 'python_deps'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# USDA Statistical Bulletin 265, table 43, printed/PDF page 46.
# Annual column visually checked against the scan, not a mean of the OCR months.
old_prices = [
    6.00, 6.20, 6.50, 6.50, 8.40, 9.80, 9.30,
    8.20, 4.95, 4.85, 4.65, 4.55, 4.75, 5.60, 6.90, 9.00, 8.60,
    6.30, 4.80, 3.80, 3.20, 3.20, 6.00, 5.60, 6.10, 5.20, 6.20,
    7.30, 8.30, 10.30, 10.70, 9.70, 10.80, 12.70, 16.50, 21.40, 19.20,
    23.10, 27.70, 21.90, 14.30, 15.50, 14.90, 14.00, 17.30, 23.00, 22.30,
]
# USDA Statistical Bulletin 680, printed/PDF page 16, NEW MEXICO annual column.
# Visually checked. Its 1959 observation agrees with bulletin 265: 22.30.
new_prices = [
    22.30, 19.80, 21.40, 21.30, 20.60, 16.80, 20.20, 23.40, 23.20, 24.40,
    27.60, 28.40, 30.90, 35.80, 45.30, 36.70, 39.30, 36.30, 38.50, 52.90,
]
# BLS historical CPI-U, December 2023 release, PDF pages 3-4, Annual avg.
# Transcribed from the BLS table obtained through web retrieval. Direct PDF
# download returned HTTP 403, so no locally held BLS original is claimed.
# Index base 1982-84=100. 1959 is 29.1, not 29.2.
cpi_values = [
    9.9, 10.0, 10.1, 10.9, 12.8, 15.1, 17.3,
    20.0, 17.9, 16.8, 17.1, 17.1, 17.5, 17.7, 17.4, 17.1, 17.1,
    16.7, 15.2, 13.7, 13.0, 13.4, 13.7, 13.9, 14.4, 14.1, 13.9,
    14.0, 14.7, 16.3, 17.3, 17.6, 18.0, 19.5, 22.3, 24.1, 23.8,
    24.1, 26.0, 26.5, 26.7, 26.9, 26.8, 27.2, 28.1, 28.9, 29.1,
    29.6, 29.9, 30.2, 30.6, 31.0, 31.5, 32.4, 33.4, 34.8, 36.7,
    38.8, 40.5, 41.8, 44.4, 49.3, 53.8, 56.9, 60.6, 65.2,
]
assert len(old_prices) == 47 and len(new_prices) == 20 and len(cpi_values) == 66
assert old_prices[-1] == new_prices[0]
prices = dict(zip(range(1913, 1960), old_prices))
prices.update(dict(zip(range(1959, 1979), new_prices)))
cpi = dict(zip(range(1913, 1979), cpi_values))
pop_source = ROOT / 'research_evidence/census_full_history_2026-09-18/published_population_series.json'
population = {int(k): v for k, v in json.loads(pop_source.read_text())['series']['Cuervo precinct 6'].items()}
rows = [dict(year=y, nominal_usd_per_cwt=prices[y], cpi_u_annual=cpi[y],
             real_1950_usd_per_cwt=prices[y]*cpi[1950]/cpi[y],
             cuervo_precinct_population=population.get(y)) for y in prices]
by_year = {r['year']: r for r in rows}
def pct(a, b):
    return (by_year[b]['real_1950_usd_per_cwt']/by_year[a]['real_1950_usd_per_cwt']-1)*100
comparisons = []
for a,b in [(1920,1930),(1930,1934),(1930,1940),(1939,1944),(1939,1949),
            (1940,1949),(1940,1950),(1951,1953),(1951,1956),(1956,1973),
            (1951,1970),(1951,1973),(1973,1976)]:
    comparisons.append(dict(start=a,end=b,real_price_change_pct=pct(a,b),
        population_change_pct=((population[b]/population[a]-1)*100)
        if a in population and b in population else None))

sources = [
    dict(id='USDA265', title='Prices Received by Farmers for Beef Cattle, 1909-59',
         url='https://esmis.nal.usda.gov/usda-esmis/files/x920fw86z/5t34sp07q/df65vc27m/prflvstckdypltry_Prices_Received_by_Farmers_for_Beef_Cattle__1909-59.pdf',
         path='sources/08_context/usda_beef_cattle_prices_1909_1959_bulletin_265.pdf',
         locator='Table 43, printed/PDF page 46; method page 3', used_years='1913-1958; 1959 overlap checked', visual_check=True),
    dict(id='USDA680', title='Prices Received by Farmers: Cattle, Milk Cows, Hogs, Sheep, Wool, 1959-78',
         url='https://esmis.nal.usda.gov/usda-esmis/files/x920fw86z/xg94hs65j/rv042x51f/prflvstckdypltry_Prices_Received_by_Farmers_-_Cattle__Milk_Cows__Hogs__Sheep__Wool__by_State_and_United_States__1959-78.pdf',
         path='sources/08_context/usda_cattle_prices_1959_1978.pdf',
         locator='Beef cattle table, NEW MEXICO, printed/PDF page 16; methods pages 4-5; January 1982', used_years='1959-1978', visual_check=True),
    dict(id='BLSCPI', title='Historical CPI-U, U.S. city average, all items: index averages',
         url='https://www.bls.gov/cpi/tables/supplemental-files/historical-cpi-u-202312.pdf',
         locator='December 2023 release, PDF pages 3-4, Annual avg. column', used_years='1913-1978',
         retrieval='BLS web text retrieved September 19, 2026; PDF download HTTP 403; original not held locally', visual_check=False),
]
for s in sources:
    if 'path' in s:
        p = ROOT / s['path']
        s.update(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())

output = dict(method='Annual NM liveweight beef-cattle price excluding calves, multiplied by annual CPI-U(1950)/CPI-U(year). Consumer purchasing power per cwt, not ranch profit, revenue, fixed-grade price, or Cuervo transaction price.',
    reference_year=1950, census_note='Published Cuervo precinct counts; no constant-boundary assumption. Population observed only at censuses; post-1950 Cuervo counts not established here. Annual census-year prices include months after enumeration.',
    sources=sources, observations=rows, comparisons=comparisons)
(OUT/'annual_prices_and_cpi.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
(OUT/'new_source_manifest.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,
                     'axes.labelcolor':'#34404b','text.color':'#23313e'})
fig, (ax, axp) = plt.subplots(2,1,figsize=(12,7.8),sharex=True,
                              gridspec_kw={'height_ratios':[2,1],'hspace':0.22})
fig.patch.set_facecolor('#fbfaf7')
for a in (ax,axp):
    a.set_facecolor('#fbfaf7')
    a.spines[['top','right']].set_visible(False)
    a.spines[['left','bottom']].set_color('#b8bec2')
    a.grid(axis='y',color='#dfe2e2',linewidth=0.8)
    a.set_axisbelow(True)
plot_rows = [r for r in rows if r['year']>=1920]
ax.plot([r['year'] for r in plot_rows],[r['real_1950_usd_per_cwt'] for r in plot_rows],color='#276e80',lw=2.5)
ax.set_ylabel('1950 dollars per 100 lb liveweight')
ax.set_ylim(0,31)
ax.set_title('New Mexico cattle prices after consumer-price inflation',loc='left',fontweight='bold',pad=12)
for y, label, xytext in [
    (1934,'1934: $5.76',(1930,2.0)),
    (1951,'1951: $25.68',(1942,28.3)),
    (1956,'1956: $12.40\n52% below 1951',(1956,4.7)),
    (1973,'1973: $24.59',(1968,28.3)),
]:
    val=by_year[y]['real_1950_usd_per_cwt']
    ax.scatter([y],[val],s=28,color='#276e80',zorder=5)
    ax.annotate(label,(y,val),xytext=xytext,fontsize=10,
                arrowprops={'arrowstyle':'-','color':'#7b858c'},ha='left')
axp.axvspan(1950.4,1979,color='#e9e8e3',zorder=0)
ps={y:v for y,v in population.items() if y>=1920}
# Census observations only: no annual interpolation is implied by a line.
axp.scatter(list(ps),list(ps.values()),s=45,color='#ac633f',zorder=4)
for y,v in ps.items():
    axp.annotate(str(v),(y,v),xytext=(0,9),textcoords='offset points',ha='center',fontweight='bold',color='#935236')
axp.text(1964.7,295,'No verified, comparable Cuervo counts\nafter 1950 in the current evidence',ha='center',va='center',color='#606a70',fontsize=10)
axp.set_title('Cuervo precinct population: census observations',loc='left',fontweight='bold',pad=12)
axp.set_ylabel('Residents')
axp.set_ylim(0,530)
axp.set_xlim(1918.5,1979)
axp.xaxis.set_major_locator(MultipleLocator(10))
axp.xaxis.set_minor_locator(MultipleLocator(5))
axp.set_xlabel('Year')
fig.suptitle('Cattle purchasing power cycled; the local outcome still needs dating',x=0.09,ha='left',fontsize=16,fontweight='bold',y=.975)
fig.subplots_adjust(left=.09,right=.97,top=.88,bottom=.15)
fig.text(.09,.060,'Sources: USDA Statistical Bulletins 265 (p. 46) and 680 (p. 16); BLS annual CPI-U; verified census precinct series.',fontsize=8.5,color='#647079')
fig.text(.09,.036,'Prices are statewide averages, excluding calves; CPI adjustment does not measure profit. Census units are not assumed to have constant boundaries.',fontsize=8.5,color='#647079')
fig.savefig(OUT/'real_cattle_prices_and_cuervo.png',dpi=180,facecolor=fig.get_facecolor())
plt.close(fig)
print(json.dumps(comparisons,indent=2))
print('SELECTED YEARS')
for y in [1920,1930,1934,1939,1940,1944,1949,1950,1951,1953,1956,1959,1960,1964,1970,1973,1976,1978]:
    r=by_year[y]
    print(y,prices[y],cpi[y],round(r['real_1950_usd_per_cwt'],2),population.get(y))
