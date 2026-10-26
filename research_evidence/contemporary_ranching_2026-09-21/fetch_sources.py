from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import json
import re

OUT = Path('sources/contemporary_ranching_2026-09-21')
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = [
    ('sand_county_award_2026', 'https://sandcountyfoundation.org/news/2026/new-mexico-leopold-conservation-award-finalists-selected'),
    ('armendariz_beef_council_interview', 'https://www.buzzsprout.com/2445388/episodes/18537637-building-a-family-ranch-with-science-grit-and-heart-with-the-armendariz-family'),
    ('nmda_ag_family_meats', 'https://members.elevatenmag.com/nmda_business/ag-family-meats/'),
    ('regenerate_jim_armendariz', 'https://regenerateconference.com/jim-armendariz/'),
]

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())

def fetch(item):
    stem, url = item
    record = {'url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(request, timeout=25) as response:
            data = response.read()
            record['resolved_url'] = response.url
            record['content_type'] = response.headers.get('Content-Type')
        path = OUT / (stem + '.html')
        path.write_bytes(data)
        html = data.decode('utf-8', errors='replace')
        parser = TextParser()
        parser.feed(html)
        text = '\n'.join(parser.parts)
        text_path = OUT / (stem + '.txt')
        text_path.write_text(text, encoding='utf-8')
        record.update({'file': path.as_posix(), 'text_file': text_path.as_posix(), 'bytes': len(data), 'sha256': sha256(data).hexdigest()})
        record['date_metadata'] = re.findall(r'"(?:datePublished|dateModified|uploadDate)"\s*:\s*"([^"]+)"', html)
        record['cuervo_mentions'] = len(re.findall('Cuervo', text, re.I))
    except Exception as exc:
        record['error'] = str(exc)
    return record

with ThreadPoolExecutor(max_workers=4) as executor:
    records = list(executor.map(fetch, SOURCES))
(OUT / 'download_manifest.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
print(json.dumps(records, indent=2))
