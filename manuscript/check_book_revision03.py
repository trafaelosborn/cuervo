"""Validate the integrated proof and prepare every page for visual review."""
from pathlib import Path
import re,json,hashlib,statistics,html
from pypdf import PdfReader
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
REV=ROOT/'manuscript/book-revision-03';QA=ROOT/'tmp/pdfs/book-revision03'
pdf=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-03.pdf'
manifest=json.loads((REV/'build-manifest.json').read_text())
reader=PdfReader(pdf);texts=[p.extract_text() or '' for p in reader.pages]
assert reader.metadata.author=='Meridian'
assert not any(any(bad in t for bad in ['\ufffd','\u25a0','LINKPLACEHOLDER','<!--','FIGURE:']) for t in texts)
page_index={p.indirect_reference.idnum:n+1 for n,p in enumerate(reader.pages)}
all_links=[];source_links=[]
for i,page in enumerate(reader.pages,1):
    for ref in page.get('/Annots',[]):
        a=ref.get_object()
        if '/Dest' in a:
            d=a['/Dest'];assert d[0].idnum in page_index
            dest_page=page_index[d[0].idnum]
            x,y=(float(d[2]),float(d[3])) if len(d)>3 else (0.0,816.0)
            assert 0<=y<=816
            all_links.append((i,dest_page,x,y))
            if i!=2:source_links.append((i,dest_page,x,y))
assert len(source_links)==manifest['references']
assert len(set(x[1:] for x in source_links))==manifest['notes']==174
assert len(reader.outline)==8
toc_pages=[x[1] for x in all_links if x[0]==2]
assert set(toc_pages)=={r['opening_page'] for r in manifest['chapters']}
def normalized(s):return ''.join(c.lower() for c in s if c.isalnum())
checks=[];missing=[]
for row in manifest['chapters']:
    n=row['chapter'];s=(ROOT/row['source']).read_text(encoding='utf-8').split('\n---\n',1)[0]
    # Exclude running furniture before testing complete paragraph preservation.
    chapter='\n'.join(texts[row['opening_page']-1:row['source_notes_page']-1])
    chapter=re.sub(r'CUERVO\s+MERIDIAN','',chapter)
    chapter=re.sub(r'COMPLETE READING PROOF / REVISION 3\s+\d+','',chapter)
    chapter=normalized(chapter)
    paragraphs=[]
    for b in s.split('\n\n'):
        if not b.strip() or b.startswith('#') or b.startswith('<!--'):continue
        b=re.sub(r'\[\^\d+\]','',b)
        b=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',b)
        paragraphs.append(b)
        # Visible reference numbers may interrupt a paragraph; check each sentence fragment around references separately below.
    for block in s.split('\n\n'):
        if not block.strip() or block.startswith('#') or block.startswith('<!--'):continue
        for fragment in re.split(r'\[\^\d+\]',block):
            fragment=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',fragment)
            if len(normalized(fragment))>12 and normalized(fragment) not in chapter:missing.append({'chapter':n,'fragment':fragment[:150]})
    sentences=re.split(r'(?<=[.!?])\s+',' '.join(paragraphs));lengths=[len(x.split()) for x in sentences if x.strip()]
    checks.append({'chapter':n,'paragraphs':len(paragraphs),'mean_sentence_words':round(statistics.mean(lengths),1),'longest_sentence_words':max(lengths)})
assert not missing,missing
pages=sorted(QA.glob('page-*.png'));assert len(pages)==len(reader.pages),(len(pages),len(reader.pages))
for offset in range(0,len(pages),8):
    sheet=Image.new('RGB',(1280,930),'#e4e4e4');draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(pages[offset:offset+8]):
        with Image.open(path) as im:
            im=im.convert('RGB');im.thumbnail((295,420));sheet.paste(im,(j%4*320+(320-im.width)//2,j//4*465+28))
        draw.text((j%4*320+14,j//4*465+9),f'Page {offset+j+1}',fill='black')
    sheet.save(QA/f'overview-{offset//8+1:02d}.png')
short=[]
exclude={1,2}|{r['opening_page'] for r in manifest['chapters']}|{r['page'] for r in manifest['figure_pages']}
for i,t in enumerate(texts,1):
    if i not in exclude and len(t.split())<100:short.append({'page':i,'words_including_furniture':len(t.split()),'text':t[:500]})
report={'pages':len(reader.pages),'body_words':manifest['body_words'],'notes':174,'valid_source_links':len(source_links),
 'distinct_note_destinations':len(set(x[1:] for x in source_links)),'contents_link_annotations':len(toc_pages),'chapter_bookmarks':len(reader.outline),
 'all_body_paragraphs_preserved_in_pdf':True,'sentence_checks':checks,'short_pages_for_review':short,
 'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'text_checks':'passed','visual_review':'pending'}
(REV/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':pass
