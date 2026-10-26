from pathlib import Path
import json, hashlib
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
(OUT / 'crops').mkdir(parents=True, exist_ok=True)
people = json.loads((ROOT / 'research_evidence/rebound_1940_1950_2026-09-19/people_name_age_readings.json').read_text(encoding='utf-8-sig'))
households = ['1940-2B-78','1940-1A-1','1950-2-17','1950-3-10','1950-5-9','1950-6-20','1950-7-11','1950-8-19']
selected = [p for p in people if p['household'] in households]
(OUT / 'candidate_rows_prior_readings.json').write_text(json.dumps(selected, indent=2), encoding='utf-8')
# Fractions identify a readable detail within the already inspected full sheet.
specs = [
 ('1950_vigil',1950,'0003',(.075,.440,.940,.590)),
 ('1950_salas',1950,'0004',(.075,.397,.940,.460)),
 ('1950_holbrook',1950,'0006',(.075,.321,.940,.385)),
 ('1950_holbrook_sample',1950,'0006',(.075,.769,.940,.825)),
 ('1950_chavez',1950,'0007',(.075,.530,.940,.650)),
 ('1950_bailey',1950,'0008',(.075,.360,.940,.528)),
 ('1950_higgins',1950,'0009',(.075,.487,.940,.549)),
 ('1940_bailey_parents',1940,'00655',(.058,.710,.900,.785)),
 ('1940_bailey_children',1940,'00656',(.058,.210,.910,.315)),
 ('1940_alfonso',1940,'00652',(.058,.220,.900,.284)),
]
manifest=[]
for name,year,num,frac in specs:
    source = ROOT / (f'sources/03_census/1950_manuscripts/ed_10-6/43290879-New_Mexico-180130-{num}.jpg' if year==1950 else f'sources/03_census/1940_manuscripts/ed_10-6/m-t0627-02445-{num}.jpg')
    im=Image.open(source)
    box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(frac))
    dest=OUT/'crops'/f'{name}.png'
    im.crop(box).save(dest)
    manifest.append({'id':name,'source':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':str(dest.relative_to(ROOT)).replace('\\','/'),'box':box,'full_sheet_viewed':True})
(OUT/'crop_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'selected_prior_rows':len(selected),'crops':len(manifest)}))
