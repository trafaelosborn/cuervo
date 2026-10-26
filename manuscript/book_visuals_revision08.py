"""Reader-facing DOT plate sequence; geometric relationships stay in the original."""
from PIL import Image as PILImage
from reportlab.platypus import Paragraph,Spacer,PageBreak,NextPageTemplate,Image,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from build_chapters02_03_pdf import ROOT,figure_title,caption_style,NAVY
FIG=ROOT/'manuscript/figures/book-revision08'
KEYS={'dot-town','dot-details','dot-access','chronology'}
def pic(name,width):
 p=FIG/f'{name}.png'
 with PILImage.open(p) as im:height=width*im.height/im.width
 result=Image(str(p),width=width,height=height);result.hAlign='CENTER';return result
def label(s):
 return Paragraph(s,ParagraphStyle('DOTLabel',parent=caption_style,fontName='Body07Bold',fontSize=8.5,leading=11,textColor=HexColor(NAVY),spaceAfter=6))
def figure(key):
 if key=='dot-town':
  title='The highway in the town'
  items=[label('CUERVO / PROJECT I-040-5(13)291'),pic('dot-town',468),Spacer(1,20),
   Paragraph('The railway runs along the upper edge. Below it, the plan brings divided highway lanes through a landscape of premises, yards and local roads. The lower portion records the road profile. Enlarged details follow on the next page.',caption_style)]
  caption='Figure 6.4. Town plan and profile, cropped from PDF p. 151. Original drawing marks are retained. The project title was approved July 15, 1963; the packet includes later changes. Building labels and construction instructions are distinct from evidence of continued trading or completed demolition. Source: New Mexico State Highway Commission/State Highway Department, as-built drawing packet; chapter note 21.'
 elif key=='dot-details':
  title='Premises and proposed removals'
  items=[label('NORTH SIDE / POST OFFICE, STORE AND PUMPS'),pic('dot-north',468),Spacer(1,10),
   Paragraph('The upper detail labels a post office and Bond and Wiest’s general-merchandise store, with a canopy and three gas pumps beside the frontage road.',caption_style),Spacer(1,18),
   label('SOUTH SIDE / BUILDINGS, WELLS AND FOUNDATIONS'),pic('dot-south',468),Spacer(1,10),
   Paragraph('The lower detail combines structure outlines with removal instructions, including foundations. Those instructions do not by themselves identify occupied businesses displaced by construction.',caption_style)]
  caption='Figure 6.5. Two separately enlarged excerpts from the town sheet, PDF p. 151; they are not a continuous image or a common-scale reconstruction. Original lettering and marks retained. Source: New Mexico State Highway Commission/State Highway Department, project I-040-5(13)291; chapter note 21.'
 elif key=='dot-access':
  title='A different route to the customer'
  items=[label('CUERVO INTERCHANGE / RAMPS AND FRONTAGE ROADS'),pic('dot-interchange',468),Spacer(1,18)]
  right=Paragraph('The interchange drawing connects the highway to a crossroad and frontage roads. Its arrows distinguish travel toward Santa Rosa and Newkirk.<br/><br/>The companion sign drawings specify the Cuervo exit and a gas-and-food panel. These are provisions for access and wayfinding; they do not count travelers who stopped.',caption_style)
  row=Table([[pic('dot-signs',120),right]],colWidths=[148,300],hAlign='CENTER')
  row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
  items.extend([row])
  caption='Figure 6.6. Cuervo interchange plan (PDF p. 137), enlarged central excerpt, with separately reproduced sign details (p. 114). Original marks retained; excerpts have different scales. The drawings establish the specified connections and signs, not their opening or installation dates. Source: New Mexico State Highway Department, project I-040-5(13)291; chapter note 21.'
 else:
  title='Connections changed at different dates';items=[pic('chronology',410)]
  caption='Figure 6.7. Selected observations, 1952–1974. Brown spans bracket a disappearance between inspected records; the navy span records nearby interstate construction. The open diamond marks approval of the separate Cuervo project’s title sheet, not an opening date. Sources: highway nomination, engineering plans, timetables, NTSB, Congressional Record and station book; chapter notes 8, 12–17 and 21.'
 if key=='chronology':return [PageBreak(),Paragraph(title,figure_title),Spacer(1,8),*items,Spacer(1,13),Paragraph(caption,caption_style),PageBreak()]
 return [NextPageTemplate('plate'),PageBreak(),Paragraph(title,figure_title),Spacer(1,10),*items,Spacer(1,18),Paragraph(caption,caption_style),NextPageTemplate('book'),PageBreak()]
