"""Compare body texture under the same requested display hierarchy."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
import build_chapters02_03_pdf as base
from revision07_typography import register
register()
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/cuervo-typography-comparison-revision-07.pdf'
styles={
 'title':ParagraphStyle('T',fontName='Playfair07Bold',fontSize=31,leading=38,textColor=HexColor(base.NAVY),spaceAfter=20),
 'head':ParagraphStyle('H',fontName='Playfair07',fontSize=21,leading=27,textColor=HexColor(base.NAVY),spaceAfter=14),
 'label':ParagraphStyle('L',fontName='Body07',fontSize=9,leading=12,textColor=HexColor(base.GRAY),spaceAfter=16),
 'sans':ParagraphStyle('S',fontName='Body07',fontSize=11.3,leading=16.2,spaceAfter=9,textColor=HexColor(base.INK)),
 'serif':ParagraphStyle('R',fontName='Garamond',fontSize=12.2,leading=16.5,spaceAfter=9,textColor=HexColor(base.INK))}
text=next((ROOT/'manuscript/book-revision-07/chapters').glob('chapter-03-*')).read_text(encoding='utf-8')
excerpt=text.split('## Selling now, collecting later\n\n')[1].split('\n\nA related Bond company')[0]
import re
excerpt=re.sub(r'\[\^\d+\]','',excerpt)
story=[]
for k,label in [('sans','A / JOST REGULAR — TEMPORARY FUTURA STAND-IN'),('serif','B / GARAMOND — CURRENT SERIF BODY COMPARISON')]:
 story.extend([Paragraph(label,styles['label']),Paragraph('The business of ranch country',styles['title']),Paragraph('Selling now, collecting later',styles['head'])])
 for p in excerpt.split('\n\n'):story.append(Paragraph(p,styles[k]))
 story.extend([Spacer(1,15),Paragraph('Playfair Display Bold title · Playfair Display Regular subhead. Both pages use the same 366-point text measure. This is a comparison of page texture, not a specimen of Futura; Futura was unavailable on this computer.',styles['label']),PageBreak()])
def footer(c,d):
 c.setFont('Body07',8);c.setFillColor(HexColor(base.GRAY));c.drawString(105,40,'MERIDIAN / CUERVO / TYPOGRAPHY PROOF');c.drawRightString(471,40,str(d.page))
SimpleDocTemplate(str(OUT),pagesize=(576,816),leftMargin=105,rightMargin=105,topMargin=64,bottomMargin=70).build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
