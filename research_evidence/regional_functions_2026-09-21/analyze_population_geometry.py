"""Audit block products and bound allocation to explicitly defined study windows."""
from pathlib import Path
import json, sys, os, zipfile, io, csv
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SRC=ROOT/'sources/regional_functions_2026-09-21'
sys.path.insert(0,str(ROOT/'tmp/regional_python'))
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/matplotlib_config')
import shapefile, openpyxl
from shapely.geometry import shape, box, Point, mapping
from shapely.ops import transform, unary_union
from pyproj import Transformer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Reproducible county extraction from the original statewide TIGER distribution.
z=zipfile.ZipFile(SRC/'tabblock2010_35_pophu.zip')
parts={s:io.BytesIO(z.read(next(n for n in z.namelist() if n.endswith('.'+s)))) for s in ['shp','shx','dbf']}
r=shapefile.Reader(**parts)
features=[]
for sr in r.iterShapeRecords():
    a=sr.record.as_dict()
    if str(a['COUNTYFP10'])!='019': continue
    features.append({'type':'Feature','geometry':sr.shape.__geo_interface__,'properties':a})
assert len(features)==1708 and sum(f['properties']['POP10'] for f in features)==4687
(HERE/'blocks_2010_guadalupe.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}),encoding='utf-8')

# Join the independently held 2020 DHC geography distribution.
OLD=ROOT/'sources/03_census/census_deep_dive_2026-09-18'
wb=openpyxl.load_workbook(OLD/'2020_dhc_geoheader.xlsx',read_only=True,data_only=True)
fields=[str(r[1]).strip() for r in wb.active.iter_rows(values_only=True) if isinstance(r[2],(int,float)) and r[1]]
dhc={};zctas=[]
with zipfile.ZipFile(OLD/'nm2020.dhc.zip') as z:
    with z.open('nmgeo2020.dhc') as f:
        for vals in csv.reader(io.TextIOWrapper(f,encoding='latin1'),delimiter='|'):
            assert len(vals)==len(fields)
            g=dict(zip(fields,vals))
            if g['GEOCOMP']!='00' or g['GEOVAR']!='00':continue
            if g['SUMLEV']=='100' and g['STATE']=='35' and g['COUNTY']=='019':
                key=g['STATE']+g['COUNTY']+g['TRACT']+g['BLOCK']
                dhc[key]={'POP100':int(g['POP100']),'HOUSING':int(g['HU100'])}
            if g['SUMLEV']=='860' and '88417' in g['NAME']:zctas.append(g)
f2020=json.loads((SRC/'blocks_2020_guadalupe.geojson').read_text())['features']
assert len({f['properties']['GEOID'] for f in f2020})==len(f2020)==902
assert len(dhc)==902,(len(dhc), list(dhc)[:3])
differences=[]
for f in f2020:
    a=f['properties'];d=dhc[a['GEOID']]
    if a['POP100']!=d['POP100'] or a['HU100']!=d['HOUSING']:
        differences.append({'geoid':a['GEOID'],'tiger_pop':a['POP100'],'dhc_pop':d['POP100'],
                            'tiger_housing':a['HU100'],'dhc_housing':d['HOUSING']})
    a['DHC_POP100']=d['POP100'];a['DHC_HOUSING']=d['HOUSING']
(HERE/'blocks_2020_guadalupe_dhc_join.geojson').write_text(json.dumps({'type':'FeatureCollection','features':f2020}),encoding='utf-8')

project=Transformer.from_crs(4326,32613,always_xy=True).transform
project2010=Transformer.from_crs(4269,32613,always_xy=True).transform
inverse=Transformer.from_crs(32613,4326,always_xy=True).transform
center=(-104.40861,35.03111)
origin=transform(project,Point(center))
window=box(-104.422,35.020,-104.395,35.043)
regions=[('core_rectangle',transform(project,window))]+[(f'radius_{mile:g}_miles',origin.buffer(mile*1609.344,quad_segs=96)) for mile in [.5,2,5]]
datasets=[(2010,features,'BLOCKID10','POP10','HOUSING10'),(2020,f2020,'GEOID','DHC_POP100','DHC_HOUSING')]
results=[];blocks=[];plot_data={}
for year,fs,gkey,pkey,hkey in datasets:
    projected=[(f['properties'],transform(project2010 if year==2010 else project,shape(f['geometry']))) for f in fs]
    plot_data[year]=projected
    for name,region in regions:
        contained=[];crossing=[]
        for a,g in projected:
            # Positive-area overlap prevents a boundary touch from importing population.
            intersection=g.intersection(region)
            if intersection.area<=.01:continue
            item={'geoid':a[gkey],'population':a[pkey],'housing':a[hkey],
                  'area_km2':round(g.area/1e6,6),'inside_area_km2':round(intersection.area/1e6,6)}
            (contained if region.covers(g) else crossing).append(item)
        rows=contained+crossing
        results.append({'year':year,'study_area':name,'area_km2':round(region.area/1e6,4),
            'population_lower':sum(x['population'] for x in contained),
            'population_upper':sum(x['population'] for x in rows),
            'housing_lower':sum(x['housing'] for x in contained),
            'housing_upper':sum(x['housing'] for x in rows),
            'fully_contained_blocks':len(contained),'boundary_crossing_blocks':len(crossing),
            'contained':contained,'crossing':crossing})
        if name=='core_rectangle':blocks.extend([dict(year=year,**x) for x in rows])

audit={'inputs':{'2010':'TIGER2010BLKPOPHU statewide original; county filter 019',
                 '2020_geometry':'TIGERweb Tracts_Blocks layer 12 (2020)',
                 '2020_counts':'DHC geography file, SUMLEV 100, GEOCOMP 00, GEOVAR 00'},
       'county_blocks':{'2010':len(features),'2020':len(f2020)},
       'county_population':{'2010':sum(f['properties']['POP10'] for f in features),
                            '2020_TIGER':sum(f['properties']['POP100'] for f in f2020),
                            '2020_DHC':sum(d['POP100'] for d in dhc.values())},
       'tiger_dhc_different_blocks':len(differences),'tiger_dhc_differences':differences,
       'center_lon_lat':center,'core_rectangle_lon_lat':list(window.bounds),
       'projection':'WGS84 / UTM zone 13N, EPSG:32613. 2010 source NAD83 EPSG:4269 (archive .prj); 2020 query outSR=4326.',
       'method':'Lower sums fully contained blocks; upper also sums positive-area crossing blocks. No areal allocation, centroid allocation or individual inference.',
       'interpretation':'Geographic allocation bounds conditional on published block counts; not confidence intervals or bounds on census/disclosure-avoidance error. Analyst-defined windows are not a legal town or census place.',
       'zcta_88417_records_in_DHC_state_geo':zctas,
       'study_areas':results}
(HERE/'population_geometry_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
(HERE/'study_windows.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[
    {'type':'Feature','geometry':mapping(transform(inverse,g)),'properties':{'id':n,'definition':'analyst study area, not a legal boundary'}} for n,g in regions]},indent=2)+'\n',encoding='utf-8')

# Show the full extent of blocks crossing the same small study rectangle.
fig,axes=plt.subplots(1,2,figsize=(13,7),layout='constrained')
selected=[]
core=regions[0][1]
for year in [2010,2020]:
    selected += [g for a,g in plot_data[year] if g.intersection(core).area>.01]
extent=unary_union(selected).bounds
for ax,year in zip(axes,[2010,2020]):
    pkey='POP10' if year==2010 else 'DHC_POP100'
    for a,g in plot_data[year]:
        if g.intersection(core).area<=.01:continue
        color='#bc7144' if a[pkey]>0 else '#ddd9d1'
        for poly in (list(g.geoms) if g.geom_type=='MultiPolygon' else [g]):
            x,y=poly.exterior.xy
            ax.fill([(v-origin.x)/1000 for v in x],[(v-origin.y)/1000 for v in y],facecolor=color,alpha=.45,edgecolor='#555',linewidth=.6)
    x,y=core.exterior.xy
    ax.plot([(v-origin.x)/1000 for v in x],[(v-origin.y)/1000 for v in y],color='#163e55',lw=2)
    ax.scatter([0],[0],s=22,color='#163e55',zorder=5)
    for mile in [2,5]:
        c=origin.buffer(mile*1609.344);x,y=c.exterior.xy
        ax.plot([(v-origin.x)/1000 for v in x],[(v-origin.y)/1000 for v in y],color='#888',lw=.6,ls=':')
    ax.set_xlim((extent[0]-origin.x)/1000-1,(extent[2]-origin.x)/1000+1)
    ax.set_ylim((extent[1]-origin.y)/1000-1,(extent[3]-origin.y)/1000+1)
    ax.set_aspect('equal');ax.set_title(str(year),fontweight='bold')
    ax.set_xlabel('Kilometers east / west of reference point');ax.set_ylabel('Kilometers north / south')
    ax.spines[['top','right']].set_visible(False)
fig.suptitle('Blocks touching Cuervo extend far beyond the settlement',fontsize=16,fontweight='bold')
fig.get_layout_engine().set(rect=(0,.14,1,.94))
fig.legend(handles=[Patch(facecolor='#bc7144',alpha=.45,label='Published population > 0'),
                    Patch(facecolor='#ddd9d1',label='Published population = 0'),
                    Patch(facecolor='none',edgecolor='#163e55',label='Fixed core study rectangle')],loc='lower center',bbox_to_anchor=(.5,.065),ncol=3,frameon=False)
fig.text(.02,.015,'Colored areas show complete blocks intersecting the rectangle; they are not residential footprints. Dotted circles: 2 and 5 miles.\n'
         'Population comes from 2010 TIGER/2010 Census and 2020 DHC. Small counts are affected by census privacy protections.',fontsize=9,color='#444')
fig.savefig(HERE/'population_boundary_problem.png',dpi=180)
print(json.dumps({'audit':{k:v for k,v in audit.items() if k not in ['study_areas','tiger_dhc_differences','zcta_88417_records_in_DHC_state_geo']},
                  'bounds':[{k:v for k,v in r.items() if k not in ['contained','crossing']} for r in results],
                  'zcta':[{'name':r['NAME'],'pop':r['POP100'],'housing':r['HU100'],'area':r.get('AREALAND')} for r in zctas]},indent=2))
