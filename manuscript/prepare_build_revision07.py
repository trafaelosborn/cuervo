"""Isolate the next builder and checker; do not alter an earlier edition."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'manuscript/build_book_revision06.py'
s=p.read_text(encoding='utf-8').replace('book-revision-06','book-revision-07').replace('book-revision06','book-revision07').replace('revision-06.pdf','revision-07.pdf').replace('REVISION 6','REVISION 7').replace('revision 6','revision 7')
s=s.replace("REV=ROOT/", "import build_chapters02_03_pdf as base_styles\nfrom revision07_typography import configure\nconfigure(base_styles)\nREV=ROOT/",1)
s=s.replace("fontName='GaramondItalic',fontSize=40,leading=46", "fontName='Playfair07Bold',fontSize=35,leading=42")
s=s.replace("fontName='Garamond',fontSize=15,leading=20", "fontName='Body07',fontSize=13,leading=19")
s=s.replace("fontName='Display',fontSize=76,leading=83", "fontName='Playfair07Bold',fontSize=70,leading=80")
s=s.replace('Indexing, final color treatment and publication design remain in preparation.', 'Typography trial: Jost body text is a temporary stand-in for the requested Futura. Titles use Playfair Display Bold; subheads use Playfair Display Regular. Indexing, final color treatment and publication design remain in preparation.')
s=s.replace("text=typography(flow.text)","text=typography(flow.text)\n        text=text.replace('Population and age changed together','Fewer residents, still young')")
# Tables and images may sit within KeepTogether or photo-pair tables.
s=s.replace('PageBreak,KeepTogether,Image','PageBreak,KeepTogether,Image,Table')
s=s.replace('BaseDocTemplate,PageTemplate,Frame,','BaseDocTemplate,PageTemplate,NextPageTemplate,Frame,')
s=s.replace('def append(story,items):',"def append(story,items):\n    if story and isinstance(story[-1],PageBreak) and len(items)>1 and isinstance(items[0],NextPageTemplate) and isinstance(items[1],PageBreak):story.pop()")
s=s.replace("    items=[tidy_legacy(x,n) for x in items]", "    if key=='functional-chronology':\n        for flow in items:\n            if isinstance(flow,Image):\n                flow.drawHeight*=430/flow.drawWidth;flow.drawWidth=430\n    items=[tidy_legacy(x,n) for x in items]")
s=s.replace("append(story,[PageBreak(),Paragraph('CHAPTER '+NUMBERS[n-1],label),h,", "append(story,[NextPageTemplate('notes'),PageBreak(),Paragraph('CHAPTER '+NUMBERS[n-1],label),h,")
s=s.replace("        manifest.append({'chapter'", "        story.append(NextPageTemplate('book'))\n        manifest.append({'chapter'")
s=s.replace("doc.addPageTemplates(PageTemplate(id='book',frames=[frame],onPage=running));doc.multiBuild(story,maxPasses=5)", "notes_frame=Frame(MARGIN-24,BOTTOM,W-2*MARGIN+48,H-TOP-BOTTOM,id='notes-frame')\n    doc.addPageTemplates([PageTemplate(id='book',frames=[frame],onPage=running),PageTemplate(id='notes',frames=[notes_frame],onPage=running)]);doc.multiBuild(story,maxPasses=5)")
s=s.replace('    return flow\n\ndef build():','''    if isinstance(flow,Table):
        for row in flow._cellvalues:
            for j,cell in enumerate(row):
                if isinstance(cell,list):row[j]=[normalize_flow(x) for x in cell]
                elif isinstance(cell,(Paragraph,Image,KeepTogether,Table)):row[j]=normalize_flow(cell)
    if isinstance(flow,Image):
        # Match placed images to 300 dpi while preserving the frame and aspect ratio.
        path=Path(flow.filename)
        if path.exists():
            key=hashlib.sha256((str(path)+str(flow.drawWidth)+str(flow.drawHeight)).encode()).hexdigest()[:20]
            photo='book-revision04-photos' in str(path) or path.stem.startswith('IMG_')
            target=QA/'images'/(key+('.jpg' if photo else '.png'));target.parent.mkdir(exist_ok=True)
            if not target.exists():
                with PILImage.open(path) as im:
                    im=im.copy();im.thumbnail((round(flow.drawWidth*300/72),round(flow.drawHeight*300/72)),PILImage.Resampling.LANCZOS)
                    if photo:im.convert('RGB').save(target,quality=95,subsampling=0,optimize=True)
                    else:im.save(target,optimize=True)
            new=Image(str(target),width=flow.drawWidth,height=flow.drawHeight)
            new.hAlign=flow.hAlign
            for k,v in vars(flow).items():
                if k.startswith('book_'):setattr(new,k,v)
            return new
    return flow

def build():''')
s=s.replace("'visual_review':'pending'", "'typography':{'body':'Jost Regular, provisional Futura stand-in','body_points':11.3,'body_leading':16.2,'titles':'Playfair Display Bold','subheads':'Playfair Display Regular','images':'300 dpi maximum at placed size, full frames retained; photographs JPEG quality 95 with no chroma subsampling; source plates PNG'},'visual_review':'pending'")
(ROOT/'manuscript/build_book_revision07.py').write_text(s,encoding='utf-8')
c=(ROOT/'manuscript/check_book_revision06.py').read_text(encoding='utf-8').replace('book-revision-06','book-revision-07').replace('book-revision06','book-revision07').replace('revision-06.pdf','revision-07.pdf').replace('REVISION 6','REVISION 7')
c=c.replace('book-revision07-delivery-review','book-revision07-verified')
c=c.replace("old=json.loads", "protected=json.loads((REV/'revision06-integrity.json').read_text(encoding='utf-8'))\nfor path,digest in protected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Revision 6 changed',path)\nold=json.loads")
(ROOT/'manuscript/check_book_revision07.py').write_text(c,encoding='utf-8')
print('Isolated Revision 7 builder and checker prepared.')
