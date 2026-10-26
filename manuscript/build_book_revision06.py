"""Typeset the edited eight-chapter manuscript with continuous pagination."""
from pathlib import Path
import re,json,hashlib,html
from PIL import Image as PILImage,ImageOps
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,KeepTogether,Image
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
from build_chapters02_03_pdf import (ROOT,W,H,MARGIN,TOP,BOTTOM,NAVY,INK,GRAY,tracked,markup,
    body_style,lead_style,head_style,note_style,caption_style,figure_title,figure_block)
from source_plates import plate
from book_photos_revision04 import opener as photo_opener, plate as photo_plate
from book_visuals_revision03 import figure as new_figure, SPECS as NEW_FIGURES
from build_chapter04_pdf import plate as plate4
from build_chapter05_pdf import figure as figure5
from build_chapter06_pdf import figure as figure6
from build_chapter07_pdf import figure as figure7
from build_chapter08_pdf import figure as figure8
from edit_book_revision01 import words
from edit_book_revision05 import typography
from finalize_book_revision06 import remap_refs
from book_visuals_revision06 import figure as revised_figure, KEYS as REVISED_FIGURES
from revision06_backmatter import credits, tidy_legacy
REV=ROOT/'manuscript/book-revision-06'
QA=ROOT/'tmp/pdfs/book-revision06';QA.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-06.pdf'
TITLES=['Reading Cuervo','Why a town here?','The business of ranch country','Keeping a town working','People across places','Changing the connections','Explaining the cumulative decline','What remained']
NUMBERS=['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT']
label=ParagraphStyle('BookLabel',fontName='Label',fontSize=9,leading=13,textColor=HexColor(NAVY),spaceAfter=14)
opener=ParagraphStyle('BookChapterTitle',fontName='GaramondItalic',fontSize=40,leading=46,textColor=HexColor(NAVY),spaceAfter=25)

def running(c,doc):
    if doc.page==1:return
    c.saveState();tracked(c,'CUERVO',48,778,7.2,spacing=1.5)
    tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    c.setStrokeColor(HexColor('#c9c2b8'));c.setLineWidth(.4);c.line(48,53,528,53)
    tracked(c,'COMPLETE READING PROOF / REVISION 6',48,36,6.7,spacing=.9)
    c.setFillColor(HexColor(INK));c.setFont('Label',9);c.drawRightString(528,35,str(doc.page));c.restoreState()

class BookDoc(BaseDocTemplate):
    def beforeDocument(self):
        self.chapter_pages={};self.figure_pages=[];self.note_pages={};self.backmatter_pages={}
    def afterFlowable(self,flow):
        if hasattr(flow,'book_chapter'):
            n=flow.book_chapter;key=f'chapter{n}'
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f'{n}. {TITLES[n-1]}',key,level=0)
            self.chapter_pages[n]=self.page
            self.notify('TOCEntry',(0,f'{n}. {TITLES[n-1]}',self.page,key))
        if hasattr(flow,'book_figure'):
            self.figure_pages.append({'page':self.page,'figure':flow.book_figure})
            self.canv.bookmarkPage('visual-'+flow.book_figure)
        if hasattr(flow,'book_backmatter'):
            key=flow.book_backmatter
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(flow.getPlainText(),key,level=0)
            self.backmatter_pages[key]=self.page
            self.notify('TOCEntry',(0,flow.getPlainText(),self.page,key))
        if hasattr(flow,'book_notes'):
            self.note_pages[flow.book_notes]=self.page

def fmt(s,n):
    # Parse emphasis inside link labels as well as ordinary prose.
    links=[]
    def emphasis(t):
        return re.sub(r'\*([^*]+)\*',r'<i>\1</i>',html.escape(t))
    def save(m):
        label,url=m.groups();label=emphasis(label)
        if url.startswith('https://'):
            label=f'<link href="{html.escape(url,quote=True)}" color="{NAVY}">{label}</link>'
        links.append(label);return f'LINKPLACEHOLDER{len(links)-1}END'
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',save,s)
    s=emphasis(s)
    s=re.sub(r'\[\^(\d+)\]',lambda m:f'<super><link href="#ch{n}-note{m[1]}" color="{NAVY}">{m[1]}</link></super>',s)
    s=s.replace('</link></super><super><link','</link></super><super>,</super><super><link')
    for i,link in enumerate(links):s=s.replace(f'LINKPLACEHOLDER{i}END',link)
    return s

def append(story,items):
    if story and isinstance(story[-1],PageBreak) and items and isinstance(items[0],PageBreak):items=items[1:]
    story.extend(items)

def figures(n,key):
    if key in REVISED_FIGURES:items=revised_figure(key)
    elif key in NEW_FIGURES:items=new_figure(key)
    elif n==1:items=plate(key,figure_title,caption_style)
    elif n in (2,3):items=figure_block(key)
    else:items={4:plate4,5:figure5,6:figure6,7:figure7,8:figure8}[n](key)
    items=[tidy_legacy(x,n) for x in items]
    src=next((REV/'chapters').glob(f'chapter-{n:02d}-*.md'))
    order=re.findall(r'<!-- FIGURE: ([\w-]+) -->',src.read_text(encoding='utf-8'))
    number=order.index(key)+1
    for i,flow in enumerate(items):
        if isinstance(flow,Paragraph) and re.match(r'Figure \d+\.\d+\.',flow.text):
            text=re.sub(r'^Figure \d+\.\d+\.',f'Figure {n}.{number}.',flow.text)
            items[i]=Paragraph(text,flow.style)
    for flow in items:
        if isinstance(flow,Paragraph):flow.book_figure=f'{n}:{key}';break
    return items


def normalize_flow(flow):
    if isinstance(flow,Paragraph):
        text=typography(flow.text)
        text=text.replace('held PDF', 'PDF').replace('held UNM scans', 'UNM scans').replace('held UNM scan', 'UNM scan')
        text=re.sub(r'(notes? )(\d+)-(\d+)', r'\1\2–\3', text)
        text=text.replace('Sources: held U.S. Census geography and regional audit;', 'Sources: U.S. Census, 2020 Guadalupe County boundary;')
        text=text.replace('chapter notes 26-27', 'chapter notes 26–27')
        new=Paragraph(text,flow.style)
        for k,v in vars(flow).items():
            if k.startswith('book_'):setattr(new,k,v)
        return new
    if isinstance(flow,KeepTogether):
        flow._content=[normalize_flow(x) for x in flow._content]
    return flow

def build():
    story=[Spacer(1,80),Paragraph('MERIDIAN',label),Spacer(1,28),
      Paragraph('Cuervo',ParagraphStyle('BookTitle',fontName='Display',fontSize=76,leading=83,textColor=HexColor(INK))),
      Spacer(1,32),Paragraph('Complete manuscript',opener),Spacer(1,20),
      Paragraph('Photographs by Taylor Osborn',caption_style),Spacer(1,30),
      Paragraph('REVISION 6 / 29 SEPTEMBER 2026',label),
      Paragraph('A complete reading proof of eight chapters. Source notes follow each chapter. Eighteen photographs by Taylor Osborn accompany the text. A consolidated bibliography and photograph credits follow the chapters. Indexing, final color treatment and publication design remain in preparation.',caption_style),PageBreak()]
    story.extend([Paragraph('Contents',opener),Spacer(1,20)])
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('TOCLevel',fontName='Garamond',fontSize=15,leading=20,textColor=HexColor(INK),spaceBefore=18,leftIndent=0,firstLineIndent=0,rightIndent=20)]
    story.extend([toc,Spacer(1,36),Paragraph('The contents and note references are clickable. Pagination is continuous throughout this proof. Main-text word counts exclude headings, captions and source notes.',caption_style),PageBreak()])
    manifest=[];combined=['# Cuervo\n\nComplete manuscript, revision 6. September 29, 2026.\n\nEdited chapter notes, consolidated bibliography and photograph credits. Indexing and final publication design pending.']
    for n,title in enumerate(TITLES,1):
        src=next((REV/'chapters').glob(f'chapter-{n:02d}-*.md'))
        text=src.read_text(encoding='utf-8');body,notes=text.split('\n---\n',1)
        refs=re.findall(r'\[\^(\d+)\]',body);defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
        assert set(refs)==set(defs) and len(defs)==len(set(defs))
        chlabel=Paragraph('CHAPTER '+NUMBERS[n-1],label);chlabel.book_chapter=n
        append(story,[PageBreak(),Spacer(1,56),chlabel,Paragraph(title,opener)])
        story.extend([tidy_legacy(x,n,remap=False) for x in photo_opener(n)])
        story.append(PageBreak());first=True
        clean=re.sub(r'<!--(?! (?:FIGURE|PHOTO):).*?-->','',body,flags=re.S)
        for block in clean.split('\n\n'):
            block=block.strip()
            if not block or block.startswith('# '):continue
            photo=re.fullmatch(r'<!-- PHOTO: ([\w-]+) -->',block)
            if photo:
                append(story,[tidy_legacy(x,n,remap=False) for x in photo_plate(n,photo.group(1))]);continue
            fig=re.fullmatch(r'<!-- FIGURE: ([\w-]+) -->',block)
            if fig:
                append(story,figures(n,fig.group(1)))
            elif block.startswith('## '):story.append(Paragraph(fmt(block[3:],n),head_style))
            else:story.append(Paragraph(fmt(block,n),lead_style if first else body_style));first=False
        h=Paragraph('Source notes',head_style);h.book_notes=n
        append(story,[PageBreak(),Paragraph('CHAPTER '+NUMBERS[n-1],label),h,
          Paragraph('Page references identify the source’s printed pagination unless a PDF page is specified. Calculations and material source limits are identified below.',caption_style)])
        for block in notes.split('\n\n'):
            m=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
            if m:
                num,content=m.groups()
                story.append(KeepTogether([Paragraph(f'<a name="ch{n}-note{num}"/><b>{num}.</b> '+fmt(content,n),note_style)]))
        manifest.append({'chapter':n,'title':title,'body_words':words(body),'notes':len(defs),'references':len(refs),
          'visual_positions':len(re.findall(r'<!-- (?:FIGURE|PHOTO):',body))+1,'source':src.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
        combined.append(re.sub(r'\[\^(\d+)\]',rf'[^ch{n}-\1]',text))
    bibliography=(REV/'bibliography.md').read_text(encoding='utf-8')
    append(story,[PageBreak()])
    h=Paragraph('Sources and bibliography',opener);h.book_backmatter='bibliography';story.append(h)
    for block in bibliography.split('\n\n'):
        if block.startswith('# '):continue
        story.append(Paragraph(fmt(block[3:] if block.startswith('## ') else block,0),head_style if block.startswith('## ') else note_style))
    append(story,[PageBreak()])
    h=Paragraph('Photograph credits',opener);h.book_backmatter='credits';story.append(h)
    credit_flows,credit_markdown=credits()
    story.extend(credit_flows)
    (REV/'photograph-credits.md').write_text(credit_markdown,encoding='utf-8')
    combined.extend([bibliography,credit_markdown])
    story=[normalize_flow(flow) for flow in story]
    doc=BookDoc(str(OUT),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=TOP,bottomMargin=BOTTOM,
        title='Cuervo | Complete manuscript, revision 6',author='Meridian',subject='Eight-chapter reading proof, September 29, 2026')
    frame=Frame(MARGIN,BOTTOM,W-2*MARGIN,H-TOP-BOTTOM,id='normal')
    doc.addPageTemplates(PageTemplate(id='book',frames=[frame],onPage=running));doc.multiBuild(story,maxPasses=5)
    for row in manifest:
        row['opening_page']=doc.chapter_pages[row['chapter']];row['source_notes_page']=doc.note_pages[row['chapter']]
    reader=PdfReader(OUT)
    report={'date':'2026-09-29','pages':len(reader.pages),'body_words':sum(c['body_words'] for c in manifest),
       'notes':sum(c['notes'] for c in manifest),'references':sum(c['references'] for c in manifest),
       'visual_positions':sum(c['visual_positions'] for c in manifest),'author_photographs':18,'chapters':manifest,'figure_pages':doc.figure_pages,
       'backmatter_pages':doc.backmatter_pages,'pdf_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'}
    (REV/'build-manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (REV/'cuervo-complete-manuscript.md').write_text('\n\n---\n\n'.join(combined),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':build()
