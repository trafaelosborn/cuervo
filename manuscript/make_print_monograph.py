"""Lossless US Letter duplex derivative of the approved Revision 10 PDF."""
from pathlib import Path
from collections import Counter
import hashlib,json,math
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import (ArrayObject,BooleanObject,ContentStream,DictionaryObject,
    FloatObject,NameObject,NullObject,RectangleObject)

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'tmp/pdfs/cuervo-monograph-typeset.pdf'
OUTPUT=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'
QA=ROOT/'tmp/pdfs/monograph-print-letter';QA.mkdir(parents=True,exist_ok=True)
RECORD=ROOT/'manuscript/monograph/print';RECORD.mkdir(parents=True,exist_ok=True)
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
assert source_hash==json.loads((ROOT/'manuscript/monograph/build-manifest.json').read_text())['pdf_sha256']
r=PdfReader(SOURCE);w=PdfWriter();w.clone_document_from_reader(r)
w.pdf_header='%PDF-1.7' # ViewerPreferences print scaling/duplex use the modern PDF schema.
S=33/34 # 816-point original height -> 792-point Letter height.
W,H=612,792
def offset(page_number):return (W-576*S)/2+(18 if page_number%2 else -18)

# The source's Helvetica declaration is unused boilerplate. Check actual text
# painting before removing its declarations and resource; all printed fonts embed.
for page in r.pages:
    active=None;stack=[]
    for a,o in ContentStream(page.get_contents(),r).operations:
        if o==b'q':stack.append(active)
        elif o==b'Q':active=stack.pop()
        elif o==b'Tf':active=str(a[0])
        elif o in (b'Tj',b'TJ',b"'",b'"'):assert active!='/F1'

page_map={p.indirect_reference.idnum:n for n,p in enumerate(w.pages,1)}
seen_dest=set();dest_count=0
def destination(value):
    global dest_count
    if not isinstance(value,ArrayObject) or id(value) in seen_dest:return
    seen_dest.add(id(value))
    if not value or not hasattr(value[0],'idnum'):return
    assert value[0].idnum in page_map
    tx=offset(page_map[value[0].idnum]);kind=str(value[1]);dest_count+=1
    def x(i):
        if not isinstance(value[i],NullObject):value[i]=FloatObject(float(value[i])*S+tx)
    def y(i):
        if not isinstance(value[i],NullObject):value[i]=FloatObject(float(value[i])*S)
    if kind=='/XYZ':x(2);y(3)
    elif kind in ('/FitH','/FitBH'):y(2)
    elif kind in ('/FitV','/FitBV'):x(2)
    elif kind=='/FitR':x(2);y(3);x(4);y(5)

for n,page in enumerate(w.pages,1):
    tx=offset(n)
    stream=ContentStream(page.get_contents(),w)
    stream.operations=[(a,o) for a,o in stream.operations if not(o==b'Tf' and str(a[0])=='/F1')]
    page.replace_contents(stream)
    fonts=page['/Resources'].get('/Font',{})
    if hasattr(fonts,'get_object'):fonts=fonts.get_object()
    if '/F1' in fonts:del fonts['/F1']
    page.add_transformation(Transformation((S,0,0,S,tx,0)))
    for key in ['/MediaBox','/CropBox','/TrimBox','/BleedBox']:
        page[NameObject(key)]=RectangleObject((0,0,W,H))
    if '/ArtBox' in page:del page['/ArtBox']
    for ref in page.get('/Annots',[]):
        annotation=ref.get_object()
        if '/Rect' in annotation:
            x1,y1,x2,y2=map(float,annotation['/Rect'])
            annotation[NameObject('/Rect')]=RectangleObject((x1*S+tx,y1*S,x2*S+tx,y2*S))
        if '/QuadPoints' in annotation:
            annotation[NameObject('/QuadPoints')]=ArrayObject([FloatObject(float(v)*S+(tx if i%2==0 else 0)) for i,v in enumerate(annotation['/QuadPoints'])])
        destination(annotation.get('/Dest'))
        action=annotation.get('/A',{});action=action.get_object() if hasattr(action,'get_object') else action
        if action.get('/S')=='/GoTo':destination(action.get('/D'))
    page.compress_content_streams()

def outlines(node):
    while node:
        node=node.get_object();destination(node.get('/Dest'))
        action=node.get('/A',{})
        if action.get('/S')=='/GoTo':destination(action.get('/D'))
        if node.get('/First'):outlines(node['/First'])
        node=node.get('/Next')
if w.root_object.get('/Outlines'):outlines(w.root_object['/Outlines'].get('/First'))

# One trailing blank produces 74 complete duplex sheets without moving a page.
blank=w.add_blank_page(width=W,height=H)
for key in ['/CropBox','/TrimBox','/BleedBox']:blank[NameObject(key)]=RectangleObject((0,0,W,H))
w.root_object[NameObject('/ViewerPreferences')]=DictionaryObject({
    NameObject('/PrintScaling'):NameObject('/None'),
    NameObject('/Duplex'):NameObject('/DuplexFlipLongEdge'),
    NameObject('/PickTrayByPDFSize'):BooleanObject(True)})
w.root_object[NameObject('/PageLayout')]=NameObject('/TwoPageRight')
w.add_metadata({'/Title':'Cuervo: An Economic History of a New Mexico Ghost Town',
    '/Subject':'An economic history of Cuervo, New Mexico',
    '/Creator':'Meridian print preparation',
    '/Producer':'Meridian / pypdf',
    '/ModDate':'D:20261021000000-06\'00\''})
w.compress_identical_objects(remove_duplicates=True,remove_unreferenced=True)
with OUTPUT.open('wb') as f:w.write(f)

def images(reader):
    found={};seen=set()
    def scan(resources):
        for ref in resources.get('/XObject',{}).values():
            key=(ref.idnum,ref.generation)
            if key in seen:continue
            seen.add(key);obj=ref.get_object()
            if obj.get('/Subtype')=='/Image':
                signature=(int(obj['/Width']),int(obj['/Height']),str(obj.get('/Filter')),hashlib.sha256(obj._data).hexdigest())
                found[key]=signature
            elif obj.get('/Subtype')=='/Form':scan(obj.get('/Resources',{}))
    for p in reader.pages:scan(p.get('/Resources',{}))
    return Counter(found.values())

out=PdfReader(OUTPUT)
assert len(out.pages)==148 and len(out.outline)==len(r.outline)==10
assert all(p.extract_text()==q.extract_text() for p,q in zip(r.pages,out.pages))
assert not out.pages[-1].extract_text()
assert images(r)==images(out),'Image data changed'
font_report={};annotation_count=0
out_pages={p.indirect_reference.idnum:n for n,p in enumerate(out.pages,1)}
for page in out.pages:
    for box in [page.mediabox,page.cropbox,page.trimbox,page.bleedbox]:assert list(box)==[0,0,612,792]
    for ref in page.get('/Resources',{}).get('/Font',{}).values():
        font=ref.get_object();desc=font.get('/FontDescriptor',{});desc=desc.get_object() if hasattr(desc,'get_object') else desc
        embedded=any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3'])
        assert embedded,font
        font_report[str(font.get('/BaseFont'))]=embedded
    for ref in page.get('/Annots',[]):
        a=ref.get_object();annotation_count+=1
        if '/Rect' in a:
            x1,y1,x2,y2=map(float,a['/Rect']);assert 0<=x1<=x2<=612 and 0<=y1<=y2<=792
        d=a.get('/Dest')
        if d:
            assert d[0].idnum in out_pages
            if d[1]=='/XYZ':assert 0<=float(d[2])<=612 and 0<=float(d[3])<=792
assert annotation_count==sum(len(p.get('/Annots',[])) for p in r.pages)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
report={'date':'2026-10-21','source':str(SOURCE),'output':str(OUTPUT),
    'source_sha256':source_hash,'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    'page_points':[612,792],'page_inches':[8.5,11],'original_pages':147,'total_pages':148,
    'duplex_sheets':74,'trailing_blank_pages':1,'artwork_scale':S,
    'mirrored_horizontal_shift_points':18,'body_font_points':11.3*S,
    'page_text_unchanged':True,'all_original_image_streams_identical':True,
    'unique_original_image_streams':sum(images(r).values()),'embedded_fonts':font_report,
    'annotation_count':annotation_count,'bookmarks':len(out.outline),'destinations_adjusted':dest_count,
    'printing':{'paper':'US Letter','orientation':'Portrait','color':'Color','scale':'100% / Actual size','sides':'Double-sided, flip on long edge','imposition':'Single pages; no booklet mode','crop_marks':False,'bleed':False},
    'visual_review':'pending'}
(RECORD/'preflight.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('embedded_fonts','printing')},indent=2))
