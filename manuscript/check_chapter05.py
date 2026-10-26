"""Check Chapter 5's source-note destinations and prepare rendered-page review sheets."""
from pathlib import Path
from PIL import Image,ImageDraw
from pypdf import PdfReader
import json,re,hashlib,statistics
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'tmp/pdfs/chapter05-draft01'
source=ROOT/'manuscript/chapter-05-people-across-places.md'
pdf=ROOT/'output/pdf/cuervo-chapter-05-people-across-places.pdf'
text=source.read_text(encoding='utf-8');body,notes=text.split('\n---\n',1)
refs=re.findall(r'\[\^(\d+)\]',body);defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
assert defs==list(dict.fromkeys(refs))==[str(i+1) for i in range(len(defs))]
reader=PdfReader(pdf);page_ids={p.indirect_reference.idnum for p in reader.pages}
texts=[p.extract_text() or '' for p in reader.pages]
assert reader.metadata.author=='Meridian'
assert all('CHAPTER FIVE' in t for t in texts)
assert not any('\ufffd' in t or '\u25a0' in t or 'PLACEHOLDER' in t for t in texts)
destinations=[]
for page in reader.pages:
    for annotation in page.get('/Annots',[]):
        annotation=annotation.get_object()
        if '/Dest' in annotation:
            dest=annotation['/Dest'];assert dest[0].idnum in page_ids and 0<=float(dest[3])<=816
            destinations.append((dest[0].idnum,float(dest[2]),float(dest[3])))
assert len(destinations)==len(refs) and len(set(destinations))==len(defs)
plain=re.sub(r'<!--.*?-->','',body,flags=re.S);plain=re.sub(r'^#+.*$','',plain,flags=re.M);plain=re.sub(r'\[\^\d+\]','',plain)
sentences=[s for s in re.split(r'(?<=[.!?])\s+',plain) if s.strip()];lengths=[len(s.split()) for s in sentences]
pages=sorted(QA.glob('page-*.png'));assert len(pages)==len(reader.pages)
for offset in range(0,len(pages),6):
    sheet=Image.new('RGB',(960,930),'#e4e4e4');draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(pages[offset:offset+6]):
        with Image.open(path) as im:
            im=im.convert('RGB');im.thumbnail((295,420));sheet.paste(im,(j%3*320+(320-im.width)//2,j//3*465+28))
        draw.text((j%3*320+14,j//3*465+9),f'Chapter 5 | Page {offset+j+1}',fill='black')
    sheet.save(QA/f'overview-{offset//6+1}.png')
report={'chapter':5,'pages':len(reader.pages),'body_words':len(plain.split()),'note_definitions':len(defs),
  'valid_internal_links':len(destinations),'distinct_internal_destinations':len(set(destinations)),
  'mean_sentence_words':round(statistics.mean(lengths),1),'longest_sentence_words':max(lengths),
  'longest_sentences':sorted(sentences,key=lambda s:len(s.split()),reverse=True)[:8],
  'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'text_checks':'passed','visual_review':'pending'}
(QA/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
print('\nPAGE STARTS\n')
for i,t in enumerate(texts):print(i+1,' | '.join(t.splitlines()[4:7]))
