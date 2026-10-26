"""Figure layouts added by the September 28 whole-book visual pass."""
from PIL import Image as PILImage
from reportlab.platypus import Paragraph, PageBreak, Image, Spacer
from build_chapters02_03_pdf import ROOT, figure_title, caption_style

FIG=ROOT/'manuscript/figures/book-revision03'
SPECS={
 'regional-locator':{
   'title':'Cuervo and its regional neighbors', 'width':450,
   'caption':'Figure 1.2. A locator using modern reference points and the 2020 Guadalupe County outline, with a separate diagram of 1926 railway mileages. The county is not the historical Cuervo precinct or a trading area. No road or railway route is drawn on the map. Sources: held U.S. Census geography and regional audit; Rock Island timetable, January 1926, Table 2, p. 18. Distances and travel opportunities are examined in Chapter 6.'},
 'trade-connections':{
   'title':'The trade that gathered at Cuervo', 'width':450,
   'caption':'Figure 3.2. Selected connections from the Clipper and Grubbs. Solid arrows identify 1910 newspaper reports; dashed arrows identify retrospective accounts. The arrows represent separate observations, not consignments followed through Cuervo or shares of total trade. Suppliers of the incoming foodstuffs are unidentified. Sources: Clipper, March 11, July 15, October 21 and December 2, 1910; Grubbs, pp. 109-110; chapter notes 9, 13-14.'},
 'prices-and-population':{
   'title':'Cattle prices and the people counted at Cuervo', 'width':440,
   'caption':'Figure 3.4. Annual New Mexico beef-cattle prices, excluding calves, adjusted with CPI-U, above five Cuervo precinct census counts. Both panels use the same dates. Population dots are not interpolated, and the precinct boundaries are not constant. Price measures purchasing power per unit sold, not ranch profit or local spending. Sources: USDA Statistical Bulletins 265 and 680, BLS CPI-U and census transcriptions; chapter notes 26-27 and Chapter 5, notes 1-4.'},
 'functional-chronology':{
   'title':'Different functions, different clocks', 'width':450,
   'caption':'Figure 7.1. Dated evidence across the book. Investment, withdrawal and continued use appear on different schedules. Equal row spacing shows sequence, not elapsed time or uninterrupted operation. The events do not form an established chain of causes. Sources: Clipper, Grubbs, Rittenhouse, railway and highway records, and attributed later accounts, documented in Chapters 1, 3, 4, 6 and 8. Compiled by Meridian.'}
}

def figure(key):
    spec=SPECS[key];path=FIG/f'{key}.png'
    with PILImage.open(path) as im:height=spec['width']*im.height/im.width
    pic=Image(str(path),width=spec['width'],height=height);pic.hAlign='CENTER'
    return [PageBreak(),Paragraph(spec['title'],figure_title),Spacer(1,8),pic,
            Spacer(1,15),Paragraph(spec['caption'],caption_style),PageBreak()]
