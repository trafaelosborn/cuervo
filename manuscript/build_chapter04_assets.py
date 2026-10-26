"""Faithful source details for Chapter 4; all coordinates refer to held page images."""
from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/chapter04-draft01'
OUT=ROOT/'manuscript/figures/chapter04'
OUT.mkdir(parents=True,exist_ok=True)
QA.mkdir(parents=True,exist_ok=True)
POP='C:/Users/Clem/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
sources={date:(ROOT/f'sources/02_newspapers/cuervo_clipper/full_scans/The Cuervo Clipper, {date} - The Cuervo Clipper {date}.pdf',2)
         for date in ['01-10-1919','09-09-1921','02-11-1921','12-01-1922','04-15-1921']}
sources.update({'school-survey':(ROOT/'Cuervo/Cuervo/Cuervo Plats/C-232.pdf',1),
                'postal-1913':(ROOT/'sources/05_postal/us_post_office_star_routes_curtailed_1914.pdf',33)})
manifest=[]
for key,(path,page) in sources.items():
    target=QA/f'{key}.png'
    if not target.exists():
        subprocess.run([POP,'-f',str(page),'-singlefile','-scale-to','4200','-png',str(path),str(target.with_suffix(''))],check=True,capture_output=True)
    manifest.append({'id':key,'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pdf_page':page})
def crop(key,name,box,basis):
    with Image.open(QA/f'{key}.png') as im:
        actual=tuple(round(value*([im.width/basis[0],im.height/basis[1]][i%2])) for i,value in enumerate(box))
        im.crop(actual).save(OUT/f'{name}.png')
    manifest.append({'output':name+'.png','source_id':key,'crop_pixels':actual,'treatment':'Crop only; original orientation and marks retained.'})
crop('02-11-1921','doctor-proposal',(765,712,927,1165),(1224,1584))
crop('09-09-1921','school-program-reading',(519,157,649,844),(1041,1347))
crop('09-09-1921','school-conditions-reading',(647,372,776,523),(1041,1347))
crop('12-01-1922','hicks-scale',(708,338,877,879),(1376,1780))
crop('12-01-1922','hicks-purpose',(877,733,1046,1083),(1376,1780))
crop('school-survey','school-overview',(0,0,1320,1000),(1500,1031))
crop('school-survey','school-footprint',(400,609,958,855),(1500,1031))
crop('postal-1913','postal-row',(105,760,1377,792),(1500,908))
crop('postal-1913','postal-headers',(110,401,1381,475),(1500,908))
teacher=ROOT/'research_evidence/school_and_merchant_2026-09-21/page_renders/clipper_1919-01-10_detail.png'
with Image.open(teacher) as im:
    im.crop((69,17,451,405)).save(OUT/'teacher-notice.png')
manifest.append({'output':'teacher-notice.png','source_id':'01-10-1919','derived_from':str(teacher),'crop_pixels':[69,17,451,405],'treatment':'Crop only, removing neighboring-column fragments.'})
(OUT/'sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Chapter 4 source details prepared.')
