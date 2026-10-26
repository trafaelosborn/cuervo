"""Verify source integrity, text transfer, destinations and final proof geometry."""
from pathlib import Path
import json,re,hashlib
from pypdf import PdfReader
from PIL import Image,ImageDraw
import pdfplumber
ROOT=Path(__file__).resolve().parents[1]
REV=ROOT/'manuscript/book-revision-06';QA=ROOT/'tmp/pdfs/book-revision06-delivery-review';QA.mkdir(parents=True,exist_ok=True)
pdf=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-06.pdf'
manifest=json.loads((REV/'build-manifest.json').read_text(encoding='utf-8'))
reader=PdfReader(pdf);texts=[p.extract_text() or '' for p in reader.pages]
assert len(reader.pages)==manifest['pages']
assert not any(any(bad in t for bad in ['\ufffd','\u25a0','LINKPLACEHOLDER','<!--','FIGURE:','*New Mexico State Rail Plan*']) for t in texts)
page_index={p.indirect_reference.idnum:n+1 for n,p in enumerate(reader.pages)}
links=[]
for i,page in enumerate(reader.pages,1):
    for ref in page.get('/Annots',[]):
        a=ref.get_object()
        if '/Dest' in a:
            d=a['/Dest'];assert d[0].idnum in page_index
            x,y=(float(d[2]),float(d[3])) if len(d)>3 else (0,816)
            assert 0<=y<=816
            links.append((i,page_index[d[0].idnum],x,y))
sources=[x for x in links if 2<x[0]<manifest['backmatter_pages']['bibliography']]
assert len(sources)==manifest['references'],(len(sources),manifest['references'])
assert len(set(x[1:] for x in sources))==manifest['notes']
assert len(reader.outline)==10
toc=[x for x in links if x[0]==2]
assert {x[1] for x in toc}=={r['opening_page'] for r in manifest['chapters']}|set(manifest['backmatter_pages'].values())
photo_links=[x for x in links if x[0]>=manifest['backmatter_pages']['credits']]
assert len(photo_links)==16 # Eighteen images on sixteen opener/plate positions.
def norm(s):return ''.join(c.lower() for c in s if c.isalnum())
missing=[];missing_notes=[];notecounts={};figcounts={};chapters={}
for row in manifest['chapters']:
    n=row['chapter'];full=(ROOT/row['source']).read_text(encoding='utf-8');body,notes=full.split('\n---\n',1);chapters[n]=full
    assert hashlib.sha256((ROOT/row['source']).read_bytes()).hexdigest()==row['sha256'],('stale chapter',n)
    refs=re.findall(r'\[\^(\d+)\]',body);defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    assert list(dict.fromkeys(refs))==defs==list(map(str,range(1,len(defs)+1)))
    notecounts[n]=len(defs);figcounts[n]=len(re.findall('<!-- FIGURE:',body))
    chapter='\n'.join(texts[row['opening_page']-1:row['source_notes_page']-1])
    chapter=re.sub(r'CUERVO\s+MERIDIAN','',chapter);chapter=re.sub(r'COMPLETE READING PROOF / REVISION 6\s+\d+','',chapter);chapter=norm(chapter)
    for block in body.split('\n\n'):
        if not block.strip() or block.startswith(('#','<!--')):continue
        for fragment in re.split(r'\[\^\d+\]',block):
            fragment=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',fragment)
            if len(norm(fragment))>12 and norm(fragment) not in chapter:missing.append({'chapter':n,'fragment':fragment[:150]})
    end=manifest['chapters'][n]['opening_page']-1 if n<8 else manifest['backmatter_pages']['bibliography']-1
    note_pages='\n'.join(texts[row['source_notes_page']-1:end])
    note_pages=re.sub(r'CUERVO\s+MERIDIAN','',note_pages);note_pages=re.sub(r'COMPLETE READING PROOF / REVISION 6\s+\d+','',note_pages);note_pages=norm(note_pages)
    for num,value in re.findall(r'^\[\^(\d+)\]: (.*?)(?=\n\n\[\^|\Z)',notes,re.M|re.S):
        value=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',value)
        if norm(value) not in note_pages:missing_notes.append({'chapter':n,'note':num})
assert not missing,missing
assert not missing_notes,missing_notes
old=json.loads((ROOT/'manuscript/book-revision-05/build-manifest.json').read_text(encoding='utf-8'))
for row in old['chapters']:assert hashlib.sha256((ROOT/row['source']).read_bytes()).hexdigest()==row['sha256']
assert hashlib.sha256((ROOT/'output/pdf/cuervo-complete-reading-proof-revision-05.pdf').read_bytes()).hexdigest()=='c7f5f7138fab067184872ee50f6891753c6445b964a80e88853a295c783271c1'
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==manifest['pdf_sha256']
for n,full in chapters.items():
    for ch,num in re.findall(r'Chapter (\d+), note (\d+)',full):assert int(num)<=notecounts[int(ch)],(n,ch,num)
    for ch,num in re.findall(r'Figure (\d+)\.(\d+)',full):assert int(num)<=figcounts[int(ch)],(n,ch,num)

short=[];excluded={1,2}|{r['opening_page'] for r in manifest['chapters']}|{r['page'] for r in manifest['figure_pages']}
for i,t in enumerate(texts,1):
    if i not in excluded and len(t.split())<100:short.append({'page':i,'words':len(t.split()),'text':t[:550]})
geometry=[]
with pdfplumber.open(pdf) as document:
    for i,p in enumerate(document.pages,1):
        bad=[c for c in p.chars if c['text'].strip() and (c['x0']<34 or c['x1']>542 or c['top']<20 or c['bottom']>790)]
        if bad:geometry.append({'page':i,'characters':''.join(c['text'] for c in bad)[:180]})
assert not geometry,geometry

pages=sorted(QA.glob('page-*.png'))
if pages:
    assert len(pages)==len(reader.pages)
    for offset in range(0,len(pages),12):
        sheet=Image.new('RGB',(1280,1390),'#dddddd');draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(pages[offset:offset+12]):
            with Image.open(path) as im:
                im=im.convert('RGB');im.thumbnail((300,430));x,y=j%4*320,j//4*463;sheet.paste(im,(x+(320-im.width)//2,y+24))
            draw.text((j%4*320+15,j//4*463+6),f'Page {offset+j+1}',fill='black')
        sheet.save(QA/f'overview-{offset//12+1:02d}.png')
report={'pages':len(reader.pages),'body_words':manifest['body_words'],'valid_source_links':len(sources),'distinct_note_destinations':len(set(x[1:] for x in sources)),'contents_links':len(toc),'photo_concordance_links':len(photo_links),'bookmarks':len(reader.outline),'all_body_text_transferred':True,'all_notes_transferred':True,'revision5_integrity':'original chapter and PDF hashes match','page_edge_checks':'passed','short_pages_for_review':short,'rendered_pages':len(pages),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'visual_review':'pending'}
(REV/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
