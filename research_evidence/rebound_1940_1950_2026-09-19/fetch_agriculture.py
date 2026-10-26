from pathlib import Path
from urllib.request import Request, urlopen
import hashlib, json
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'sources'/'03_census'/'agriculture_rebound_2026-09-19'
OUT.mkdir(parents=True,exist_ok=True)
specs=[
 ('1945_nm_agriculture_full.pdf','https://www.nass.usda.gov/AgCensus/archive/files/1945-New_Mexico-1945-01-full.pdf'),
 ('1950_nm_az_agriculture_introduction.pdf','https://www.nass.usda.gov/AgCensus/archive/files/1950-New_Mexico_and_Arizona-Table_of_Contents-1809-Table-01.pdf'),
 ('1950_nm_agriculture_counties.pdf','https://www.nass.usda.gov/AgCensus/archive/files/1950-New_Mexico_and_Arizona-Table_of_Contents-1809-Table-03.pdf'),
]
manifest=[]
for filename,url in specs:
    p=OUT/filename
    if not p.exists():
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0 archival research'}),timeout=90) as resp: data=resp.read()
        assert data.startswith(b'%PDF'), (url,data[:80])
        p.write_bytes(data)
    data=p.read_bytes()
    reader=PdfReader(p)
    manifest.append({'file':str(p.relative_to(ROOT)), 'url':url,'bytes':len(data),'pages':len(reader.pages),'sha256':hashlib.sha256(data).hexdigest()})
    text=[]
    for n,page in enumerate(reader.pages,1):
        text.append(f'\n--- PDF PAGE {n} ---\n'+(page.extract_text() or ''))
    (OUT/(p.stem+'.txt')).write_text('\n'.join(text),encoding='utf-8')
    print(filename,len(reader.pages),len(data),flush=True)
(OUT/'download_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
