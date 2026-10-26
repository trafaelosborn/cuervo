"""Reproduce selected author photographs at proof size, preserving the full frame.

CR2 files supply the camera's full-size embedded JPEG. Originals are read only.
No crop, retouching, reconstruction, exposure adjustment or color grade is applied.
"""
from pathlib import Path
import json, hashlib, io
from PIL import Image, ImageOps
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'manuscript/figures/book-revision04-photos'
OUT.mkdir(parents=True,exist_ok=True)
MARCH=Path('B:/Photos/Raw Collections/2024.03.26 Cuervo NM')
OCTOBER=Path('B:/Photos/Raw Collections/2024.10.24 Cuervo NM')

OPENERS={
 1:('IMG_7453.JPG','Building and surrounding land, Cuervo.'),
 2:('IMG_7436.JPG','A gabled building among brush, Cuervo.'),
 3:('1Y5A2051.CR2','Neighboring buildings and their surroundings, Cuervo.'),
 4:('1Y5A2043.CR2','Stone facade and entrance path, Cuervo.'),
 5:('1Y5A2060.CR2','Light through an exposed roof, Cuervo.'),
 6:('IMG_7445.JPG','Vehicle remains, buildings and a passing truck, Cuervo.'),
 7:('1Y5A2046.CR2','Stone walls and fallen timber, Cuervo.'),
 8:('1Y5A2119.CR2','A stone church and adjoining buildings, Cuervo.')
}
PLATES={
 'window-inscription':{'chapter':1,'files':['1Y5A2086.CR2'],
     'caption':'Window and graffiti, Cuervo.','layout':'single'},
 'entrances':{'chapter':2,'files':['1Y5A2044.CR2','1Y5A2054.CR2'],
     'caption':'Two entrances, Cuervo: a stone arch at left; a timber surround at right.','layout':'pair'},
 'building-fabric':{'chapter':4,'files':['1Y5A2095.CR2'],
     'caption':'Exposed lath, door framing and sunlight, Cuervo.','layout':'single'},
 'domestic-interiors':{'chapter':5,'files':['IMG_9759.JPG','1Y5A2085.CR2'],
     'caption':'Kitchen fittings above; a window and painted walls below. Interiors, Cuervo. These photographs are not assigned to the named households discussed in this chapter.','layout':'stack'},
 'road-and-ground':{'chapter':6,'files':['IMG_7396.JPG'],
     'caption':'An unpaved road, utility poles and surviving masonry, Cuervo.','layout':'single'},
 'rooms-and-structure':{'chapter':7,'files':['1Y5A2097.CR2'],
     'caption':'Roof framing, exposed lath and doorways, Cuervo.','layout':'single'}
}
RETained=['IMG_7385.JPG','IMG_7456.JPG']
filenames=list(dict.fromkeys([v[0] for v in OPENERS.values()]+[f for v in PLATES.values() for f in v['files']]+RETained))
assert len(filenames)==18
assets={}
for name in filenames:
    p=(OCTOBER if name.startswith('1Y5A') or name.startswith('IMG_97') else MARCH)/name
    with Image.open(p) as original:
        ex=original.getexif();orientation=ex.get(274,1);date=ex.get_ifd(34665).get(36867)
        if p.suffix=='.CR2':
            offset,length=ex[273],ex[279]
            offset=offset[0] if isinstance(offset,tuple) else offset
            length=length[0] if isinstance(length,tuple) else length
            with p.open('rb') as f:f.seek(offset);blob=f.read(length)
            assert blob[:2]==b'\xff\xd8'
            im=Image.open(io.BytesIO(blob));im.load()
            if orientation==6:im=im.transpose(Image.Transpose.ROTATE_270)
            elif orientation==8:im=im.transpose(Image.Transpose.ROTATE_90)
            elif orientation==3:im=im.transpose(Image.Transpose.ROTATE_180)
            method='Camera full-size embedded JPEG extracted from CR2; orientation applied; no raw development.'
        else:
            im=ImageOps.exif_transpose(original).copy()
            method='Original JPEG; EXIF orientation applied.'
        original_size=im.size
        im.thumbnail((3600,3600),Image.Resampling.LANCZOS)
        dest=OUT/f'{p.stem}.jpg';im.convert('RGB').save(dest,quality=95,subsampling=0)
        assets[name]={'source':p.as_posix(),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
             'proof_image':dest.relative_to(ROOT).as_posix(),'proof_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
             'oriented_source_pixels':original_size,'proof_pixels':im.size,'exif_date_time_original':date,
             'original_orientation_tag':orientation,'method':method,'credit':'Taylor Osborn',
             'treatment':'Full frame; aspect ratio preserved; reproduction resizing only.',
             'caption_date':'Unassigned: directory labels and embedded camera dates differ.'}
report={'date':'2026-09-28','credit':'Taylor Osborn','total_selected_photographs':18,
 'previous_proof_photographs':3,'new_photographs':15,'new_chapter_opening_photographs':7,
 'new_photo_pages':6,'new_photo_page_images':8,
 'review_scope':'73 March JPEGs on seven existing contact sheets; 79 October CR2 camera previews and 15 October-folder JPEGs on eight new contact sheets. Eight DNGs and videos not reviewed for this selection. DJI JPEGs are indoor test frames, not aerials.',
 'date_note':'March file dates and folder dates differ; Canon EXIF reports August 2020 within the October 2024 folder. No exact capture dates are printed. Source metadata is retained here without silently correcting it.',
 'caption_rule':'Describe visible subject and place. Do not infer named occupants, exact historical uses, closure dates, causal explanations, ownership or present activity from these views. The stone facade in Chapter 4 is not assigned a school identity.',
 'raw_note':'Full-size camera JPEGs are adequate for this reading proof. Original CR2 files remain available for an authored final color workflow.',
 'openers':{str(n):{'file':v[0],'caption':v[1]} for n,v in OPENERS.items()},'plates':PLATES,
 'existing_chapter08_figures':{'8.2':'IMG_7385.JPG','8.3':'IMG_7456.JPG'},'assets':assets,'visual_review':'pending'}
(OUT/'sources.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['total_selected_photographs','new_photographs','new_photo_pages']},indent=2))
