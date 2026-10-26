"""Provisional geometric sans body with the requested Playfair hierarchy."""
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
FONT=ROOT/'manuscript/fonts/revision07'
def register():
    for alias,file in [('Body07','Jost-Regular.ttf'),('Body07Italic','Jost-Italic-Regular.ttf'),('Body07Bold','Jost-Semibold.ttf'),('Body07BoldItalic','Jost-Italic-Semibold.ttf'),('Playfair07','PlayfairDisplay-Regular.ttf'),('Playfair07Bold','PlayfairDisplay-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(alias,str(FONT/file)))
    pdfmetrics.registerFontFamily('Body07',normal='Body07',bold='Body07Bold',italic='Body07Italic',boldItalic='Body07BoldItalic')
    pdfmetrics.registerFontFamily('Playfair07',normal='Playfair07',bold='Playfair07Bold',italic='Playfair07',boldItalic='Playfair07Bold')

def configure(base):
    register()
    # Legacy tables use these aliases directly. Rebind them in this process only.
    # registerFont preserves an existing alias; explicit rebinding is needed.
    for alias,target in [('Garamond','Body07'),('GaramondItalic','Body07Italic'),('GaramondBold','Body07Bold'),('Display','Playfair07Bold'),('Label','Body07')]:
        pdfmetrics._fonts[alias]=pdfmetrics.getFont(target)
    import build_chapter04_pdf as ch4, build_chapter05_pdf as ch5, build_chapter06_pdf as ch6, build_chapter07_pdf as ch7
    for module in [ch4,ch5,ch6]:
        module.side_style.fontName='Body07';module.side_style.fontSize=10.5;module.side_style.leading=14.5
    ch7.cell_style.fontName='Body07';ch7.cell_style.fontSize=10.5;ch7.cell_style.leading=14
    ch7.cell_head.fontName='Playfair07';ch7.cell_head.fontSize=16;ch7.cell_head.leading=20
    base.body_style.fontName='Body07';base.body_style.fontSize=11.3;base.body_style.leading=16.2;base.body_style.spaceAfter=8
    base.lead_style.fontName='Body07';base.lead_style.fontSize=14.3;base.lead_style.leading=20;base.lead_style.spaceAfter=17
    base.head_style.fontName='Playfair07';base.head_style.fontSize=21;base.head_style.leading=26;base.head_style.spaceBefore=21;base.head_style.spaceAfter=12
    base.figure_title.fontName='Playfair07';base.figure_title.fontSize=20;base.figure_title.leading=25
    base.note_style.fontName='Body07';base.note_style.fontSize=9.4;base.note_style.leading=12.5;base.note_style.spaceAfter=7
    base.caption_style.fontName='Body07';base.caption_style.fontSize=8.9;base.caption_style.leading=12.2
