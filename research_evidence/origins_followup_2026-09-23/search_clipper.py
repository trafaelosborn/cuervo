from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
pages = json.loads((ROOT / 'research_evidence/full_life_chronology_2026-09-21/canonical_ocr_pages.json').read_text(encoding='utf-8'))
patterns = {
    'bond_wiest': r'\b(?:[Ww][iI1l]e[s5]t|[Ww]e[iI1l][s5]t)\b',
    'founding': r'\b(?:organiz\w*|establish\w*|incorporat\w*|purchas\w*|open\w*|erect\w*|start\w*)\b.{0,80}\b(?:store|business|mercantile|hotel|townsite|bank)\b',
    'rail_facility': r'\b(?:depot|stock\s*(?:yards|pens)|warehouse|loading\s+pens|siding)\b',
    'hinterland': r'\b(?:wool|sheep|hides|pelts)\b.{0,80}\b(?:buy|bought|market|ship\w*|store|business|Wiest)\b',
}
hits=[]
for p in pages:
    text=(ROOT / p['text_file']).read_text(encoding='utf-8')
    flat=re.sub(r'\s+',' ',text)
    for name,pattern in patterns.items():
        for match in re.finditer(pattern,flat,re.I):
            hits.append({**p,'category':name,'snippet':flat[max(0,match.start()-250):min(len(flat),match.end()+400)]})
(OUT/'targeted_clipper_leads.json').write_text(json.dumps(hits,ensure_ascii=False,indent=2),encoding='utf-8')
print('pages',len(pages),'hits',len(hits))
for name in patterns:
    subset=[h for h in hits if h['category']==name]
    print(name,len(subset))
    priority=[h for h in subset if h['issue_date']<'1912-01-01']
    if name=='bond_wiest':
        priority=[h for h in subset if re.search(r'\b(?:wool|sheep|bought|manager|purchas\w*|open\w*|new|sold|start\w*)\b',h['snippet'],re.I)]
    for h in priority[:35]:
        print(h['issue_date'],h['page_id'],h['snippet'])
