"""Retrieve UNM's public CONTENTdm metadata/OCR; preserve source responses."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, re, sys, threading, time, urllib.request

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'sources/02_newspapers/cuervo_clipper/repository_ocr_2026-09-21'
DEST.mkdir(parents=True, exist_ok=True)
BASE = 'https://econtent.unm.edu/digital/api/'
LOCK = threading.Lock()

def get(url, name):
    path = DEST / name
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Cuervo historical research (public archive metadata)'})
            with urllib.request.urlopen(req, timeout=45) as response:
                raw = response.read()
            data = json.loads(raw)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            entry = {'url':url, 'file':str(path.relative_to(ROOT)), 'bytes':len(raw),
                     'sha256':hashlib.sha256(raw).hexdigest(),
                     'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
            with LOCK:
                with (DEST / 'download_manifest.jsonl').open('a', encoding='utf-8') as log:
                    log.write(json.dumps(entry) + '\n')
            return data
        except Exception:
            if attempt == 2: raise
            time.sleep(1 + attempt)

def index():
    records = []
    for page in (1, 2):
        url = BASE + f'search/collection/dignews/searchterm/Cuervo/field/title/mode/all/conn/and/maxRecords/200/page/{page}'
        data = get(url, f'index_page_{page}.json')
        print('SEARCH', page, 'total', data.get('totalResults'), flush=True)
        items = data.get('items', data.get('results', []))
        print('ITEMS', len(items), flush=True)
        records.extend(items)
    (DEST / 'index_records.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    return records

def children(obj):
    if isinstance(obj, list):
        for value in obj: yield from children(value)
    elif isinstance(obj, dict):
        if 'pageptr' in obj: yield obj
        else:
            for value in obj.values(): yield from children(value)

def run():
    records = index()
    pages, errors = [], []
    def parent(item):
        ident = item['itemId']
        obj = get(BASE + f'singleitem/collection/dignews/id/{ident}', f'items/{ident}.json')
        found = re.search(r'(\d{4}-\d{2}-\d{2})', item['title'])
        date = found.group(1) if found else None
        return [{'issue_date':date, 'issue_title':item['title'], 'parent_id':ident,
                 'scan_ordinal':i+1, 'page_id':p['pageptr'], 'repository_page_label':p['pagetitle'],
                 'source_url':BASE + f"singleitem/collection/dignews/id/{p['pageptr']}",
                 'scan_url':BASE + f"collection/dignews/id/{p['pageptr']}/download"}
                for i,p in enumerate(children(obj.get('objectInfo',{})))]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(parent, x): x for x in records}
        for n,f in enumerate(concurrent.futures.as_completed(futures),1):
            try: pages.extend(f.result())
            except Exception as e: errors.append({'item':futures[f], 'error':repr(e)})
            if n % 40 == 0: print('PARENTS',n,'/',len(records),flush=True)
    pages.sort(key=lambda p:(p['issue_date'] or '',p['parent_id'],p['scan_ordinal']))
    (DEST / 'page_index.json').write_text(json.dumps(pages,indent=2),encoding='utf-8')
    print('PAGES',len(pages),'PARENT ERRORS',len(errors),flush=True)
    def page(p):
        ident = p['page_id']
        obj = get(p['source_url'], f'pages/{ident}.json')
        content = obj.get('text') or ''
        path = DEST / 'text' / f"{p['issue_date']}_scan{p['scan_ordinal']:02d}_id{ident}.txt"
        path.parent.mkdir(exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return dict(p, text_file=str(path.relative_to(ROOT)), characters=len(content))
    completed=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(page,x):x for x in pages}
        for n,f in enumerate(concurrent.futures.as_completed(futures),1):
            try: completed.append(f.result())
            except Exception as e: errors.append({'item':futures[f],'error':repr(e)})
            if n % 100 == 0: print('OCR',n,'/',len(pages),flush=True)
    completed.sort(key=lambda p:(p['issue_date'] or '',p['parent_id'],p['scan_ordinal']))
    (DEST / 'ocr_page_index.json').write_text(json.dumps(completed,indent=2),encoding='utf-8')
    (DEST / 'errors.json').write_text(json.dumps(errors,indent=2),encoding='utf-8')
    print('COMPLETE',len(completed),'ERRORS',len(errors),'EMPTY',sum(p['characters']==0 for p in completed),flush=True)

if __name__ == '__main__':
    run()
