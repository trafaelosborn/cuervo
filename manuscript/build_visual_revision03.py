"""Four original editorial figures from the project's held, checked evidence.

No network requests. Geographic points are modern reference locations; connection
arrows are schematic, and discrete observations never become invented lifespans.
"""
from pathlib import Path
import os, sys, json, hashlib, math, textwrap
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tmp/chapter-build-deps'))
sys.path.insert(0, str(ROOT / 'tmp/regional_python'))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch, FancyArrowPatch
from shapely.geometry import shape
from shapely.ops import unary_union, transform
from pyproj import Transformer, CRS

OUT = ROOT / 'manuscript/figures/book-revision03'
OUT.mkdir(parents=True, exist_ok=True)
NAVY, INK, GRAY, BROWN, RULE, PALE = '#1b3558', '#242528', '#756e65', '#96714f', '#d8d2c9', '#f2eee7'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12,
                    'svg.fonttype':'none', 'axes.unicode_minus':False})
manifest = {'date':'2026-09-28', 'scope':'Original figures using held evidence; no new source acquisition.',
            'figures':[], 'visual_review':'pending'}

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def source(rel):
    p=ROOT/rel
    return {'path':rel, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def save(fig, key, info):
    paths=[]
    for ext in ['png','svg']:
        p=OUT/f'{key}.{ext}'
        fig.savefig(p, dpi=300, facecolor='white')
        paths.append(p.relative_to(ROOT).as_posix())
    plt.close(fig)
    manifest['figures'].append({'key':key, **info, 'outputs':paths})

def style(ax):
    ax.spines[['top','right','left']].set_visible(False)
    ax.spines['bottom'].set_color(RULE)
    ax.tick_params(length=0, pad=7, colors=GRAY, labelsize=11)
    ax.grid(axis='y', color='#e8e4df', lw=.7)
    ax.set_axisbelow(True)

# 1. Geographic locator. County outline dissolved from all 902 held census blocks.
GEO='sources/regional_functions_2026-09-21/blocks_2020_guadalupe.geojson'
PLACES='research_evidence/census_deep_dive_2026-09-18/modern_2020_extract.json'
REFERENCE='research_evidence/regional_functions_2026-09-21.md'
features=load(GEO)['features']
assert len(features)==902
county=unary_union([shape(f['geometry']) for f in features])
locations={'Cuervo':(-104.40861,35.03111)}
for row in load(PLACES):
    g=row['geography']
    for short,full in [('Santa Rosa','Santa Rosa city'),('Tucumcari','Tucumcari city'),
                       ('Newkirk','Newkirk CDP'),('Vaughn','Vaughn town')]:
        if g['NAME']==full:
            locations[short]=(float(g['INTPTLON']),float(g['INTPTLAT']))
assert len(locations)==5
crs=CRS.from_proj4('+proj=aeqd +lat_0=35.03111 +lon_0=-104.40861 +datum=WGS84 +units=m +no_defs')
project=Transformer.from_crs('EPSG:4326',crs,always_xy=True).transform
projected=transform(project, county)
fig=plt.figure(figsize=(8,7.3))
fig.text(.075,.975,'SELECTED PLACES IN EASTERN NEW MEXICO',color=GRAY,fontsize=11,va='top')
ax=fig.add_axes([.045,.36,.91,.57]);ax.set_aspect('equal');ax.axis('off')
polys=list(projected.geoms) if hasattr(projected,'geoms') else [projected]
for poly in polys:
    xy=[(x/1000,y/1000) for x,y in poly.exterior.coords]
    ax.add_patch(Polygon(xy,closed=True,facecolor=PALE,edgecolor='#bdb4a8',lw=1))
    for ring in poly.interiors:
        ax.add_patch(Polygon([(x/1000,y/1000) for x,y in ring.coords],facecolor='white',edgecolor=RULE,lw=.4))
points={k:tuple(v/1000 for v in project(*xy)) for k,xy in locations.items()}
offsets={'Cuervo':(8,-25,'left'),'Santa Rosa':(-9,10,'right'),
         'Newkirk':(6,12,'left'),'Tucumcari':(0,12,'center'),'Vaughn':(0,-21,'center')}
for name,(x,y) in points.items():
    ax.scatter(x,y,s=76 if name=='Cuervo' else 31,color=NAVY if name=='Cuervo' else BROWN,zorder=5)
    dx,dy,align=offsets[name]
    ax.annotate(name,(x,y),xytext=(dx,dy),textcoords='offset points',ha=align,
                fontsize=15 if name=='Cuervo' else 13,color=NAVY if name=='Cuervo' else INK,
                weight='bold' if name=='Cuervo' else 'normal')
ax.text(-42,-41,'GUADALUPE\nCOUNTY',ha='center',color=GRAY,fontsize=12,linespacing=1.5)
ax.set_xlim(-105,88);ax.set_ylim(min(projected.bounds[1]/1000-8,-66),48)
# True north at the projection center. Distance scale is exact there.
ax.annotate('',xy=(-96,36),xytext=(-96,20),arrowprops={'arrowstyle':'-|>','color':NAVY,'lw':1.2})
ax.text(-96,39,'N',ha='center',color=NAVY,fontsize=12)
ax.plot([28,68],[-51,-51],color=NAVY,lw=1.4)
for x in [28,48,68]:ax.plot([x,x],[-53,-49],color=NAVY,lw=1)
for x,s in [(28,'0'),(48,'20'),(68,'40 km')]:ax.text(x,-58,s,ha='center',fontsize=10,color=GRAY)
fig.text(.075,.332,'Modern county outline and place reference points',color=GRAY,fontsize=10)
fig.text(.075,.285,'THE RAILWAY DISTANCES IN 1926',color=NAVY,fontsize=11)
rail=fig.add_axes([.10,.12,.81,.12]);rail.set_xlim(-3,62);rail.set_ylim(-.8,1.15);rail.axis('off')
rail.plot([0,59],[0,0],lw=1.5,color=NAVY)
for x,name in [(0,'Santa Rosa'),(17,'Cuervo'),(59,'Tucumcari')]:
    rail.scatter(x,0,s=50 if x==17 else 30,color=NAVY)
    rail.text(x,-.42,name,ha='center',fontsize=12,color=NAVY)
rail.text(8.5,.35,'17 miles',ha='center',fontsize=11,color=BROWN)
rail.text(38,.35,'42 miles',ha='center',fontsize=11,color=BROWN)
fig.text(.075,.040,'Distance diagram below the map; it does not trace the railway route.',color=GRAY,fontsize=10)
save(fig,'regional-locator',{
    'title':'Cuervo and its regional neighbors',
    'inputs':[source(GEO),source(PLACES),source(REFERENCE),source('sources/01_railroad/rock_island_public_timetable_1926-01.pdf')],
    'coordinates_lon_lat':locations,'projection_wkt':crs.to_wkt(),'county_blocks':len(features),
    'rail_miles':{'Santa Rosa-Cuervo':17,'Cuervo-Tucumcari':42},
    'source_locator':'2020 DHC internal points; held 2020 block polygons; regional audit section 6; January 1926 timetable, Table 2 p.18, notes p.19.',
    'limits':'Modern county outline is neither the historical Cuervo precinct nor a trading catchment. Cuervo is the audit reference point, other points are Census internal points. No roads or historic railway routes are drawn.'})

# 2. Schematic connections. Every arrow maps to a specific observation ID.
NETWORK='research_evidence/economic_synthesis_2026-09-23/trade_network_observations.json'
network={r['id']:r for r in load(NETWORK)['observations']}
left=[('N18','ENCINO','Hides and pelts\ncombined at Cuervo','1905 and 1907',True),
      ('N08','SURROUNDING COUNTRY','Wool brought in\nfor marketing','July 1910',False),
      ('N07','OUTSIDE SUPPLIERS','Flour, sugar and grain\nunloaded at Cuervo','March 1910',False)]
right=[('N10','KANSAS','6,000 lambs and wethers\nshipped for feeding','October 1910',False),
       ('N13','LOS ANGELES','Cattle shipped\nfrom Cuervo','December 1910',False),
       ('N17','BOSTON','Wool-buyer\nrelationships','Early operations; undated',True)]
fig=plt.figure(figsize=(8,7.7));ax=fig.add_axes([.035,.14,.93,.83]);ax.set_xlim(0,10);ax.set_ylim(0,10);ax.axis('off')
ax.add_patch(FancyBboxPatch((3.5,2.5),3,5.3,boxstyle='round,pad=.10,rounding_size=.06',facecolor=PALE,edgecolor='none'))
ax.text(5,6.35,'CUERVO',ha='center',color=NAVY,fontsize=21,weight='bold')
ax.text(5,5.30,'Assembling goods\nHandling freight\nTrading and credit',ha='center',va='center',fontsize=13.4,color=INK,linespacing=1.8)
ax.text(5,3.55,'A place where\ntransactions gathered',ha='center',color=GRAY,fontsize=11.5,linespacing=1.5)
for side,rows in [('left',left),('right',right)]:
    for y,(ident,place,goods,date,secondary) in zip([8.3,5.1,1.9],rows):
        assert ident in network
        xx=.1 if side=='left' else 7.22
        ax.text(xx,y+.77,place,ha='left',fontsize=10.3,color=NAVY,weight='bold')
        ax.text(xx,y+.24,goods,ha='left',va='top',fontsize=12.1,color=INK,linespacing=1.5)
        ax.text(xx,y-.88,date,ha='left',fontsize=10,color=GRAY)
        yc=min(7.35,max(2.9,y-.2))
        start,end=((2.93,y-.2),(3.45,yc)) if side=='left' else ((6.55,yc),(7.08,y-.2))
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=14,
                                   linewidth=1.6,linestyle=(0,(3,3)) if secondary else '-',color=BROWN if secondary else NAVY))
fig.text(.055,.095,'Solid arrows: contemporary newspaper reports, 1910',color=NAVY,fontsize=10.5)
fig.text(.055,.057,'Dashed arrows: relationships described in Grubbs\'s 1958 history',color=BROWN,fontsize=10.5)
fig.text(.055,.019,'Selected connections; position and arrow width do not encode route or volume.',color=GRAY,fontsize=9.6)
ids=[r[0] for r in left+right]
save(fig,'trade-connections',{'title':'A small place in a wide trading network','inputs':[source(NETWORK)],
     'observations':[network[i] for i in ids],
     'limits':'Schematic, not a route map or volume balance. Left and right arrows are separate observations; no consignment is tracked through the diagram. All traffic is not assigned to one shipper. Report dates do not necessarily equal transaction dates.'})

# 3. Aligned panels replace the price-only chart. No twin axes or interpolation.
PRICES='research_evidence/real_cattle_prices_2026-09-19/annual_prices_and_cpi.json'
AGE='research_evidence/chapter05_2026-09-28/calculations.json'
raw=load(PRICES);rows=sorted(raw['observations'],key=lambda r:r['year']);by_year={r['year']:r for r in rows}
assert [r['year'] for r in rows]==list(range(1913,1979))
for r in rows:
    assert math.isclose(r['nominal_usd_per_cwt']*24.1/r['cpi_u_annual'],r['real_1950_usd_per_cwt'],rel_tol=1e-10)
base=by_year[1951]['real_1950_usd_per_cwt']
index=[r['real_1950_usd_per_cwt']/base*100 for r in rows]
population={1910:545,1920:438,1930:287,1940:188,1950:210}
age=load(AGE)
# Read the same population series used in the existing Chapter 5 figure.
age_rows=age['age'] if 'age' in age else age['age_observations']
assert all(age_rows[str(y)]['population']==n for y,n in population.items())
fig=plt.figure(figsize=(8,8));a=fig.add_axes([.11,.54,.85,.38]);b=fig.add_axes([.11,.16,.85,.26],sharex=a)
for ax in [a,b]:style(ax);ax.set_xlim(1907,1981);ax.set_xticks([1910,1920,1930,1940,1950,1960,1970,1978])
a.plot([r['year'] for r in rows],index,color=NAVY,lw=2.1);a.set_ylim(0,123);a.set_yticks([0,25,50,75,100]);a.tick_params(labelbottom=False)
a.set_title('New Mexico cattle prices, adjusted for inflation',loc='left',fontsize=13,color=NAVY,pad=18)
a.text(0,1.015,'Annual index; 1951 = 100',transform=a.transAxes,fontsize=10.5,color=GRAY)
for y,offset,ha in [(1951,(-8,13),'right'),(1956,(9,-21),'left'),(1973,(0,13),'center')]:
    value=index[y-1913];a.scatter(y,value,color=NAVY,s=25,zorder=4)
    a.annotate(f'{y}: {value:.0f}',(y,value),xytext=offset,textcoords='offset points',ha=ha,color=NAVY,fontsize=11,
               bbox={'facecolor':'white','edgecolor':'none','pad':2})
b.axvspan(1950.6,1981,color='#f5f3ef',zorder=0)
b.scatter(list(population),list(population.values()),color=BROWN,s=45,zorder=4)
for y,n in population.items():b.annotate(str(n),(y,n),xytext=(0,10),textcoords='offset points',ha='center',fontsize=12,color=BROWN)
b.set_ylim(0,680);b.set_yticks([0,200,400,600]);b.set_title('Population in the named Cuervo precinct',loc='left',fontsize=13,color=NAVY,pad=17)
b.text(1965,330,'No comparable later\nprecinct counts in this series',ha='center',va='center',fontsize=10.5,color=GRAY,linespacing=1.5)
fig.text(.11,.072,'Prices: 66 annual state averages. Population: five census observations.',fontsize=10.2,color=GRAY)
fig.text(.11,.032,'Shared dates aid comparison; the two panels do not estimate a causal effect.',fontsize=10.2,color=GRAY)
save(fig,'prices-and-population',{'title':'Cattle prices and the people counted at Cuervo',
    'inputs':[source(PRICES),source(AGE)],'sources':raw['sources'],
    'index_formula':'100 * (nominal price / CPI in year) / (nominal price / CPI in 1951)',
    'price_observations':66,'population_observations':5,'population':population,
    'price_series':[{'year':r['year'],'index_1951_100':v} for r,v in zip(rows,index)],
    'limits':'State prices and precinct population have different geographies. Precinct boundaries are not held constant. Decennial dots are not interpolated. Annual averages include months after the census. Prices measure purchasing power per unit sold, not profit, income or local spending. The later shaded area denotes missing comparable observations, not zero population.'})

# 4. Cross-chapter chronology, deliberately not a continuous service-duration chart.
events=[
 {'date':'1903','function':'MERCHANT','text':'The move from Cabra to Cuervo was complete by year end.','reference':'Chapter 1, note 5. Grubbs, pp.96-101.'},
 {'date':'1911','function':'MIXED FORTUNES','text':'A school was being built; lumber stock was withdrawn; the depot platform was improved.','reference':'Chapter 1, note 1. Clipper, September 14, 1911, p.1.'},
 {'date':'1919','function':'SCHOOLING','text':'A teacher left. Ninth-grade instruction was interrupted and a replacement was proposed.','reference':'Chapter 7, note 5. Clipper, January 10, 1919.'},
 {'date':'1922','function':'PUBLISHING','text':'Katharine A. Hicks withdrew financial support and argued for publication at Santa Rosa.','reference':'Chapter 4, note 13; Chapter 7, note 7. Clipper, December 1, 1922.'},
 {'date':'1946','function':'ROADSIDE TRADE','text':'Rittenhouse recorded gas and groceries, but no cafe, garage or tourist accommodation.','reference':'Chapter 6, note 6. Rittenhouse, A Guide Book to Highway 66 (1946), pp.73-74.'},
 {'date':'1958','function':'TRADE AND RAIL','text':'The merchant still operated. Advertised local passenger stops disappeared between April and October.','reference':'Chapter 3, note 17; Chapter 6, note 12. Grubbs p.115; April 27 and October 26 timetables.'},
 {'date':'1963-65','function':'INTERSTATE','text':'The documented nearby I-40 project was built, decades after the first recorded withdrawals.','reference':'Chapter 6, note 21. NTSB report, project near mileposts 282.7-290.7.'},
 {'date':'1974','function':'RAIL ADMINISTRATION','text':'Cuervo was listed without an agent. Its billing was assigned to Tucumcari, as was Santa Rosa\'s.','reference':'Chapter 6, note 17. Rock Island Station Book, December 15, C15 / PDF p.67.'},
 {'date':'2017','function':'CHURCH','text':'A funeral Mass was announced at the Cuervo church; the notice also described restoration work.','reference':'Chapter 8, note 7. Dorothy Chavez obituary, March 2017.'},
 {'date':'2020 / 2026','function':'RANCHING','text':'A 2020 ranch purchase outside Cuervo was reported in 2026. The operation became a conservation-award finalist that year.','reference':'Chapter 8, notes 1-2. January 2026 interview; July 2026 Leopold Conservation Award finalist announcement.'}
]
fig=plt.figure(figsize=(8,8.7));ax=fig.add_axes([.025,.045,.95,.89]);ax.set_xlim(0,1);ax.set_ylim(-1.2,9.8);ax.axis('off')
fig.text(.06,.98,'SELECTED OBSERVATIONS / 1903-2026',color=GRAY,fontsize=11,va='top')
ax.plot([.225,.225],[0,9],color=RULE,lw=1.4,zorder=1)
for i,row in enumerate(events):
    y=9-i;ax.scatter(.225,y,s=30,color=NAVY,zorder=3)
    ax.text(.193,y+.08,row['date'],ha='right',va='top',color=NAVY,fontsize=13,weight='bold')
    ax.text(.265,y+.20,row['function'],va='top',color=BROWN,fontsize=9.4,weight='bold')
    ax.text(.265,y-.055,textwrap.fill(row['text'],width=58),va='top',color=INK,fontsize=11.9,linespacing=1.38)
fig.text(.06,.023,'Rows are equally spaced. They do not measure elapsed time or continuous operation.',color=GRAY,fontsize=9.4)
chapter_paths=sorted((ROOT/'manuscript/book-revision-02/chapters').glob('*.md'))
save(fig,'functional-chronology',{'title':'Different functions, different clocks',
    'inputs':[source(p.relative_to(ROOT).as_posix()) for p in chapter_paths],
    'events':events,
    'limits':'Selected observations, not exhaustive business lifespans. Blank periods do not mean inactivity. Dates identify reports, observations or stated intervals; newspaper termination and merchant closure are not inferred. The 2017 notice announced a Mass; it does not independently verify performance. Ranching outside the village is distinguished from village employment.'})

(OUT/'sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'figures':[r['key'] for r in manifest['figures']],'output_directory':str(OUT)},indent=2))
