from pathlib import Path
import json,re
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE=ROOT/'sources/school_and_merchant_2026-09-21'
OUT=HERE/'text'
OUT.mkdir(exist_ok=True)
RENDERS=HERE/'page_renders'
RENDERS.mkdir(exist_ok=True)
for name in ['superintendent_report_ia.pdf','education_survey_1921.pdf','nm_education_bulletin_30_1958.pdf']:
    path=BASE/name
    if not path.exists():continue
    reader=PdfReader(path)
    texts=[p.extract_text() or '' for p in reader.pages]
    (OUT/(path.stem+'.txt')).write_text('\n'.join(f'[PDF PAGE {i}]\n{t}' for i,t in enumerate(texts,1)),encoding='utf-8')
    matches=[{'pdf_page':i,'context':t[max(0,m.start()-300):m.end()+600]} for i,t in enumerate(texts,1) for m in re.finditer(r'Cuervo',t,re.I)]
    print(name,'PAGES',len(texts),'CUERVO',json.dumps(matches))
    print('FRONT MATTER',json.dumps([{'pdf_page':i,'text':t[:1200]} for i,t in enumerate(texts[:12],1) if len(t.strip())>50]))
    render_pages=sorted(set([i for i,t in enumerate(texts[:12],1) if re.search(r'(report|bulletin|directory|education)',t,re.I)] + [m['pdf_page'] for m in matches]))[:14]
    doc=pdfium.PdfDocument(str(path))
    for i in render_pages:
        target=RENDERS/f'{path.stem}_pdf{i}.jpg'
        if target.exists():continue
        page=doc[i-1];im=page.render(scale=1.5).to_pil();im.thumbnail((1600,2200));im.convert('RGB').save(target,quality=94);page.close()
    doc.close()
    print('RENDERED',render_pages)

names=json.loads((ROOT/'research_evidence/rebound_1940_1950_2026-09-19/people_name_age_readings.json').read_text(encoding='utf-8'))
print('TEACHER NAMES',json.dumps([x for x in names if x['year']==1950 and x.get('sheet')=='4' and x['line'] in [6,8]]))
for x in names:
    if x['year']==1950 and x.get('pdf_page')==4 and x['line'] in [6,8]:print('TEACHER BY PDF PAGE',json.dumps(x))
