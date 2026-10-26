import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'sources/archive_acquisition_2026-09-23/SANM_request_form_blank.pdf'
OUT = ROOT / 'output/pdf/Cuervo_State_Archives_Request_UNSIGNED.pdf'
citations = json.loads((Path(__file__).parent / 'citations.json').read_text(encoding='utf-8'))
reader = PdfReader(SRC)
# Check that each widget is the same object as its canonical field before filling.
canonical = {r.get_object().get('/T'): r.idnum for r in reader.trailer['/Root']['/AcroForm']['/Fields']}
for page in reader.pages:
    for ref in page.get('/Annots', []):
        widget = ref.get_object()
        if widget.get('/Subtype') == '/Widget':
            assert canonical[widget['/T']] == ref.idnum, widget['/T']

writer = PdfWriter()
writer.clone_document_from_reader(reader)
values = {'Please printtype': 'Taylor Osborn', 'Personal Interest': 'X'}
def wrap_citation(text):
    lines, line = [], ''
    for word in text.split():
        candidate = (line + ' ' + word).strip()
        if line and stringWidth(candidate, 'Helvetica', 8.7) > 268:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    assert len(lines) <= 5, lines
    return '\n'.join(lines)

for i, item in enumerate(citations, 1):
    values['CITE ITEM' if i == 1 else f'CITE ITEM_{i}'] = wrap_citation(item['citation'])
for page in writer.pages:
    for ref in page.get('/Annots', []):
        widget = ref.get_object()
        name = widget.get('/T')
        if name in values:
            size = 8.7 if name.startswith('CITE ITEM') else 12
            widget[NameObject('/DA')] = TextStringObject(f'/Helv {size} Tf 0 g')
writer.update_page_form_field_values(None, values, auto_regenerate=False)
# Preserve all fields, including the blank patron and archivist signatures.
writer.add_metadata({'/Title': 'Cuervo research - State Archives records request (unsigned)', '/Author': 'Taylor Osborn', '/Subject': 'Eight catalog citations; signature and internal fields left blank'})
writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('wb') as stream:
    writer.write(stream)

check = PdfReader(OUT)
fields = check.get_fields()
verified = []
for name, expected in values.items():
    assert fields[name]['/V'] == expected, name
for page in check.pages:
    for ref in page.get('/Annots', []):
        widget = ref.get_object()
        name = widget.get('/T')
        if name in values:
            assert widget['/V'] == values[name], name
            assert len(widget['/AP']['/N'].get_data()) > 0, name
            verified.append(name)
assert set(verified) == set(values)
assert not fields['Signature'].get('/V')
result = {'output': str(OUT), 'bytes': OUT.stat().st_size, 'page_count': len(check.pages), 'verified_values': values, 'widget_values_and_appearances_valid': True, 'signature_blank': True, 'interactive': True}
(Path(__file__).parent / 'form_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='verified_values'}, indent=2))
