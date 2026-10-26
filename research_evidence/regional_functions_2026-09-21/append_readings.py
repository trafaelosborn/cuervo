from pathlib import Path
import json,sys
here=Path(__file__).resolve().parent
target=here/'santa_rosa_occupation_readings.json'
data=json.loads(target.read_text(encoding='utf-8'))
incoming=json.loads((here/sys.argv[1]).read_text(encoding='utf-8'))
ids={(p['ed'],p['image']) for p in data['pages']}
assert not any((p['ed'],p['image']) in ids for p in incoming)
data['pages'].extend(incoming)
target.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(len(data['pages']),'pages;',sum(len(p['rows']) for p in data['pages']),'occupation readings')
