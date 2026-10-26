"""Build Chapter 6 only, using the established Meridian reading-proof typography."""
from pathlib import Path
import re,json,hashlib
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether,Image,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor,white
from pypdf import PdfReader
from build_chapters02_03_pdf import (ROOT,W,H,MARGIN,TOP,BOTTOM,NAVY,INK,GRAY,tracked,markup,running_for,
    body_style,lead_style,head_style,note_style,caption_style,figure_title)
QA=ROOT/'tmp/pdfs/chapter06-draft01';QA.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'manuscript/figures/chapter06'
SRC=ROOT/'manuscript/chapter-06-changing-the-connections.md'
OUT=ROOT/'output/pdf/cuervo-chapter-06-changing-the-connections.pdf'
SPEC={'number':6,'word':'SIX','title':'Changing the connections'}
label_style=ParagraphStyle('PlateLabel6',fontName='Label',fontSize=8.5,leading=11,textColor=HexColor(NAVY),spaceAfter=8)
side_style=ParagraphStyle('PlateSide6',fontName='Garamond',fontSize=11.5,leading=15,textColor=HexColor(INK),spaceAfter=12)
def cover(c,doc):
    c.saveState();c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    tracked(c,'CUERVO',48,778);tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    tracked(c,'CHAPTER SIX',48,726,8,NAVY,2.1)
    for y,text,font,size in [(660,'Changing','Display',54),(592,'the','GaramondItalic',64),(524,'connections','GaramondItalic',64)]:
        c.setFont(font,size);c.setFillColor(HexColor(NAVY if font=='GaramondItalic' else INK));c.drawString(45,y,text)
    p=Paragraph('Roads, railways and the changing reasons to stop, trade and work in Cuervo.',
      ParagraphStyle('Deck6',fontName='GaramondItalic',fontSize=20,leading=25,textColor=HexColor(NAVY)))
    _,height=p.wrap(410,90);p.drawOn(c,48,428-height)
    c.setStrokeColor(HexColor(NAVY));c.setLineWidth(.6);c.line(48,316,528,316)
    for i,(year,label) in enumerate([('1926','A longer rail journey offers a useful day trip'),('1958','Advertised local passenger stops disappear'),('1974','Cuervo billing is assigned to Tucumcari')]):
        yy=280-i*44;c.setFont('GaramondItalic',19);c.setFillColor(HexColor(NAVY));c.drawString(48,yy,year)
        c.setFont('Label',10.3);c.setFillColor(HexColor(INK));c.drawString(125,yy+1,label)
    p=Paragraph('Road alignment, passenger access, railway staffing and freight administration changed at different dates. Passing traffic and local custom were different measures.',caption_style)
    _,height=p.wrap(430,70);p.drawOn(c,48,132-height)
    tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
    tracked(c,'READING PROOF / DRAFT 1 / 28 SEPTEMBER 2026',48,45,6.7,spacing=1)
    c.restoreState()
def pic(name,width):
    p=FIG/f'{name}.png'
    with PILImage.open(p) as im:height=width*im.height/im.width
    result=Image(str(p),width=width,height=height);result.hAlign='CENTER';return result
def figure(key):
    if key=='journeys':
        title='The farther town, the easier day trip'
        items=[pic(key,410)]
        caption='Figure 6.1. Four advertised journeys on daily trains 1 and 2, January 1926. Time at the destination is shown in brown; railway travel in navy. Shading marks the next day. Tucumcari offered a daytime visit and evening return. The Santa Rosa pairing required an overnight stay. Railway mileages are not road distances. Source: Rock Island public timetable, Table 2, p. 18, and reference notes p. 19; chapter note 2.'
    elif key=='retail':
        title='A commercial center before the interstate'
        items=[pic(key,410)]
        caption='Figure 6.2. Santa Rosa shares of Guadalupe County retail activity in 1929, compared with its 1930 population share. Stocks are valued at cost at year end. These are the census\'s retail categories, not all businesses or an estimate of Cuervo spending captured by Santa Rosa. Source: U.S. Census, Retail Distribution, Table 13, New Mexico, p. 166; definitions and chapter notes 3-5.'
    elif key=='station-book':
        title='A place remained in the accounts'
        items=[Paragraph('ROCK ISLAND / STATION BOOK / 15 DECEMBER 1974',label_style),
            pic('station-headings',450),Spacer(1,8),pic('station-rows',450),Spacer(1,8),pic('station-legend',330),Spacer(1,24)]
        rows=[['Station','No agent','Own revenue\ncode','Billing\ncode'],['Tucumcari','Unmarked','8310','8310'],
          ['Montoya','Yes','8353','8310'],['Newkirk','Yes','8354','8310'],['Cuervo','Yes','8355','8310'],['Santa Rosa','Yes','8357','8310']]
        table=Table(rows,colWidths=[128,90,86,86],hAlign='CENTER')
        table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'Label'),('FONTNAME',(0,1),(-1,-1),'Garamond'),
           ('FONTSIZE',(0,0),(-1,0),9),('FONTSIZE',(0,1),(-1,-1),11),('TEXTCOLOR',(0,0),(-1,-1),HexColor(INK)),
           ('TEXTCOLOR',(0,0),(-1,0),HexColor(NAVY)),('BACKGROUND',(0,4),(-1,4),HexColor('#eef1f5')),
           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOTTOMPADDING',(0,0),(-1,0),10),('TOPPADDING',(0,1),(-1,-1),7),
           ('BOTTOMPADDING',(0,1),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.5,HexColor(NAVY)),
           ('LINEBELOW',(0,-1),(-1,-1),.5,HexColor(NAVY))]))
        items.extend([table,Spacer(1,18),Paragraph('All five entries use Tucumcari\'s 8310 billing code. Santa Rosa shares the arrangement with the smaller stations. The table describes administration; it does not count shipments.',side_style)])
        caption='Figure 6.3. Headings, corridor rows and symbol legend from C 15 / PDF p. 67, with a selected transcription below. Intervening and surrounding rows are omitted; source markings are retained. The asterisk means no agent is listed. An unmarked entry is not a verified payroll. Source: Rock Island Station Book; chapter note 17. Retained codes do not prove usable stockyards or livestock traffic.'
    elif key=='chronology':
        title='Connections changed at different dates'
        items=[pic(key,410)]
        caption='Figure 6.4. Selected observations, 1952-1974. Brown spans bracket a disappearance between inspected records; they do not show the duration of an event. The navy span is the reported interstate construction interval; points identify dated changes or a listing. Freight traffic and payroll end dates remain unestablished. Sources: highway nomination, timetables, NTSB, Congressional Record and Rock Island Station Book; chapter notes 8 and 12-17, 21.'
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
    story.extend([PageBreak(),Paragraph('Working source notes',head_style),Paragraph('Draft 1 / September 28, 2026. Held railway, road, census and commercial sources; selected original pages reread. Dated observations and proposed mechanisms remain distinct. Source coverage and reproducible calculations accompany the manuscript.',caption_style)])
    for block in notes.split('\n\n'):
        match=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
        if match:
            number,content=match.groups();story.append(KeepTogether([Paragraph(f'<a name="note{number}"/><b>{number}.</b> '+markup(content),note_style)]))
    doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=TOP,bottomMargin=BOTTOM,
      title='Cuervo | Chapter 6: Changing the connections',author='Meridian',subject='Chapter 6, draft 1, September 28, 2026')
    doc.build(story,onFirstPage=cover,onLaterPages=running_for(SPEC))
    reader=PdfReader(OUT);plain=re.sub(r'<!--.*?-->','',body,flags=re.S);plain=re.sub(r'^#+.*$','',plain,flags=re.M)
    report={'chapter':6,'source':str(SRC),'output':str(OUT),'body_words':len(re.sub(r'\[\^\d+\]','',plain).split()),
       'pages':len(reader.pages),'note_definitions':len(defs),'note_references':len(refs),'figure_positions':4,
       'missing_local_links':missing,'all_note_references_resolve':True,
       'page_word_counts':[len((p.extract_text() or '').split()) for p in reader.pages],
       'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/'chapter-06-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':build()
