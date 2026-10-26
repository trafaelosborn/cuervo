from pathlib import Path
import json, re
from html.parser import HTMLParser
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE=ROOT/'sources/school_and_merchant_2026-09-21'
OUT=HERE/'text'
OUT.mkdir(exist_ok=True)
class Clean(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0;self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if tag in ('p','div','h1','h2','h3','li','tr','br'):self.parts.append('\n')
        if tag=='a':self.links.extend(v for k,v in attrs if k=='href')
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
for path in BASE.glob('*.html'):
    parser=Clean();parser.feed(path.read_text(encoding='utf-8',errors='replace'))
    text=re.sub(r'[ \t]+',' ',''.join(parser.parts))
    (OUT/(path.stem+'.txt')).write_text(text,encoding='utf-8')
    (OUT/(path.stem+'_links.json')).write_text(json.dumps(parser.links,indent=2),encoding='utf-8')
    if path.stem=='srlions_home':
        print('SCHOOL LINKS',json.dumps([x for x in parser.links if re.search('board|minute|agenda|doc|histor',x,re.I)],indent=2))
    if 'Making sure' in text:print('BOT CHALLENGE, NOT CATALOG CONTENT',path.name)
for path in BASE.glob('*.pdf'):
    reader=PdfReader(path)
    print('PDF',path.name,len(reader.pages))
    content=[]
    for i,page in enumerate(reader.pages,1):
        text=page.extract_text() or ''
        content.append(f'\n[PDF PAGE {i}]\n'+text)
        if re.search(r'Cuervo|Santa Rosa|Guadalupe',text,re.I):
            print('MATCH PDF PAGE',i,text[:5000])
    (OUT/(path.stem+'.txt')).write_text('\n'.join(content),encoding='utf-8')

audit=json.loads((ROOT/'sources/02_newspapers/cuervo_clipper/full_scan_audit_2026-09-17.json').read_text(encoding='utf-8'))
issues={x['issue_date']:x for x in audit['issues']}
renders=HERE/'page_renders';renders.mkdir(exist_ok=True)
for date in ['1910-10-07','1910-11-18','1911-01-27','1912-02-08','1919-01-10','1921-02-11','1922-07-07']:
    path=renders/f'clipper_{date}_pdf2.jpg'
    if not path.exists():
        doc=pdfium.PdfDocument(str(ROOT/issues[date]['file']))
        page=doc[1]
        image=page.render(scale=1.7).to_pil()
        image.thumbnail((2100,3000))
        image.convert('RGB').save(path,quality=95)
        page.close();doc.close()
    print('RENDER',path)
