"""Record completion after the final rendered proof has been visually reviewed."""
from pathlib import Path
import json,hashlib,re,shutil
ROOT=Path(__file__).resolve().parents[1]
REV=ROOT/'manuscript/book-revision-06'
manifest=json.loads((REV/'build-manifest.json').read_text(encoding='utf-8'))
validation=json.loads((REV/'validation.json').read_text(encoding='utf-8'))
pdf=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-06.pdf'
assert manifest['pdf_sha256']==validation['pdf_sha256']==hashlib.sha256(pdf.read_bytes()).hexdigest()
assert validation['rendered_pages']==manifest['pages']
assert validation['all_body_text_transferred'] and validation['all_notes_transferred']
assert manifest['body_words']==20990 and manifest['pages']==150
assert [x['page'] for x in validation['short_pages_for_review']]==[55]
prior=ROOT/'tmp/pdfs/book-revision06-final-review';final=ROOT/'tmp/pdfs/book-revision06-delivery-review'
unchanged=[n for n in range(1,114) if (prior/f'page-{n:03d}.png').read_bytes()==(final/f'page-{n:03d}.png').read_bytes()]
assert unchanged==[n for n in range(1,114) if n!=2]
review={'date':'2026-09-29','status':'passed','pdf_sha256':manifest['pdf_sha256'],
 'rendered_pages':manifest['pages'],'overview_pages_reviewed':list(range(1,manifest['pages']+1)),
 'review_method':'Poppler renders of every page, overview inspection, and selected larger PDFium renderings of figures, source plates, notes, contents and back matter. Final pages 1–113 except the newly checked contents page are byte-identical to the reviewed preceding renders; the remaining final pages were inspected after repagination.',
 'detail_review':'Sanborn map; financial chart; population and household charts; school, doctor, census and station-book plates; journey comparison; both chronologies; service comparison; notes; bibliography; photograph credits.',
 'repairs':'Moved plates to complete paragraph breaks and tightened the Chapter 2 transition. No clipped, overlapping or missing content found in the final review.',
 'accepted_short_page':{'page':55,'reason':'Two complete concluding source notes before the next chapter; retained without splitting notes or shrinking type.'},
 'limits':'Reading proof, not a physical press proof. Index and final publication design remain.'}
(REV/'visual-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
for path,data in [(REV/'build-manifest.json',manifest),(REV/'validation.json',validation)]:
    data['visual_review']='passed';path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

response=REV/'editorial-response.md';s=response.read_text(encoding='utf-8')
line='The final proof has **150 pages**. All 150 were rendered and reviewed; all body text and notes transferred, all 211 source-note links reach the 169 intended destinations, the 20 contents links and 16 photograph-concordance links resolve, and all 10 bookmarks pass. Page-edge checks found no overflow. Revision 5 chapter and PDF hashes are unchanged. The remaining short page, page 55, holds two complete concluding source notes before the next chapter.\n\n'
assert line not in s
s=s.replace('## Verification and limits\n\n','## Verification and limits\n\n'+line)
response.write_text(s,encoding='utf-8')
shutil.copyfile(response,ROOT/'output/editorial/cuervo-revision-06-completed-edit.md')

summary=ROOT/'SUMMARY.md';s=summary.read_text(encoding='utf-8');heading,rest=s.split('\n',1)
entry='**Complete editorial update, September 29:** [Revision 6](B:/Meridian/Cuervo/manuscript/book-revision-06/cuervo-complete-manuscript.md) implements all 49 agreed edits and the copy, illustration and layout repairs. It contains **20,990 main-text words, 169 source notes, 211 note references, 18 photographs and 40 visual positions** in a **150-page proof**. AC and Los Lunas remain compact alternative-path comparisons in Chapter 7; economic mechanisms are tied to decisions and evidence, with most theoretical attribution in notes. The revised Sanborn plate uses an intact original with readable details. A consolidated bibliography and photograph credits are included. All pages, text transfer, links and bookmarks pass review. [Completed edit record](B:/Meridian/Cuervo/manuscript/book-revision-06/editorial-response.md). Revision 5 is preserved. Indexing, outside critique and final publication design remain separate next steps.\n\n'
assert '**Complete editorial update, September 29:**' not in s
summary.write_text(heading+'\n\n'+entry+rest.lstrip('\n'),encoding='utf-8')

register=ROOT/'DOCUMENT-REGISTER.md';s=register.read_text(encoding='utf-8')
start=s.index('**Current manuscript, September 28:**');end=s.index('\n\n',start)
entry='**Current manuscript, September 29:** [Revision 6 manuscript](B:/Meridian/Cuervo/manuscript/book-revision-06/cuervo-complete-manuscript.md), [complete proof](B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof-revision-06.pdf) and [completed editorial record](B:/Meridian/Cuervo/manuscript/book-revision-06/editorial-response.md). The eight chapters contain **20,990 main-text words, 169 notes and 211 note calls**, with **18 photographs and 40 visual positions**, in **150 pages**. All agreed editorial edits are incorporated; a consolidated bibliography and photograph concordance are included. Text, notes, links, bookmarks and rendered pages pass verification. Earlier revisions remain dated snapshots. Final indexing, outside critique and publication design remain.'
register.write_text(s[:start]+entry+s[end:],encoding='utf-8')

report=ROOT/'output/editorial/cuervo-revision-05-final-editorial-pass.md';s=report.read_text(encoding='utf-8')
s=s.replace('The source PDF and manuscript have not been changed.','The Revision 5 source PDF and manuscript remain unchanged.')
s=s.replace('These directions are incorporated below; manuscript implementation remains pending.','These directions are incorporated below and were implemented in Revision 6 on September 29, 2026. See the [completed edit record](B:/Meridian/Cuervo/manuscript/book-revision-06/editorial-response.md). The recommendations below are retained as the original review record.')
report.write_text(s,encoding='utf-8')
print(json.dumps({'pages':manifest['pages'],'body_words':manifest['body_words'],'status':'complete','sha256':manifest['pdf_sha256']},indent=2))
