"""Stream explicitly selected public census microfilms; keep a verifiable manifest."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, urllib.request
from datetime import datetime, timezone
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'sources/_logs/census_full_history_2026-09-18'
spec=json.loads((LOG/'download_spec.json').read_text(encoding='utf-8'))

def fetch(item):
    row=dict(item)
    try:
        dest=(ROOT/item['path']).resolve()
        allowed=(ROOT/'sources').resolve()
        if not dest.is_relative_to(allowed):
            raise ValueError(f'Download target outside source directory: {dest}; permitted: {allowed}')
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():
            stage=dest.with_suffix('.pdf.part')
            print('Downloading '+item['identifier'],flush=True)
            req=urllib.request.Request(item['url'],headers={'User-Agent':'CuervoHistoricalResearch/1.0'})
            with urllib.request.urlopen(req,timeout=60) as response, stage.open('wb') as f:
                row['response_url']=response.url
                while chunk:=response.read(2**20):f.write(chunk)
            assert stage.stat().st_size==item['expected_bytes'],stage.stat().st_size
            PdfReader(stage)
            stage.replace(dest)
            row['status']='downloaded-validated'
        else:row['status']='existing-validated'
        assert dest.stat().st_size==item['expected_bytes']
        h=hashlib.sha256()
        with dest.open('rb') as f:
            while chunk:=f.read(2**20):h.update(chunk)
        row.update(bytes=dest.stat().st_size,sha256=h.hexdigest(),pages=len(PdfReader(dest).pages),checked_utc=datetime.now(timezone.utc).isoformat())
    except Exception as e:row.update(status='failed',error=str(e))
    return row

rows=[]
with ThreadPoolExecutor(max_workers=3) as pool:
    for f in as_completed([pool.submit(fetch,x) for x in spec]):
        row=f.result();rows.append(row)
        (LOG/'download_manifest.json').write_text(json.dumps(sorted(rows,key=lambda x:x['identifier']),indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:row.get(k) for k in ['identifier','status','bytes','pages','error']}),flush=True)
