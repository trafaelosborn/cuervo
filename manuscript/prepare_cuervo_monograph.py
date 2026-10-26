"""Create a reader-facing edition from the preserved Revision 10 typesetter."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'manuscript/build_book_revision10.py').read_text(encoding='utf-8')

def replace_once(old, new):
    global source
    assert source.count(old) == 1, old
    source = source.replace(old, new)

replace_once("REV=ROOT/'manuscript/book-revision-10'", "SOURCE=ROOT/'manuscript/book-revision-10'\nREV=ROOT/'manuscript/monograph';REV.mkdir(parents=True,exist_ok=True)")
replace_once("OUT=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-10.pdf'", "OUT=ROOT/'tmp/pdfs/cuervo-monograph-typeset.pdf'")
source = source.replace("(REV/'chapters')", "(SOURCE/'chapters')")
source = source.replace("(REV/'bibliography.md')", "(SOURCE/'bibliography.md')")
replace_once("    tracked(c,'COMPLETE READING PROOF / REVISION 10',48,36,6.7,spacing=.9)\n", '')
old_start = source.index('    story=[Spacer(1,80)')
old_end = source.index("    story.extend([Paragraph('Contents'", old_start)
source = source[:old_start] + """    story=[Spacer(1,110),Paragraph('MERIDIAN',label),Spacer(1,28),
      Paragraph('Cuervo',ParagraphStyle('BookTitle',fontName='Playfair07Bold',fontSize=70,leading=80,textColor=HexColor(INK))),
      Spacer(1,22),Paragraph('An Economic History of a<br/>New Mexico Ghost Town',ParagraphStyle('BookSubtitle',fontName='Playfair07',fontSize=22,leading=29,textColor=HexColor(NAVY))),
      Spacer(1,40),Paragraph('Photographs by Taylor Osborn',ParagraphStyle('TitleCredit',fontName='Body07',fontSize=12,leading=17,textColor=HexColor(INK))),PageBreak()]
""" + source[old_end:]
replace_once('Contents and note references are clickable. Distances use kilometers (miles); elevations use meters (feet).', 'Distances use kilometers (miles); elevations use meters (feet).')
replace_once("manifest=[];combined=['# Cuervo\\n\\nComplete manuscript, revision 10. October 2, 2026.\\n\\nEdited chapter notes, consolidated bibliography and photograph credits. Indexing and final publication design pending.']", "manifest=[];combined=['# Cuervo\\n\\n## An Economic History of a New Mexico Ghost Town\\n\\nMeridian\\n\\nPhotographs by Taylor Osborn']")
replace_once("title='Cuervo | Complete manuscript, revision 10',author='Meridian',subject='Eight-chapter reading proof, October 2, 2026'", "title='Cuervo: An Economic History of a New Mexico Ghost Town',author='Meridian',subject='An economic history of Cuervo, New Mexico'")
replace_once("report={'date':'2026-10-02'", "report={'date':'2026-10-21'")
replace_once("'body':'Jost Regular, provisional Futura stand-in'", "'body':'Jost Regular'")
replace_once("from revision06_backmatter import credits, tidy_legacy", "from revision06_backmatter import tidy_legacy\nfrom monograph_credits import credits")
(ROOT / 'manuscript/build_cuervo_monograph.py').write_text(source, encoding='utf-8')
printer=(ROOT/'manuscript/make_print_revision10.py').read_text(encoding='utf-8')
for old,new in [
    ("SOURCE=ROOT/'output/pdf/cuervo-complete-reading-proof-revision-10.pdf'", "SOURCE=ROOT/'tmp/pdfs/cuervo-monograph-typeset.pdf'"),
    ("OUTPUT=ROOT/'output/pdf/cuervo-revision-10-print-letter.pdf'", "OUTPUT=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'"),
    ("QA=ROOT/'tmp/pdfs/revision10-print-letter'", "QA=ROOT/'tmp/pdfs/monograph-print-letter'"),
    ("RECORD=ROOT/'manuscript/print-revision10'", "RECORD=ROOT/'manuscript/monograph/print'"),
    ("ROOT/'manuscript/book-revision-10/build-manifest.json'", "ROOT/'manuscript/monograph/build-manifest.json'"),
    ("'/Title':'Cuervo | Revision 10 | US Letter print edition'", "'/Title':'Cuervo: An Economic History of a New Mexico Ghost Town'"),
    ("'/Subject':'US Letter portrait; color; actual size; duplex long-edge; 147 original pages plus one blank.'", "'/Subject':'An economic history of Cuervo, New Mexico'"),
]:
    assert printer.count(old)==1,old
    printer=printer.replace(old,new)
(ROOT/'manuscript/make_print_monograph.py').write_text(printer,encoding='utf-8')
print('Created reader-facing typesetter; original Revision 10 source and build remain preserved.')
