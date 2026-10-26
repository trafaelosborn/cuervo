"""Revision 6 figure overrides; older editions remain reproducible."""
from pathlib import Path
from PIL import Image as PILImage
from reportlab.platypus import Paragraph,PageBreak,Spacer,Image,Table,TableStyle
from build_chapters02_03_pdf import ROOT,figure_title,caption_style
from book_visuals_revision03 import SPECS
FIG=ROOT/'manuscript/figures/book-revision06'
KEYS={'santa-rosa-map','population-and-age','regional-households','functional-chronology','chronology'}
def pic(name,width):
    p=FIG/f'{name}.png'
    with PILImage.open(p) as im:h=width*im.height/im.width
    o=Image(str(p),width=width,height=h);o.hAlign='CENTER';return o
def figure(key):
    if key=='santa-rosa-map':
        title='A regional center before Route 66'
        items=[pic('santa-rosa-full',145),Spacer(1,12)]
        for name,label,detail in [('warehouse','WHOLESALE WAREHOUSE','Charles Ilfeld Co.: groceries and farm implements, beside a spur track.'),('station','RAILWAY STATION','The station appears in the separate upper-right area of the sheet.'),('bank','BANK ON PARKER AVENUE','The bank shares a frontage with general merchandise.')]:
            row=Table([[pic('santa-rosa-'+name,215),Paragraph('<b>'+label+'</b><br/>'+detail,caption_style)]],colWidths=[232,195],hAlign='CENTER')
            row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
            items.extend([row,Spacer(1,9)])
        caption='Figure 2.2. Santa Rosa, December 1908, Sanborn sheet 1: full-sheet overview and three separately enlarged details. Insets are displaced; the details do not form a continuous street plan. Original map marks are retained. Source: Library of Congress, Geography and Map Division, Sanborn Maps collection; chapter note 10.'
    elif key=='population-and-age':
        title='Population and age changed together';items=[pic(key,410)]
        caption='Figure 5.1. Cuervo precinct, 1910–1950: five reported populations and medians calculated from the named schedules. Points are not an annual series or constant-boundary estimates. Age ranges allow for seven unread entries across the five censuses; they are not confidence intervals. The 1950 median is 25.5. Sources: U.S. Census and the author’s transcription; chapter notes 2–5.'
    elif key=='regional-households':
        title='Growth has different components';items=[pic(key,440)]
        caption='Figure 5.4. Santa Rosa municipal population at five censuses, 1980–2020. Stacked bars separate household residents from group-quarters residents; labels give totals. Municipal boundaries can change. Subtracting institutional residents does not estimate the city without its institutions. Sources: U.S. Census; chapter notes 20–21.'
    elif key=='functional-chronology':
        title=SPECS[key]['title'];items=[pic(key,450)];caption=SPECS[key]['caption']
    else:
        title='Connections changed at different dates';items=[pic(key,410)]
        caption='Figure 6.4. Selected observations, 1952–1974. Brown spans bracket a disappearance between inspected records; the navy span records interstate construction. Points mark dated changes or a listing. Local freight traffic and payroll end dates remain unestablished. Sources: highway nomination, timetables, NTSB, Congressional Record and station book; chapter notes 8, 12–17 and 21.'
    return [PageBreak(),Paragraph(title,figure_title),Spacer(1,8),*items,Spacer(1,13),Paragraph(caption,caption_style),PageBreak()]
