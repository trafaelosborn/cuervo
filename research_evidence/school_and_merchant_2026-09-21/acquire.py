"""Preserve public research sources with URLs and checksums. No messages sent."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, sys, urllib.parse, urllib.request

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT/'sources/school_and_merchant_2026-09-21'
DEST.mkdir(parents=True, exist_ok=True)
CONFIG = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('acquisitions.json')

def acquire(item):
    path=DEST/item['file']
    try:
        if path.exists():
            return {'file':str(path.relative_to(ROOT)), 'url':item['url'], 'status':'already_held'}
        request=urllib.request.Request(item['url'],headers={'User-Agent':'Mozilla/5.0 (Cuervo historical research)'})
        with urllib.request.urlopen(request,timeout=45) as response:
            data=response.read()
            final_url=response.url
            content_type=response.headers.get('Content-Type','')
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        return {'file':str(path.relative_to(ROOT)), 'url':item['url'], 'final_url':final_url,
                'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest(),
                'content_type':content_type, 'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'status':'downloaded'}
    except Exception as error:
        return {'url':item['url'], 'file':item['file'], 'error':repr(error), 'status':'failed'}

items=json.loads(CONFIG.read_text(encoding='utf-8'))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    for entry in pool.map(acquire,items):
        with (DEST/'download_manifest.jsonl').open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(entry)+'\n')
        print(json.dumps(entry),flush=True)
