from pathlib import Path
from datetime import datetime, timezone
import urllib.request,hashlib,json
from html.parser import HTMLParser
class PageText(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.hidden=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.hidden+=1
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.hidden=max(0,self.hidden-1)
 def handle_data(self,data):
  if not self.hidden and data.strip():self.parts.append(data.strip())
OUT=Path(__file__).resolve().parents[2]/'sources/economic_synthesis_2026-09-23'
targets=[('burguete_bond_1938','https://law.justia.com/cases/new-mexico/supreme-court/1938/43-nm-97.html'),('smith_1776_book1_ch3','https://geolib.com/smith.adam/won1-03.html'),('fujita_krugman_venables_introduction','https://web.mit.edu/krugman/www/fkvintro.html')]
rows=[]
for name,url in targets:
 row={'id':name,'url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=60) as response: data=response.read()
  (OUT/(name+'.html')).write_bytes(data)
  parser=PageText();parser.feed(data.decode('utf-8',errors='replace'))
  (OUT/(name+'.txt')).write_text('\n'.join(parser.parts),encoding='utf-8')
  row.update(status='held',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),file=(OUT/(name+'.html')).name)
 except Exception as exc:row.update(status='failed',error=str(exc))
 rows.append(row);print(json.dumps(row),flush=True)
(OUT/'web_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
