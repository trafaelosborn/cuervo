"""Preserve public sources and page-separated text for the Cuervo origins follow-up."""
from pathlib import Path
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'sources' / 'origins_followup_2026-09-23'
OUT.mkdir(parents=True, exist_ok=True)
TARGETS = [
    ('grubbs_bond_thesis_1958', 'https://digitalrepository.unm.edu/cgi/viewcontent.cgi?article=1010&context=anderson_etds', 'https://digitalrepository.unm.edu/anderson_etds/11/'),
    ('grubbs_bond_nmhr_35_4_1960', 'https://digitalrepository.unm.edu/cgi/viewcontent.cgi?article=2079&context=nmhr', 'https://digitalrepository.unm.edu/nmhr/vol35/iss4/4/'),
]
manifest = []
for name, url, landing in TARGETS:
    row = {'id': name, 'source_url': url, 'landing_url': landing, 'retrieved_utc': datetime.now(timezone.utc).isoformat()}
    path = OUT / (name + '.pdf')
    try:
        if not path.exists():
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': landing})
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
                row['final_url'] = response.url
                row['content_type'] = response.headers.get('Content-Type')
            if not data.startswith(b'%PDF-'):
                raise ValueError('Response is not a PDF: ' + repr(data[:120]))
            path.write_bytes(data)
        data = path.read_bytes()
        reader = PdfReader(path)
        pages = [{'pdf_page': i+1, 'text': page.extract_text() or ''} for i, page in enumerate(reader.pages)]
        (OUT / (name + '_pages.json')).write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding='utf-8')
        (OUT / (name + '.txt')).write_text('\n\n'.join('=== PDF PAGE %d ===\n%s' % (p['pdf_page'], p['text']) for p in pages), encoding='utf-8')
        row.update(status='held', file=str(path.relative_to(ROOT)).replace('\\','/'), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), pages=len(pages))
        hits = [p for p in pages if any(s in p['text'].lower() for s in ['cuervo', 'wiest', 'weist'])]
        row['search_hit_pdf_pages'] = [p['pdf_page'] for p in hits]
    except Exception as exc:
        row.update(status='download_failed', error=str(exc))
    manifest.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
(OUT / 'download_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
