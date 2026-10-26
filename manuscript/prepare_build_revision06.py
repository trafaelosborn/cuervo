"""Create an isolated Revision 6 typesetter from the established proof design."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'manuscript/build_book_revision05.py'
s=p.read_text(encoding='utf-8').replace('book-revision-05','book-revision-06').replace('book-revision05','book-revision06').replace('revision-05.pdf','revision-06.pdf').replace('REVISION 5','REVISION 6').replace('revision 5','revision 6')
s=s.replace('from edit_book_revision05 import typography','from edit_book_revision05 import typography\nfrom finalize_book_revision06 import remap_refs\nfrom book_visuals_revision06 import figure as revised_figure, KEYS as REVISED_FIGURES\nfrom revision06_backmatter import credits, tidy_legacy')
s=s.replace('self.chapter_pages={};self.figure_pages=[];self.note_pages={}','self.chapter_pages={};self.figure_pages=[];self.note_pages={};self.backmatter_pages={}')
s=s.replace("self.figure_pages.append({'page':self.page,'figure':flow.book_figure})", "self.figure_pages.append({'page':self.page,'figure':flow.book_figure})\n            self.canv.bookmarkPage('visual-'+flow.book_figure)\n        if hasattr(flow,'book_backmatter'):\n            key=flow.book_backmatter\n            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(flow.getPlainText(),key,level=0)\n            self.backmatter_pages[key]=self.page\n            self.notify('TOCEntry',(0,flow.getPlainText(),self.page,key))")
a=s.index('def fmt(');z=s.index('def append(',a)
s=s[:a]+'''def fmt(s,n):
    # Parse emphasis inside link labels as well as ordinary prose.
    links=[]
    def emphasis(t):
        return re.sub(r'\\*([^*]+)\\*',r'<i>\\1</i>',html.escape(t))
    def save(m):
        label,url=m.groups();label=emphasis(label)
        if url.startswith('https://'):
            label=f'<link href="{html.escape(url,quote=True)}" color="{NAVY}">{label}</link>'
        links.append(label);return f'LINKPLACEHOLDER{len(links)-1}END'
    s=re.sub(r'\\[([^\\]]+)\\]\\(([^)]+)\\)',save,s)
    s=emphasis(s)
    s=re.sub(r'\\[\\^(\\d+)\\]',lambda m:f'<super><link href="#ch{n}-note{m[1]}" color="{NAVY}">{m[1]}</link></super>',s)
    s=s.replace('</link></super><super><link','</link></super><super>,</super><super><link')
    for i,link in enumerate(links):s=s.replace(f'LINKPLACEHOLDER{i}END',link)
    return s

''' + s[z:]
s=s.replace("if key in NEW_FIGURES:items=new_figure(key)","if key in REVISED_FIGURES:items=revised_figure(key)\n    elif key in NEW_FIGURES:items=new_figure(key)")
s=s.replace("    src=next((REV/'chapters').glob(f'chapter-{n:02d}-*.md'))", "    items=[tidy_legacy(x,n) for x in items]\n    src=next((REV/'chapters').glob(f'chapter-{n:02d}-*.md'))",1)
s=s.replace("        text=text.replace('Chapter 5, notes 1-4.', 'Chapter 5, notes 2–4.')\n",'')
s=s.replace('Final bibliography, index, color treatment and publication design remain in preparation.','A consolidated bibliography and photograph credits follow the chapters. Indexing, final color treatment and publication design remain in preparation.')
s=s.replace('Reader-facing chapter notes; final bibliography, index and publication design pending.','Edited chapter notes, consolidated bibliography and photograph credits. Indexing and final publication design pending.')
s=s.replace('story.extend(photo_opener(n))','story.extend([tidy_legacy(x,n,remap=False) for x in photo_opener(n)])')
s=s.replace('append(story,photo_plate(n,photo.group(1)))','append(story,[tidy_legacy(x,n,remap=False) for x in photo_plate(n,photo.group(1))])')
s=s.replace("                if n in (1,6):\n                    assert all(isinstance(p,Paragraph) for p in story[-3:])\n                    story[-3:]=[KeepTogether(story[-3:])]\n",'')
s=s.replace("                if (n==7 and fig.group(1)=='support') or (n==4 and fig.group(1)=='doctor-support'):\n                    assert all(isinstance(p,Paragraph) for p in story[-2:])\n                    story[-2:]=[KeepTogether(story[-2:])]\n",'')
s=s.replace("        if n in (3,6):\n            assert all(isinstance(p,Paragraph) for p in story[-3:])\n            story[-3:]=[KeepTogether(story[-3:])]\n",'')
insertion='''    bibliography=(REV/'bibliography.md').read_text(encoding='utf-8')
    append(story,[PageBreak()])
    h=Paragraph('Sources and bibliography',opener);h.book_backmatter='bibliography';story.append(h)
    for block in bibliography.split('\\n\\n'):
        if block.startswith('# '):continue
        story.append(Paragraph(fmt(block[3:] if block.startswith('## ') else block,0),head_style if block.startswith('## ') else note_style))
    append(story,[PageBreak()])
    h=Paragraph('Photograph credits',opener);h.book_backmatter='credits';story.append(h)
    credit_flows,credit_markdown=credits()
    story.extend(credit_flows)
    (REV/'photograph-credits.md').write_text(credit_markdown,encoding='utf-8')
    combined.extend([bibliography,credit_markdown])
'''
s=s.replace('    story=[normalize_flow(flow) for flow in story]',insertion+'    story=[normalize_flow(flow) for flow in story]')
s=s.replace("'pdf_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'", "'backmatter_pages':doc.backmatter_pages,'pdf_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'")
(ROOT/'manuscript/build_book_revision06.py').write_text(s,encoding='utf-8')
print('Revision 6 builder prepared.')
