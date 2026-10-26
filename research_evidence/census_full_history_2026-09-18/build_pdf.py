"""Typeset the full-history study from its human-readable Markdown source."""
from pathlib import Path
import re, html
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether,CondPageBreak
from PIL import Image as PILImage

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
SOURCE=HERE.parent/'census_full_history_2026-09-18.md'
OUT=ROOT/'output/pdf/cuervo_whole_census_history_2026-09-18.pdf'
FONTS=ROOT/'tmp/deep_dive/python_deps/matplotlib/mpl-data/fonts/ttf'
for family,base in [('Body','DejaVuSerif'),('Sans','DejaVuSans')]:
    for suffix,style in [('', ''),('-Bold','Bold'),('-Italic' if family=='Body' else '-Oblique','Italic')]:
        pdfmetrics.registerFont(TTFont(family+style,str(FONTS/(base+suffix+'.ttf'))))
    pdfmetrics.registerFontFamily(family,normal=family,bold=family+'Bold',italic=family+'Italic',boldItalic=family+'Bold')
INK=colors.HexColor('#203344');TEAL=colors.HexColor('#116466');GOLD=colors.HexColor('#B26A32');PALE=colors.HexColor('#EEF3F2')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.6,leading=14.1,textColor=INK,spaceAfter=8.3,allowWidows=0,allowOrphans=0),
 'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=16.5,leading=21,textColor=TEAL,spaceBefore=8,spaceAfter=12,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=11.2,leading=15,textColor=INK,spaceBefore=10,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=8,leading=11,textColor=INK),
 'headcell':ParagraphStyle('headcell',fontName='SansBold',fontSize=7.8,leading=10.5,textColor=colors.white),
 'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8.2,leading=11.5,textColor=TEAL,spaceAfter=12),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.3,leading=12,textColor=INK,spaceAfter=8),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=9.6,leading=14.1,textColor=INK,leftIndent=13,firstLineIndent=-10,spaceAfter=8.3)
}
def inline(s):
    s=s.replace('—',' - ').replace('–','-').replace('−','-').replace('\u2011','-').replace('\u00a0',' ')
    s=html.escape(s,quote=False)
    def link(m):
        label,url=m.group(1),html.unescape(m.group(2))
        return f'<a href="{html.escape(url,quote=True)}" color="#116466">{label}</a>' if url.startswith('https://') else label
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Sans">\1</font>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
    return s
def footer(c,doc):
    c.saveState();c.setFillColor(TEAL);c.setFont('Sans',7.5)
    if doc.page>1:
        c.drawString(48,765,'CUERVO / SANTA ROSA  |  THE WHOLE CENSUS HISTORY')
        c.setStrokeColor(colors.HexColor('#CBD8D8'));c.line(48,755,564,755)
    c.drawString(48,27,'September 18, 2026  |  Manuscript readings and published comparisons')
    c.drawRightString(564,27,str(doc.page));c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=51,bottomMargin=47,
    title='The Whole Census History: Cuervo and its Regional Comparisons',author='Research prepared for Taylor Osborn')
story=[Spacer(1,42),Paragraph('CUERVO / SANTA ROSA / LOS LUNAS',ParagraphStyle('eyebrow',fontName='SansBold',fontSize=10.7,textColor=GOLD,spaceAfter=22)),
 Paragraph('The whole<br/>census history',ParagraphStyle('title',fontName='SansBold',fontSize=35,leading=41,textColor=INK,spaceAfter=24)),
 Paragraph('Five household censuses of Cuervo.<br/>A regional baseline in 1900.<br/>Published comparisons through 2020.',ParagraphStyle('subtitle',fontName='Body',fontSize=13,leading=21,textColor=TEAL,spaceAfter=24)),
 Paragraph('Prepared for Taylor Osborn<br/>September 18, 2026',styles['small']),Spacer(1,24)]
cover='Cuervo\'s 1940 median recorded age was <b>18</b>. At least <b>90 of its 188 residents</b> were children. The shrinking precinct still contained a substantial young population before World War II.'
story.append(Table([[Paragraph(cover,ParagraphStyle('covernote',parent=styles['body'],fontSize=11.2,leading=17,spaceAfter=0))]],colWidths=[516],style=TableStyle([
 ('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.4,colors.HexColor('#CBD8D8')),
 ('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),('TOPPADDING',(0,0),(-1,-1),16),('BOTTOMPADDING',(0,0),(-1,-1),16)])))
story += [Spacer(1,25),Paragraph('1,668 census appearances | 1,661 readable ages | 7 unresolved ages',styles['small']),
 Paragraph('Includes source locations, age tables, two figures, ten new microfilm acquisitions, and a clear distinction between completed readings and household linkage still to be done.',styles['small']),PageBreak()]
lines=SOURCE.read_text(encoding='utf-8').splitlines();i=0
while i<len(lines):
    line=lines[i].strip()
    if not line or line.startswith('# ') or line.startswith('*Research update'):i+=1;continue
    if line.startswith('## '):
        title=line[3:]
        if not title.startswith('1.'):story.append(CondPageBreak(240))
        story.append(Paragraph(inline(title),styles['h2']));i+=1;continue
    if line.startswith('### '):
        if line[4:]=='Local study package':story.append(CondPageBreak(280))
        story.append(Paragraph(inline(line[4:]),styles['h3']));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',x) for x in cells):rows.append(cells)
            i+=1
        n=len(rows[0]);assert all(len(x)==n for x in rows)
        if n==8:widths=[54]+[66]*7
        elif n==6:widths=[52,64,90,99,103,108]
        elif n==4:
            widths=[45,124,283,64] if rows[0][1]=='Original source' else [45,90,301,80]
        elif n==3:
            widths=[90,208,218] if rows[0][0]=='Period' else [60,228,228]
        else:widths=[516/n]*n
        assert sum(widths)==516
        data=[[Paragraph(inline(x),styles['headcell'] if j==0 else styles['cell']) for x in r] for j,r in enumerate(rows)]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#B9CCCC'))]))
        group=[]
        if story and isinstance(story[-1],Paragraph) and story[-1].style.name=='h3':
            heading=story.pop();heading.keepWithNext=False;group.append(heading)
        group.extend([t,Spacer(1,12)])
        story.append(KeepTogether(group));continue
    if line.startswith('!['):
        m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',line);fp=Path(m.group(2));w,h=PILImage.open(fp).size
        group=[Image(str(fp),width=516,height=516*h/w),Paragraph(inline(m.group(1)),styles['caption'])]
        story.append(KeepTogether(group));i+=1;continue
    if line.startswith('- '):story.append(Paragraph('- '+inline(line[2:]),styles['bullet']));i+=1;continue
    if re.match(r'\d+\. ',line):story.append(Paragraph(inline(line),styles['bullet']));i+=1;continue
    story.append(Paragraph(inline(line),styles['body']));i+=1
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
