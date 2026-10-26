"""Make a size-limited sharing copy with live text and full-resolution source scans."""
from pathlib import Path
from io import BytesIO
import hashlib,json,struct,zlib
from PIL import Image
from pypdf import PdfReader,PdfWriter
from pypdf.filters import ASCII85Decode
from pypdf.generic import NameObject,NumberObject,DictionaryObject

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'
OUTPUT=ROOT/'output/pdf/cuervo-monograph-compact.pdf'
RECORD=ROOT/'manuscript/monograph/compact';RECORD.mkdir(parents=True,exist_ok=True)
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'manuscript/monograph/build-manifest.json').read_text())
photo_pages={v['page'] for v in manifest['figure_pages'] if 'photo' in v['figure'] or v['figure'] in ['8:road','8:fabric']}
r=PdfReader(SOURCE);w=PdfWriter();w.clone_document_from_reader(r)
entries=[];seen=set()

def original_encoding(obj):
    data=obj._data;filters=obj.get('/Filter',[])
    if isinstance(filters,str):filters=[filters]
    filters=list(filters)
    if filters and filters[0]=='/ASCII85Decode':
        data=ASCII85Decode.decode(data);filters=filters[1:]
    assert len(filters)==1,filters
    return {'data':data,'filter':str(filters[0]),'decode':obj.get('/DecodeParms'),'method':'lossless stream cleanup'}

def png_encoding(im):
    buf=BytesIO();im.save(buf,format='PNG',optimize=True)
    data=buf.getvalue();offset=8;chunks=[]
    while offset<len(data):
        length=struct.unpack('>I',data[offset:offset+4])[0];kind=data[offset+4:offset+8]
        if kind==b'IDAT':chunks.append(data[offset+8:offset+8+length])
        offset+=12+length
    colors=3 if im.mode=='RGB' else 1
    return {'data':b''.join(chunks),'filter':'/FlateDecode','method':'lossless PNG predictor',
      'decode':DictionaryObject({NameObject('/Predictor'):NumberObject(15),NameObject('/Colors'):NumberObject(colors),NameObject('/BitsPerComponent'):NumberObject(8),NameObject('/Columns'):NumberObject(im.width)})}

def add_image(obj,page,photo=False,is_mask=False):
    ref=obj.indirect_reference
    if ref.idnum in seen:return
    seen.add(ref.idnum)
    base=original_encoding(obj);im=None
    if base['filter']=='/DCTDecode':
        im=Image.open(BytesIO(base['data']));im.load()
    elif base['filter']=='/FlateDecode' and obj.get('/BitsPerComponent')==8 and obj.get('/ColorSpace') in ['/DeviceRGB','/DeviceGray']:
        mode='RGB' if obj['/ColorSpace']=='/DeviceRGB' else 'L'
        im=Image.frombytes(mode,(int(obj['/Width']),int(obj['/Height'])),obj.get_data())
        compressed=png_encoding(im)
        if len(compressed['data'])<len(base['data']):base=compressed
    kind='mask' if is_mask else 'photograph' if photo else 'chart' if '/SMask' in obj else 'source scan'
    entries.append({'obj':obj,'ref':ref.idnum,'page':page,'kind':kind,'base':base,'im':im,
        'original_bytes':len(obj._data),'cache':{},'pixels':[int(obj['/Width']),int(obj['/Height'])]})
    if '/SMask' in obj:add_image(obj['/SMask'],page,is_mask=True)

for n,page in enumerate(w.pages,1):
    for ref in page.get('/Resources',{}).get('/XObject',{}).values():
        obj=ref.get_object()
        if obj.get('/Subtype')=='/Image':add_image(obj,n,n in photo_pages)

def jpeg(entry,quality,edge=None,subsampling=0):
    key=(quality,edge,subsampling)
    if key not in entry['cache']:
        im=entry['im']
        assert im is not None and im.mode in ('L','RGB')
        im=im.copy()
        if edge:im.thumbnail((edge,edge),Image.Resampling.LANCZOS)
        data=BytesIO();im.save(data,format='JPEG',quality=quality,optimize=True,subsampling=subsampling)
        entry['cache'][key]={'data':data.getvalue(),'filter':'/DCTDecode','decode':None,'pixels':list(im.size),'method':f'JPEG quality {quality}, maximum edge {edge or "original"}, chroma subsampling {subsampling}'}
    result=entry['cache'][key]
    return result if len(result['data'])<len(entry['base']['data']) else entry['base']

overhead=SOURCE.stat().st_size-sum(e['original_bytes'] for e in entries)
print(json.dumps({'overhead':overhead,'categories':{kind:{'count':sum(e['kind']==kind for e in entries),'original_bytes':sum(e['original_bytes'] for e in entries if e['kind']==kind)} for kind in set(e['kind'] for e in entries)}}),flush=True)
trials=[];selected=None
# Photographs may be reduced modestly; archival scans retain all their pixels.
# Generated charts and their masks are always encoded losslessly.
profiles=[(80,84,1150,2),(78,84,1150,2),(76,84,1150,2),(76,84,1120,2),(76,84,1100,2)]
for photo_quality,scan_quality,photo_edge,photo_subsampling in profiles:
    candidates=[]
    for e in entries:
        candidate=e['base']
        if photo_quality is not None and e['kind']=='photograph':candidate=jpeg(e,photo_quality,photo_edge,photo_subsampling)
        elif scan_quality is not None and e['kind']=='source scan':candidate=jpeg(e,scan_quality)
        candidates.append(candidate)
    estimated=overhead+sum(len(c['data']) for c in candidates)
    trials.append({'photo_quality':photo_quality,'scan_quality':scan_quality,'photo_edge':photo_edge,'estimated_bytes':estimated,'category_bytes':{kind:sum(len(c['data']) for e,c in zip(entries,candidates) if e['kind']==kind) for kind in set(e['kind'] for e in entries)}})
    print(json.dumps(trials[-1]),flush=True)
    if estimated<9_700_000:
        selected=candidates;break
assert selected is not None,'No profile meets the conservative 9.7 MB target'
changes=[]
for e,c in zip(entries,selected):
    obj=e['obj'];obj._data=c['data'];obj.decoded_self=None
    obj[NameObject('/Filter')]=NameObject(c['filter'])
    pixels=c.get('pixels',e['pixels'])
    obj[NameObject('/Width')]=NumberObject(pixels[0]);obj[NameObject('/Height')]=NumberObject(pixels[1])
    if c['decode'] is None:obj.pop(NameObject('/DecodeParms'),None)
    else:obj[NameObject('/DecodeParms')]=c['decode']
    changes.append({'page':e['page'],'kind':e['kind'],'original_pixels':e['pixels'],'output_pixels':pixels,'before_bytes':e['original_bytes'],'after_bytes':len(c['data']),'method':c['method']})
w.compress_identical_objects(remove_duplicates=True,remove_unreferenced=True)
with OUTPUT.open('wb') as f:w.write(f)
assert OUTPUT.stat().st_size<9_800_000
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==source_hash
report={'source':str(SOURCE),'output':str(OUTPUT),'source_sha256':source_hash,
  'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
  'source_bytes':SOURCE.stat().st_size,'output_bytes':OUTPUT.stat().st_size,
  'size_limit_bytes':9_800_000,'maximum_photograph_edge':photo_edge,
  'source_scans_full_pixel_dimensions':True,'charts_and_masks_lossless':True,
  'trials':trials,'images':changes,'visual_review':'pending'}
(RECORD/'compression.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['images','trials']},indent=2))
