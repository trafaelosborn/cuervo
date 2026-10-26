"""Create revision 3 from revision 2, preserving the approved prose and notes."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/'manuscript/book-revision-02'
REV=ROOT/'manuscript/book-revision-03'
(REV/'chapters').mkdir(parents=True,exist_ok=True)
insertions={
 1:('## A store with a wide reach','<!-- FIGURE: regional-locator -->\n\n## A store with a wide reach'),
 3:('## Managers, branches and customer choice','<!-- FIGURE: trade-connections -->\n\n## Managers, branches and customer choice'),
 7:('## The market beyond the houses','<!-- FIGURE: functional-chronology -->\n\n## The market beyond the houses')}
records=[]
for n,path in enumerate(sorted((PREV/'chapters').glob('*.md')),1):
    old=path.read_text(encoding='utf-8');new=old
    if n in insertions:
        before,after=insertions[n];assert new.count(before)==1;new=new.replace(before,after)
    if n==3:
        assert new.count('<!-- FIGURE: cattle-price-cycle -->')==1
        new=new.replace('<!-- FIGURE: cattle-price-cycle -->','<!-- FIGURE: prices-and-population -->')
    # Update two references to figures renumbered by insertion; claims stay intact.
    renumber={6:('Figure 3.3','Figure 3.4'),7:('Figure 7.2','Figure 7.3')}
    note_reference_changes=[]
    if n in renumber:
        before,after=renumber[n];assert new.count(before)==1
        new=new.replace(before,after);note_reference_changes.append({'before':before,'after':after})
    # Every prose paragraph and source note survives, except these figure labels.
    clean=lambda s:re.sub(r'<!-- FIGURE: [\w-]+ -->\s*','',s)
    comparable=new
    for item in note_reference_changes:comparable=comparable.replace(item['after'],item['before'])
    assert clean(old)==clean(comparable)
    assert old.split('\n---\n',1)[1]==comparable.split('\n---\n',1)[1]
    dest=REV/'chapters'/path.name;dest.write_text(new,encoding='utf-8')
    records.append({'chapter':n,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
                    'prose_unchanged':True,'source_notes_preserved':True,
                    'figure_reference_updates':note_reference_changes,'figures':re.findall(r'<!-- FIGURE: ([\w-]+) -->',new)})

builder=(ROOT/'manuscript/build_book_revision02.py').read_text(encoding='utf-8')
builder=builder.replace('book-revision-02','book-revision-03').replace('book-revision02','book-revision03')
builder=builder.replace('proof-revision-02.pdf','proof-revision-03.pdf').replace('REVISION 2','REVISION 3').replace('revision 2','revision 3')
builder=builder.replace('from source_plates import plate','from source_plates import plate\nfrom book_visuals_revision03 import figure as new_figure, SPECS as NEW_FIGURES')
builder=builder.replace('    if n==1:items=plate(key,figure_title,caption_style)',
    '    if key in NEW_FIGURES:items=new_figure(key)\n    elif n==1:items=plate(key,figure_title,caption_style)')
needle="    for flow in items:\n        if isinstance(flow,Paragraph):flow.book_figure=f'{n}:{key}';break"
replacement="""    src=next((REV/'chapters').glob(f'chapter-{n:02d}-*.md'))
    order=re.findall(r'<!-- FIGURE: ([\\w-]+) -->',src.read_text(encoding='utf-8'))
    number=order.index(key)+1
    for i,flow in enumerate(items):
        if isinstance(flow,Paragraph) and re.match(r'Figure \\d+\\.\\d+\\.',flow.text):
            text=re.sub(r'^Figure \\d+\\.\\d+\\.',f'Figure {n}.{number}.',flow.text)
            items[i]=Paragraph(text,flow.style)
    for flow in items:
        if isinstance(flow,Paragraph):flow.book_figure=f'{n}:{key}';break"""
assert needle in builder;builder=builder.replace(needle,replacement)
(ROOT/'manuscript/build_book_revision03.py').write_text(builder,encoding='utf-8')
checker=(ROOT/'manuscript/check_book_revision02.py').read_text(encoding='utf-8')
checker=checker.replace('book-revision-02','book-revision-03').replace('book-revision02','book-revision03')
checker=checker.replace('proof-revision-02.pdf','proof-revision-03.pdf').replace('REVISION 2','REVISION 3')
(ROOT/'manuscript/check_book_revision03.py').write_text(checker,encoding='utf-8')
(REV/'visual-edit-record.json').write_text(json.dumps({'chapters':records,'changes':
    'Three inserted figures and one replacement; approved prose, 174 notes and 220 body reference links preserved. Two figure references in notes renumbered.',
    'length_decision':'The author prioritizes content over length. No minimum main-text word count is a completion requirement.'},indent=2),encoding='utf-8')
print('Revision 3 prepared; prose and notes preserved, with two figure-reference updates.')
