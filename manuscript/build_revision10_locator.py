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

OUT = ROOT / 'manuscript/figures/book-revision10'
OUT.mkdir(parents=True, exist_ok=True)
NAVY, INK, GRAY, BROWN, RULE, PALE = '#1b3558', '#242528', '#756e65', '#96714f', '#d8d2c9', '#f2eee7'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12,
                    'svg.fonttype':'none', 'axes.unicode_minus':False})
manifest = {'date':'2026-10-02', 'scope':'Original figures using held evidence; no new source acquisition.',
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
# Separate exact scale bars: kilometers above, miles below.
for y,span,unit,mid in [(-47,40,'km',20),(-61,25*1.609344,'mi',12.5)]:
    ax.plot([28,28+span],[y,y],color=NAVY,lw=1.4)
    for x in [28,28+span/2,28+span]:ax.plot([x,x],[y-1.5,y+1.5],color=NAVY,lw=1)
    for x,s in [(28,'0'),(28+span/2,f'{mid:g}'),(28+span,f'{mid*2:g} {unit}')]:
        ax.text(x,y+4,s,ha='center',fontsize=10,color=GRAY)
fig.text(.075,.332,'Modern county outline and place reference points',color=GRAY,fontsize=10)
fig.text(.075,.285,'THE RAILWAY DISTANCES IN 1926',color=NAVY,fontsize=11)
rail=fig.add_axes([.10,.12,.81,.12]);rail.set_xlim(-3,62);rail.set_ylim(-.8,1.15);rail.axis('off')
rail.plot([0,59],[0,0],lw=1.5,color=NAVY)
for x,name in [(0,'Santa Rosa'),(17,'Cuervo'),(59,'Tucumcari')]:
    rail.scatter(x,0,s=50 if x==17 else 30,color=NAVY)
    rail.text(x,-.42,name,ha='center',fontsize=12,color=NAVY)
rail.text(8.5,.35,'27 km (17 mi)',ha='center',fontsize=11,color=BROWN)
rail.text(38,.35,'68 km (42 mi)',ha='center',fontsize=11,color=BROWN)
fig.text(.075,.040,'Distance diagram below the map; it does not trace the railway route.',color=GRAY,fontsize=10)
save(fig,'regional-locator',{
    'title':'Cuervo and its regional neighbors',
    'inputs':[source(GEO),source(PLACES),source(REFERENCE),source('sources/01_railroad/rock_island_public_timetable_1926-01.pdf')],
    'coordinates_lon_lat':locations,'projection_wkt':crs.to_wkt(),'county_blocks':len(features),
    'rail_miles':{'Santa Rosa-Cuervo':17,'Cuervo-Tucumcari':42},
    'source_locator':'2020 DHC internal points; held 2020 block polygons; regional audit section 6; January 1926 timetable, Table 2 p.18, notes p.19.',
    'limits':'Modern county outline is neither the historical Cuervo precinct nor a trading catchment. Cuervo is the audit reference point, other points are Census internal points. No roads or historic railway routes are drawn.'})


manifest['conversion']={'kilometers_per_mile':1.609344,'rail_km_exact':{'Santa Rosa-Cuervo':17*1.609344,'Cuervo-Tucumcari':42*1.609344},'display':'Whole kilometers, with original whole miles retained'}
(OUT/'locator-sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
