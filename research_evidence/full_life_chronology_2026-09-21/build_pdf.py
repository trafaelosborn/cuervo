"""Typeset the curated chronology; keep the JSON/Markdown as the evidence master."""
from pathlib import Path
import html, json, re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, CondPageBreak,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'research_evidence/full_life_chronology_2026-09-21.md'
OUT = ROOT / 'output/pdf/cuervo_full_life_chronology_2026-09-21.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
FONTS = ROOT / 'tmp/deep_dive/python_deps/matplotlib/mpl-data/fonts/ttf'
for family, base in [('Body', 'DejaVuSerif'), ('Sans', 'DejaVuSans')]:
    suffixes = {
        '': '', 'Bold': '-Bold',
        'Italic': '-Italic' if family == 'Body' else '-Oblique',
        'BoldItalic': '-BoldItalic' if family == 'Body' else '-BoldOblique',
    }
    for style, suffix in suffixes.items():
        pdfmetrics.registerFont(TTFont(family + style, str(FONTS / (base + suffix + '.ttf'))))
    pdfmetrics.registerFontFamily(family, normal=family, bold=family+'Bold',
                                italic=family+'Italic', boldItalic=family+'BoldItalic')

INK = colors.HexColor('#25373B')
TEAL = colors.HexColor('#24645C')
GOLD = colors.HexColor('#A16335')
PALE = colors.HexColor('#F0F4F2')
LINE = colors.HexColor('#CCD8D3')
WIDTH = 516
styles = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=9.7, leading=14.2,
                           textColor=INK, spaceAfter=9, splitLongWords=True),
    'h2': ParagraphStyle('h2', fontName='SansBold', fontSize=16, leading=20,
                         textColor=TEAL, spaceBefore=7, spaceAfter=13, keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='SansBold', fontSize=11.2, leading=15,
                         textColor=INK, spaceBefore=12, spaceAfter=7, keepWithNext=True),
    'cell': ParagraphStyle('cell', fontName='Sans', fontSize=8.1, leading=11.25,
                           textColor=INK, splitLongWords=True),
    'headcell': ParagraphStyle('headcell', fontName='SansBold', fontSize=8.2,
                               leading=11, textColor=colors.white),
    'small': ParagraphStyle('small', fontName='Sans', fontSize=8.3, leading=12,
                            textColor=INK, spaceAfter=8),
    'bullet': ParagraphStyle('bullet', fontName='Body', fontSize=9.7, leading=14.2,
                             textColor=INK, spaceAfter=8, leftIndent=11, firstLineIndent=-9),
    'source': ParagraphStyle('source', fontName='Sans', fontSize=8.5, leading=12.2,
                             textColor=INK, spaceAfter=11),
}

def normalize(text):
    return (text.replace('\u2014', ' - ').replace('\u2013', '-')
            .replace('\u2011', '-').replace('\u2212', '-').replace('\u00a0', ' '))

def inline(text):
    text = html.escape(normalize(text), quote=False)
    def link(match):
        label, url = match.group(1), html.unescape(match.group(2))
        if url.startswith('https://'):
            return f'<a href="{html.escape(url, quote=True)}" color="#24645C">{label}</a>'
        return label  # Local source paths remain usable in the Markdown and sources.json.
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Sans">\1</font>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)

class ResearchDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'h2':
            title = flowable.getPlainText()
            key = 'section_' + re.sub(r'\W+', '_', title)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, 0)

def decorate(canv, doc):
    canv.saveState()
    canv.setFillColor(TEAL)
    canv.setFont('Sans', 7.4)
    if doc.page > 1:
        canv.drawString(48, 765, 'CUERVO  |  FORMATION, CHANGING FUNCTIONS AND DECLINE')
        canv.setStrokeColor(LINE)
        canv.line(48, 755, 564, 755)
    canv.drawString(48, 27, 'September 21, 2026  |  Source-based working chronology')
    canv.drawRightString(564, 27, str(doc.page))
    canv.restoreState()

doc = ResearchDoc(str(OUT), pagesize=(612, 792), leftMargin=48, rightMargin=48,
                  topMargin=51, bottomMargin=47,
                  title='Cuervo: Formation, Changing Functions and Decline',
                  author='Research prepared for Taylor Osborn',
                  subject='Full-life chronology, business register and source assessment, September 21, 2026')
events = json.loads((HERE/'chronology.json').read_text(encoding='utf-8'))
entities = json.loads((HERE/'business_register.json').read_text(encoding='utf-8'))
story = [Spacer(1, 40), Paragraph('THE CUERVO MONOGRAPH / RESEARCH', ParagraphStyle(
    'eyebrow', fontName='SansBold', fontSize=10, textColor=GOLD, spaceAfter=23)),
    Paragraph('Formation,<br/>changing functions<br/>and decline', ParagraphStyle(
        'title', fontName='SansBold', fontSize=32, leading=38, textColor=INK, spaceAfter=22)),
    Paragraph("Following Cuervo from its beginnings around 1900<br/>through the functions that survive today.",
              ParagraphStyle('subtitle', fontName='Body', fontSize=12.2, leading=19,
                             textColor=TEAL, spaceAfter=23)),
    Paragraph('Prepared for Taylor Osborn<br/>September 21, 2026', styles['small']), Spacer(1, 17)]

cover = ("The early record shows a town that already traded livestock, supported merchants "
         "and drew families to its school. Investment, withdrawal and reopening occurred "
         "side by side. The task is to explain how those functions changed, and why enough "
         "of them were eventually lost.")
story.append(Table([[Paragraph(cover, ParagraphStyle('covernote', parent=styles['body'],
    fontSize=10.4, leading=16, spaceAfter=0))]], colWidths=[WIDTH], style=TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),PALE), ('BOX',(0,0),(-1,-1),0.5,LINE),
        ('LEFTPADDING',(0,0),(-1,-1),15), ('RIGHTPADDING',(0,0),(-1,-1),15),
        ('TOPPADDING',(0,0),(-1,-1),14), ('BOTTOMPADDING',(0,0),(-1,-1),14)])))
story.extend([Spacer(1, 19), Paragraph(
    f'<b>{len(events)} dated observations</b>  /  <b>{len(entities)} register entries</b>  /  '
    '<b>33 source references</b>', styles['small']),
    Paragraph('Includes a full chronology, named businesses and institutions, remaining tests, '
              'source locators and a newspaper-coverage audit.', styles['small']),
    Paragraph('Scope: targeted visual reading supported by searchable repository OCR. '
              'This is a working reconstruction, not an exhaustive reading of the collection '
              'or a completed causal explanation.', styles['small']), PageBreak()])

lines = SOURCE.read_text(encoding='utf-8').splitlines()
i = 0
in_sources = False
table_counts = []
while i < len(lines):
    line = lines[i].strip()
    if not line or line.startswith('# ') or line.startswith('*A chronology from'):
        i += 1
        continue
    if line.startswith('## '):
        title = line[3:]
        if title.startswith(('5.', '6.', '7.', '8.', '9.')):
            story.append(PageBreak())
        elif re.match(r'\d+\.', title):
            story.append(CondPageBreak(200))
        in_sources = title.startswith('9.')
        story.append(Paragraph(inline(title), styles['h2']))
        i += 1
        continue
    if line.startswith('### '):
        story.append(Paragraph(inline(line[4:]), styles['h3']))
        i += 1
        continue
    if line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                rows.append(cells)
            i += 1
        table_counts.append(len(rows)-1)
        widths = [86, 256, 174] if rows[0][0] == 'Date' else [121, 234, 161]
        cells = [[Paragraph(inline(c), styles['headcell'] if n == 0 else styles['cell'])
                  for c in row] for n, row in enumerate(rows)]
        table = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT', splitByRow=1)
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),TEAL), ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),7), ('RIGHTPADDING',(0,0),(-1,-1),7),
            ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
            ('LINEBELOW',(0,-1),(-1,-1),0.5,LINE)]))
        story.extend([table, Spacer(1, 10)])
        continue
    if line.startswith('- ') or re.match(r'^\d+\. ', line):
        if in_sources:
            text = line[2:] if line.startswith('- ') else line
            style = styles['source']
        else:
            text = line
            style = styles['bullet']
        story.append(Paragraph(inline(text), style))
        i += 1
        continue
    para = [line]
    i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||\- |\d+\. )', lines[i]):
        para.append(lines[i].strip())
        i += 1
    story.append(Paragraph(inline(' '.join(para)), styles['small'] if in_sources else styles['body']))

assert table_counts == [len(events), len(entities)], table_counts
doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
print(json.dumps({'pdf': str(OUT), 'chronology_rows': table_counts[0],
                  'register_rows': table_counts[1]}, indent=2))
