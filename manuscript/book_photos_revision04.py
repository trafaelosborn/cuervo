"""Photography in chapter openings and generous full-frame picture pages."""
import json
from reportlab.platypus import Image,Paragraph,Spacer,PageBreak,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from build_chapters02_03_pdf import ROOT,caption_style,NAVY
DATA=json.loads((ROOT/'manuscript/figures/book-revision04-photos/sources.json').read_text(encoding='utf-8'))
photo_label=ParagraphStyle('PhotoLabel04',fontName='Label',fontSize=8,leading=11,textColor=HexColor(NAVY),spaceAfter=16)

def pic(name,width,maxheight=550):
    row=DATA['assets'][name];w,h=row['proof_pixels'];height=width*h/w
    if height>maxheight:width*=maxheight/height;height=maxheight
    result=Image(str(ROOT/row['proof_image']),width=width,height=height)
    result.hAlign='CENTER';return result

def opener(n):
    row=DATA['openers'][str(n)]
    im=pic(row['file'],450,maxheight=335);im.book_figure=f'{n}:opening-photo'
    caption=row['caption']+' Photograph: Taylor Osborn. '+row['file'].rsplit('.',1)[0]+'.'
    return [im,Spacer(1,12),Paragraph(caption,caption_style)]

def plate(n,key):
    row=DATA['plates'][key];assert row['chapter']==n
    label=Paragraph('PHOTOGRAPHS / TAYLOR OSBORN',photo_label);label.book_figure=f'{n}:photo-{key}'
    if row['layout']=='single':
        items=[Spacer(1,70),pic(row['files'][0],480),Spacer(1,20)]
    elif row['layout']=='pair':
        cells=[pic(name,228) for name in row['files']]
        table=Table([[cells[0],'',cells[1]]],colWidths=[228,24,228],hAlign='CENTER')
        table.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
                                  ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),('VALIGN',(0,0),(-1,-1),'TOP')]))
        items=[Spacer(1,60),table,Spacer(1,20)]
    else:
        items=[pic(row['files'][0],366),Spacer(1,16),pic(row['files'][1],366),Spacer(1,17)]
    ids=' / '.join(name.rsplit('.',1)[0] for name in row['files'])
    caption=Paragraph(row['caption']+' '+ids+'.',caption_style)
    return [PageBreak(),label,*items,caption,PageBreak()]
