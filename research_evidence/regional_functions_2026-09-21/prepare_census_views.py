from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'census_views'
OUT.mkdir(exist_ok=True)
manifest=[]
for ed in ['10-8','10-9','10-10']:
    paths=sorted((ROOT/f'sources/03_census/1950_manuscripts/ed_{ed}').glob('*.jpg'))
    for path in paths[1:]:
        im=Image.open(path)
        box=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate((.064,.220,.948,.697)))
        main=im.crop(box); main.thumbnail((2100,1400))
        header=im.crop((round(.06*im.width),round(.04*im.height),round(.95*im.width),round(.115*im.height)))
        header.thumbnail((2100,200))
        out=Image.new('RGB',(max(main.width,header.width),main.height+header.height+40),'white')
        ImageDraw.Draw(out).text((5,8),path.name+' | ED '+ed,fill='black')
        out.paste(header,(0,40));out.paste(main,(0,40+header.height))
        dest=OUT/(ed+'_'+path.stem.rsplit('-',1)[-1]+'.jpg');out.save(dest,quality=93)
        manifest.append({'id':dest.stem,'source':path.relative_to(ROOT).as_posix(),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'view':dest.relative_to(ROOT).as_posix(),'main_box':box,'note':'Derived reading view; source original retains full fields and supplementary questions.'})
(OUT.parent/'census_view_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(len(manifest),'reading views')
