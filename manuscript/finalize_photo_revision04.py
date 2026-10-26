"""Record the checked photographic proof and update the project's current pointers."""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
REV=ROOT/'manuscript/book-revision-04'
manifest=json.loads((REV/'build-manifest.json').read_text())
validation=json.loads((REV/'validation.json').read_text())
photo_path=ROOT/'manuscript/figures/book-revision04-photos/sources.json'
photos=json.loads(photo_path.read_text())
assert validation['text_checks']=='passed' and not validation['short_pages_for_review']
for asset in photos['assets'].values():
    assert hashlib.sha256(Path(asset['source']).read_bytes()).hexdigest()==asset['source_sha256']
    assert hashlib.sha256((ROOT/asset['proof_image']).read_bytes()).hexdigest()==asset['proof_sha256']
prior=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-03.pdf'
assert hashlib.sha256(prior.read_bytes()).hexdigest()=='899664555ee31795604dc290392439246c4ee705df13d3f719f64dd6738d84ca'
for new in (REV/'chapters').glob('*.md'):
    old=ROOT/'manuscript/book-revision-03/chapters'/new.name
    assert re.sub(r'<!-- PHOTO: [\w-]+ -->\s*','',new.read_text(encoding='utf-8'))==old.read_text(encoding='utf-8')
pages=manifest['pages']
positions={r['figure']:r['page'] for r in manifest['figure_pages']}
rows=[]
for n,row in photos['openers'].items():
    rows.append((positions[f'{n}:opening-photo'],f'Chapter {n} opening',row['file'],row['caption']))
for key,row in photos['plates'].items():
    rows.append((positions[f"{row['chapter']}:photo-{key}"],f"Chapter {row['chapter']} picture page",' + '.join(row['files']),row['caption']))
for fig,name in photos['existing_chapter08_figures'].items():
    key='road' if fig=='8.2' else 'fabric'
    rows.append((positions[f'8:{key}'],f'Retained Figure {fig}',name,'Existing caption retained.'))
table='\n'.join(f'| {page} | {place} | {name} | {caption} |' for page,place,name,caption in sorted(rows))
report=f'''# Photographic edit: revision 4

September 28, 2026. Current proof: **{pages} pages, 18 author photographs, 41 visual positions, 31,494 main-text words, 174 source notes and 220 note references**.

## Editorial decision

The prior proof underused Taylor Osborn's photographs. Three images gave too little of the place's physical character, and the earlier contact-sheet review omitted the October collection. The new sequence adds fifteen distinct photographs: seven chapter-opening images and eight images on six dedicated photographic pages. All eight chapters now open with a photograph; the Chapter 1 opening photograph and two Chapter 8 photographs are retained.

Photographs contribute setting, form, texture and pauses in the reading. They need not each establish a new economic claim. The selection moves between wider views, entrances, domestic rooms, construction details and the church. It includes modern road traffic and utility infrastructure as well as damaged buildings. Its purpose is to give the author's photography a sustained presence in the book. The impersonal prose style does not restrict that presence.

The window-and-graffiti photograph previously proposed for the cover, 1Y5A2086, appears within Chapter 1. This placement leaves a future cover design open.

## Sequence and proof pages

| Page | Position | Original file | Caption |
|---|---|---|---|
{table}

## Review coverage and image handling

Reviewed 167 still-image previews: 73 March JPEGs on seven existing contact sheets, plus 79 embedded Canon RAW previews and 15 JPEGs from the October directory on eight new sheets. Eight DNGs and the video files were not reviewed for this selection. The DJI JPEGs show indoor test scenes and were excluded.

Originals are in `B:/Photos/Raw Collections/2024.03.26 Cuervo NM/` and `B:/Photos/Raw Collections/2024.10.24 Cuervo NM/`. All source files remain unchanged; their hashes were rechecked after production. Selected proof derivatives and the complete provenance record are in [the photograph inventory](B:/Meridian/Cuervo/manuscript/figures/book-revision04-photos/sources.json).

The Canon files supplied full-size embedded camera JPEGs. This establishes their usability for the proof; it is not a finished RAW color treatment. New derivatives preserve the full composition and aspect ratio, apply stored orientation and resize for reproduction. No retouching or synthetic image content was added. The two retained Chapter 8 images continue to use their existing proof assets.

Folder dates and embedded capture dates conflict. The Canon files report August 2020 within an October 2024 folder; March JPEG metadata also differs from its folder label. Exact capture dates are therefore omitted from the new captions. The inventory retains the metadata without silently resolving it.

Captions describe visible subjects. They do not assign unsupported building histories, owners or occupants. In particular, the Chapter 4 stone facade is not identified as a school, and the domestic interiors are not assigned to named census households.

## Verification

All {pages} final pages were rendered and visually reviewed on contact sheets. All 16 photographic positions were also checked at larger reproduction size. Stray lines before photographic and documentary pages were corrected by keeping the adjacent paragraphs together.

All chapter prose, source notes and existing figure references are unchanged from revision 3. Every body paragraph is present in the PDF. All 220 note references resolve to 174 distinct source-note destinations; eight chapter bookmarks and linked contents are valid. No unplanned short text pages remain. The revision 3 PDF and all selected photographic originals retain their prior hashes.

## Remaining production choices

The photographic sequence is now a developed part of the reading proof. Final facing-page design, a coordinated color treatment from the originals, the cover and a physical print proof remain production work. Exact photographic dates can be resolved with the author during final caption preparation. The available collection emphasizes buildings and interiors; it supplies less direct coverage of the wider working ranch landscape. No new photography is required to assess this sequence.
'''
(REV/'photographic-review.md').write_text(report,encoding='utf-8')
for target,data in [(REV/'build-manifest.json',manifest),(REV/'validation.json',validation),(photo_path,photos)]:
    data['visual_review']='passed: all final pages inspected; photographic positions checked at larger size'
    data['original_photographs_unchanged']=True
    target.write_text(json.dumps(data,indent=2),encoding='utf-8')

def first_paragraph(path,prefix,new):
    p=ROOT/path;s=p.read_text(encoding='utf-8')
    pattern=re.escape(prefix)+r'[^\n]*(?:\n(?!\n)[^\n]*)*'
    s,count=re.subn(pattern,lambda m:new,s,count=1)
    assert count==1,(path,prefix)
    p.write_text(s,encoding='utf-8')

summary=f'**Photographic revision, September 28:** [Revision 4](B:/Meridian/Cuervo/manuscript/book-revision-04/cuervo-complete-manuscript.md) increases the author photographs from **3 to 18**, across all eight chapter openings and six additional picture pages. The [{pages}-page proof](B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof-revision-04.pdf) contains **31,494 main-text words, 174 source notes, 220 note references and 41 visual positions**. All prior prose, notes and analytical figures are retained. All pages were rendered and reviewed, and all note links and chapter bookmarks pass. [Photographic edit and sequence](B:/Meridian/Cuervo/manuscript/book-revision-04/photographic-review.md). The current priorities are focused scholarly positioning, publication apparatus, outside critique and final production design. Content governs length; no minimum word count or general source-acquisition requirement applies. Earlier revisions are preserved.'
p=ROOT/'SUMMARY.md';s=p.read_text(encoding='utf-8');i=s.index('\n\n')+2
s=s[:i]+summary+'\n\n'+s[i:];p.write_text(s,encoding='utf-8')
first_paragraph('manuscript/book-architecture.md','**Current status, September 28:**',f'**Current status, September 28:** Revision 4 contains **31,494 main-text words, 174 source notes, 18 author photographs and 41 visual positions** in a **{pages}-page continuously paginated proof**. Voice/compression, analytical visuals and the expanded photographic sequence are complete. [Current manuscript](B:/Meridian/Cuervo/manuscript/book-revision-04/cuervo-complete-manuscript.md), [proof](B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof-revision-04.pdf) and [photographic edit](B:/Meridian/Cuervo/manuscript/book-revision-04/photographic-review.md). Content determines length. Earlier allocations below are historical planning guidance. Earlier revisions and chapter releases are preserved.')
first_paragraph('manuscript/visual-program.md','**Current complete reading proof, revision 3:**',f'**Current complete reading proof, revision 4:** The book has **18 author photographs and 41 visual positions** across eight chapters. Fifteen photographs have been added: seven new chapter openers and eight images on six new picture pages. All revision 3 maps, graphs, diagrams and source plates are retained. [Photographic sequence and review](B:/Meridian/Cuervo/manuscript/book-revision-04/photographic-review.md), [current proof](B:/Meridian/Cuervo/output/pdf/cuervo-complete-reading-proof-revision-04.pdf) and [photographic provenance](B:/Meridian/Cuervo/manuscript/figures/book-revision04-photos/sources.json). Final color treatment and publication spreads remain. The material below records earlier development.')
p=ROOT/'manuscript/visual-program.md';s=p.read_text(encoding='utf-8');s=s.replace('Each selected visual should answer a question, establish a spatial relationship, show an observation or let the reader inspect a consequential source.','Selected visuals can answer a question, establish a spatial relationship, show an observation, let the reader inspect a source, or contribute atmosphere, texture and pacing. Photographs do not each need to establish an economic claim.');p.write_text(s,encoding='utf-8')
first_paragraph('cuervo-monograph-plan.md','**Current phase:**','**Current phase:** Eight chapters drafted; voice/compression, analytical-visual and expanded photographic passes complete. Revision 4 contains 31,494 main-text words, 18 author photographs and 41 visual positions. Focused scholarly positioning, publication apparatus, outside critique and final production design remain.')
first_paragraph('cuervo-monograph-plan.md','The scope, provisional argument, source foundation, chapter architecture and bounded scholarly positioning are in place.','The scope, provisional argument, source foundation, chapter architecture and bounded scholarly positioning are in place. [Revision 4](manuscript/book-revision-04/photographic-review.md) combines the completed eight-chapter text, the voice/compression edit, expanded analytical figures and an eighteen-photograph sequence. Its 31,494 main-text words are governed by content. Publication fact-check, focused scholarly comparison, apparatus, outside critique and final production remain.')
first_paragraph('cuervo-monograph-plan.md','**Immediate work:**','**Immediate work:** Use the [revision 4 manuscript](manuscript/book-revision-04/cuervo-complete-manuscript.md) and [photographic review](manuscript/book-revision-04/photographic-review.md) as the current baseline. Regional orientation, the functional chronology and the expanded photographic sequence are integrated. Strengthen specific scholarly comparison, prepare publication apparatus, obtain outside critique and finish production design. No minimum length or new general source-acquisition gate applies.')
p=ROOT/'cuervo-monograph-plan.md';s=p.read_text(encoding='utf-8')
s=s.replace('- [ ] Select roughly 12–18 initial candidates; assess the full-resolution files before judging print quality.','- [x] Select 18 photographs from 167 reviewed previews; prepare full-frame proof derivatives and check reproduction layouts. Final print color remains a production step.')
s=s.replace('- [ ] Pair and sequence images with the essay; favor distinct functions over repeated views of the same material.','- [x] Sequence 18 author photographs across eight chapter openings and eight other photographic positions, including two retained Chapter 8 figures.')
s=s.replace('- [x] Integrate 25 provisional visual positions, including documentary figures and source excerpts, where they aid the reader.','- [x] Integrate 41 visual positions, including photographs, maps, graphs, diagrams and source excerpts.')
s=s.replace('- [ ] Identify any indispensable missing image functions after the provisional sequence exists.','- [x] Assess remaining image functions after sequencing: wider working ranch landscape coverage is limited, but no indispensable missing image blocks this proof.')
p.write_text(s,encoding='utf-8')
first_paragraph('manuscript/argument-and-outline.md','**Length and format clarified:**','**Length and format clarified:** On September 28 the author made content more important than the earlier 40,000–60,000-word ambition. The current book has 31,494 main-text words and a developed eighteen-photograph sequence. [Revision 4](B:/Meridian/Cuervo/manuscript/book-revision-04/cuervo-complete-manuscript.md) is the current text; [book architecture](B:/Meridian/Cuervo/manuscript/book-architecture.md) records the broader brief. The scope remains the whole settlement with selected close-ups.')
first_paragraph('manuscript/argument-and-outline.md','The eight-chapter draft and first repetition/continuity edit are complete.','The eight-chapter draft, voice/compression edit, analytical visuals and expanded photographic sequence are complete. Use [revision 4](B:/Meridian/Cuervo/manuscript/book-revision-04/photographic-review.md) as the baseline. Remaining work: focused scholarly comparison, publication fact-check and apparatus, outside critique, final color treatment and production design. Further acquisition serves a named passage or caption.')
print(json.dumps({'pages':pages,'photographs':18,'photo_positions':len(rows),'original_hashes_verified':len(photos['assets']),'status':'photographic review and project pointers updated'},indent=2))
