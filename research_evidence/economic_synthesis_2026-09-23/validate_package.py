"""Check the saved evidence package's integrity and local citation targets.
This validates files and arithmetic, not causal conclusions or every transcription.
"""
import hashlib
import json
import re
from functools import lru_cache
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
SRC = ROOT / 'sources/economic_synthesis_2026-09-23'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
checks = []

@lru_cache(maxsize=None)
def page_count(path):
    return len(PdfReader(path).pages)

manifest = read(SRC / 'manifest.json')
for row in manifest:
    assert row['status'] == 'held', row
    path = ROOT / row['file']
    assert len(path.read_bytes()) == row['bytes'], path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], path
    assert page_count(path) == row['pages'], path
checks.append({'check': 'PDF downloads, hashes and page counts', 'files': len(manifest), 'pages': sum(r['pages'] for r in manifest)})

ag = read(OUT / 'agriculture_transcription.json')
assert len(ag['series']) == 7
for row in ag['series']:
    assert abs(row['land_in_farms_acres'] / row['all_farms'] - row['mean_farm_acres']) < 0.051, row
for ref in ag['sources'].values():
    path = ROOT / ref['file']
    total = page_count(path)
    pages = ref.get('pdf_pages', [ref.get('pdf_page')])
    assert all(1 <= page <= total for page in pages), ref
checks.append({'check': 'Agricultural mean-area arithmetic and physical source-page ranges', 'observations': len(ag['series'])})

network = read(OUT / 'trade_network_observations.json')
assert len(network['observations']) == 20
for row in network['observations']:
    path = ROOT / row['local_file']
    assert path.exists(), path
    assert 1 <= row['pdf_page'] <= page_count(path), row
for row in read(OUT / 'newspaper_verification.json'):
    assert (ROOT / row['render']).exists()
    assert hashlib.sha256((ROOT / row['local_issue_file']).read_bytes()).hexdigest() == row['sha256']
checks.append({'check': 'Trade source files, page ranges and four newspaper image/source hashes', 'observations': 20})

branch = read(OUT / 'branch_comparison.json')
total = page_count(ROOT / branch['source_file'])
for row in branch['branches']:
    for obs in row['observations']:
        pages = obs.get('pdf_pages', [obs.get('pdf_page')])
        assert all(1 <= page <= total for page in pages), obs
assert (ROOT / branch['independent_check']['local_file']).exists()
checks.append({'check': 'Branch comparison source page ranges', 'branches': len(branch['branches'])})

report = ROOT / 'research_evidence/economic_synthesis_2026-09-23.md'
text = report.read_text(encoding='utf-8')
local_links = re.findall(r'\]\((B:/[^)]+)\)', text)
for target in local_links:
    assert Path(target).exists(), target
checks.append({'check': 'Report local file and image links', 'links': len(local_links)})

for path in OUT.glob('*.json'):
    read(path)
checks.append({'check': 'Companion JSON parsing', 'status': 'passed'})

result = {'status': 'passed', 'checks': checks, 'visual_qa': 'Both generated figures visually inspected; agricultural layout adjusted and re-inspected.', 'limits': 'File integrity, link validity and arithmetic checks do not independently verify historical interpretations or eliminate source limitations.'}
(OUT / 'validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
