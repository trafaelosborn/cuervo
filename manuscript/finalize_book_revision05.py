"""Record completion after mechanical checks and explicit visual review."""
from pathlib import Path
import json, re, hashlib

ROOT=Path(__file__).resolve().parents[1]
REV=ROOT/'manuscript/book-revision-05'

def main():
    m=json.loads((REV/'build-manifest.json').read_text())
    v=json.loads((REV/'validation.json').read_text())
    assert v['text_checks']=='passed' and not v['short_pages_for_review']
    assert m['pdf_sha256']==v['pdf_sha256']
    review=json.loads((REV/'visual-review.json').read_text())
    assert review['status']=='passed' and review['pdf_sha256']==m['pdf_sha256']
    for f in ['build-manifest.json','validation.json']:
        p=REV/f; data=json.loads(p.read_text());data['visual_review']='passed'
        p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    words=f"{m['body_words']:,}";pages=m['pages']
    manuscript='B:/Meridian/Cuervo/manuscript/book-revision-05/cuervo-complete-manuscript.md'
    pdf='B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof-revision-05.pdf'
    response='B:/Meridian/Cuervo/manuscript/book-revision-05/editorial-response.md'
    status=f"**First editor pass incorporated, September 29:** [Revision 5]({manuscript}) contains **{words} main-text words, 174 reader-facing source notes, 221 note references, 18 author photographs and 41 visual positions** in a [{pages}-page proof]({pdf}). Six substantive comments are resolved; the three Thursday Clipper dates and the bulletin's publication/collection dates are confirmed. The Golden State claim now cites an explicit contemporary discontinuance report. Thirty-two cadence edits and consistent quotation/range typography accompany the citation rewrite. All body text, note destinations, contents links and bookmarks pass verification; revised page layouts are checked. [Response to the editor]({response}). Revision 4 is preserved. Consolidated bibliography, index, focused scholarly critique and final print design remain."
    p=ROOT/'SUMMARY.md';s=p.read_text(encoding='utf-8');heading,rest=s.split('\n',1)
    p.write_text(heading+'\n\n'+status+'\n'+rest,encoding='utf-8')
    p=ROOT/'manuscript/book-architecture.md';s=p.read_text(encoding='utf-8')
    s=re.sub(r'^\*\*Current status, September 28:.*$',status,s,count=1,flags=re.M)
    p.write_text(s,encoding='utf-8')
    p=ROOT/'manuscript/visual-program.md';s=p.read_text(encoding='utf-8')
    new=f"**Current complete reading proof, revision 5:** The [{pages}-page proof]({pdf}) retains **18 author photographs and 41 visual positions**. The first editor pass corrects dates and locators, rewrites source notes and normalizes caption typography. The [photographic sequence and provenance](B:/Meridian/Cuervo/manuscript/book-revision-04/photographic-review.md) remain those established in revision 4. [Editorial response]({response}). Final color treatment, print design and an independent figure-content audit remain distinct from the completed layout checks. The material below records earlier development."
    s=re.sub(r'^\*\*Current complete reading proof, revision 4:.*$',new,s,count=1,flags=re.M)
    p.write_text(s,encoding='utf-8')
    p=ROOT/'manuscript/argument-and-outline.md';s=p.read_text(encoding='utf-8')
    s=s.replace('The current book has 31,494 main-text words',f'The current book has {words} main-text words')
    s=s.replace('[Revision 4](B:/Meridian/Cuervo/manuscript/book-revision-04/cuervo-complete-manuscript.md) is the current text',f'[Revision 5]({manuscript}) is the current text')
    s=s.replace('Use [revision 4](B:/Meridian/Cuervo/manuscript/book-revision-04/photographic-review.md) as the baseline.',f'Use [revision 5]({response}) as the baseline; the first editor pass and reader-facing chapter notes are complete.')
    p.write_text(s,encoding='utf-8')
    p=ROOT/'cuervo-monograph-plan.md';s=p.read_text(encoding='utf-8')
    s=s.replace('Current editorial direction: September 28, 2026','Current editorial direction: September 29, 2026')
    s=re.sub(r'^\*\*Current phase:.*$',f'**Current phase:** Eight chapters and the first editor pass are complete. Revision 5 contains {words} main-text words, 174 reader-facing notes, 18 author photographs and 41 visual positions. Consolidated bibliography, index, focused scholarly critique and final production design remain.',s,count=1,flags=re.M)
    s=s.replace('[Revision 4](manuscript/book-revision-04/photographic-review.md)',f'[Revision 5]({response})')
    s=s.replace('Its 31,494 main-text words',f'Its {words} main-text words')
    s=s.replace('[revision 4 manuscript](manuscript/book-revision-04/cuervo-complete-manuscript.md)',f'[revision 5 manuscript]({manuscript})')
    p.write_text(s,encoding='utf-8')
    p=REV/'editorial-response.md';s=p.read_text(encoding='utf-8')
    s=s.replace('Final pagination and visual-review results are recorded below after the completed proof has been checked.',f'''## Final verification

The released proof has **{pages} pages and {words} main-text words**, with 174 notes, 221 internal note calls, eight chapter bookmarks and 41 visual positions, including eighteen author photographs. All original note calls remain; the siding paragraph adds one. Text preservation and internal destinations pass. The export contains no straight apostrophes, straight double quotation marks, working-note references or local-file links. Year ranges retain en dashes.

All pages were rendered. Every preliminary page was visually reviewed; final changed layouts and representative source-note pages were inspected again. The final render comparison and review record identify the pages checked. Chapter 4's stranded closing paragraph was removed by tightening its repetitive transition. No short orphan pages remain. Public links are syntactically valid HTTPS targets; this pass does not claim a fresh availability test of every remote server.

Revision 4 remains byte-for-byte unchanged. Final PDF SHA-256: `{m['pdf_sha256']}`.
''')
    p.write_text(s,encoding='utf-8')
    print(json.dumps({'pages':pages,'words':m['body_words'],'status':'complete','sha256':m['pdf_sha256']}))

if __name__=='__main__':main()
