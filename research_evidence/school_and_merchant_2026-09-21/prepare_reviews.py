from pathlib import Path
import datetime,hashlib,json,re,shutil
from html.parser import HTMLParser
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE=ROOT/'sources/school_and_merchant_2026-09-21'
RENDERS=HERE/'page_renders'

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
    p=Clean();p.feed(path.read_text(encoding='utf-8',errors='replace'))
    text=re.sub(r'[ \t]+',' ',''.join(p.parts))
    (HERE/'text'/(path.stem+'.txt')).write_text(text,encoding='utf-8')
    (HERE/'text'/(path.stem+'_links.json')).write_text(json.dumps(p.links,indent=2),encoding='utf-8')

source=Path('C:/Users/Clem/.codex/codex-remote-attachments/01a0a217-4d22-7781-bb4a-12f5574a12a1/7117EDE5-9DE7-4F73-B81A-9A6A01132FE1/1-IRPA-REQUEST-T.-OSBORN.pdf')
dest=BASE/'santa_rosa_schools_acknowledgment_2026-09-16.pdf'
if not dest.exists():
    shutil.copyfile(source,dest)
    entry={'file':str(dest.relative_to(ROOT)),'origin':'user-provided attachment','original_path':str(source),
           'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size,
           'copied_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'held acknowledgment; no historical records attached'}
    with (BASE/'download_manifest.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(entry)+'\n')
(HERE/'text'/(dest.stem+'.txt')).write_text('\n'.join(p.extract_text() or '' for p in PdfReader(dest).pages),encoding='utf-8')

audit=json.loads((ROOT/'sources/02_newspapers/cuervo_clipper/full_scan_audit_2026-09-17.json').read_text(encoding='utf-8'))
issues={x['issue_date']:x for x in audit['issues']}
doc=pdfium.PdfDocument(str(ROOT/issues['1921-09-09']['file']));p=doc[1]
p.render(scale=1.7).to_pil().convert('RGB').save(RENDERS/'clipper_1921-09-09_pdf2.jpg',quality=95)
p.close();doc.close()
for date,box in [('1919-01-10',(.73,.56,.9,.67)),('1922-07-07',(.135,.327,.264,.388))]:
    doc=pdfium.PdfDocument(str(ROOT/issues[date]['file']));p=doc[1];im=p.render(scale=5).to_pil();w,h=im.size
    im.crop(tuple(int(n*size) for n,size in zip(box,(w,h,w,h)))).save(RENDERS/f'clipper_{date}_detail.png');p.close();doc.close()

for name,nums in [('superintendent_report_ia.pdf',list(range(2,14))),('education_directory_1969_1970.pdf',[1,2,14,15])]:
    doc=pdfium.PdfDocument(str(BASE/name));thumbs=[]
    for n in nums:
        p=doc[n-1];im=p.render(scale=1.4).to_pil().convert('RGB');p.close()
        im.save(RENDERS/f'{Path(name).stem}_pdf{n}.jpg',quality=94)
        im.thumbnail((300,400));thumb=Image.new('RGB',(310,430),'white');thumb.paste(im,((310-im.width)//2,24));ImageDraw.Draw(thumb).text((8,5),f'PDF {n}',fill='black');thumbs.append(thumb)
    doc.close()
    contact=Image.new('RGB',(1240,430*((len(thumbs)+3)//4)), '#DDDDDD')
    for i,im in enumerate(thumbs):contact.paste(im,((i%4)*310,(i//4)*430))
    contact.save(RENDERS/f'{Path(name).stem}_contact.jpg',quality=94)
print('HTML text, acknowledgment, and source review images prepared.')
