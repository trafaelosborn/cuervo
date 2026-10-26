"""Download public primary sources; retain hashes and page-level extracted text."""
from pathlib import Path
import json, hashlib, urllib.request, concurrent.futures
from datetime import datetime, timezone
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'sources/economic_synthesis_2026-09-23'
OUT.mkdir(parents=True,exist_ok=True)
targets=json.loads((Path(__file__).parent/'targets.json').read_text(encoding='utf-8'))
def get(t):
    row=dict(t); path=OUT/(t['id']+'.pdf')
    try:
        if not path.exists():
            req=urllib.request.Request(t['url'],headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=90) as r: data=r.read()
            if not data.startswith(b'%PDF-'): raise ValueError('Not a PDF')
            path.write_bytes(data)
        data=path.read_bytes(); reader=PdfReader(path)
        pages=[{'pdf_page':n+1,'text':p.extract_text() or ''} for n,p in enumerate(reader.pages)]
        (OUT/(t['id']+'_pages.json')).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
        (OUT/(t['id']+'.txt')).write_text('\n\n'.join('=== PDF PAGE %d ===\n%s'%(p['pdf_page'],p['text']) for p in pages),encoding='utf-8')
        row.update(status='held',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),pages=len(pages),file=path.relative_to(ROOT).as_posix(),retrieved_utc=datetime.now(timezone.utc).isoformat())
    except Exception as exc: row.update(status='failed',error=str(exc))
    print(json.dumps(row),flush=True); return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(get,targets))
(OUT/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
