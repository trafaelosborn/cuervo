"""Download explicitly listed public census sources; retain original bytes and provenance."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib, json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'sources/_logs/census_deep_dive_2026-09-18'
LOG.mkdir(parents=True, exist_ok=True)
SPEC=LOG/'download_spec.json'

def fetch(item):
    row=dict(item)
    dest=(ROOT/item['path']).resolve()
    assert dest.is_relative_to(ROOT)
    try:
        if dest.exists():
            data=dest.read_bytes(); row['status']='existing-validated'
        else:
            req=urllib.request.Request(item['url'],headers={'User-Agent':'CuervoHistoryResearch/1.0'})
            with urllib.request.urlopen(req,timeout=50) as r:
                data=r.read(); row['response_url']=r.url; row['content_type']=r.headers.get('Content-Type','')
            row['status']='downloaded-validated'
        if dest.suffix=='.json':json.loads(data)
        if dest.suffix=='.pdf':
            assert data.startswith(b'%PDF-'), 'Not a PDF'
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():dest.write_bytes(data)
        row.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),checked_utc=datetime.now(timezone.utc).isoformat())
    except Exception as e:
        row.update(status='failed',error=f'{type(e).__name__}: {e}')
    return row

if __name__=='__main__':
    specs=json.loads(SPEC.read_text(encoding='utf-8'));results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for future in as_completed([pool.submit(fetch,s) for s in specs]):
            r=future.result(); results.append(r)
            (LOG/'download_manifest.json').write_text(json.dumps(sorted(results,key=lambda x:x['path']),indent=2)+'\n',encoding='utf-8')
            print(json.dumps({k:r[k] for k in ('path','status','bytes','error') if k in r}),flush=True)
