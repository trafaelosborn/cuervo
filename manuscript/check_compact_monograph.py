"""Verify that size reduction changes image encoding only."""
from pathlib import Path
from io import BytesIO
import hashlib,json,math
from PIL import Image,ImageChops,ImageStat
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'
OUTPUT=ROOT/'output/pdf/cuervo-monograph-compact.pdf'
RECORD=ROOT/'manuscript/monograph/compact'
report=json.loads((RECORD/'compression.json').read_text())
a=PdfReader(SOURCE);b=PdfReader(OUTPUT)
assert OUTPUT.stat().st_size<9_800_000
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==report['source_sha256']
assert len(a.pages)==len(b.pages)==148
assert a.metadata.title==b.metadata.title=='Cuervo: An Economic History of a New Mexico Ghost Town'
ai={p.indirect_reference.idnum:n for n,p in enumerate(a.pages,1)}
bi={p.indirect_reference.idnum:n for n,p in enumerate(b.pages,1)}
def destination(d,index):return [index[d[0].idnum],*list(d[1:])]
def links(page,index):
    values=[]
    for ref in page.get('/Annots',[]):
        obj=ref.get_object();value={'rect':list(obj.get('/Rect',[])),'subtype':obj.get('/Subtype')}
        if '/Dest' in obj:value['dest']=destination(obj['/Dest'],index)
        if '/A' in obj:
            action=obj['/A'];value['action']=dict(action)
            if action.get('/S')=='/GoTo':value['action']['/D']=destination(action['/D'],index)
        values.append(value)
    return values
def font_signature(font):
    desc=font['/FontDescriptor'];embedded=next(k for k in ['/FontFile','/FontFile2','/FontFile3'] if k in desc)
    return (font['/BaseFont'],hashlib.sha256(desc[embedded].get_data()).hexdigest(),hashlib.sha256(font['/ToUnicode'].get_data()).hexdigest())
seen=set();image_checks=[];font_count=set();annotations=0;chart_count=0
for n,(p,q) in enumerate(zip(a.pages,b.pages),1):
    assert p.extract_text()==q.extract_text(),('text',n)
    pc=p.get_contents();qc=q.get_contents()
    assert pc.get_data()==qc.get_data() if pc is not None else qc is None,('drawing commands',n)
    for key in ['/MediaBox','/CropBox','/TrimBox','/BleedBox']:assert p.get(key)==q.get(key),(key,n)
    assert links(p,ai)==links(q,bi),('links',n)
    annotations+=len(q.get('/Annots',[]))
    pf=p.get('/Resources',{}).get('/Font',{});qf=q.get('/Resources',{}).get('/Font',{})
    assert set(pf)==set(qf)
    for key in pf:
        original=pf[key].get_object();compact=qf[key].get_object()
        assert font_signature(original)==font_signature(compact)
        font_count.add(str(original['/BaseFont']))
    px=p.get('/Resources',{}).get('/XObject',{});qx=q.get('/Resources',{}).get('/XObject',{})
    assert set(px)==set(qx)
    for name,ref in px.items():
        original=ref.get_object();compact=qx[name].get_object()
        if original.get('/Subtype')!='/Image' or ref.idnum in seen:continue
        seen.add(ref.idnum)
        row=next(x for x in report['images'] if x['page']==n and x['original_pixels']==[original['/Width'],original['/Height']] and x['kind']!='mask')
        assert [compact['/Width'],compact['/Height']]==row['output_pixels']
        if row['kind'] in ['chart','source scan']:assert row['output_pixels']==row['original_pixels']
        if row['kind']=='chart':
            assert original.get_data()==compact.get_data()
            assert original['/SMask'].get_data()==compact['/SMask'].get_data()
            chart_count+=1
        image_checks.append({'page':n,'kind':row['kind'],'original_pixels':row['original_pixels'],'compact_pixels':row['output_pixels']})
assert annotations==367 and len(a.outline)==len(b.outline)==10
for old,new in zip(a.outline,b.outline):
    assert old.title==new.title
    assert a.get_destination_page_number(old)==b.get_destination_page_number(new)
assert a.trailer['/Root']['/ViewerPreferences']==b.trailer['/Root']['/ViewerPreferences']
result={'status':'passed','pages':148,'output_bytes':OUTPUT.stat().st_size,
    'decimal_MB':round(OUTPUT.stat().st_size/1_000_000,3),'all_text_unchanged':True,
    'all_page_drawing_commands_unchanged':True,'all_page_boxes_unchanged':True,
    'annotations_preserved':annotations,'bookmarks_preserved':10,
    'font_programs_and_character_maps_unchanged':True,'embedded_fonts':len(font_count),
    'charts_and_masks_pixel_identical':chart_count,'source_scans_full_resolution':True,
    'source_master_unchanged':True,'image_checks':image_checks,
    'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'visual_review':'pending'}
(RECORD/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='image_checks'},indent=2))
