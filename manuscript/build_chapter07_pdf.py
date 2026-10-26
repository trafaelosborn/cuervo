"""Build Chapter 7 alone, with original vector figures and established Meridian typography."""
from pathlib import Path
import re, json, hashlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from pypdf import PdfReader
from build_chapters02_03_pdf import (ROOT,W,H,MARGIN,TOP,BOTTOM,NAVY,INK,GRAY,tracked,markup,running_for,
    body_style,lead_style,head_style,note_style,caption_style,figure_title)

QA=ROOT/'tmp/pdfs/chapter07-draft01'; QA.mkdir(parents=True,exist_ok=True)
EVIDENCE=ROOT/'research_evidence/chapter07_2026-09-28'; EVIDENCE.mkdir(parents=True,exist_ok=True)
SRC=ROOT/'manuscript/chapter-07-explaining-the-cumulative-decline.md'
OUT=ROOT/'output/pdf/cuervo-chapter-07-explaining-the-cumulative-decline.pdf'
SPEC={'number':7,'word':'SEVEN','title':'Explaining the cumulative decline'}
label_style=ParagraphStyle('PlateLabel7',fontName='Label',fontSize=8,leading=11,textColor=HexColor(NAVY),spaceAfter=6)
cell_style=ParagraphStyle('PlateCell7',fontName='Garamond',fontSize=11.3,leading=14.5,textColor=HexColor(INK))
cell_head=ParagraphStyle('PlateHead7',fontName='GaramondItalic',fontSize=17,leading=20,textColor=HexColor(NAVY))

SUPPORT=[
    {'activity':'Merchant','date':'1904–1915 / 1958','requirement':'Transactions with the surrounding country, across several lines of business.',
     'observation':'Positive net profits in twelve supplied annual accounts; business still operating in 1958.',
     'limit':'Shared-cost savings and the final closure are unmeasured.','note':2},
    {'activity':'Ninth grade','date':'1919','requirement':'Someone able to teach the pupils.',
     'observation':'Interruption after Simmons left; Sanchez announced that she would take the pupils.',
     'limit':'Reason for departure and actual resumption are unknown.','note':5},
    {'activity':'Resident physician','date':'1921 / PROPOSAL','requirement':'Dependable support between individual occasions of illness.',
     'observation':'Terry proposed monthly contributions from one hundred families across a locality.',
     'limit':'Subscriptions and recruitment are not established.','note':6},
    {'activity':'Newspaper','date':'1922','requirement':'Revenue or a backer willing to sustain losses for another purpose.',
     'observation':'Hicks explained financial withdrawal in commercial and political terms.',
     'limit':'Her account does not establish the final issue date.','note':7},
]

def cover(c,doc):
    c.saveState(); c.setFillColor(white); c.rect(0,0,W,H,fill=1,stroke=0)
    tracked(c,'CUERVO',48,778); tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
    tracked(c,'CHAPTER SEVEN',48,726,8,NAVY,2.1)
    for y,text,font,size in [(660,'Explaining','Display',54),(592,'the cumulative','GaramondItalic',57),(524,'decline','GaramondItalic',64)]:
        c.setFont(font,size); c.setFillColor(HexColor(NAVY if font=='GaramondItalic' else INK)); c.drawString(45,y,text)
    p=Paragraph('Markets, institutions and the changing reasons to maintain a town.',
      ParagraphStyle('Deck7',fontName='GaramondItalic',fontSize=20,leading=25,textColor=HexColor(NAVY)))
    _,height=p.wrap(410,90); p.drawOn(c,48,428-height)
    c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(.6); c.line(48,316,528,316)
    for i,(label,detail) in enumerate([('MARKETS','Demand beyond the village population'),('SUPPORT','Different requirements for each service'),('FEEDBACK','How changes could reinforce one another')]):
        yy=280-i*44; tracked(c,label,48,yy+2,8,NAVY,1.1)
        c.setFont('Garamond',13); c.setFillColor(HexColor(INK)); c.drawString(149,yy,detail)
    p=Paragraph('A synthesis of the historical evidence and established economics. Cumulative contraction, uneven adaptation and the limits of a universal survival threshold.',caption_style)
    _,height=p.wrap(430,70); p.drawOn(c,48,132-height)
    tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
    tracked(c,'READING PROOF / DRAFT 1 / 28 SEPTEMBER 2026',48,45,6.7,spacing=1)
    c.restoreState()

class Feedback(Flowable):
    """A qualitative diagram: arrows carry no fitted weight or causal estimate."""
    def __init__(self):
        Flowable.__init__(self); self.width=410; self.height=458; self.hAlign='CENTER'
    def draw(self):
        c=self.canv
        def paragraph(text,x,top,width,style):
            p=Paragraph(text,style); _,height=p.wrap(width,200); p.drawOn(c,x,top-height); return height
        def box(y,title,body):
            c.setFillColor(HexColor('#eff2f5')); c.rect(0,y,410,86,fill=1,stroke=0)
            paragraph(title,18,y+69,374,cell_head)
            paragraph(body,18,y+42,374,cell_style)
        box(342,'Local provision','Shops, schooling, professional services and jobs')
        box(146,'Households and transactions','Residence, visits, purchases and institutional support')
        c.setStrokeColor(HexColor(NAVY)); c.setFillColor(HexColor(NAVY)); c.setLineWidth(1.1); c.setDash(4,4)
        c.line(38,327,38,247); c.line(371,247,371,327); c.setDash()
        for x,y,up in [(38,247,False),(371,327,True)]:
            p=c.beginPath(); p.moveTo(x,y); p.lineTo(x-4,y-8 if up else y+8); p.lineTo(x+4,y-8 if up else y+8); p.close(); c.drawPath(p,fill=1,stroke=0)
        paragraph('Can attract or retain households and visits',57,304,132,cell_style)
        paragraph('Can support receipts, staffing and contributions',212,304,142,cell_style)
        paragraph('OBSERVED RELATIONSHIP',0,122,410,label_style)
        paragraph('Schooling attracted households in 1910 and 1912. The later reverse sequence has not been traced in full.',0,104,410,cell_style)
        c.setStrokeColor(HexColor(NAVY)); c.setLineWidth(.4); c.line(0,58,410,58)
        paragraph('Responses can interrupt the loop: travel, delivery, replacement staff or new backing.',0,43,410,cell_style)

def figure(key):
    if key=='support':
        title='Different requirements for staying open'
        rows=[[Paragraph('ACTIVITY / DATE',label_style),Paragraph('SUPPORT AND OBSERVATION',label_style)]]
        for item in SUPPORT:
            left=[Paragraph(item['activity'],cell_head),Spacer(1,6),Paragraph(item['date'],label_style)]
            right=[Paragraph(item['requirement'],cell_style),Spacer(1,7),Paragraph(item['observation'],cell_style),Spacer(1,6),
                Paragraph(item['limit'],ParagraphStyle('Limit'+str(item['note']),parent=caption_style,fontSize=9,leading=11.5))]
            rows.append([left,right])
        table=Table(rows,colWidths=[125,285],hAlign='CENTER')
        table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
            ('RIGHTPADDING',(0,0),(0,-1),14),('RIGHTPADDING',(1,0),(1,-1),0),
            ('TOPPADDING',(0,1),(-1,-1),14),('BOTTOMPADDING',(0,1),(-1,-1),14),
            ('LINEBELOW',(0,0),(-1,0),.6,HexColor(NAVY)),('LINEBELOW',(0,1),(-1,-1),.35,HexColor('#bbc3cb'))]))
        items=[table]
        caption='Figure 7.1. Selected service arrangements. The rows compare sources of support and observed decisions, not financial performance on a common scale. A proposal, an announcement and a completed withdrawal have different evidential status. Sources: Grubbs and the Cuervo Clipper; chapter notes 2 and 5-7.'
    elif key=='feedback':
        title='A possible reinforcing relationship'
        items=[Feedback()]
        caption='Figure 7.2. Qualitative illustration of interaction between provision and local activity. Dashed arrows show possible responses, not estimated effects or a complete documented cascade. School-related moves establish one historical relationship; later travel and replacement arrangements could weaken the feedback. Sources and limits: chapter notes 16-18. This is not a fitted economic model.'
    else: raise ValueError(key)
    return [PageBreak(),Paragraph(title,figure_title),Spacer(1,8),*items,Spacer(1,15),Paragraph(caption,caption_style),PageBreak()]

def build():
    text=SRC.read_text(encoding='utf-8'); body,notes=text.split('\n---\n',1)
    refs=re.findall(r'\[\^(\d+)\]',body); defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    assert defs==list(dict.fromkeys(refs))==[str(i+1) for i in range(len(defs))]
    missing=[p for p in re.findall(r'\]\((B:/[^)]+)\)',text) if not Path(p).exists()]; assert not missing,missing
    blocks=[b.strip() for b in body.split('\n\n') if b.strip() and not b.startswith('# ')]
    story=[Spacer(1,H-TOP-BOTTOM-15),PageBreak()]; first=True
    for block in blocks:
        fig=re.fullmatch(r'<!-- FIGURE: ([\w-]+) -->',block)
        if fig: story.extend(figure(fig.group(1)))
        elif block.startswith('## '): story.append(Paragraph(markup(block[3:]),head_style))
        else: story.append(Paragraph(markup(block),lead_style if first else body_style)); first=False
    story.extend([PageBreak(),Paragraph('Working source notes',head_style),Paragraph('Draft 1 / September 28, 2026. Historical findings are drawn from the preceding chapters and checked source registers. Selected primary economic texts were reread for the synthesis. Analytical illustrations remain distinct from measured local effects.',caption_style)])
    for block in notes.split('\n\n'):
        match=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
        if match:
            number,content=match.groups(); story.append(KeepTogether([Paragraph(f'<a name="note{number}"/><b>{number}.</b> '+markup(content),note_style)]))
    doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,topMargin=TOP,bottomMargin=BOTTOM,
      title='Cuervo | Chapter 7: Explaining the cumulative decline',author='Meridian',subject='Chapter 7, draft 1, September 28, 2026')
    doc.build(story,onFirstPage=cover,onLaterPages=running_for(SPEC))
    reader=PdfReader(OUT); plain=re.sub(r'<!--.*?-->','',body,flags=re.S); plain=re.sub(r'^#+.*$','',plain,flags=re.M)
    report={'chapter':7,'source':str(SRC),'output':str(OUT),'body_words':len(re.sub(r'\[\^\d+\]','',plain).split()),
       'pages':len(reader.pages),'note_definitions':len(defs),'note_references':len(refs),'figure_positions':2,
       'missing_local_links':missing,'all_note_references_resolve':True,
       'page_word_counts':[len((p.extract_text() or '').split()) for p in reader.pages],
       'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/'chapter-07-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (EVIDENCE/'figure-data.json').write_text(json.dumps({'support':SUPPORT,'feedback':{'kind':'qualitative; no numerical data or fitted parameters',
        'observed':'Schooling attracted households, 1910 and 1912','conditional':'Both dashed arrows; no full later cascade established',
        'interruptions':['travel','delivery','replacement staff','new backing'],'notes':[16,17,18]}},indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': build()
