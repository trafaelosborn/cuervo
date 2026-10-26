from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = ROOT / 'sources/pupil_links_and_holbrook_2026-09-21'
DEST.mkdir(parents=True, exist_ok=True)

def acquire(item):
    path = DEST / item['file']
    result = {'url':item['url'], 'local':str(path.relative_to(ROOT)).replace('\\','/')}
    try:
        request=urllib.request.Request(item['url'], headers={'User-Agent':'Mozilla/5.0 (Cuervo historical research)'})
        with urllib.request.urlopen(request,timeout=35) as response:
            data=response.read()
            result.update(final_url=response.url, content_type=response.headers.get('Content-Type'))
        path.write_bytes(data)
        result.update(status='downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    except Exception as e:
        result.update(status='failed',error=repr(e))
    return result

items=json.loads((HERE/'acquisitions.json').read_text(encoding='utf-8'))
with ThreadPoolExecutor(max_workers=5) as pool:
    results=list(pool.map(acquire,items))
(DEST/'download_manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for result in results:
    print(json.dumps(result),flush=True)
