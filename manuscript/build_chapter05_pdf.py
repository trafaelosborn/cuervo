"""Build only the Chapter 5 illustrated reading proof."""
from pathlib import Path
import re,json,hashlib
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Image,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from pypdf import PdfReader
from build_chapters02_03_pdf import (ROOT,W,H,MARGIN,TOP,BOTTOM,NAVY,INK,GRAY,tracked,markup,running_for,
    body_style,lead_style,head_style,note_style,caption_style,figure_title)
QA=ROOT/'tmp/pdfs/chapter05-draft01';QA.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'manuscript/figures/chapter05'
SRC=ROOT/'manuscript/chapter-05-people-across-places.md'
OUT=ROOT/'output/pdf/cuervo-chapter-05-people-across-places.pdf'
SPEC={'number':5,'word':'FIVE','title':'People across places'}
label_style=ParagraphStyle('PlateLabel5',fontName='Label',fontSize=8.5,leading=11,textColor=HexColor(NAVY),spaceAfter=8)
side_style=ParagraphStyle('PlateSide5',fontName='Garamond',fontSize=11.5,leading=15,textColor=HexColor(INK),spaceAfter=12)

def cover(c,doc):
    c.saveState();c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    tracked(c,'CUERVO',48,778);tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    tracked(c,'CHAPTER FIVE',48,726,8,NAVY,2.1)
    for y,text,font,size in [(660,'People','Display',54),(592,'across','GaramondItalic',64),(524,'places','GaramondItalic',64)]:
        c.setFont(font,size);c.setFillColor(HexColor(NAVY if font=='GaramondItalic' else INK));c.drawString(45,y,text)
    p=Paragraph('The changing households and regional connections behind the population counts.',
      ParagraphStyle('Deck5',fontName='GaramondItalic',fontSize=20,leading=25,textColor=HexColor(NAVY)))
    _,height=p.wrap(410,90);p.drawOn(c,48,428-height)
    c.setStrokeColor(HexColor(NAVY));c.setLineWidth(.6);c.line(48,316,528,316)
    for i,(year,label) in enumerate([('1940','Nearly half the recorded residents are children'),('1950','More people, in smaller household groups'),('2020','Different forms of regional growth and persistence')]):
        yy=280-i*44;c.setFont('GaramondItalic',19);c.setFillColor(HexColor(NAVY));c.drawString(48,yy,year)
        c.setFont('Label',10.3);c.setFillColor(HexColor(INK));c.drawString(125,yy+1,label)
    p=Paragraph('Historical precincts, municipalities and modern study windows count different territories. Residence, work and schooling have separate histories.',caption_style)
    _,height=p.wrap(430,70);p.drawOn(c,48,132-height)
    tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
    tracked(c,'READING PROOF / DRAFT 1 / 28 SEPTEMBER 2026',48,45,6.7,spacing=1)
    c.restoreState()

def pic(name,width=None,height=None):
    path=FIG/f'{name}.png'
    with PILImage.open(path) as im:
        if height is None:height=width*im.height/im.width
        else:width=height*im.width/im.height
    result=Image(str(path),width=width,height=height);result.hAlign='CENTER';return result

def paired_details(left,right,height):
    a,b=pic(left,height=height),pic(right,height=height)
    table=Table([[a,'',b]],colWidths=[a.drawWidth,18,b.drawWidth],hAlign='CENTER')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return table

def figure(key):
    if key=='population-and-age':
        title='A smaller, still young population'
        items=[pic(key,410)]
        caption='Figure 5.1. Cuervo precinct, 1910-1950: five reported populations and medians calculated from the named schedules. Points are not an annual series or constant-boundary estimates. Age ranges allow for seven unread entries across the five censuses; they are not confidence intervals. The corrected 1950 readings give a median of 25.5. Sources: U.S. Census and the project transcription; chapter notes 2-5.'
    elif key=='people-and-households':
        title='More people, smaller groups'
        items=[pic(key,410)]
        caption='Figure 5.2. Cuervo precinct, 1940 and 1950. Population rose from 188 to 210; head-listed household groups rose from 42 to 59. One- and two-person groups account for 14 of the 17 additional groups. Average group size fell from 4.48 to 3.56. These are reconstructed groups, not new houses or migrant families. Sources: census schedules and corrected household transcription; chapter notes 8-9.'
    elif key=='work-under-one-roof':
        title='Several livelihoods, one household'
        items=[Paragraph('CUERVO / HIGGINS HOUSEHOLD / SHEET 8, LINES 19-22',label_style),
            paired_details('higgins-names','higgins-work',56),Spacer(1,13),
            Paragraph('At left, names, relationships and ages. At right, work entries: the father in ranch work and his son a veterans instructor. The instructor\'s workplace is not named.',side_style),
            Spacer(1,21),Paragraph('SANTA ROSA / SHEET 71, LINES 1-5',label_style),
            paired_details('cafe-names','cafe-work',81),Spacer(1,13),
            Paragraph('The father has Southern Pacific railway work. His wife is proprietor of the 66 Cafe. Two daughters have unpaid cafe work; another has paid housekeeping work.',side_style)]
        caption='Figure 5.3. Selected 1950 census household rows: Cuervo ED 10-6 and Santa Rosa ED 10-8. Each pair reproduces two portions of the same rows; intervening columns are omitted. These are selected examples, not a household diversification rate or evidence of pooled earnings. Original writing and marks are retained. Source: National Archives schedules; chapter notes 14-15. Original scans and crop provenance are preserved.'
    elif key=='regional-households':
        title='Growth has different components'
        items=[pic(key,410)]
        caption='Figure 5.4. Municipal populations at five censuses, 1980-2020. Above: Santa Rosa household and group-quarters residents; labels give totals. Below: people living in households in Santa Rosa and Los Lunas. Lines join census observations, not annual estimates. Municipal boundaries changed, and group-quarters subtraction is not a counterfactual without an institution. Sources: U.S. Census tables and bulk files; chapter notes 20-22.'
    else:raise ValueError(key)
    return [PageBreak(),Paragraph(title,figure_title),Spacer(1,8),*items,Spacer(1,15),Paragraph(caption,caption_style),PageBreak()]

def build():
    text=SRC.read_text(encoding='utf-8');body,notes=text.split('\n---\n',1)
    refs=re.findall(r'\[\^(\d+)\]',body);defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    assert defs==list(dict.fromkeys(refs))==[str(i+1) for i in range(len(defs))]
    missing=[p for p in re.findall(r'\]\((B:/[^)]+)\)',text) if not Path(p).exists()];assert not missing,missing
    clean=re.sub(r'<!--(?! FIGURE:).*?-->','',body,flags=re.S)
    blocks=[b.strip() for b in clean.split('\n\n') if b.strip() and not b.startswith('# ')]
    story=[Spacer(1,H-TOP-BOTTOM-15),PageBreak()];first=True
    for block in blocks:
        fig=re.fullmatch(r'<!-- FIGURE: ([\w-]+) -->',block)
        if fig:story.extend(figure(fig.group(1)))
        elif block.startswith('## '):story.append(Paragraph(markup(block[3:]),head_style))
        else:story.append(Paragraph(markup(block),lead_style if first else body_style));first=False
    story.extend([PageBreak(),Paragraph('Working source notes',head_style),Paragraph('Draft 1 / September 28, 2026. Prior checked census readings and selected family accounts, with corrected ages, explicit geographic units and reproducible calculations. This chapter is not a complete person-linkage or migration study.',caption_style)])
    for block in notes.split('\n\n'):
        match=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
        if match:
            number,content=match.groups();story.append(KeepTogether([Paragraph(f'<a name="note{number}"/><b>{number}.</b> '+markup(content),note_style)]))
    doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=TOP,bottomMargin=BOTTOM,
      title='Cuervo | Chapter 5: People across places',author='Meridian',subject='Chapter 5, draft 1, September 28, 2026')
    doc.build(story,onFirstPage=cover,onLaterPages=running_for(SPEC))
    reader=PdfReader(OUT);plain=re.sub(r'<!--.*?-->','',body,flags=re.S);plain=re.sub(r'^#+.*$','',plain,flags=re.M)
    report={'chapter':5,'source':str(SRC),'output':str(OUT),'body_words':len(re.sub(r'\[\^\d+\]','',plain).split()),
       'pages':len(reader.pages),'note_definitions':len(defs),'note_references':len(refs),'figure_positions':4,
       'missing_local_links':missing,'all_note_references_resolve':True,
       'page_word_counts':[len((p.extract_text() or '').split()) for p in reader.pages],
       'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/'chapter-05-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':build()
