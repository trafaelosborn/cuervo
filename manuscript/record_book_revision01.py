"""Update current editorial records after the complete manuscript build."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
REV=ROOT/'manuscript/book-revision-01'
m=json.loads((REV/'build-manifest.json').read_text())
e=json.loads((REV/'edits.json').read_text())
words=m['body_words'];pages=m['pages'];cut=e['original_body_words']-words
summary=f'All eight chapters are drafted. The first whole-book edit contains **{words:,} main-text words, 174 source notes and 25 visual positions**, assembled in one **{pages}-page continuously paginated reading proof** with linked contents and source notes. The edit removes {cut:,} words of repeated explanation, preserves all note references and keeps the documented limits beside the evidence. [Current edited manuscript](B:/Meridian/Cuervo/manuscript/book-revision-01/cuervo-complete-manuscript.md), [complete proof](B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof.pdf) and [editorial record](B:/Meridian/Cuervo/manuscript/book-revision-01/editorial-review.md). Separate chapter releases remain dated snapshots; their combined main text is 42,286 words. Next: publication fact-check and apparatus, photographic sequence, outside critique and final design.'
table='\n'.join(f"| {r['chapter']}. {r['title']} | {r['body_words']:,} | {r['notes']} | {r['opening_page']} |" for r in m['chapters'])
review=f'''# Cuervo: first whole-book edit

**September 28, 2026 — revision 1**

## Current reading text

The [complete PDF](B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof.pdf) and [combined Markdown](B:/Meridian/Cuervo/manuscript/book-revision-01/cuervo-complete-manuscript.md) are the current integrated manuscript. Editable chapter files are in `manuscript/book-revision-01/chapters/`. The standalone chapter manuscripts and PDFs remain dated releases. Further substantive edits should begin from the revision folder, then rebuild the combined files; rerunning `edit_book_revision01.py` resets those copies to this recorded edit.

**{words:,} main-text words; 174 notes; 220 note references; 25 visual positions; {pages} pages.** This meets the user's 40,000–60,000-word range without expansion for length alone. Headings, captions and apparatus are excluded from the main-text count.

| Chapter | Main-text words | Notes | Opening page |
|---|---:|---:|---:|
{table}

## Editorial coverage and changes

Read the bodies of all eight chapters as a continuous argument. The edit cuts nineteen repeated recap paragraphs across Chapters 1–7, a net reduction of {cut:,} words after three small wording changes. It shortens the introductory survey and removes repeated assurances about causation, regional connections and indicators. Evidence-specific qualifications remain beside their claims. The new Chapter 8 supplies the conclusion and has already received its own drafting edit.

Changed “people present” to “people enumerated” in the census introduction, replaced “petrol” with “gasoline” for usage consistency, and repaired the transition into the merchant's later survival. Read the resulting joins. No citation or source definition was removed or renumbered. [Exact edits and before/after hashes](B:/Meridian/Cuervo/manuscript/book-revision-01/edits.json).

The sequence now moves from the problem, through formation, trade, institutions, population and transport, to economic synthesis and persistence. Chapters 4 and 7 deliberately revisit the same service cases for different purposes: the former reconstructs them; the latter compares their economic requirements. Chapters 1 and 8 remain shorter framing chapters. This is the first continuity and repetition edit, not an exhaustive new source audit or outside scholarly review.

## Layout and validation

Continuous pagination, eight PDF chapter bookmarks, clickable contents and chapter-specific note destinations are new. Source-note numbers remain local to each chapter. The assembled text retains the established type sizes and source figures. Vector diagrams remain vector objects. The title page identifies the artifact as a reading proof; it does not substitute for the eventual cover.

[Build manifest](B:/Meridian/Cuervo/manuscript/book-revision-01/build-manifest.json) and [validation](B:/Meridian/Cuervo/manuscript/book-revision-01/validation.json) record current hashes, text-preservation checks, navigation and visual review status. Rendering and QA are separate from final print specifications. Earlier seven PDF hashes are unchanged, checked in the [Chapter 8 totals](B:/Meridian/Cuervo/research_evidence/chapter08_2026-09-28/manuscript_totals.json).

## Finite remaining work

1. **Publication fact-check and apparatus.** Check the precise quotations, names, dates, numbers and page locators in the text that exists. Consolidate the working notes into a consistent citation style, bibliography, source/illustration credits and a concise methods note. Prepare an index after pagination stabilizes. Return to a source only for a named claim; qualify or remove unsupported precision.
2. **Photographic edit and final visual sequence.** Choose from the user's full-resolution collection, balance surviving structures with geographic context, and place additional images only where they improve the book. Verify any building identification actually used in a caption. Resolve rights and credit requirements for the selected reproductions before publication. The existing cover photograph remains a candidate.
3. **Outside critique and response.** Obtain relevant historical/geographical and economic criticism of the full manuscript, plus a readability review. Record and address substantive objections. No invitations or messages have been sent in this task.
4. **Production.** Set title and cover, trim, paper, binding, color treatment and printer specifications. Finish layout and an actual physical proof; check small source text and photographic reproduction. Publication approval remains with the author.

Exact final cattle loading, every business closure, full household migration histories, exhaustive parcel chains and a universal point of irreversible decline remain outside the completion requirements. A consequential contradiction raised by the manuscript or reviewers is a reason for a bounded check.
'''
(REV/'editorial-review.md').write_text(review,encoding='utf-8')
(REV/'editorial-progress.json').write_text(json.dumps({'read_complete':[1,2,3,4,5,6,7,8],'remaining_body_reading':[],'first_whole_book_edit':'complete','publication_fact_check':'pending','outside_review':'pending','final_production':'pending'},indent=2),encoding='utf-8')

def change(path,fn):
    p=ROOT/path;t=p.read_text(encoding='utf-8');p.write_text(fn(t),encoding='utf-8')
def insert_after_title(t,p):
    first,rest=t.split('\n',1);return first+'\n\n'+p+'\n'+rest
change('SUMMARY.md',lambda t:insert_after_title(t,'**Current complete manuscript, September 28:** '+summary+'\n\n**Chapter 8 completed:** [What remained](manuscript/chapter-08-what-remained.md), 3,059 main-text words, 13 notes, three visual positions and a checked 17-page proof. [Editorial and source-review record](manuscript/chapter-08-editorial-notes.md). Dated entries below document earlier stages.'))
change('DOCUMENT-REGISTER.md',lambda t:re.sub(r'\*\*Current chapter proofs, September 28:\*\*[^\n]+','**Current manuscript, September 28:** '+summary,t,count=1)+f'\n| PJ-30 | Chapter 8, What remained | DRAFT 1 COMPLETE Sep 28 | [Manuscript](manuscript/chapter-08-what-remained.md), [PDF](output/pdf/cuervo-chapter-08-what-remained.pdf), [editorial record](manuscript/chapter-08-editorial-notes.md). 3,059 words, 13 notes, 14 resolving references, 17 reviewed pages and three visual positions. Production, property, church affiliation and physical survival distinguished. |\n| PJ-31 | Complete manuscript, first whole-book edit | REVISION 1 COMPLETE Sep 28 | [Edited text](manuscript/book-revision-01/cuervo-complete-manuscript.md), [PDF](output/pdf/cuervo-complete-reading-proof.pdf), [review](manuscript/book-revision-01/editorial-review.md). {words:,} main-text words, 174 notes, 25 visual positions, {pages} continuously paginated pages. Nineteen repeated recaps removed; earlier releases preserved. Publication fact-check, apparatus, final image sequence, outside critique and production remain. |\n')
change('manuscript/argument-and-outline.md',lambda t:re.sub(r'\*\*Drafting progress:\*\*[^\n]+','**Drafting and first revision complete:** '+summary,t,count=1).replace('The existing prose remains an initial argument draft; the scope remains the whole settlement with selected close-ups.','The complete manuscript and first whole-book edit now exist; the scope remains the whole settlement with selected close-ups.').split('## 8. The next work, in order')[0]+'## 8. The next work, in order\n\nThe eight-chapter draft and first repetition/continuity edit are complete. Follow the finite remaining-work list in [the revision record](B:/Meridian/Cuervo/manuscript/book-revision-01/editorial-review.md): publication fact-check and apparatus; photographic sequence; outside critique; final production. Further acquisition serves a named passage or caption.\n')
change('manuscript/book-architecture.md',lambda t:insert_after_title(t,'**Current status, September 28:** '+summary).replace('Chapter 8, *What remained*, is the remaining first draft. Its provisional 2,500-4,500 words would place the whole manuscript at about 41,700-43,700 main-text words, within the requested range; additional length must earn its place.','Chapter 8 subsequently added 3,059 words; all eight chapter releases total 42,286 words. The current edited text is the separate whole-book revision linked above.').split('### Continuing the manuscript')[0]+'### From manuscript to publication\n\nThe first whole-book edit is complete at '+f'{words:,}'+' main-text words. The user’s length target is met. Further length should answer an actual editorial need. The next work concerns the finished draft: publication fact-check and apparatus, photographic sequence, outside critique and production. No new broad acquisition program follows.\n')
change('manuscript/visual-program.md',lambda t:insert_after_title(t,'**Complete reading proof:** All eight chapters now contain 25 visual positions. Chapter 8 adds one parish source plate and two credited photographs. The integrated proof uses the same 25 positions; the final photographic sequence remains to be edited.').replace('Chapters 4-6 add twelve completed positions below; Chapters 7-8 remain proposals.','Chapters 4-6 add twelve completed positions below; Chapters 7-8 add five more.').replace('## Later chapters: selected directions','## Chapter 8: completed conclusion visuals\n\nFigure 8.1 reproduces the dated collection box and mission list from the December 21, 2025 parish bulletin, without inferring local service frequency. Figure 8.2 uses IMG_7385 for the road embankment and adjoining ground; Figure 8.3 uses IMG_7456 for surviving wall/interior fabric. Credit Taylor Osborn. No exact capture date, historical building use or construction/closure date is assigned. [Provenance](B:/Meridian/Cuervo/manuscript/figures/chapter08/sources.json) and [verification](B:/Meridian/Cuervo/manuscript/chapter-08-editorial-notes.md).\n\n## Earlier selected directions for the final image edit'))
def plan(t):
    t=re.sub(r'\*\*Current phase:\*\*[^\n]+','**Current phase:** Eight chapters drafted; first whole-book edit complete; publication review and visual development next',t,count=1)
    t=t.replace('The full manuscript, final image sequence and production design remain unfinished. The contribution must still be realized in the chapters and assessed through outside critique.','The full manuscript and first whole-book edit are complete. Final apparatus, photographic sequence, outside critique and production design remain.')
    lines=t.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('| 2. Develop and write'):
            lines[i]=f'| 2. Develop and write the chapters — COMPLETE; first whole-book edit COMPLETE September 28 | [Complete manuscript](manuscript/book-revision-01/cuervo-complete-manuscript.md), {words:,} main-text words, 174 notes, 25 visual positions and a {pages}-page integrated proof | All eight chapters carry a continuous argument and working source notes. Publication verification and outside critique remain. |'
        elif line.startswith('**Immediate work:**'):
            lines[i]='**Immediate work:** Review the complete manuscript, then finish the finite publication tasks in [the editorial record](manuscript/book-revision-01/editorial-review.md). Consolidate notes and bibliography, make the final photographic sequence, obtain outside critique and complete production. No new general source-acquisition gate applies.'
        elif line.startswith('- [ ] Develop the short draft into chapters'):
            lines[i]=f'- [x] Complete all eight chapters and the first integrated edit: {words:,} main-text words, within the user’s range.'
        elif line.startswith('- [ ] Select a few strong examples;'):
            lines[i]='- [x] Complete the first selection and repetition edit; retain consequential case evidence and qualifications.'
        elif line.startswith('- [ ] Read for argument, pacing, human agency and counterevidence.'):
            lines[i]='- [x] Read all eight chapter bodies for argument, pacing, agency and counterevidence; perform the first continuity edit.'
    t='\n'.join(lines)+'\n'
    t=t.replace('## Narrative structure','## Early narrative movements (developed into the eight-chapter architecture)')
    return t
change('cuervo-monograph-plan.md',plan)
print(json.dumps({'main_text_words':words,'pages':pages,'net_words_removed':cut,'review_record':str(REV/'editorial-review.md')},indent=2))
