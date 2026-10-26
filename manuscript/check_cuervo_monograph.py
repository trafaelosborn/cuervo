"""Verify publication cleanup without loss of scholarly or visual content."""
from pathlib import Path
from collections import Counter
import hashlib,json,re
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'manuscript/monograph'
OLD=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-10.pdf'
PDF=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'
old=PdfReader(OLD);new=PdfReader(PDF)
old_manifest=json.loads((ROOT/'manuscript/book-revision-10/build-manifest.json').read_text())
manifest=json.loads((RECORD/'build-manifest.json').read_text())
assert hashlib.sha256(OLD.read_bytes()).hexdigest()==old_manifest['pdf_sha256']
assert len(new.pages)==148 and len(old.pages)==147
old_text=[p.extract_text() or '' for p in old.pages]
new_text=[p.extract_text() or '' for p in new.pages]
def norm(t):return ' '.join(t.split())
for i in range(2,145):
    assert norm(old_text[i].replace('COMPLETE READING PROOF / REVISION 10',''))==norm(new_text[i]),f'Content changed on page {i+1}'
assert norm(old_text[1].replace('COMPLETE READING PROOF / REVISION 10','').replace('Contents and note references are clickable.',''))==norm(new_text[1])
assert norm(new_text[0])=='MERIDIAN Cuervo An Economic History of a New Mexico Ghost Town Photographs by Taylor Osborn'
assert not new_text[147]
all_text='\n'.join(new_text)
for term in ['Complete manuscript','complete reading proof','revision 10','typography trial','temporary stand-in','in preparation','project concordance','LINKPLACEHOLDER','\ufffd','\u25a0','<!--','FIGURE:']:
    assert term.lower() not in all_text.lower(),term
assert not re.search(r'\b(?:IMG_\d+|1Y5A\d+)\.(?:JPG|CR2)\b',all_text)
assert new.metadata.title=='Cuervo: An Economic History of a New Mexico Ghost Town'
for field in ['figure_pages','backmatter_pages','chapters','body_words','notes','references','visual_positions','author_photographs']:
    assert manifest[field]==old_manifest[field],field

def images(reader):
    found=[];seen=set()
    def scan(resources):
        for ref in resources.get('/XObject',{}).values():
            key=(ref.idnum,ref.generation)
            if key in seen:continue
            seen.add(key);obj=ref.get_object()
            if obj.get('/Subtype')=='/Image':
                found.append((int(obj['/Width']),int(obj['/Height']),str(obj.get('/Filter')),hashlib.sha256(obj._data).hexdigest()))
            elif obj.get('/Subtype')=='/Form':scan(obj.get('/Resources',{}))
    for p in reader.pages:scan(p.get('/Resources',{}))
    return Counter(found)
assert images(old)==images(new),'Original image streams changed'

index={p.indirect_reference.idnum:n for n,p in enumerate(new.pages,1)}
links=[];external=0;fonts=set()
for i,p in enumerate(new.pages,1):
    for box in [p.mediabox,p.cropbox,p.trimbox,p.bleedbox]:assert list(box)==[0,0,612,792]
    for ref in p.get('/Resources',{}).get('/Font',{}).values():
        font=ref.get_object();desc=font['/FontDescriptor']
        assert any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3'])
        fonts.add(str(font.get('/BaseFont')))
    for ref in p.get('/Annots',[]):
        a=ref.get_object()
        if '/Dest' in a:
            d=a['/Dest'];assert d[0].idnum in index
            if d[1]=='/XYZ':assert 0<=float(d[2])<=612 and 0<=float(d[3])<=792
            links.append((i,index[d[0].idnum],*[float(v) for v in d[2:4]]))
        if '/A' in a and a['/A'].get('/S')=='/URI':external+=1
assert len(links)==247 and external==120 and len(new.outline)==10
notes=[l for l in links if 2<l[0]<142]
assert len(notes)==211 and len(set(l[1:] for l in notes))==169
assert {l[1] for l in links if l[0]==2}=={c['opening_page'] for c in manifest['chapters']}|set(manifest['backmatter_pages'].values())
photo_links=[l for l in links if l[0]>=146]
assert len(photo_links)==16
assert [l[1] for l in photo_links]==[int(x) for x in re.findall(r'Page (\d+):','\n'.join(new_text[145:147]))]

minimum_text=999;minimum_image=999
with pdfplumber.open(PDF) as doc:
    for i,p in enumerate(doc.pages,1):
        for c in p.chars:
            if not c['text'].strip():continue
            clearance=min(c['x0'],612-c['x1'],c['top'],792-c['bottom'])
            assert clearance>=18,(i,c['text'],clearance)
            minimum_text=min(minimum_text,clearance)
        for image in p.images:
            clearance=min(image['x0'],612-image['x1'],image['top'],792-image['bottom'])
            assert clearance>=18,(i,clearance)
            minimum_image=min(minimum_image,clearance)
report={
    'status':'passed','pages':148,'duplex_sheets':74,'main_text_and_notes_unchanged':True,
    'chapter_and_figure_pagination_unchanged':True,'production_labels_removed':True,
    'reader_facing_photo_page_references':16,'source_note_calls':211,'distinct_notes':169,
    'internal_links':len(links),'external_links':external,'bookmarks':len(new.outline),
    'all_original_image_streams_preserved':True,'unique_image_streams':sum(images(new).values()),
    'embedded_fonts':sorted(fonts),'minimum_text_edge_clearance_points':minimum_text,
    'minimum_image_edge_clearance_points':minimum_image,
    'source_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),
    'output_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'visual_review':'pending'}
(RECORD/'publication-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
