"""Record completed checks for the reader-facing Letter edition."""
from pathlib import Path
import json,hashlib

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'manuscript/monograph'
PDF=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'
digest=hashlib.sha256(PDF.read_bytes()).hexdigest()
for path in [RECORD/'build-manifest.json',RECORD/'publication-check.json',RECORD/'print/preflight.json']:
    data=json.loads(path.read_text(encoding='utf-8'))
    data['visual_review']='passed'
    path.write_text(json.dumps(data,indent=2),encoding='utf-8')
review={
    'date':'2026-10-21','status':'passed','output_sha256':digest,
    'all_148_pages_rendered':True,
    'pages_3_through_145_pixel_identical_to_prior_print_copy_above_removed_footer':True,
    'full_size_inspection':[1,2,146,147],
    'overview_inspection':[1,2,3,8,9,48,108,109,110,121,137,142,146,147,148],
    'findings':'Approved subtitle added to the clean title page and PDF title metadata. Clean contents and photograph credits; no visible production labels, clipping or overlap. Body artwork and scholarly content are unchanged. Final blank is intentional.',
    'raster_comparison':'B:/Meridian/Cuervo/tmp/pdfs/monograph-print-letter/raster-comparison.json'}
(RECORD/'visual-review.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
(RECORD/'print/print-instructions.txt').write_text(
    'CUERVO\nAn Economic History of a New Mexico Ghost Town\n\nUS Letter (8.5 x 11 inches), portrait, color.\n'
    'Actual size / 100%; double-sided, flip on long edge.\n'
    'One PDF page per side. No booklet mode.\n'
    '148 pages / 74 sheets, with one intentional final blank.\n\n'
    'Print file: B:/Meridian/Cuervo/output/pdf/cuervo-monograph-print-letter.pdf\n',encoding='utf-8')
(RECORD/'edition-record.json').write_text(json.dumps({
    'date':'2026-10-21','current_print_file':str(PDF),'sha256':digest,
    'source_revision':10,'title':'Cuervo: An Economic History of a New Mexico Ghost Town','supersedes_print_file':'B:/Meridian/Cuervo/output/pdf/cuervo-revision-10-print-letter.pdf',
    'changes':['Added the approved subtitle to the title page and PDF title metadata.',
    'Removed Complete manuscript and revision/date labels from title page.',
    'Removed proof status and revision text from all running footers.',
    'Removed typography-trial and unfinished-production paragraph.',
    'Removed digital-navigation instruction from printed contents.',
    'Replaced camera filenames and internal project-concordance language with linked photo page references.',
    'Cleaned document title and subject metadata.'],
    'preserved':['Chapter text and source notes','All images and original image streams','Chapter, figure and bibliography pagination','All 367 links and ten bookmarks','US Letter duplex print setup']
},indent=2),encoding='utf-8')
print(json.dumps({'status':'passed','output':str(PDF),'sha256':digest}))
