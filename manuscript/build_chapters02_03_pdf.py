"""Build Meridian reading proofs for Chapters 2-3 from their Markdown sources."""
from pathlib import Path
import sys
import os
import html
import json
import re
import hashlib
_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_root / 'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR', str(_root / 'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
from source_plates import plate

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'tmp/pdfs/rewrite-2026-09-28'
FIG = ROOT / 'manuscript/figures/chapters02-03'
OUT = ROOT / 'output/pdf'
for folder in [QA, FIG, OUT]:
    folder.mkdir(parents=True, exist_ok=True)

NAVY, INK, GRAY, RULE = '#1b3558', '#242528', '#756e65', '#c9c2b8'
for name, file in [('Garamond','GARA.TTF'),('GaramondItalic','GARAIT.TTF'),
                   ('GaramondBold','GARABD.TTF'),('Display','BASKVILL.TTF'),
                   ('Label','calibri.ttf')]:
    font_path=Path('C:/Windows/Fonts')/file
    if os.environ.get('CUERVO_PORTABLE_FONTS')=='1' or not font_path.exists():
        portable={'Garamond':'Jost-Regular.ttf','GaramondItalic':'Jost-Italic-Regular.ttf',
                  'GaramondBold':'Jost-Semibold.ttf','Display':'PlayfairDisplay-Bold.ttf','Label':'Jost-Regular.ttf'}
        font_path=ROOT/'manuscript/fonts/revision07'/portable[name]
    pdfmetrics.registerFont(TTFont(name,str(font_path)))
pdfmetrics.registerFontFamily('Garamond',normal='Garamond',bold='GaramondBold',
                             italic='GaramondItalic',boldItalic='GaramondItalic')
W,H=576,816
MARGIN, TOP, BOTTOM=105,75,75
TEXT_W=W-2*MARGIN

def normalize(s):
    return s.replace('\u2013','-').replace('\u2014',' - ').replace('\u2011','-')

def markup(s):
    links=[]
    def save(m):
        label,url=m.groups()
        label=html.escape(normalize(label))
        # Keep local-source labels readable. Online source links remain clickable.
        if url.startswith('https://'):
            label=f'<link href="{html.escape(url,quote=True)}" color="{NAVY}">{label}</link>'
        links.append(label)
        return f'LINKPLACEHOLDER{len(links)-1}END'
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',save,s)
    s=html.escape(normalize(s))
    s=re.sub(r'\*([^*]+)\*',r'<i>\1</i>',s)
    s=re.sub(r'\[\^(\d+)\]',r'<super><link href="#note\1" color="'+NAVY+r'">\1</link></super>',s)
    s=s.replace('</link></super><super><link','</link></super><super>,</super><super><link')
    for n,link in enumerate(links): s=s.replace(f'LINKPLACEHOLDER{n}END',link)
    return s

body_style=ParagraphStyle('Body',fontName='Garamond',fontSize=12.2,leading=16.5,
                          textColor=HexColor(INK),spaceAfter=8.2,allowWidows=0,allowOrphans=0)
lead_style=ParagraphStyle('Lead',parent=body_style,fontSize=16,leading=21.5,
                          spaceAfter=19,textColor=HexColor(NAVY))
head_style=ParagraphStyle('Section',fontName='GaramondItalic',fontSize=23,leading=28,
                          textColor=HexColor(NAVY),spaceBefore=23,spaceAfter=13,keepWithNext=True)
note_style=ParagraphStyle('Note',fontName='Garamond',fontSize=10.1,leading=13.3,
                          textColor=HexColor(INK),spaceAfter=9,allowWidows=0,allowOrphans=0)
caption_style=ParagraphStyle('Caption',fontName='Label',fontSize=9,leading=12,
                             textColor=HexColor(GRAY),spaceAfter=14)
figure_title=ParagraphStyle('FigureTitle',parent=head_style,fontSize=21,leading=25,spaceBefore=0)

def chart_style(ax):
    ax.spines[['top','right','left']].set_visible(False)
    ax.spines['bottom'].set_color(RULE)
    ax.tick_params(axis='both',labelsize=9,colors=INK,length=0,pad=6)
    ax.grid(axis='y',color='#e8e4df',linewidth=.6)
    ax.set_axisbelow(True)

def make_figures():
    data=json.loads((ROOT/'research_evidence/monetary_revision_2026-09-28/calculations.json').read_text())
    def series(key):
        return [[r['year'],r['constant_2025_thousands']] for r in data['series'][key]]
    merchandise=series('table_32')
    sheep=series('table_34')
    profit=series('table_35')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,1,figsize=(7,6.4),layout='constrained')
    for ax in axes: chart_style(ax)
    axes[0].plot([r[0] for r in merchandise],[r[1] for r in merchandise],color=NAVY,
                 marker='o',markersize=3,linewidth=1.7,label='Merchandise inventory')
    axes[0].plot([r[0] for r in sheep],[r[1] for r in sheep],color='#9c7151',
                 marker='s',markersize=3,linewidth=1.7,label='Sheep investment')
    axes[0].set_title('Resources held at year end',loc='left',fontsize=12,color=NAVY,pad=12)
    axes[0].set_ylabel('2025 dollars, thousands',fontsize=10)
    axes[0].legend(frameon=False,fontsize=9,loc='upper left')
    axes[0].set_xticks([1903,1905,1907,1909,1911,1913,1915])
    axes[1].bar([r[0] for r in profit],[r[1] for r in profit],color=NAVY,width=.64)
    axes[1].set_title('Reported annual company net profit',loc='left',fontsize=12,color=NAVY,pad=12)
    axes[1].set_ylabel('2025 dollars, thousands',fontsize=10)
    axes[1].set_xticks([1904,1906,1908,1910,1912,1914,1915])
    axes[0].set_ylim(0,1400)
    axes[1].set_ylim(0,700)
    assert max(r[1] for r in merchandise+sheep) < axes[0].get_ylim()[1]
    assert max(r[1] for r in profit) < axes[1].get_ylim()[1]
    for extension in ['png','svg']:
        fig.savefig(FIG/f'merchant-finance.{extension}',dpi=300,facecolor='white')
    plt.close(fig)
    ag=json.loads((ROOT/'research_evidence/economic_synthesis_2026-09-23/agriculture_transcription.json').read_text())
    rows=ag['series']
    fig,ax=plt.subplots(figsize=(7,4.5),layout='constrained')
    chart_style(ax)
    # Separate markers show the seven actual observations; no annual interpolation.
    ax.scatter([r['year'] for r in rows],[r['sheep_lambs_head']/1000 for r in rows],
               color='#9c7151',marker='s',s=42,label='Sheep and lambs')
    ax.scatter([r['year'] for r in rows],[r['cattle_head']/1000 for r in rows],
               color=NAVY,marker='o',s=42,label='Cattle and calves')
    ax.set_ylabel('Head, thousands',fontsize=10)
    ax.set_xticks([r['year'] for r in rows])
    ax.set_xlim(1928,1961)
    ax.set_ylim(0,110)
    ax.legend(frameon=False,loc='upper right',fontsize=10)
    for extension in ['png','svg']:
        fig.savefig(FIG/f'county-livestock.{extension}',dpi=300,facecolor='white')
    plt.close(fig)
    manifest={'financial_source':'research_evidence/origins_followup_2026-09-23/financial_transcription.json',
              'agriculture_source':'research_evidence/economic_synthesis_2026-09-23/agriculture_transcription.json',
              'financial_units':'Thousands of 2025 consumer-purchasing-power dollars; year-end balances and annual net profit in separate panels.',
              'financial_calculations':'research_evidence/monetary_revision_2026-09-28/calculations.json',
              'agriculture_units':'Guadalupe County head counts, thousands; seven discrete observations, not Cuervo totals.',
              'agriculture_limits':'Inventory dates and definitions vary; 1930 cattle exclude animals under 3 months.'}
    (FIG/'sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

def tracked(c,text,x,y,size=8,color=GRAY,spacing=1.6):
    c.saveState()
    obj=c.beginText(x,y);obj.setFont('Label',size);obj.setFillColor(HexColor(color))
    obj.setCharSpace(spacing);obj.textLine(text);c.drawText(obj)
    c.restoreState()

CHAPTERS=[
    {'number':2,'word':'TWO','title':'Why a town here?', 'slug':'why-a-town-here',
     'display':[('Why a','Display',54),('town here?','GaramondItalic',64)],
     'deck':'How a railway location brought together an economy already at work.',
     'labels':[('1899','The predecessor store at Cabra'),('1903','Premises and a warehouse at Cuervo'),('1904','Bond & Wiest incorporated')],
     'cover_note':'Formation was a sequence of commitments. Dates refer to the merchant, not a single founding event for the town.'},
    {'number':3,'word':'THREE','title':'The business of ranch country','slug':'the-business-of-ranch-country',
     'display':[('The business','Display',43),('of ranch','GaramondItalic',57),('country','GaramondItalic',62)],
     'deck':'Goods, credit, livestock and the work that a small town could retain.',
     'labels':[('1904-1915','Twelve positive reported net-profit years'),('1947','Bond & Wiest listed as a feed dealer'),('1958','The Cuervo business still operating')],
     'cover_note':'A durable business within a changing economy. The observations do not establish uninterrupted profitability.'}
]

def cover_for(spec):
    def cover(c,doc):
        c.saveState();c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
        tracked(c,'CUERVO',48,778)
        tracked(c,'MERIDIAN',452,778,7.2,spacing=1.2)
        tracked(c,'CHAPTER '+spec['word'],48,726,8,NAVY,2.1)
        y=660
        for line,font,size in spec['display']:
            c.setFont(font,size);c.setFillColor(HexColor(NAVY if font=='GaramondItalic' else INK))
            c.drawString(45,y,line);y-=68
        p=Paragraph(spec['deck'],ParagraphStyle('Deck',fontName='GaramondItalic',fontSize=20,
                                               leading=25,textColor=HexColor(NAVY)))
        _,height=p.wrap(410,90);p.drawOn(c,48,428-height)
        c.setStrokeColor(HexColor(NAVY));c.setLineWidth(.6);c.line(48,316,528,316)
        for index,(date,label) in enumerate(spec['labels']):
            yy=280-index*44
            c.setFont('GaramondItalic',19);c.setFillColor(HexColor(NAVY));c.drawString(48,yy,date)
            c.setFont('Label',10.3);c.setFillColor(HexColor(INK));c.drawString(157,yy+1,label)
        p=Paragraph(spec['cover_note'],caption_style)
        _,height=p.wrap(430,70);p.drawOn(c,48,132-height)
        tracked(c,'HISTORY / ECONOMICS',48,73,8,INK,1.8)
        tracked(c,'READING PROOF / DRAFT 2 / 28 SEPTEMBER 2026',48,45,6.7,spacing=1)
        c.restoreState()
    return cover

def running_for(spec):
    def running(c,doc):
        c.saveState();c.setStrokeColor(HexColor(RULE));c.setLineWidth(.4);c.line(48,768,W-48,768)
        tracked(c,'CUERVO',48,779,7,spacing=1.5)
        c.setFont('Label',7.5);c.setFillColor(HexColor(GRAY));c.drawRightString(W-48,779,spec['title'].upper())
        tracked(c,'CHAPTER '+spec['word'],48,40,6.6,spacing=1.3)
        c.setFont('Garamond',10);c.drawRightString(W-48,39,str(doc.page));c.restoreState()
    return running

def figure_block(key):
    if key in {'cuervo-map','trade-notices'}:
        return plate(key,figure_title,caption_style)
    if key=='santa-rosa-map':
        path=ROOT/'sources/06_maps/sanborn_santa_rosa_1908_sheet_01.jpg'
        title='A regional center before Route 66'
        caption='Figure 2.2. Santa Rosa, December 1908, Sanborn sheet 1. The rail-side wholesale warehouse appears in the upper-left inset; the station is at upper right. A bank and general stores face Parker Avenue. Insets are displaced and should not be read as one continuous street plan. Source: Library of Congress, Geography and Map Division, Sanborn Maps collection; chapter note 10. Full sheet reproduced without retouching.'
        width=390
    elif key=='merchant-finance':
        path=FIG/'merchant-finance.png';width=410
        title='Recovery and a changing business mix'
        caption='Figure 3.1. Bond & Wiest, 1903-1915. The upper panel compares year-end balances; the lower shows annual company net profit. Values are expressed in 2025 consumer purchasing power; the original sums were rounded in Grubbs. Balances and annual profits are not additive. Sources: Grubbs, Tables 32, 34 and 35; Minneapolis Fed historical CPI. Chapter notes 1, 2 and 7. Lines join supplied annual balances only.'
    elif key=='county-livestock':
        path=FIG/'county-livestock.png';width=410
        title='Two livestock histories'
        caption='Figure 3.2. Guadalupe County cattle and sheep inventories, 1930-1959. Markers show seven census observations, not an annual series or Cuervo totals. Inventory dates and coverage vary; 1930 cattle exclude animals under three months. Head counts are not equivalent units of output or grazing demand. Source: agricultural censuses; chapter note 20.'
    elif key=='cattle-price-cycle':
        path=ROOT/'manuscript/figures/revision-2026-09-28/cattle-price-cycle.png';width=410
        title='The cattle-price cycle'
        caption='Figure 3.3. New Mexico prices received for beef cattle, 1913-1978. All 66 annual observations are adjusted for consumer prices and indexed to 1951 = 100. Purchasing power per unit sold rose about 81% in 1939-1949, fell about 52% in 1951-1956 and approached the earlier peak in 1973. State averages per 100 lb liveweight, excluding calves; these are not ranch profits or Cuervo transactions. Sources: USDA Statistical Bulletins 265 and 680; BLS annual CPI-U. Chapter note 26.'
    else: raise ValueError(key)
    with PILImage.open(path) as im: height=width*im.height/im.width
    image=Image(str(path),width=width,height=height)
    image.hAlign='CENTER'
    return [PageBreak(),Paragraph(title,figure_title),Spacer(1,7),image,
            Spacer(1,14),Paragraph(caption,caption_style),PageBreak()]

def build(spec):
    src=ROOT/f"manuscript/chapter-{spec['number']:02d}-{spec['slug']}.md"
    output=OUT/f"cuervo-chapter-{spec['number']:02d}-{spec['slug']}.pdf"
    text=src.read_text(encoding='utf-8')
    body,notes=text.split('\n---\n',1)
    refs=re.findall(r'\[\^(\d+)\]',body)
    definitions=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
    assert set(refs)==set(definitions) and len(definitions)==len(set(definitions))
    missing=[p for p in re.findall(r'\]\((B:/[^)]+)\)',text) if not Path(p).exists()]
    assert not missing,missing
    # Keep figure directives; omit the editorial draft comment and title lines.
    body=re.sub(r'<!--(?! FIGURE:).*?-->','',body,flags=re.S)
    blocks=[b.strip() for b in body.split('\n\n') if b.strip() and not b.startswith('# ')]
    story=[Spacer(1,H-TOP-BOTTOM-15),PageBreak()]
    first=True
    for block in blocks:
        figmatch=re.fullmatch(r'<!-- FIGURE: ([\w-]+) -->',block)
        if figmatch:
            story.extend(figure_block(figmatch.group(1)))
        elif block.startswith('## '): story.append(Paragraph(markup(block[3:]),head_style))
        else:
            story.append(Paragraph(markup(block),lead_style if first else body_style));first=False
    story.extend([PageBreak(),Paragraph('Working source notes',head_style),
                  Paragraph('Draft 2 / September 28, 2026. Sources, page locators and consequential limits. The chapter uses held documents and prior checked readings; original merchant manuscripts are distinguished from Grubbs\u2019s reconstruction.',caption_style)])
    for block in notes.split('\n\n'):
        match=re.match(r'\[\^(\d+)\]:\s*(.*)',block.strip(),re.S)
        if match:
            number,content=match.groups()
            story.append(KeepTogether([Paragraph(f'<a name="note{number}"/><b>{number}.</b> '+markup(content),note_style)]))
    doc=SimpleDocTemplate(str(output),pagesize=(W,H),leftMargin=MARGIN,rightMargin=MARGIN,
                          topMargin=TOP,bottomMargin=BOTTOM,title=f"Cuervo | Chapter {spec['number']}: {spec['title']}",
                          author='Meridian',subject=f"Chapter {spec['number']}, draft 2, September 28, 2026")
    doc.build(story,onFirstPage=cover_for(spec),onLaterPages=running_for(spec))
    reader=PdfReader(output)
    plain=re.sub(r'<!--.*?-->','',body,flags=re.S)
    plain=re.sub(r'^#+.*$','',plain,flags=re.M)
    words=len(re.sub(r'\[\^\d+\]','',plain).split())
    report={'chapter':spec['number'],'source':str(src),'output':str(output),'body_words':words,
             'pages':len(reader.pages),'note_definitions':len(definitions),'note_references':len(refs),
             'missing_local_links':missing,'all_note_references_resolve':True,
             'page_word_counts':[len((p.extract_text() or '').split()) for p in reader.pages],
             'pdf_annotations':sum(len(p.get('/Annots',[])) for p in reader.pages),
             'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'visual_review':'pending'}
    (QA/f"chapter-{spec['number']:02d}-build.json").write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    make_figures()
    print(json.dumps([build(spec) for spec in CHAPTERS],indent=2))
