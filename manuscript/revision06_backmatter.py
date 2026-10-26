"""Caption cleanup and centralized photographic provenance."""
import re,json,html
from reportlab.platypus import Paragraph,Spacer,KeepTogether,Table
from build_chapters02_03_pdf import ROOT,caption_style,note_style,head_style
from finalize_book_revision06 import remap_refs

def tidy_legacy(flow,n,remap=True):
    if isinstance(flow,Paragraph):
        s=flow.text
        s=s.replace('The corrected 1950 readings give a median of 25.5.','The 1950 median is 25.5.')
        s=s.replace('the project transcription',"the author’s transcription").replace('corrected household transcription',"the author’s household transcription")
        s=s.replace(' Original scans and crop provenance are preserved.','')
        s=s.replace(' These are selected examples, not a household diversification rate or evidence of pooled earnings. Original writing and marks are retained.',' Original writing and marks are retained.')
        s=re.sub(r'\b((?:18|19|20)\d{2})-((?:18|19|20)\d{2})\b',r'\1–\2',s)
        s=re.sub(r'((?:LINES|lines)\s+\d+)-(\d+)',r'\1–\2',s)
        s=s.replace('Chapter 5, notes 1-4.','Chapter 5, notes 2–4.')
        if remap:s=remap_refs(s,n)
        # Camera identifiers belong in the concordance, not in picture captions.
        s=re.sub(r'(?:\s*/\s*)?\b(?:IMG_\d+|1Y5A\d+)(?:\.(?:JPG|CR2))?\.?','',s)
        s=s.replace('Taylor Osborn, .','Taylor Osborn.').replace('Taylor Osborn,','Taylor Osborn.')
        if n==8:
            s=s.replace(' No exact capture date is assigned.','').replace(' Orientation corrected; no retouching.','')
            s=s.replace(' The image shows the road’s level relative to adjoining ground; it does not establish a construction date or a business effect.','')
            s=s.replace(" The image shows the road's level relative to adjoining ground; it does not establish a construction date or a business effect.",'')
            s=s.replace(' Condition at the time of photography does not date the end of occupation.','')
        new=Paragraph(s,flow.style)
        for key,value in vars(flow).items():
            if key.startswith('book_'):setattr(new,key,value)
        return new
    if isinstance(flow,KeepTogether):flow._content=[tidy_legacy(x,n,remap) for x in flow._content]
    if isinstance(flow,Table):
        for i,row in enumerate(flow._cellvalues):
            for j,cell in enumerate(row):
                if isinstance(cell,list):flow._cellvalues[i][j]=[tidy_legacy(x,n,remap) for x in cell]
                elif isinstance(cell,Paragraph):flow._cellvalues[i][j]=tidy_legacy(cell,n,remap)
    return flow

def credits():
    data=json.loads((ROOT/'manuscript/figures/book-revision04-photos/sources.json').read_text(encoding='utf-8'))
    intro='All eighteen photographs are by Taylor Osborn. The sequence moves from buildings and their settings to entrances, interiors, road relationships and surviving fabric. It accompanies the documentary history without assigning unidentified rooms to named residents or inferring closure dates from condition.'
    method='Photographs retain their full frames and aspect ratios, with orientation corrected and reproduction resizing only. Exact capture dates are unassigned because archive-folder labels and embedded camera dates conflict. The original identifiers below connect each published view to the photographic collection; metadata and source hashes are retained in the project concordance.'
    flows=[Paragraph(intro,note_style),Paragraph(method,note_style),Spacer(1,12)]
    md=['# Photograph credits',intro,method]
    for n in range(1,9):
        flows.append(Paragraph('Chapter '+str(n),head_style));md.append('## Chapter '+str(n))
        op=data['openers'][str(n)];rows=[('Opening photograph',op['caption'],op['file'],f'{n}:opening-photo')]
        for key,row in data['plates'].items():
            if row['chapter']==n:rows.append(('Photograph plate',row['caption'],' / '.join(row['files']),f'{n}:photo-{key}'))
        if n==8:rows.extend([('Figure 8.2','Road embankment and culvert.','IMG_7385.JPG','8:road'),('Figure 8.3','Wall opening and interior fabric.','IMG_7456.JPG','8:fabric')])
        for label,caption,files,anchor in rows:
            text=f'{label}: {caption} Original: {files}.'
            flows.append(Paragraph(f'<link href="#visual-{anchor}">{html.escape(label)}</link>: {html.escape(caption)} Original: {files}.',note_style));md.append(text)
    return flows,'\n\n'.join(md)+'\n'
