from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
import html
from revision07_typography import register
register()
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'output/editorial/cuervo-outside-reader-brief-revision-07.md'
styles={
'title':ParagraphStyle('T',fontName='Playfair07Bold',fontSize=27,leading=33,spaceAfter=17,textColor=HexColor('#1b3558')),
'head':ParagraphStyle('H',fontName='Playfair07',fontSize=17,leading=22,spaceBefore=14,spaceAfter=9,keepWithNext=True,textColor=HexColor('#1b3558')),
'body':ParagraphStyle('B',fontName='Body07',fontSize=10.5,leading=14.7,spaceAfter=8,allowWidows=0,allowOrphans=0,textColor=HexColor('#242528'))}
story=[]
for block in source.read_text(encoding='utf-8').split('\n\n'):
 if block.strip()=='---':story.append(PageBreak());continue
 if block.startswith('# '):style='title';block=block[2:]
 elif block.startswith('## '):style='head';block=block[3:]
 else:style='body'
 if block.startswith('- '):
  for line in block.splitlines():story.append(Paragraph('• '+html.escape(line[2:]),styles['body']))
 else:story.append(Paragraph(html.escape(block),styles[style]))
def footer(c,d):
 c.setFont('Body07',8);c.setFillColor(HexColor('#756e65'));c.drawString(58,35,'MERIDIAN / CUERVO / OUTSIDE-READER BRIEF');c.drawRightString(518,35,str(d.page))
out=ROOT/'output/pdf/cuervo-outside-reader-brief-revision-07.pdf'
SimpleDocTemplate(str(out),pagesize=(576,816),leftMargin=58,rightMargin=58,topMargin=45,bottomMargin=57).build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
