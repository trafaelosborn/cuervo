"""Build the Chapter 1 reading proof from the editable Markdown manuscript."""
from pathlib import Path
import re
import html
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'manuscript/chapter-01-reading-cuervo.md'
OUTPUT = ROOT / 'output/pdf/cuervo-chapter-01-reading-cuervo.pdf'
QA = ROOT / 'tmp/pdfs/chapter01-draft03'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)
PHOTO = Path('B:/Photos/Raw Collections/2024.03.26 Cuervo NM')
FONTS = Path('C:/Windows/Fonts')
for name, filename in [('Garamond','GARA.TTF'), ('GaramondItalic','GARAIT.TTF'),
                       ('GaramondBold','GARABD.TTF'), ('Display','BASKVILL.TTF'),
                       ('Label','calibri.ttf'), ('LabelBold','calibrib.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS/filename)))
pdfmetrics.registerFontFamily('Garamond', normal='Garamond', bold='GaramondBold',
                             italic='GaramondItalic', boldItalic='GaramondItalic')

NAVY = HexColor('#1b3558')
INK = HexColor('#242528')
GRAY = HexColor('#756e65')
RULE = HexColor('#c9c2b8')
W, H = 576, 816
LEFT, RIGHT, TOP, BOTTOM = 105, 105, 75, 75
TEXT_W = W-LEFT-RIGHT

def normalize(s):
    return s.replace('\u2013','-').replace('\u2014',' - ').replace('\u2011','-')

def markup(s, note=False):
    links = []
    def hold_link(m):
        label, url = m.group(1), m.group(2)
        label = html.escape(normalize(label))
        if url.startswith('https://'):
            value = f'<link href="{html.escape(url, quote=True)}" color="#1b3558">{label}</link>'
        else:
            value = label
        links.append(value)
        return f'LINKPLACEHOLDER{len(links)-1}END'
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', hold_link, s)
    s = html.escape(normalize(s))
    s = re.sub(r'\*([^*]+)\*',r'<i>\1</i>',s)
    s = re.sub(r'\[\^(\d+)\]',r'<super><link href="#note\1" color="#1b3558">\1</link></super>',s)
    for i, value in enumerate(links):
        s = s.replace(f'LINKPLACEHOLDER{i}END',value)
    return s

body_style = ParagraphStyle('Body', fontName='Garamond', fontSize=12.2, leading=16.5,
                            textColor=INK, spaceAfter=8.2, alignment=TA_LEFT,
                            allowWidows=0, allowOrphans=0)
lead_style = ParagraphStyle('Lead', parent=body_style, fontSize=16, leading=21.5,
                            spaceAfter=19, textColor=NAVY)
head_style = ParagraphStyle('Section', fontName='GaramondItalic', fontSize=23,
                            leading=28, textColor=NAVY, spaceBefore=23,
                            spaceAfter=13, keepWithNext=True)
note_style = ParagraphStyle('Note', fontName='Garamond', fontSize=10.1,
                            leading=13.3, textColor=INK, spaceAfter=9,
                            allowWidows=0, allowOrphans=0)
caption_style = ParagraphStyle('Caption', fontName='Label', fontSize=8.3,
                               leading=11.1, textColor=GRAY, spaceAfter=18)

def tracked(c, text, x, y, size=8, color=GRAY, spacing=1.6):
    obj=c.beginText(x,y);obj.setFont('Label',size);obj.setFillColor(color)
    obj.setCharSpace(spacing);obj.textLine(text);c.drawText(obj)

def draw_photo(c, filename, x, y, width):
    with PILImage.open(PHOTO/filename) as im:
        height = width*im.height/im.width
        # Preserve the original JPEG stream. No crop, retouching or color change.
        c.drawImage(str(PHOTO/filename),x,y,width=width,height=height,mask='auto')
    return height

def cover(c, doc):
    c.saveState()
    c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    tracked(c,'CUERVO',48,778)
    tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    tracked(c,'CHAPTER ONE',48,735,8,NAVY,2.1)
    c.setFillColor(INK);c.setFont('Display',51);c.drawString(45,673,'Reading')
    c.setFillColor(NAVY);c.setFont('GaramondItalic',62);c.drawString(47,617,'Cuervo')
    draw_photo(c,'IMG_7453.JPG',48,229,480)
    tracked(c,'A BUILDING AND ITS SURROUNDINGS',48,215,7.1,spacing=1.1)
    c.setStrokeColor(NAVY);c.setLineWidth(.6);c.line(48,187,528,187)
    p=Paragraph('How a town took shape, and why its services fell away.',
                ParagraphStyle('Deck',fontName='GaramondItalic',fontSize=20,
                               leading=24,textColor=NAVY))
    _,h=p.wrap(360,80);p.drawOn(c,48,158-h)
    tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
    tracked(c,'READING PROOF / DRAFT 3 / 24 SEPTEMBER 2026',48,45,6.7,spacing=1)
    c.restoreState()

def running(c, doc):
    c.saveState()
    c.setStrokeColor(RULE);c.setLineWidth(.4);c.line(48,768,W-48,768)
    tracked(c,'CUERVO',48,779,7,spacing=1.5)
    title='READING CUERVO'
    c.setFont('Label',7.5);c.setFillColor(GRAY);c.drawRightString(W-48,779,title)
    tracked(c,'CHAPTER ONE',48,40,6.6,spacing=1.3)
    c.setFont('Garamond',10);c.drawRightString(W-48,39,str(doc.page))
    c.restoreState()

class ReadingDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name=='Section':
            if flowable.getPlainText()=='Working source notes':
                self.in_notes=True

text=SOURCE.read_text(encoding='utf-8')
text=re.sub(r'<!--.*?-->','',text,flags=re.S)
body, notes = text.split('\n---\n',1)
blocks=[b.strip() for b in body.split('\n\n') if b.strip() and not b.startswith('# Chapter') and not b.startswith('# Reading')]
story=[Spacer(1,H-TOP-BOTTOM-15),PageBreak()]
first=True
for block in blocks:
    if block.startswith('## '):
        story.append(Paragraph(markup(block[3:]),head_style))
    else:
        story.append(Paragraph(markup(block),lead_style if first else body_style))
        first=False
story.append(PageBreak())
story.append(Paragraph('Working source notes',head_style))
story.append(Paragraph('Draft 3 / September 24, 2026. These working notes give sources, links and limits on the evidence. Cover photograph: Taylor Osborn\u2019s Cuervo collection, IMG_7453. Its building identity and exact capture date have not been established.',caption_style))
for block in notes.split('\n\n'):
    match=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
    if match:
        num, content=match.groups()
        story.append(KeepTogether([Paragraph(f'<a name="note{num}"/><b>{num}.</b> '+markup(content),note_style)]))

doc=ReadingDoc(str(OUTPUT),pagesize=(W,H),leftMargin=LEFT,rightMargin=RIGHT,
               topMargin=TOP,bottomMargin=BOTTOM,title='Cuervo | Chapter 1: Reading Cuervo',
               author='Meridian',subject='Chapter 1, draft 3: accessibility revision and air conditioning')
doc.build(story,onFirstPage=cover,onLaterPages=running)
reader=PdfReader(str(OUTPUT))
report={'output':str(OUTPUT),'page_count':len(reader.pages),
        'body_words':len(re.sub(r'\[\^\d+\]','', '\n'.join(blocks)).split()),
        'page_word_counts':[len((p.extract_text() or '').split()) for p in reader.pages],
        'photos':[str(PHOTO/'IMG_7453.JPG')],
        'visual_review':'pending'}
(QA/'build_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
