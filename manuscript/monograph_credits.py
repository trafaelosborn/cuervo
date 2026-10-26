"""Reader-facing photograph credits, keyed to published page locations."""
import json,html
from reportlab.platypus import Paragraph,Spacer,PageBreak
from build_chapters02_03_pdf import ROOT,note_style,head_style

def credits():
    data=json.loads((ROOT/'manuscript/figures/book-revision04-photos/sources.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'manuscript/book-revision-10/build-manifest.json').read_text(encoding='utf-8'))
    pages={row['figure']:row['page'] for row in manifest['figure_pages']}
    intro='All eighteen photographs are by Taylor Osborn.'
    method='Photographs retain their full frames and aspect ratios, with orientation corrected and resizing for reproduction. Exact capture dates are omitted because folder labels and embedded camera dates conflict.'
    flows=[Paragraph(intro,note_style),Paragraph(method,note_style),Spacer(1,12)]
    md=['# Photograph credits',intro,method]
    for n in range(1,9):
        if n==5:
            flows.extend([PageBreak(),Paragraph('Photograph credits',head_style),Spacer(1,10)])
        flows.append(Paragraph('Chapter '+str(n),head_style));md.append('## Chapter '+str(n))
        op=data['openers'][str(n)];rows=[(op['caption'],f'{n}:opening-photo')]
        for key,row in data['plates'].items():
            if row['chapter']==n:rows.append((row['caption'],f'{n}:photo-{key}'))
        if n==8:rows.extend([('Road embankment and culvert.','8:road'),('Wall opening and interior fabric.','8:fabric')])
        for caption,anchor in rows:
            label=f'Page {pages[anchor]}'
            flows.append(Paragraph(f'<link href="#visual-{anchor}">{label}</link>: {html.escape(caption)}',note_style))
            md.append(f'{label}: {caption}')
    return flows,'\n\n'.join(md)+'\n'
