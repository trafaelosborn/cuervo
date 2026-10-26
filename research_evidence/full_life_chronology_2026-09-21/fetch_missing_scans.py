from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
PAGES=json.loads((Path(__file__).parent/'canonical_ocr_pages.json').read_text(encoding='utf-8'))
DEST=ROOT/'sources/02_newspapers/cuervo_clipper/supplemental_scans_2026-09-21'
DEST.mkdir(parents=True,exist_ok=True)
selected=[x for x in PAGES if x['issue_date'] in ['1910-02-11','1912-02-22','1917-09-28'] or (x['issue_date']=='1921-11-04' and x['content_page_ordinal']>1)]
def fetch(x):
    path=DEST/f"{x['issue_date']}_page{x['content_page_ordinal']:02d}_unm{x['page_id']}.pdf"
    if not path.exists():
        req=urllib.request.Request(x['scan_url'],headers={'User-Agent':'Mozilla/5.0 (Cuervo historical research)'})
        with urllib.request.urlopen(req,timeout=60) as r: path.write_bytes(r.read())
    raw=path.read_bytes();reader=PdfReader(path)
    return dict(x,file=str(path.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                pdf_pages=len(reader.pages),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    fs={pool.submit(fetch,x):x for x in selected}
    for f in concurrent.futures.as_completed(fs):
        try:r=f.result();results.append(r);print('OK',r['file'],flush=True)
        except Exception as e:results.append(dict(fs[f],error=repr(e)));print('FAIL',repr(e),flush=True)
(DEST/'download_manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print('FINISHED',len(results),'ERRORS',sum('error' in x for x in results),flush=True)
