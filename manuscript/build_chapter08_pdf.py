"""Build Chapter 8 and expose its figures for the integrated manuscript proof."""
from pathlib import Path
import re,json,hashlib
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from pypdf import PdfReader
from build_chapters02_03_pdf import (ROOT,W,H,MARGIN,TOP,BOTTOM,NAVY,INK,GRAY,tracked,markup,running_for,
    body_style,lead_style,head_style,note_style,caption_style,figure_title)
QA=ROOT/'tmp/pdfs/chapter08-draft01'; QA.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'manuscript/figures/chapter08'
SRC=ROOT/'manuscript/chapter-08-what-remained.md'
OUT=ROOT/'output/pdf/cuervo-chapter-08-what-remained.pdf'
SPEC={'number':8,'word':'EIGHT','title':'What remained'}
label_style=ParagraphStyle('PlateLabel8',fontName='Label',fontSize=8.5,leading=11,textColor=HexColor(NAVY),spaceAfter=8)

def cover(c,doc):
    c.saveState(); c.setFillColor(white); c.rect(0,0,W,H,fill=1,stroke=0)
    tracked(c,'CUERVO',48,778); tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    tracked(c,'CHAPTER EIGHT',48,726,8,NAVY,2.1)
    c.setFont('Display',62);c.setFillColor(HexColor(INK));c.drawString(45,650,'What')
    c.setFont('GaramondItalic',72);c.setFillColor(HexColor(NAVY));c.drawString(45,565,'remained')
    p=Paragraph('Working land, enduring connections and the limits of a town\'s disappearance.',
      ParagraphStyle('Deck8',fontName='GaramondItalic',fontSize=20,leading=25,textColor=HexColor(NAVY)))
    _,height=p.wrap(410,90);p.drawOn(c,48,428-height)
    c.setStrokeColor(HexColor(NAVY));c.setLineWidth(.6);c.line(48,316,528,316)
    for i,(year,label) in enumerate([('2013','The lot grid in a later land exchange'),('2025','Cuervo appears in parish accounts'),('2026','A documented ranching operation')]):
        yy=280-i*44;c.setFont('GaramondItalic',19);c.setFillColor(HexColor(NAVY));c.drawString(48,yy,year)
        c.setFont('Label',10.3);c.setFillColor(HexColor(INK));c.drawString(125,yy+1,label)
    p=Paragraph('Different kinds of persistence: production, ownership, institutional affiliation and physical fabric.',caption_style)
    _,height=p.wrap(430,70);p.drawOn(c,48,132-height)
    tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
    tracked(c,'READING PROOF / DRAFT 1 / 28 SEPTEMBER 2026',48,45,6.7,spacing=1)
    c.restoreState()

def pic(name,width):
    p=FIG/f'{name}.png'
    with PILImage.open(p) as im:height=width*im.height/im.width
    image=Image(str(p),width=width,height=height);image.hAlign='CENTER';return image

def figure(key):
    if key=='church':
        title='An institutional connection remained'
        items=[Paragraph('ST. ROSE OF LIMA / 21 DECEMBER 2025',label_style),Spacer(1,8),
            pic('collection',250),Spacer(1,24),pic('missions',330)]
        caption='Figure 8.1. Two excerpts from the parish bulletin: collection report on PDF p. 2 and mission list on p. 3. Surrounding material is omitted. The financial entry identifies Cuervo by name, while the list places Santo Niño within the parish. Neither supplies local attendance, event venue or service frequency. Chapter notes 8-9.'
    elif key=='road':
        title='Two levels in the same landscape'
        items=[Spacer(1,24),pic('IMG_7385',460),Spacer(1,18)]
        caption='Figure 8.2. Road embankment and culvert, Cuervo photographic collection. The image shows the road\'s level relative to adjoining ground; it does not establish a construction date or a business effect. Photograph: Taylor Osborn, IMG_7385. No exact capture date is assigned. Chapter note 12.'
    elif key=='fabric':
        title='The material that survived'
        items=[pic('IMG_7456',330)]
        caption='Figure 8.3. Wall opening and visible interior fabric, Cuervo photographic collection. The former use and proprietor are unassigned. Condition at the time of photography does not date the end of occupation. Photograph: Taylor Osborn, IMG_7456. Orientation corrected; no retouching. Chapter note 12.'
    else:raise ValueError(key)
    return [PageBreak(),Paragraph(title,figure_title),Spacer(1,8),*items,Spacer(1,15),Paragraph(caption,caption_style),PageBreak()]

def build():
    text=SRC.read_text(encoding='utf-8');body,notes=text.split('\n---\n',1)
    refs=re.findall(r'\[\^(\d+)\]',body);defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    assert defs==list(dict.fromkeys(refs))==[str(i+1) for i in range(len(defs))]
    missing=[p for p in re.findall(r'\]\((B:/[^)]+)\)',text) if not Path(p).exists()];assert not missing,missing
    blocks=[b.strip() for b in body.split('\n\n') if b.strip() and not b.startswith('# ')]
    story=[Spacer(1,H-TOP-BOTTOM-15),PageBreak()];first=True
    for block in blocks:
        fig=re.fullmatch(r'<!-- FIGURE: ([\w-]+) -->',block)
        if fig:
            items=figure(fig.group(1))
            if isinstance(story[-1],PageBreak):items=items[1:]
            story.extend(items)
        elif block.startswith('## '):story.append(Paragraph(markup(block[3:]),head_style))
        else:story.append(Paragraph(markup(block),lead_style if first else body_style));first=False
    story.extend([PageBreak(),Paragraph('Working source notes',head_style),Paragraph('Draft 1 / September 28, 2026. Dated observations of production, property and institutions, with photographic provenance. Prior chapter findings retain their original limits.',caption_style)])
    for block in notes.split('\n\n'):
        m=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
        if m:
            n,content=m.groups();story.append(KeepTogether([Paragraph(f'<a name="note{n}"/><b>{n}.</b> '+markup(content),note_style)]))
    doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=TOP,bottomMargin=BOTTOM,
      title='Cuervo | Chapter 8: What remained',author='Meridian',subject='Chapter 8, draft 1, September 28, 2026')
    doc.build(story,onFirstPage=cover,onLaterPages=running_for(SPEC))
    reader=PdfReader(OUT);plain=re.sub(r'<!--.*?-->','',body,flags=re.S);plain=re.sub(r'^#+.*$','',plain,flags=re.M)
    report={'chapter':8,'body_words':len(re.sub(r'\[\^\d+\]','',plain).split()),'pages':len(reader.pages),
       'note_definitions':len(defs),'note_references':len(refs),'figure_positions':3,'missing_local_links':missing,
       'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/'chapter-08-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':build()
