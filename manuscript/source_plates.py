"""Source plates shared by the three chapter proof builders."""
from pathlib import Path
from PIL import Image as PILImage
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'manuscript/figures/revision-2026-09-28'

def img(name,width):
    path=ASSETS/name
    with PILImage.open(path) as im:height=width*im.height/im.width
    result=Image(str(path),width=width,height=height)
    result.hAlign='CENTER'
    return result

def plate(key,title_style,caption_style):
    small=ParagraphStyle('PlateDescription',parent=caption_style,fontSize=10,leading=13.5,spaceAfter=0)
    contents=[]
    def paired(name,label,description):
        row=Table([[img(name,165),Paragraph('<b>'+label+'</b><br/>'+description,small)]],colWidths=[179,187])
        row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
        contents.extend([row,Spacer(1,15)])
    if key=='simultaneous-change':
        title='Three changes, one town'
        contents.extend([img('1911-masthead.png',366),Spacer(1,19)])
        paired('1911-depot.png','The railway invests','The section foreman had widened and improved the depot platform.')
        paired('1911-lumber.png','Stock leaves town','Big Jo Lumber was shipping out stock and cutting prices on what remained.')
        paired('1911-school.png','A school takes shape','A notice about a barbecue identifies the contractor erecting the new school building.')
        caption='Figure 1.1. Three notices on the same front page of the Cuervo Clipper, September 14, 1911 (held PDF p. 2). Details are separately cropped and rearranged; the masthead identifies the issue. The stock notice does not establish the lumberyard\'s closing date. Source: UNM newspaper collection; chapter note 1.'
    elif key=='cuervo-map':
        title='Where storage met the railway'
        contents.extend([img('cuervo-map-overview.png',170),Spacer(1,10),
                         Paragraph('RAILWAY CORRIDOR / ENLARGED DETAIL',caption_style),
                         img('cuervo-rail-detail.png',430),Spacer(1,15)])
        caption='Figure 2.1. Annotated Cuervo parcel map, undated. The overview preserves the sheet\'s context; the enlarged corridor identifies the depot and Bond &amp; Wiest warehouse. The colored ownership marks belong to a later, separately undated layer. This is a spatial relationship, not a dated reconstruction of the 1903 premises. Source: Guadalupe County packet, City of Cuervo sheet; chapter note 8.'
    elif key=='trade-notices':
        title='Goods out, supplies in'
        paired('1910-sheep.png','Fourteen cars of sheep','The notice records loading at Cuervo for Kansas. It does not name the owner of this consignment.')
        paired('1910-supplies.png','A carload of supplies','Potatoes, grain and dried fruit were unloaded for Bond &amp; Wiest. The report also describes regular produce deliveries.')
        contents.extend([img('1910-advertisement.png',325),Spacer(1,15)])
        caption='Figure 2.3. Cuervo Clipper, March 4, 1910, front page (held PDF p. 2). Two notices and an advertisement, separately cropped and rearranged. The advertisement joins the sale of supplies to the buying of hides and pelts. A separate notice of a purchase of more than 4,000 sheep is not treated as the fourteen-car shipment. Source: UNM newspaper collection; chapter note 12.'
    else:raise ValueError(key)
    return [PageBreak(),Paragraph(title,title_style),Spacer(1,8),*contents,
            Paragraph(caption,caption_style),PageBreak()]
