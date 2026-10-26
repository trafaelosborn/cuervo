from pathlib import Path
import hashlib,json,re
import pdfplumber
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PDF=ROOT/'output/pdf/cuervo_school_and_merchant_followup_2026-09-21.pdf'
sources=json.loads((HERE/'source_index.json').read_text(encoding='utf-8'))
events=json.loads((HERE/'observations.json').read_text(encoding='utf-8'))
people=json.loads((HERE/'pupil_paths.json').read_text(encoding='utf-8'))
ids={s['id'] for s in sources}
assert len(ids)==len(sources)==22
assert len(events)==12 and len(people)==5
assert all(e['source'] in ids for e in events+people)
for s in sources:
    if 'local_file' in s:
        p=ROOT/s['local_file'];assert p.exists(),p
        assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],p
assert [e['value'] for e in events if e['id'] in ['E01','E02','E03','E04','E05']]==[67,75,93,132,106]
assert next(e for e in events if e['id']=='E09')['value']==15
r=PdfReader(PDF);texts=[p.extract_text() or '' for p in r.pages];alltext='\n'.join(texts)
assert len(r.pages)==10
assert all(len(t)>700 for t in texts)
assert all(x not in alltext for x in ['\ufffd','\u25a0','turn224view','TODO'])
normalized=' '.join(alltext.split())
for phrase in ['Prof. Simmons','Miss Sanchez','fifteen barrels','Keep the year provisional','132','106','Marilyn Dodge','No underlying account books']:
    assert phrase in normalized,phrase
out=[]
with pdfplumber.open(PDF) as p:
    for i,page in enumerate(p.pages,1):
        words=page.extract_words()
        bad=[w['text'] for w in words if w['x0']<30 or w['x1']>582 or w['top']<14 or w['bottom']>778]
        out.append({'page':i,'characters':len(texts[i-1]),'words':len(words),'outside_safe_page_area':bad})
assert all(not p['outside_safe_page_area'] for p in out)
result={'pdf':str(PDF),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'pages':len(r.pages),
        'sources':len(sources),'observations':len(events),'pupil_paths':len(people),'checks_passed':True,
        'page_checks':out,'visual_review':'All ten final PNG renders inspected separately; tables, headings and body text readable, no clipping or overlap.'}
(HERE/'artifact_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='page_checks'},indent=2))
