from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
base=ROOT/'sources/regional_functions_2026-09-21/rittenhouse_1946/c857f5e4-2baf-42d5-ae44-d0ff1324820b'
raw=json.loads((base/'manifest.json').read_text())
items=[]
for a in raw['assets']:
 p=base/Path(a['path']).name
 if not p.exists():continue
 im=Image.open(p)
 items.append(dict(a,local_path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=im.size))
(HERE/'rittenhouse_asset_index.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
for n in range(0,len(items),15):
 page=Image.new('RGB',(1500,1700),'white');d=ImageDraw.Draw(page)
 for k,a in enumerate(items[n:n+15]):
  im=Image.open(ROOT/a['local_path']);im.thumbnail((490,300));x=(k%3)*500;y=(k//3)*340
  page.paste(im,(x,y+25));d.text((x+5,y+5),a['name']+' | '+a['id'],fill='black')
 page.save(HERE/f'guide_contact_{n//15+1}.jpg')
print(len(items),'images indexed; contact sheets written')
