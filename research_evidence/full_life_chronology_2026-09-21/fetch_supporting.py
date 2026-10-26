from pathlib import Path
import datetime, hashlib, json, urllib.request

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'sources/full_life_chronology_2026-09-21'
DEST.mkdir(parents=True,exist_ok=True)
ITEMS=[
 ('bond_archaeological_report_193.pdf','https://nmarchaeology.org/wp-content/uploads/2024/04/193.pdf'),
 ('state_line_tribune_bond_wiest.pdf','https://newspapers.swco.ttu.edu/server/api/core/bitstreams/b7594ff9-73d9-44dc-bc81-8fa4829d50a3/content'),
 ('el_paso_times_1911-05-16_p7.html','https://texashistory.unt.edu/ark:/67531/metapth581912/m1/7/'),
 ('usps_postmasters_city.html','https://about.usps.com/who/profile/history/postmaster-finder/postmasters-by-city.htm'),
 ('loc_clipper_catalog.json','https://www.loc.gov/item/sn92072379/?fo=json'),
]
manifest=[]
for name,url in ITEMS:
 p=DEST/name
 try:
  if not p.exists():
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (historical research)'}),timeout=45) as r: p.write_bytes(r.read())
  data=p.read_bytes()
  manifest.append({'file':str(p.relative_to(ROOT)),'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  print('OK',name,len(data),flush=True)
 except Exception as e:
  manifest.append({'url':url,'error':repr(e)})
  print('FAIL',name,repr(e),flush=True)
(DEST/'download_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
