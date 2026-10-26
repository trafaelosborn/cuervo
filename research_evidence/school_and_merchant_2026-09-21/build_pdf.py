"""Typeset the school/merchant addendum from its maintained Markdown text."""
from pathlib import Path
import html,json,re
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,CondPageBreak,Image,KeepTogether

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'research_evidence/school_and_merchant_2026-09-21.md'
OUT=ROOT/'output/pdf/cuervo_school_and_merchant_followup_2026-09-21.pdf'
FONTS=ROOT/'tmp/deep_dive/python_deps/matplotlib/mpl-data/fonts/ttf'
for family,base in [('Body','DejaVuSerif'),('Sans','DejaVuSans')]:
    for style,suffix in {'':'','Bold':'-Bold','Italic':'-Italic' if family=='Body' else '-Oblique','BoldItalic':'-BoldItalic' if family=='Body' else '-BoldOblique'}.items():
        pdfmetrics.registerFont(TTFont(family+style,str(FONTS/(base+suffix+'.ttf'))))
    pdfmetrics.registerFontFamily(family,normal=family,bold=family+'Bold',italic=family+'Italic',boldItalic=family+'BoldItalic')
INK=colors.HexColor('#25373B');TEAL=colors.HexColor('#24645C');PALE=colors.HexColor('#F0F4F2');LINE=colors.HexColor('#CCD8D3')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.8,leading=14.3,textColor=INK,spaceAfter=9,allowWidows=0,allowOrphans=0),
 'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=15.5,leading=20,textColor=TEAL,spaceAfter=12,spaceBefore=8,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SansBold',fontSize=11,leading=15,textColor=INK,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=8.3,leading=11.6,textColor=INK),
 'headcell':ParagraphStyle('headcell',fontName='SansBold',fontSize=8.3,leading=11.6,textColor=colors.white),
 'small':ParagraphStyle('small',fontName='Sans',fontSize=8.2,leading=11.6,textColor=INK,spaceAfter=8),
 'source':ParagraphStyle('source',fontName='Sans',fontSize=8.6,leading=12.3,textColor=INK,spaceAfter=10),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=9.8,leading=14.3,textColor=INK,spaceAfter=7,leftIndent=10,firstLineIndent=-8)
}
def inline(text):
    text=text.replace('\u2014',' - ').replace('\u2013','-').replace('\u2011','-').replace('\u00a0',' ')
    text=html.escape(text,quote=False)
    def link(m):
        label,url=m.group(1),html.unescape(m.group(2))
        if url.startswith('https://'):return f'<a href="{html.escape(url,quote=True)}" color="#24645C">{label}</a>'
        return label
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
    return re.sub(r'`([^`]+)`',r'<font name="Sans">\1</font>',text)
class Doc(SimpleDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='h2':
            key='s'+re.sub(r'\W+','_',f.getPlainText());self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0)
def decor(c,d):
    c.saveState();c.setFillColor(TEAL);c.setFont('Sans',7.2)
    if d.page>1:
        c.drawString(48,765,'CUERVO  |  SCHOOLS, FAMILIES AND MERCHANT SURVIVAL');c.setStrokeColor(LINE);c.line(48,755,564,755)
    c.drawString(48,27,'September 21, 2026  |  Research addendum and records checklist');c.drawRightString(564,27,str(d.page));c.restoreState()

story=[Paragraph('THE CUERVO MONOGRAPH / RESEARCH',ParagraphStyle('eyebrow',fontName='SansBold',fontSize=9,textColor=TEAL,spaceAfter=16)),
       Paragraph('Schools, families and<br/>merchant survival',ParagraphStyle('title',fontName='SansBold',fontSize=28,leading=34,textColor=INK,spaceAfter=16)),
       Paragraph('Prepared for Taylor Osborn  |  September 21, 2026',styles['small']),
       Paragraph('School-first follow-up: 12 dated observations, five pupil histories and 22 source references.',styles['small']),Spacer(1,6)]
lines=SOURCE.read_text(encoding='utf-8').splitlines();i=0;in_sources=False;table_sizes=[]
while i<len(lines):
    line=lines[i].strip()
    if not line or line.startswith('# ') or line.startswith('*School-first'):
        i+=1;continue
    if line.startswith('## '):
        title=line[3:];in_sources=title.startswith('8.')
        if title.startswith(('2.','3.','4.')):story.append(PageBreak())
        else:story.append(CondPageBreak(180))
        story.append(Paragraph(inline(title),styles['h2']));i+=1;continue
    if line.startswith('### '):story.append(Paragraph(inline(line[4:]),styles['h3']));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',x) for x in row):rows.append(row)
            i+=1
        first=rows[0][0]
        widths=[94,207,215] if first=='Date' else [112,190,214] if first.startswith('Person') else [117,204,195] if first=='Research window' else [120,229,167]
        cells=[[Paragraph(inline(x),styles['headcell'] if j==0 else styles['cell']) for x in row] for j,row in enumerate(rows)]
        tab=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1)
        tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,-1),(-1,-1),.5,LINE)]))
        story.extend([tab,Spacer(1,10)]);table_sizes.append(len(rows)-1);continue
    if line.startswith('- '):
        story.append(Paragraph(inline(line[2:] if in_sources else line),styles['source' if in_sources else 'bullet']));i+=1;continue
    para=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||- )',lines[i]):para.append(lines[i].strip());i+=1
    story.append(Paragraph(inline(' '.join(para)),styles['body']))

OUT.parent.mkdir(parents=True,exist_ok=True)
doc=Doc(str(OUT),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=51,bottomMargin=47,
        title='Cuervo: Schools, Families and Merchant Survival',author='Research prepared for Taylor Osborn',
        subject='School and merchant follow-up, September 21, 2026')
doc.build(story,onFirstPage=decor,onLaterPages=decor)
print(json.dumps({'output':str(OUT),'table_rows':table_sizes}))
