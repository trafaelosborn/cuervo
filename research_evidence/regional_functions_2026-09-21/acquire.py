from pathlib import Path
import concurrent.futures, hashlib, json, sys, urllib.request
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'sources/regional_functions_2026-09-21'
OUT.mkdir(parents=True,exist_ok=True)
tasks=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
def fetch(t):
    item=dict(t)
    try:
        request=urllib.request.Request(t['url'],headers={'User-Agent':'Cuervo historical research / public source retrieval'})
        with urllib.request.urlopen(request,timeout=45) as r:
            data=r.read(); item.update(final_url=r.url,content_type=r.headers.get('Content-Type'))
        path=OUT/t['filename']; path.write_bytes(data)
        item.update(local_file=path.relative_to(ROOT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),retrieved_utc=datetime.now(timezone.utc).isoformat(),status='downloaded')
    except Exception as e: item.update(status='failed',error=str(e))
    return item
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(fetch,tasks))
manifest=OUT/'download_manifest.json'
prior=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
manifest.write_text(json.dumps(prior+results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(results,ensure_ascii=True))
