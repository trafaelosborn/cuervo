"""Revision 10 graphic replacements and editorial caption clarifications."""
from pathlib import Path
from PIL import Image as PILImage
from reportlab.platypus import Image,Paragraph
ROOT=Path(__file__).resolve().parents[1]

def revise_figure(items,key):
    out=[]
    for flow in items:
        if isinstance(flow,Image) and key in ('regional-locator','journeys'):
            path=ROOT/f'manuscript/figures/book-revision10/{key}.png'
            with PILImage.open(path) as im:height=flow.drawWidth*im.height/im.width
            flow=Image(str(path),width=flow.drawWidth,height=height);flow.hAlign='CENTER'
        elif isinstance(flow,Paragraph):
            text=flow.text
            if key=='regional-locator':
                text=text.replace('1926 railway mileages','1926 railway distances')
                text=text.replace('Distances and travel opportunities are examined in Chapter 6.','Railway distances are rounded to whole kilometers, with original miles retained; travel opportunities are examined in Chapter 6.')
            if key=='santa-rosa-map':
                text=text.replace('Original map marks are retained.','Original map marks are retained. The service note concerns public water provision in 1908, not the absence of natural water sources. Map scales retain feet (1 foot = 0.3048 meters).')
            if key=='journeys':
                text=text.replace('Shading marks the next day.','Shading marks the next day. Distances are rounded to whole kilometers, with original miles retained.')
            flow=Paragraph(text,flow.style)
        out.append(flow)
    return out
