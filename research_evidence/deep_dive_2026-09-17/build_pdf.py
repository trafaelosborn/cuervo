"""Typeset the reviewed research assessment, preserving its source notes and tables."""
from pathlib import Path
import re, html
from urllib.parse import unquote
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, CondPageBreak
from PIL import Image as PILImage

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SOURCE=HERE.parent/'deep_dive_2026-09-17.md'
OUT=ROOT/'output/pdf/cuervo_santa_rosa_deep_dive_2026-09-17.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
FONTS=ROOT/'tmp/deep_dive/python_deps/matplotlib/mpl-data/fonts/ttf'
for family,base in [('Body','DejaVuSerif'),('Sans','DejaVuSans')]:
    suffixes={'':'','Bold':'-Bold','Italic':'-Italic' if family=='Body' else '-Oblique','BoldItalic':'-BoldItalic' if family=='Body' else '-BoldOblique'}
    for style,suffix in suffixes.items():pdfmetrics.registerFont(TTFont(family+style,str(FONTS/(base+suffix+'.ttf'))))
    pdfmetrics.registerFontFamily(family,normal=family,bold=family+'Bold',italic=family+'Italic',boldItalic=family+'BoldItalic')
INK=colors.HexColor('#203344');TEAL=colors.HexColor('#116466');PALE=colors.HexColor('#EEF3F2');GOLD=colors.HexColor('#B26A32')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.8,leading=14.4,textColor=INK,spaceAfter=8.5,splitLongWords=True),
 'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=17,leading=21,textColor=TEAL,spaceBefore=8,spaceAfter=13,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=11.4,leading=15,textColor=INK,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'quote':ParagraphStyle('quote',fontName='BodyItalic',fontSize=10,leading=15,leftIndent=13,rightIndent=10,textColor=TEAL,spaceBefore=5,spaceAfter=13,borderColor=GOLD,borderWidth=0,borderPadding=8),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=8.0,leading=11,textColor=INK,splitLongWords=True),
 'headcell':ParagraphStyle('headcell',fontName='SansBold',fontSize=7.9,leading=10.7,textColor=colors.white),
 'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8,leading=11,textColor=TEAL,spaceAfter=12),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.3,leading=12,textColor=INK,spaceAfter=8),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=9.8,leading=14.4,textColor=INK,spaceAfter=8,leftIndent=12,firstLineIndent=-10),
}
def normalize(s):
    return s.replace('—',' - ').replace('–','-').replace('\u2011','-').replace('−','-').replace('\u00a0',' ')
def inline(s):
    s=html.escape(normalize(s),quote=False)
    def link(m):
        label,url=m.group(1),html.unescape(m.group(2))
        if url.startswith('https://'):
            return f'<a href="{html.escape(url,quote=True)}" color="#116466">{label}</a>'
        return label # Local source files are identified in the source index / Markdown companion.
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Sans">\1</font>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
    return s

class NumberedCanvas(canvas.Canvas):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.states=[]
    def showPage(self):self.states.append(dict(self.__dict__));self._startPage()
    def save(self):
        total=len(self.states)
        for state in self.states:
            self.__dict__.update(state)
            self.setFillColor(TEAL);self.setFont('Sans',7.5)
            if self._pageNumber>1:
                self.drawString(48,765,'CUERVO / SANTA ROSA  |  RESEARCH ASSESSMENT')
                self.setStrokeColor(colors.HexColor('#CBD8D8'));self.line(48,755,564,755)
            self.drawString(48,27,'September 17, 2026  |  Source-based working assessment')
            self.drawRightString(564,27,f'{self._pageNumber} / {total}')
            super().showPage()
        super().save()

doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=51,bottomMargin=47,
    title='Cuervo and Santa Rosa: What the New Evidence Changes',author='Research prepared for Taylor Osborn',subject='Primary-source assessment, September 17, 2026')
story=[]
story += [Spacer(1,45),Paragraph('CUERVO / SANTA ROSA',ParagraphStyle('eyebrow',fontName='SansBold',fontSize=11,textColor=GOLD,spaceAfter=20)),
    Paragraph('What the new<br/>evidence changes',ParagraphStyle('title',fontName='SansBold',fontSize=33,leading=39,textColor=INK,spaceAfter=20)),
    Paragraph('A close reading of newspapers, census schedules,<br/>retail tables, railway records, and historic maps.',ParagraphStyle('subtitle',fontName='Body',fontSize=13,leading=20,textColor=TEAL,spaceAfter=25)),
    Paragraph('Prepared for Taylor Osborn<br/>September 17, 2026',styles['small']),Spacer(1,20)]
cover='The evidence supports a long, uneven divergence between towns with different functions. It also shows a Cuervo community still working in 1950, before the 1952 road relocation and the later interstate project.'
story.append(Table([[Paragraph(cover,ParagraphStyle('covernote',parent=styles['body'],fontSize=11,leading=17,spaceAfter=0))]],colWidths=[516],style=TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.4,colors.HexColor('#CBD8D8')),('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),('TOPPADDING',(0,0),(-1,-1),16),('BOTTOMPADDING',(0,0),(-1,-1),16)])))
story += [Spacer(1,25),Paragraph('Based on 56 occupation readings and a 210-person schedule count. Includes retail and population calculations, three figures, precise source locators, and a reassessment of the earlier thesis.',styles['small']),Paragraph('Scope: targeted close reading. The complete newspaper collection and the other acquired census districts have not been exhaustively transcribed.',styles['small']),PageBreak()]
lines=SOURCE.read_text(encoding='utf-8').splitlines();i=0
in_sources=False
while i<len(lines):
    line=lines[i].strip()
    if not line or line.startswith('# '):i+=1;continue
    if line.startswith('## '):
        title=line[3:]
        if title.startswith(('1.','12.')):story.append(PageBreak())
        elif re.match(r'\d+\.',title):story.append(CondPageBreak(190))
        if title.startswith('12.'):in_sources=True
        story.append(Paragraph(inline(title),styles['h2']));i+=1;continue
    if line.startswith('### '):story.append(Paragraph(inline(line[4:]),styles['h3']));i+=1;continue
    if line.startswith('|'):
        table=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',c) for c in cells):table.append(cells)
            i+=1
        n=len(table[0])
        if n==11:widths=[105]+[41.1]*10
        elif n==7:widths=[150]+[61]*6
        elif n==5:
            widths=[176,78,111,81,70] if table[0][0]=='Measure' else [172,80,84,84,96]
        elif n==4:widths=[210,85,99,122]
        elif n==3:
            widths=[165,76,275] if table[0][0]=='Analytical grouping' else [165,160,191]
        elif n==2:widths=[212,304]
        else:widths=[516/n]*n
        assert abs(sum(widths)-516)<.1,(n,widths)
        tdata=[[Paragraph(inline(c),styles['headcell'] if row==0 else styles['cell']) for c in cc] for row,cc in enumerate(table)]
        t=Table(tdata,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#B9CCCC'))]))
        story+=[t,Spacer(1,13)];continue
    if line.startswith('!['):
        m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        fp=SOURCE.parent/unquote(m.group(2));im=PILImage.open(fp);w,h=im.size;ww=516;hh=ww*h/w
        group=[]
        if story and isinstance(story[-1],Paragraph) and story[-1].style.name=='h3':
            heading=story.pop();heading.keepWithNext=False;group.append(heading)
        group += [Image(str(fp),width=ww,height=hh),Paragraph(inline(m.group(1))+'. Calculated from the cited published tables; see adjacent discussion for geography and coverage.',styles['caption'])]
        story.append(KeepTogether(group))
        i+=1;continue
    if line.startswith('> '):
        text=[]
        while i<len(lines) and lines[i].startswith('> '):text.append(lines[i][2:]);i+=1
        story.append(Paragraph(inline(' '.join(text)),styles['quote']));continue
    if line.startswith('- ') or re.match(r'^\d+\. ',line):
        story.append(Paragraph(inline(line if not line.startswith('- ') else '- '+line[2:]),styles['bullet']));i+=1;continue
    para=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||!\[|> |\- |\d+\. )',lines[i]):para.append(lines[i].strip());i+=1
    story.append(Paragraph(inline(' '.join(para)),styles['small'] if in_sources else styles['body']))
doc.build(story,canvasmaker=NumberedCanvas)
print(OUT)
