"""Place the selected photographs without changing the approved argument."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
PREV=ROOT/'manuscript/book-revision-03';REV=ROOT/'manuscript/book-revision-04'
(REV/'chapters').mkdir(parents=True,exist_ok=True)
insertions={
 1:('## What the buildings can show','window-inscription'),
 2:('## Competing expectations for the land','entrances'),
 4:('## Paying for a doctor to be there','building-fabric'),
 5:('## A regional center that persisted','domestic-interiors'),
 6:('## Losing a passenger stop','road-and-ground'),
 7:('## A sequence with several causes','rooms-and-structure')}
record=[]
for n,path in enumerate(sorted((PREV/'chapters').glob('*.md')),1):
    old=path.read_text(encoding='utf-8');new=old
    if n in insertions:
        anchor,key=insertions[n];assert old.count(anchor)==1
        new=new.replace(anchor,f'<!-- PHOTO: {key} -->\n\n'+anchor)
    assert re.sub(r'<!-- PHOTO: [\w-]+ -->\s*','',new)==old
    dest=REV/'chapters'/path.name;dest.write_text(new,encoding='utf-8')
    record.append({'chapter':n,'prior_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'new_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'prose_and_notes_unchanged':True,
        'new_photo_marker':insertions.get(n,(None,None))[1]})
s=(ROOT/'manuscript/build_book_revision03.py').read_text(encoding='utf-8')
s=s.replace('book-revision-03','book-revision-04').replace('book-revision03','book-revision04')
s=s.replace('proof-revision-03.pdf','proof-revision-04.pdf').replace('REVISION 3','REVISION 4').replace('revision 3','revision 4')
s=s.replace('from source_plates import plate','from source_plates import plate\nfrom book_photos_revision04 import opener as photo_opener, plate as photo_plate')
a=s.index('        if n==1:\n            photo=Path(');b=s.index('        story.append(PageBreak());first=True',a)
s=s[:a]+'        story.extend(photo_opener(n))\n'+s[b:]
s=s.replace("<!--(?! FIGURE:).*?-->","<!--(?! (?:FIGURE|PHOTO):).*?-->")
s=s.replace("            fig=re.fullmatch", "            photo=re.fullmatch(r'<!-- PHOTO: ([\\w-]+) -->',block)\n            if photo:\n                append(story,photo_plate(n,photo.group(1)));continue\n            fig=re.fullmatch")
s=s.replace("            if photo:\n                append", "            if photo:\n                if n in (1,6):\n                    assert all(isinstance(p,Paragraph) for p in story[-3:])\n                    story[-3:]=[KeepTogether(story[-3:])]\n                append")
s=s.replace("                if n==7 and fig.group(1)=='support':", "                if (n==7 and fig.group(1)=='support') or (n==4 and fig.group(1)=='doctor-support'):")
s=s.replace("len(re.findall(r'<!-- FIGURE:',body))+(1 if n==1 else 0)","len(re.findall(r'<!-- (?:FIGURE|PHOTO):',body))+1")
s=s.replace("Paragraph('Complete manuscript',opener),Spacer(1,70),", "Paragraph('Complete manuscript',opener),Spacer(1,20),\n      Paragraph('Photographs by Taylor Osborn',caption_style),Spacer(1,30),")
s=s.replace('The final bibliography, index, photographic sequence and publication design remain in preparation.',
 'Eighteen photographs by Taylor Osborn accompany the text. Final bibliography, index, color treatment and publication design remain in preparation.')
s=s.replace("'visual_positions':sum(c['visual_positions'] for c in manifest),", "'visual_positions':sum(c['visual_positions'] for c in manifest),'author_photographs':18,")
(ROOT/'manuscript/build_book_revision04.py').write_text(s,encoding='utf-8')
s=(ROOT/'manuscript/check_book_revision03.py').read_text(encoding='utf-8')
s=s.replace('book-revision-03','book-revision-04').replace('book-revision03','book-revision04')
s=s.replace('proof-revision-03.pdf','proof-revision-04.pdf').replace('REVISION 3','REVISION 4')
(ROOT/'manuscript/check_book_revision04.py').write_text(s,encoding='utf-8')
(REV/'photographic-edit-record.json').write_text(json.dumps({'changes':'Seven added chapter-opening photographs and six new picture pages containing eight more photographs. Three prior photographs retained. Prose, notes and figure references unchanged.','chapters':record},indent=2),encoding='utf-8')
print('Revision 4 prepared. All eight chapter bodies and notes preserved.')
