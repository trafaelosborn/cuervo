"""Download OFL fonts from Google Fonts and make static proof instances."""
from pathlib import Path
import sys, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tmp/chapter-build-deps'))
from urllib.request import urlopen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
DEST = ROOT/'manuscript/fonts/revision07'
DEST.mkdir(parents=True, exist_ok=True)
records=[]
for folder, name in [('playfairdisplay','PlayfairDisplay'), ('jost','Jost')]:
    for suffix in ['', '-Italic']:
        filename=name+suffix+'[wght].ttf'
        url='https://raw.githubusercontent.com/google/fonts/main/ofl/'+folder+'/'+filename.replace('[','%5B').replace(']','%5D')
        data=urlopen(url, timeout=30).read()
        source=DEST/filename
        source.write_bytes(data)
        for weight, label in [(400,'Regular'), (600,'Semibold'), (700,'Bold')]:
            font=instantiateVariableFont(TTFont(source), {'wght':weight}, inplace=False)
            stem=name+suffix+'-'+label
            family='Playfair Display' if name=='PlayfairDisplay' else 'Jost'
            style=label+(' Italic' if suffix else '')
            for platform,encoding,language in [(3,1,1033),(1,0,0)]:
                for key,value in [(1,family),(2,style),(4,family+' '+style),(6,stem.replace('-','')+'R07')]:
                    font['name'].setName(value,key,platform,encoding,language)
            font.save(DEST/(stem+'.ttf'))
        records.append({'source':url,'file':filename,'sha256':hashlib.sha256(data).hexdigest()})
    (DEST/(name+'-OFL.txt')).write_bytes(urlopen('https://raw.githubusercontent.com/google/fonts/main/ofl/'+folder+'/OFL.txt', timeout=30).read())
(DEST/'sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Prepared Playfair Display and Jost static instances and licenses.')
