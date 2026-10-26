"""Integrity/coverage checks and visual-review sheets; no source files modified."""
from pathlib import Path
import datetime, hashlib, json, re
from urllib.parse import unquote
from PIL import Image, ImageDraw
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT/'sources/02_newspapers/cuervo_clipper/repository_ocr_2026-09-21'
API = 'https://econtent.unm.edu/digital/api/'
logged = {r['file'].replace('\\','/'): r for line in (BASE/'download_manifest.jsonl').read_text(encoding='utf-8').splitlines() if (r:=json.loads(line))}
raw_files = sorted(list((BASE/'items').glob('*.json')) + list((BASE/'pages').glob('*.json')) + list(BASE.glob('index_page_*.json')))
inventory = []
for path in raw_files:
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    record = logged.get(rel)
    if record:
        assert digest == record['sha256'], rel
        url = record['url']
    elif path.stem.startswith('index_page_'):
        page = path.stem.rsplit('_',1)[1]
        url = API+f'search/collection/dignews/searchterm/Cuervo/field/title/mode/all/conn/and/maxRecords/200/page/{page}'
    else:
        url = API+f'singleitem/collection/dignews/id/{path.stem}'
    entry = {'file':rel, 'url':url, 'bytes':len(raw), 'sha256':digest,
             'file_modified_utc':datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat()}
    if record:
        entry['retrieved_utc'] = record['retrieved_utc']
    else:
        entry['note'] = 'Initial retrieval preceded manifest logging. Filesystem modification time is retained separately; it is not asserted as an exact retrieval time.'
    inventory.append(entry)
(BASE/'raw_metadata_inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')

events = json.loads((HERE/'chronology.json').read_text(encoding='utf-8'))
register = json.loads((HERE/'business_register.json').read_text(encoding='utf-8'))
sources = json.loads((HERE/'sources.json').read_text(encoding='utf-8'))
for record in events+register:
    assert all(key in sources for key in record['source_ids']), record
assert all((ROOT/item['file']).is_file() for item in sources.values())
assert datetime.date(1922,9,27).strftime('%A') == 'Wednesday'

link_errors = []
for name in ['SUMMARY.md','DOCUMENT-REGISTER.md','research_evidence/full_life_chronology_2026-09-21.md',
             'research_evidence/cuervo_clipper_index_plan.md','research_evidence/research_status_2026-09-21.md']:
    path = ROOT/name
    for url in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        if url.startswith(('http://','https://','#')):
            continue
        target = path.parent/unquote(url.split('#')[0])
        if not target.exists():
            link_errors.append({'file':name,'link':url})

pdf = ROOT/'output/pdf/cuervo_full_life_chronology_2026-09-21.pdf'
reader = PdfReader(pdf)
text = '\n'.join(page.extract_text() for page in reader.pages)
normalized = re.sub(r'\s+',' ',text)
assert all(record['subject'] in normalized for record in events), 'Missing chronology subject'
assert all(record['entity'] in normalized for record in register), 'Missing register entity'
assert all(f'[{key}]' in normalized for key in sources), 'Missing source note'
assert '\ufffd' not in text, 'Replacement glyph in text extraction'

qa = HERE/'pdf_qa'
images = sorted(qa.glob('page-*.png'))
assert len(images) == len(reader.pages)
for start in range(0,len(images),6):
    group = images[start:start+6]
    sheet = Image.new('RGB',(1260,1140),'#e7e7e5')
    draw = ImageDraw.Draw(sheet)
    for k,path in enumerate(group):
        image = Image.open(path).convert('RGB')
        image.thumbnail((390,515))
        x = 20+(k%3)*415
        y = 30+(k//3)*565
        sheet.paste(image,(x,y))
        draw.text((x,y+519),f'PAGE {start+k+1}',fill='#263b37')
    sheet.save(qa/f'contact_{start+1:02d}_{start+len(group):02d}.jpg',quality=94)

result = {'pdf_pages':len(reader.pages), 'chronology_observations':len(events),
          'register_entries':len(register), 'source_entries':len(sources),
          'raw_metadata_files':len(inventory),
          'raw_metadata_with_retrieval_log':sum('retrieved_utc' in row for row in inventory),
          'pdf_external_link_annotations':sum(len(page.get('/Annots',[])) for page in reader.pages),
          'link_errors':link_errors,
          'page_word_counts':[len(page.extract_text().split()) for page in reader.pages],
          'visual_review':'Contact sheets and full-page renders require human inspection after this script.'}
(HERE/'artifact_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
assert not link_errors
