"""Record the completed visual checks for the compact sharing edition."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'manuscript/monograph/compact'
OUTPUT=ROOT/'output/pdf/cuervo-monograph-compact.pdf'
raster=json.loads((ROOT/'tmp/pdfs/monograph-compact/raster-comparison.json').read_text())
assert OUTPUT.stat().st_size<9_800_000
assert raster['rendered_pages']==148 and len(raster['pixel_identical_pages'])==119
for name in ['compression.json','validation.json']:
    path=RECORD/name;data=json.loads(path.read_text())
    data['visual_review']='passed'
    path.write_text(json.dumps(data,indent=2),encoding='utf-8')
review={'date':'2026-10-21','status':'passed','rendered_pages':148,
    'pixel_identical_pages':119,'changed_image_pages_reviewed':[r['page'] for r in raster['changed_pages']],
    'full_page_photo_review':[3,137],'side_by_side_DOT_detail_review_at_160_dpi':[108,109,110],
    'findings':'No missing content, clipping, color shifts, or disruptive compression artifacts observed. DOT lettering remains comparable to the full-quality source at the inspected scale. Photo detail is reduced at high magnification; the original print master is preserved. Text, vector drawing commands, fonts, links, and chart pixels are unchanged.',
    'output_bytes':OUTPUT.stat().st_size,'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}
(RECORD/'visual-review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
print(json.dumps({'output':str(OUTPUT),'bytes':OUTPUT.stat().st_size,'status':'passed'}))
