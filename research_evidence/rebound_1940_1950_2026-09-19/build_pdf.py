"""Typeset the dated rebound evidence brief from Markdown."""
from pathlib import Path
import html,re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from PIL import Image as PILImage

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
SOURCE=HERE.parent/'rebound_1940_1950_2026-09-19.md'
OUT=ROOT/'output/pdf/cuervo_1940_1950_rebound_2026-09-19.pdf'
FONTS=ROOT/'tmp/deep_dive/python_deps/matplotlib/mpl-data/fonts/ttf'
for family,base in [('Body','DejaVuSerif'),('Sans','DejaVuSans')]:
    for suffix,style in [('', ''),('-Bold','Bold'),('-Italic' if family=='Body' else '-Oblique','Italic')]:
        pdfmetrics.registerFont(TTFont(family+style,str(FONTS/(base+suffix+'.ttf'))))
    pdfmetrics.registerFontFamily(family,normal=family,bold=family+'Bold',italic=family+'Italic',boldItalic=family+'Bold')
INK=colors.HexColor('#203344'); TEAL=colors.HexColor('#14666a'); GOLD=colors.HexColor('#b46e35'); PALE=colors.HexColor('#eef4f3')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.5,leading=13.5,textColor=INK,spaceAfter=8,allowWidows=0,allowOrphans=0),
 'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=17,leading=21,textColor=TEAL,spaceAfter=13,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=11,leading=14,textColor=INK,spaceBefore=5,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=8.4,leading=11.5,textColor=INK),
 'headcell':ParagraphStyle('headcell',fontName='SansBold',fontSize=8,leading=10.7,textColor=colors.white),
 'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8.1,leading=11,textColor=TEAL,spaceAfter=10),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.4,leading=12,textColor=INK,spaceAfter=8),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=9.5,leading=13.5,textColor=INK,leftIndent=11,firstLineIndent=-9,spaceAfter=8)
}
def inline(s):
    for char in ['\u2014','\u2013','\u2212','\u2011']:s=s.replace(char,'-')
    s=html.escape(s,quote=False)
    def link(m):
        label,url=m.group(1),html.unescape(m.group(2))
        return f'<a href="{html.escape(url,quote=True)}" color="#14666a">{label}</a>' if url.startswith('https://') else label
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Sans">\1</font>',s)
    return s
def footer(c,doc):
    c.saveState();c.setFillColor(TEAL);c.setFont('Sans',7.5)
    c.drawString(46,766,'CUERVO MONOGRAPH  |  RESEARCH BRIEF  |  SEPTEMBER 19, 2026')
    c.setStrokeColor(colors.HexColor('#cbd8d8'));c.line(46,756,566,756)
    c.drawString(46,27,'Twenty-two people: the 1940-1950 rebound')
    c.drawRightString(566,27,str(doc.page));c.restoreState()

story=[Paragraph('Twenty-two people',ParagraphStyle('title',fontName='SansBold',fontSize=31,leading=36,textColor=INK,spaceAfter=7)),
    Paragraph("Explaining Cuervo's 1940-1950 rebound",ParagraphStyle('subtitle',fontName='Body',fontSize=14,leading=18,textColor=GOLD,spaceAfter=10)),
    Paragraph('Prepared for Taylor Osborn | Evidence, provisional explanations, and an audit trail',styles['small']),Spacer(1,4)]
lines=SOURCE.read_text(encoding='utf-8').splitlines();i=0
while i<len(lines):
    line=lines[i].strip()
    if not line or line.startswith('# ') or line.startswith('*Research brief'):i+=1;continue
    if line=='<!-- pagebreak -->':story.append(PageBreak());i+=1;continue
    if line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['h2']));i+=1;continue
    if line.startswith('### '):story.append(Paragraph(inline(line[4:]),styles['h3']));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',x) for x in cells):rows.append(cells)
            i+=1
        header=rows[0];n=len(header)
        if header[0]=='Family':widths=[81,226,213]
        elif header[0]=='Measure':widths=[324,98,98]
        elif header[0]=='Resident and 1950 age':widths=[154,298,68]
        elif header[0]=='Name as read':widths=[117,65,64,274]
        elif header[0].startswith('Guadalupe'):widths=[193,109,109,109]
        else:widths=[520/n]*n
        data=[[Paragraph(inline(x),styles['headcell'] if j==0 else styles['cell']) for x in row] for j,row in enumerate(rows)]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#b9cccc'))]))
        story.extend([t,Spacer(1,10)]);continue
    if line.startswith('!['):
        m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line);path=Path(m.group(2));w,h=PILImage.open(path).size
        story.extend([Image(str(path),width=520,height=520*h/w),Paragraph(inline(m.group(1)),styles['caption'])]);i+=1;continue
    if line.startswith('- '):story.append(Paragraph('- '+inline(line[2:]),styles['bullet']));i+=1;continue
    if re.match(r'\d+\. ',line):story.append(Paragraph(inline(line),styles['bullet']));i+=1;continue
    story.append(Paragraph(inline(line),styles['body']));i+=1
OUT.parent.mkdir(parents=True,exist_ok=True)
doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),leftMargin=46,rightMargin=46,topMargin=49,bottomMargin=45,
    title="Twenty-two people: explaining Cuervo's 1940-1950 rebound",author='Research prepared for Taylor Osborn')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
