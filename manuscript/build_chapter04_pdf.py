"""Build Chapter 4 alone, using the established Meridian proof typography."""
from pathlib import Path
import re, json, hashlib, sys
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from pypdf import PdfReader
from build_chapters02_03_pdf import (ROOT, W, H, MARGIN, TOP, BOTTOM, NAVY, INK, GRAY,
    tracked, markup, running_for, body_style, lead_style, head_style, note_style,
    caption_style, figure_title)

QA=ROOT/'tmp/pdfs/chapter04-draft01'
FIG=ROOT/'manuscript/figures/chapter04'
OUT=ROOT/'output/pdf/cuervo-chapter-04-keeping-a-town-working.pdf'
SRC=ROOT/'manuscript/chapter-04-keeping-a-town-working.md'
SPEC={'number':4,'word':'FOUR','title':'Keeping a town working'}
label_style=ParagraphStyle('PlateLabel',fontName='Label',fontSize=8.5,leading=11,
                           textColor=HexColor(NAVY),spaceAfter=9)
side_style=ParagraphStyle('PlateSide',fontName='Garamond',fontSize=12,leading=16,
                          textColor=HexColor(INK),spaceAfter=14)

def cover(c,doc):
    c.saveState();c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    tracked(c,'CUERVO',48,778);tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    tracked(c,'CHAPTER FOUR',48,726,8,NAVY,2.1)
    for y,text,font,size in [(660,'Keeping','Display',54),(592,'a town','GaramondItalic',64),(524,'working','GaramondItalic',64)]:
        c.setFont(font,size);c.setFillColor(HexColor(NAVY if font=='GaramondItalic' else INK));c.drawString(45,y,text)
    p=Paragraph('The people, money and organization behind local services.',
        ParagraphStyle('Deck4',fontName='GaramondItalic',fontSize=20,leading=25,textColor=HexColor(NAVY)))
    _,height=p.wrap(410,90);p.drawOn(c,48,428-height)
    c.setStrokeColor(HexColor(NAVY));c.setLineWidth(.6);c.line(48,316,528,316)
    for i,(year,label) in enumerate([('1919','A teacher leaves; instruction is interrupted'),('1921','Plans for school support and a local doctor'),('1922','A publisher explains her withdrawal')]):
        yy=280-i*44;c.setFont('GaramondItalic',19);c.setFillColor(HexColor(NAVY));c.drawString(48,yy,year)
        c.setFont('Label',10.3);c.setFillColor(HexColor(INK));c.drawString(125,yy+1,label)
    p=Paragraph('Services had different requirements for continuation. These records identify appointments, proposals and decisions, each with its own outcome to establish.',caption_style)
    _,height=p.wrap(430,70);p.drawOn(c,48,132-height)
    tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
    tracked(c,'READING PROOF / DRAFT 1 / 28 SEPTEMBER 2026',48,45,6.7,spacing=1)
    c.restoreState()

def pic(name,width):
    path=FIG/f'{name}.png'
    with PILImage.open(path) as im: height=width*im.height/im.width
    result=Image(str(path),width=width,height=height);result.hAlign='CENTER'
    return result

def columns(left,right,widths=(173,18,173)):
    table=Table([[left,'',right]],colWidths=list(widths),hAlign='CENTER')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                              ('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),
                              ('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    return table

def plate(key):
    if key=='school-staff-and-care':
        title='Staff and upkeep'
        items=[columns([Paragraph('JANUARY 1919 / INSTRUCTION',label_style),pic('teacher-notice',173)],
                       [Paragraph('SEPTEMBER 1921 / PREMISES',label_style),pic('school-conditions-reading',173)]),
               Spacer(1,28),Paragraph('One service, several requirements',side_style),
               Paragraph('The first notice offers a replacement for a departed teacher. The second records proposals for maintaining the schoolhouse and grounds. Both concern work needed to keep the institution useful.',side_style)]
        caption='Figure 4.1. Cuervo Clipper, January 10, 1919 and September 9, 1921, front-page details. Miss Sanchez announced that she would teach ninth grade; the later committee recommended cleaning, repairs and precautions. The notices do not establish when instruction resumed or which improvements were completed. Sources: held UNM scans; chapter notes 1 and 6. Cropped excerpts, reproduced at different scales without retouching.'
    elif key=='school-parcel':
        title='The institution and its property'
        items=[pic('school-overview',370),Spacer(1,16),Paragraph('DETAIL / BUILDING FOOTPRINT AND DEED REFERENCES',label_style),pic('school-footprint',370)]
        caption='Figure 4.2. School boundary survey C-232, December 2010. The sheet identifies a 2.0661-acre parcel; the enlarged detail labels the District No. 6 masonry school and cites earlier deeds. The survey preserves the property record after ordinary teaching had ended. It does not establish the construction date or connect this footprint to the 1912 school. Source: Guadalupe County packet; chapter note 7. Cropped sheet and enlarged detail; source orientation retained.'
    elif key=='doctor-support':
        title='Paying for availability'
        items=[columns([pic('doctor-proposal',166)],
            [Paragraph('FEBRUARY 1921 / A PROPOSAL',label_style),
             Paragraph('W. B. Terry of Newkirk proposed a monthly contribution from families, including in months when they needed no treatment.',side_style),
             Paragraph('A dollar per family would be about $18 in 2025 purchasing power. His hoped-for hundred families implied about $1,800 a month.',side_style),
             Paragraph('The report identifies an attempt to organize dependable support. It supplies no collected fund, medical appointment or agreed treatment fees.',side_style)],(166,25,173))]
        caption='Figure 4.3. Cuervo Clipper, February 11, 1921, front-page detail, "Doctor Wanted." The proposed locality and contributor pool should not be equated with Cuervo resident households. Sources: held UNM scan; chapter notes 9-10. Column cropped from the original page; no retouching.'
    elif key=='newspaper-purpose':
        title='Scale, subsidy and purpose'
        items=[columns([Paragraph('THE CASE FOR A COUNTY PAPER',label_style),pic('hicks-scale',144)],
                       [Paragraph('THE PURPOSE OF THE INVESTMENT',label_style),pic('hicks-purpose',166)],(168,28,168))]
        caption='Figure 4.4. Two excerpts from Katharine A. Hicks, "To My Clipper Readers," December 1, 1922. At left, she explains her withdrawal and argues for a first-class county weekly. At right, she treats the financial loss as a campaign contribution after the political objectives were achieved. Her account combines financial and political purposes. Source: held UNM scan; chapter note 13. Noncontiguous excerpts at different scales; no retouching.'
    else: raise ValueError(key)
    return [PageBreak(),Paragraph(title,figure_title),Spacer(1,7),*items,Spacer(1,16),Paragraph(caption,caption_style),PageBreak()]

def build():
    text=SRC.read_text(encoding='utf-8');body,notes=text.split('\n---\n',1)
    refs=re.findall(r'\[\^(\d+)\]',body);definitions=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    assert set(refs)==set(definitions) and len(definitions)==len(set(definitions))
    assert list(dict.fromkeys(refs))==definitions,'Notes must follow first appearance.'
    missing=[p for p in re.findall(r'\]\((B:/[^)]+)\)',text) if not Path(p).exists()]
    assert not missing,missing
    clean=re.sub(r'<!--(?! FIGURE:).*?-->','',body,flags=re.S)
    blocks=[b.strip() for b in clean.split('\n\n') if b.strip() and not b.startswith('# ')]
    story=[Spacer(1,H-TOP-BOTTOM-15),PageBreak()];first=True
    for block in blocks:
        fig=re.fullmatch(r'<!-- FIGURE: ([\w-]+) -->',block)
        if fig: story.extend(plate(fig.group(1)))
        elif block.startswith('## '):story.append(Paragraph(markup(block[3:]),head_style))
        else:story.append(Paragraph(markup(block),lead_style if first else body_style));first=False
    story.extend([PageBreak(),Paragraph('Working source notes',head_style),Paragraph('Draft 1 / September 28, 2026. Sources, page locators and consequential limits. New readings of held pages are distinguished from prior checked readings. Proposals and announced visits remain distinct from implemented services.',caption_style)])
    for block in notes.split('\n\n'):
        match=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
        if match:
            number,content=match.groups();story.append(KeepTogether([Paragraph(f'<a name="note{number}"/><b>{number}.</b> '+markup(content),note_style)]))
    doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=TOP,bottomMargin=BOTTOM,
        title='Cuervo | Chapter 4: Keeping a town working',author='Meridian',subject='Chapter 4, draft 1, September 28, 2026')
    doc.build(story,onFirstPage=cover,onLaterPages=running_for(SPEC))
    reader=PdfReader(OUT);plain=re.sub(r'<!--.*?-->','',body,flags=re.S);plain=re.sub(r'^#+.*$','',plain,flags=re.M)
    report={'chapter':4,'source':str(SRC),'output':str(OUT),'body_words':len(re.sub(r'\[\^\d+\]','',plain).split()),
        'pages':len(reader.pages),'note_definitions':len(definitions),'note_references':len(refs),'figure_positions':4,
        'missing_local_links':missing,'all_note_references_resolve':True,
        'page_word_counts':[len((p.extract_text() or '').split()) for p in reader.pages],
        'pdf_annotations':sum(len(p.get('/Annots',[])) for p in reader.pages),
        'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/'chapter-04-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':build()
