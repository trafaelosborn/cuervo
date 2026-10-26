"""Mechanical checks and contact sheets for all three revised chapter reading proofs."""
from pathlib import Path
from PIL import Image, ImageDraw
from pypdf import PdfReader
import json
import re

ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/rewrite-2026-09-28'
results=[]
for number,slug in [(1,'reading-cuervo'),(2,'why-a-town-here'),(3,'the-business-of-ranch-country')]:
    source=ROOT/f'manuscript/chapter-{number:02d}-{slug}.md'
    text=source.read_text(encoding='utf-8')
    body,notes=text.split('\n---\n',1)
    refs=re.findall(r'\[\^(\d+)\]',body)
    definitions=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    expected=[str(i+1) for i in range(len(definitions))]
    assert list(dict.fromkeys(refs))==expected
    assert definitions==expected
    missing=[p for p in re.findall(r'\]\((B:/[^)]+)\)',text) if not Path(p).exists()]
    assert not missing,missing
    reader=PdfReader(ROOT/f'output/pdf/cuervo-chapter-{number:02d}-{slug}.pdf')
    texts=[p.extract_text() or '' for p in reader.pages]
    assert reader.metadata.author=='Meridian'
    assert all('CHAPTER '+{1:'ONE',2:'TWO',3:'THREE'}[number] in t for t in texts)
    assert not any('\ufffd' in t or '\u25a0' in t or 'PLACEHOLDER' in t for t in texts)
    page_ids={p.indirect_reference.idnum for p in reader.pages}
    destinations=[]
    for page in reader.pages:
        for annotation in page.get('/Annots',[]):
            annotation=annotation.get_object()
            if '/Dest' in annotation:
                dest=annotation['/Dest']
                assert dest[0].idnum in page_ids
                assert 0<=float(dest[3])<=816
                destinations.append((dest[0].idnum,float(dest[2]),float(dest[3])))
    assert len(destinations)==len(refs)
    assert len(set(destinations))==len(definitions)
    prose=re.sub(r'<!--.*?-->','',body,flags=re.S)
    prose=re.sub(r'^#+.*$','',prose,flags=re.M)
    prose=re.sub(r'\[\^\d+\]','',prose)
    sentences=[s for s in re.split(r'(?<=[.!?])\s+',prose) if s.strip()]
    lengths=[len(s.split()) for s in sentences]
    longest=sorted(sentences,key=lambda x:len(x.split()),reverse=True)[:5]
    pages=sorted(QA.glob(f'ch{number:02d}-page-*.png'))
    assert len(pages)==len(reader.pages)
    for offset in range(0,len(pages),6):
        sheet=Image.new('RGB',(960,930),'#e4e4e4')
        draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(pages[offset:offset+6]):
            im=Image.open(path).convert('RGB');im.thumbnail((295,420))
            sheet.paste(im,(j%3*320+(320-im.width)//2,j//3*465+28))
            draw.text((j%3*320+14,j//3*465+9),f'Chapter {number} | Page {offset+j+1}',fill='black')
        sheet.save(QA/f'ch{number:02d}-overview-{offset//6+1}.png')
    results.append({'chapter':number,'pages':len(pages),'unique_notes':len(definitions),
                    'note_references':len(refs),'valid_internal_links':len(destinations),
                    'distinct_internal_destinations':len(set(destinations)),
                    'mean_sentence_words':round(sum(lengths)/len(lengths),1),
                    'longest_sentence_words':max(lengths),'longest_sentences':longest,
                    'text_checks':'passed','metadata':dict(reader.metadata)})
(QA/'validation.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k not in ['longest_sentences','metadata']} for r in results],indent=2))
