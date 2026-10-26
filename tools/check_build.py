"""Check the current print PDF, optionally against a published reference."""
from pathlib import Path
import argparse,json,hashlib
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reference',type=Path)
args=parser.parse_args()
path=ROOT/'output/pdf/cuervo-monograph-print-letter.pdf'
r=PdfReader(path)
assert len(r.pages)==148
assert r.metadata.title=='Cuervo: An Economic History of a New Mexico Ghost Town'
assert 'An Economic History of a' in r.pages[0].extract_text()
assert len(r.outline)==10
fonts=set();annotations=0
for page in r.pages:
    assert list(page.mediabox)==[0,0,612,792]
    annotations+=len(page.get('/Annots',[]))
    for ref in page.get('/Resources',{}).get('/Font',{}).values():
        f=ref.get_object();d=f['/FontDescriptor']
        assert any(k in d for k in ['/FontFile','/FontFile2','/FontFile3'])
        fonts.add(str(f['/BaseFont']))
    assert 'COMPLETE READING PROOF' not in page.extract_text()
assert annotations==367
if args.reference:
    expected=PdfReader(args.reference)
    assert len(expected.pages)==len(r.pages)
    index={p.indirect_reference.idnum:n for n,p in enumerate(r.pages)}
    expected_index={p.indirect_reference.idnum:n for n,p in enumerate(expected.pages)}
    for n,(p,q) in enumerate(zip(r.pages,expected.pages),1):
        assert p.extract_text()==q.extract_text(),f'Page {n} text differs'
        assert p.mediabox==q.mediabox
        pa=p.get('/Annots',[]);qa=q.get('/Annots',[]);assert len(pa)==len(qa)
        for x,y in zip(pa,qa):
            x=x.get_object();y=y.get_object();assert x.get('/Rect')==y.get('/Rect')
            if '/Dest' in x:
                assert index[x['/Dest'][0].idnum]==expected_index[y['/Dest'][0].idnum]
                assert x['/Dest'][1:]==y['/Dest'][1:]
            if '/A' in x:assert dict(x['/A'])==dict(y['/A'])
result={'pages':148,'annotations':annotations,'bookmarks':10,'embedded_fonts':len(fonts),
    'reference_text_and_links_match':bool(args.reference),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
