from pathlib import Path
import json, sys, os
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tmp/regional_python'))
os.environ['MPLCONFIGDIR']=str(ROOT/'tmp/matplotlib_config')
from shapely.geometry import shape, box
from shapely.ops import transform
from pyproj import Transformer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
xform=Transformer.from_crs(4326,32613,always_xy=True).transform
fig,axes=plt.subplots(1,2,figsize=(14,7))
datasets=[(2010,'research_evidence/regional_functions_2026-09-21/blocks_2010_guadalupe.geojson','POP10','HOUSING10'),(2020,'sources/regional_functions_2026-09-21/blocks_2020_guadalupe.geojson','POP100','HU100')]
records=[]
for n,(year,path,pk,hk) in enumerate(datasets):
    data=json.loads((ROOT/path).read_text())['features'];ax=axes[n]
    bounds=box(-104.422,35.02,-104.395,35.043)
    print('YEAR',year,'county total',sum(f['properties'][pk] for f in data))
    for f in data:
        g=shape(f['geometry']);a=f['properties']
        if not g.intersects(bounds):continue
        identifier=a.get('GEOID',a.get('BLOCKID10'))
        clip=g.intersection(bounds)
        polygons=list(clip.geoms) if clip.geom_type=='MultiPolygon' else [clip]
        for poly in polygons:
            if poly.geom_type!='Polygon': continue
            x,y=poly.exterior.xy;ax.fill(x,y,alpha=.22,color='#cb7d37' if a[pk] else '#ddd');ax.plot(x,y,color='#777',lw=.7)
        rp=clip.representative_point();ax.text(rp.x,rp.y,identifier[-4:]+'\n'+str(a[pk])+'p/'+str(a[hk])+'h',ha='center',va='center',fontsize=8)
        records.append({'year':year,'geoid':identifier,'population':a[pk],'housing':a[hk],'bounds':g.bounds,'area_km2':round(transform(xform,g).area/1e6,4)})
    ax.plot(-104.40861,35.03111,'k+',markersize=10)
    ax.set_title(str(year));ax.set_xlim(bounds.bounds[0],bounds.bounds[2]);ax.set_ylim(bounds.bounds[1],bounds.bounds[3]);ax.set_aspect(1/.819);ax.ticklabel_format(useOffset=False)
fig.suptitle('Cuervo vicinity: census blocks, population (p), housing units (h)')
fig.tight_layout();fig.savefig(OUT/'block_inspection.png',dpi=150)
(OUT/'block_inspection.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records))
