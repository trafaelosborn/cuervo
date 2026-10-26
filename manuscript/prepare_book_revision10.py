"""Create isolated Revision 10 build and graphics code from preserved layouts."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'manuscript'

builder=(M/'build_book_revision09.py').read_text(encoding='utf-8')
for old,new in [('book-revision-09','book-revision-10'),('book-revision09','book-revision10'),('revision-09.pdf','revision-10.pdf'),('REVISION 9','REVISION 10'),('revision 9','revision 10'),('29 SEPTEMBER 2026','2 OCTOBER 2026'),('September 29, 2026','October 2, 2026'),('2026-09-29','2026-10-02')]:
    builder=builder.replace(old,new)
builder=builder.replace('from revision09_captions import edit_figure','from revision09_captions import edit_figure\nfrom revision10_visuals import revise_figure')
builder=builder.replace('items=edit_figure(items,key)','items=revise_figure(edit_figure(items,key),key)')
builder=builder.replace('The contents and note references are clickable. Pagination is continuous throughout this proof. Main-text word counts exclude headings, captions and source notes.','Contents and note references are clickable. Distances use kilometers (miles); elevations use meters (feet). Original source-image lettering and highway milepost identifiers retain source units.')
(M/'build_book_revision10.py').write_text(builder,encoding='utf-8')
check=(M/'check_book_revision09.py').read_text(encoding='utf-8')
for old,new in [('book-revision-09','book-revision-10'),('book-revision09','book-revision10'),('revision-09.pdf','revision-10.pdf'),('REVISION 9','REVISION 10')]:check=check.replace(old,new)
check=check.replace("old=json.loads((ROOT/'manuscript/book-revision-05/build-manifest.json')", "protected9=json.loads((REV/'revision09-integrity.json').read_text(encoding='utf-8'))\nfor path,digest in protected9.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Revision 9 changed',path)\nold=json.loads((ROOT/'manuscript/book-revision-05/build-manifest.json')")
(M/'check_book_revision10.py').write_text(check,encoding='utf-8')

locator=(M/'build_visual_revision03.py').read_text(encoding='utf-8').split('# 2. Schematic connections.')[0]
locator=locator.replace('manuscript/figures/book-revision03','manuscript/figures/book-revision10').replace("'date':'2026-09-28'","'date':'2026-10-02'")
start=locator.index('ax.plot([28,68],[-51,-51]')
end=locator.index("fig.text(.075,.332",start)
locator=locator[:start]+'''# Separate exact scale bars: kilometers above, miles below.
for y,span,unit,mid in [(-47,40,'km',20),(-61,25*1.609344,'mi',12.5)]:
    ax.plot([28,28+span],[y,y],color=NAVY,lw=1.4)
    for x in [28,28+span/2,28+span]:ax.plot([x,x],[y-1.5,y+1.5],color=NAVY,lw=1)
    for x,s in [(28,'0'),(28+span/2,f'{mid:g}'),(28+span,f'{mid*2:g} {unit}')]:
        ax.text(x,y+4,s,ha='center',fontsize=10,color=GRAY)
''' +locator[end:]
locator=locator.replace("'17 miles'","'27 km (17 mi)'").replace("'42 miles'","'68 km (42 mi)'")
locator += "\nmanifest['conversion']={'kilometers_per_mile':1.609344,'rail_km_exact':{'Santa Rosa-Cuervo':17*1.609344,'Cuervo-Tucumcari':42*1.609344},'display':'Whole kilometers, with original whole miles retained'}\n(OUT/'locator-sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')\n"
(M/'build_revision10_locator.py').write_text(locator,encoding='utf-8')

journeys=(M/'build_chapter06_assets.py').read_text(encoding='utf-8').split("save(fig,'journeys')")[0]+"save(fig,'journeys')\n"
journeys=journeys.replace('manuscript/figures/chapter06','manuscript/figures/book-revision10')
journeys=journeys.replace("EV=ROOT/'research_evidence/chapter06_2026-09-28';EV.mkdir(parents=True,exist_ok=True)","")
journeys=journeys.replace('Tucumcari / 42 railway miles','Tucumcari / 68 km (42 mi) by rail').replace('Santa Rosa / 17 railway miles','Santa Rosa / 27 km (17 mi) by rail')
journeys += "(OUT/'journey-sources.json').write_text(json.dumps({'date':'2026-10-02','inputs':manifest,'journey_minutes':trip,'kilometers_per_mile':1.609344,'distance_rounding':'Nearest whole kilometer; original whole-mile distances retained'},indent=2),encoding='utf-8')\n"
(M/'build_revision10_journeys.py').write_text(journeys,encoding='utf-8')
print('Isolated builder, checker and two graphics scripts prepared.')
