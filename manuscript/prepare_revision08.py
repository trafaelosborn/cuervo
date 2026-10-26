"""Prepare the bounded agency-source and illustration revision from Revision 7."""
from pathlib import Path
import shutil, json, hashlib, re
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'manuscript/book-revision-07'
NEW=ROOT/'manuscript/book-revision-08'
assert not NEW.exists(), 'Revision 8 already exists; do not overwrite it.'
(NEW/'chapters').mkdir(parents=True)
protected={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OLD.rglob('*') if p.is_file()}
pdf=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-07.pdf'
protected[pdf.relative_to(ROOT).as_posix()]=hashlib.sha256(pdf.read_bytes()).hexdigest()
(NEW/'revision07-integrity.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
for p in (OLD/'chapters').glob('*.md'):shutil.copy2(p,NEW/'chapters'/p.name)
shutil.copy2(OLD/'bibliography.md',NEW/'bibliography.md')
shutil.copy2(OLD/'revision06-integrity.json',NEW/'revision06-integrity.json')

def chapter(n):return next((NEW/'chapters').glob(f'chapter-{n:02}-*.md'))
def replace(n,old,new):
 p=chapter(n);s=p.read_text(encoding='utf-8');assert s.count(old)==1,(n,old[:90]);p.write_text(s.replace(old,new),encoding='utf-8')
def note(n,num,addition=None,replacement=None):
 p=chapter(n);s=p.read_text(encoding='utf-8');pat=rf'^\[\^{num}\]: .*?(?=\n\n|\Z)';m=re.search(pat,s,re.M|re.S);assert m
 value=f'[^{num}]: '+replacement if replacement else m[0]+' '+addition
 p.write_text(s[:m.start()]+value+s[m.end():],encoding='utf-8')

# Retain existing note identities so the rest of the book's references remain stable.
p=chapter(4);s=p.read_text(encoding='utf-8')
anchor=next(b for b in s.split('\n\n') if b.startswith('The property’s later sale'))
replace(4,anchor,anchor+' The district had begun preparing the property for sale in July 2010; that December, the superintendent reported the survey work complete, with paperwork still pending.[^8]')
note(4,8,addition='Santa Rosa Consolidated Schools, regular board minutes, July 8, 2010, item IX.A (PDF p. 7), and December 9, 2010, item VIII.A (PDF p. 10), supplied September 29, 2026, place the survey within the property-sale process. The July file is incorrectly named July 10; its meeting header gives July 8. Marilyn Dodge, records response of September 29, 2026, p. 2, reports inability to locate other school-property documents; the final teaching date remains unconfirmed.')

replace(6,'The bibliography cites plans dated December 1 of that year.', 'The bibliography cites plans dated December 1 of that year; the original E-Federal Aid Project 114-C title sheet now confirms that approval date.')
note(6,8,addition='New Mexico State Highway Commission, E-Federal Aid Project 114-C, as-built packet, title sheet (PDF p. 2), approved December 1, 1932. The title gives 7.678 project miles, a different extent from the nomination’s 6.9-mile historic segment.')
p=chapter(6);s=p.read_text(encoding='utf-8')
start=s.index('Interstate construction changed another set of connections.')
end=s.index('The NTSB report’s later traffic table',start)
new='''Interstate construction changed another set of connections. The NTSB’s investigation of a 2002 accident near Cuervo dates a nearby highway project to 1963–1965, with approximate limits near mileposts 282.7 and 290.7. The engineering records identify the adjoining Cuervo project as I-040-5(13)291. Its title sheet received state approval on July 15, 1963.[^21]

The Cuervo plans make the intervention visible. The town sheet sets divided carriageways among houses, shops, wells and other structures. It labels Bond and Wiest’s store, a post office, gas pumps and a church. Instructions call for foundations and other features to be removed. These drawings record a built landscape through which the project had to pass. A building label alone does not establish that its former business was still operating.

The interchange plan shows ramps, a crossroad and frontage roads. The sign drawings include a Cuervo exit and a gas-and-food panel. Travelers were given a route into the town, but reaching premises required a different approach. A business could remain accessible while losing the advantage of drivers passing its entrance.

Earlier contraction therefore remains part of the explanation, alongside the interstate’s later intervention. The plans establish the designed changes and clearance instructions. They leave the dates of individual removals, the opening of each connection and the resulting losses of trade to other evidence.[^21]

<!-- FIGURE: dot-town -->

<!-- FIGURE: dot-details -->

<!-- FIGURE: dot-access -->

'''
s=s[:start]+new+s[end:];p.write_text(s,encoding='utf-8')
note(6,21,addition='New Mexico State Highway Commission/State Highway Department, I-040-5(13)291, as-built drawing packet: title (PDF pp. 1 and 166), approved July 15, 1963; town plan/profile (p. 151); Cuervo interchange plan (p. 137); sign locations (p. 117); sign details (p. 114). Figures 6.4–6.6 reproduce these source drawings and enlarged excerpts. Later amendments coexist with survey labels; neither every label nor every removal can be dated from the title alone. Approval is not an opening certificate. The neighboring project’s engineering title reads I-040-5(18)283 (PDF p. 1 of that packet).')

replace(8,'The school property acquired a later owner with a personal connection to the institution. After the 2010 survey, the school board reportedly accepted Flora Page’s purchase offer in September 2012. Her later obituary described schooling in Cuervo and Santa Rosa.[^5] Land transactions continued even though the final date of teaching remained uncertain.', 'The former school property still attracted buyers. In December 2011, the school board chose Flora Page’s $10,250 offer from four bids. It approved the quitclaim deed the following January, with the proceeds earmarked for the band program. Page had attended school in Cuervo and Santa Rosa, according to her later obituary.[^5] The property retained value long after the teaching whose final date remains uncertain.')
note(8,5,replacement='Santa Rosa Consolidated Schools, regular board minutes, December 8, 2011, item IX.A (PDF p. 8): four submitted bids, Flora Page’s highest offer of $10,250 and a 4–1 award vote. January 11, 2012, items VIII.B and IX.C (PDF pp. 9–10): band-program earmark and 5–0 approval of the quitclaim deed. Minutes supplied September 29, 2026. These establish award and deed approval, not an executed conveyance date or receipt of funds. The award predates the September 17, 2012 Route 66 News report cited in earlier editions. Guadalupe County survey C-232 is discussed in Chapter 4, note 8. Marilyn Dodge’s September 29, 2026 response reports no other school-property documents located; the repeated 1958 closure date remains unconfirmed. Chavez Funeral Home, [Flora S. Page obituary, 2023](https://www.chavezfuneralhome.com/obituaries/flora-page), records schooling in Cuervo and Santa Rosa without dates. The bid is stated in nominal dollars, with no cross-year price comparison.')

p=NEW/'bibliography.md';s=p.read_text(encoding='utf-8')
s=s.replace('## Population, agriculture, prices and public records','Santa Rosa Consolidated Schools. Regular board minutes, July 8 and December 9, 2010; December 8, 2011; January 11, 2012. Copies supplied by records custodian Marilyn Dodge, September 29, 2026. Dodge’s final records response of that date describes the search outcome.\n\n## Population, agriculture, prices and public records')
s=s.replace('## Railways and highways','## Railways and highways\n\nNew Mexico State Highway Commission/State Highway Department. E-Federal Aid Project 114-C, title approved December 1, 1932; project I-040-5(13)291, title approved July 15, 1963, as-built drawing packet with later amendments; adjoining project I-040-5(18)283, title sheet. New Mexico Department of Transportation copies supplied September 2026. Specific PDF pages appear in Chapter 6; excerpts retain original drawing marks.')
p.write_text(s,encoding='utf-8')

s=(ROOT/'manuscript/build_book_revision07.py').read_text(encoding='utf-8')
for a,b in [('book-revision-07','book-revision-08'),('book-revision07','book-revision08'),('revision-07.pdf','revision-08.pdf'),('REVISION 7','REVISION 8'),('revision 7','revision 8')]:s=s.replace(a,b)
s=s.replace('from revision07_typography import configure','from book_visuals_revision08 import figure as dot_figure, KEYS as DOT_FIGURES\nfrom revision07_typography import configure')
s=s.replace('    if key in REVISED_FIGURES:items=revised_figure(key)','    if key in DOT_FIGURES:items=dot_figure(key)\n    elif key in REVISED_FIGURES:items=revised_figure(key)')
s=s.replace('items=[tidy_legacy(x,n) for x in items]','items=[tidy_legacy(x,n,remap=key not in DOT_FIGURES) for x in items]')
s=s.replace("doc.addPageTemplates([PageTemplate(id='book'", "plate_frame=Frame(48,BOTTOM,480,H-TOP-BOTTOM,id='plate-frame')\n    doc.addPageTemplates([PageTemplate(id='plate',frames=[plate_frame],onPage=running),PageTemplate(id='book'")
# BaseDocTemplate takes its first template as initial; retain book as the first entry.
s=s.replace("[PageTemplate(id='plate',frames=[plate_frame],onPage=running),PageTemplate(id='book',frames=[frame],onPage=running),PageTemplate(id='notes',frames=[notes_frame],onPage=running)]", "[PageTemplate(id='book',frames=[frame],onPage=running),PageTemplate(id='notes',frames=[notes_frame],onPage=running),PageTemplate(id='plate',frames=[plate_frame],onPage=running)]")
(ROOT/'manuscript/build_book_revision08.py').write_text(s,encoding='utf-8')
s=(ROOT/'manuscript/check_book_revision07.py').read_text(encoding='utf-8')
for a,b in [('book-revision-07','book-revision-08'),('book-revision07','book-revision08'),('revision-07.pdf','revision-08.pdf'),('REVISION 7','REVISION 8')]:s=s.replace(a,b)
s=s.replace("old=json.loads", "protected7=json.loads((REV/'revision07-integrity.json').read_text(encoding='utf-8'))\nfor path,digest in protected7.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Revision 7 changed',path)\nold=json.loads")
(ROOT/'manuscript/check_book_revision08.py').write_text(s,encoding='utf-8')
print('Revision 8 chapters, bibliography, builder and checker prepared.')
