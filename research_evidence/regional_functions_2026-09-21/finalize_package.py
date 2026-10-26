"""Register this dated research package and validate links, counts and held files."""
from pathlib import Path
import json, re, hashlib
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SRC=ROOT/'sources/regional_functions_2026-09-21'

guide='sources/regional_functions_2026-09-21/rittenhouse_1946/b99b026a-2ef9-4995-b8f4-107c50846580/'
observations=[
 dict(id='RF-B01',entity='Cuervo roadside provision',date='1946',source_type='Contemporary guide',
      observation='Gasoline and groceries reported; cafe, garage and tourist accommodation absent in the guide description.',
      locator='Rittenhouse, A guide book to highway 66, p. 73; Newberry G89.747',
      local_file=guide+'21978e4f91fb7dc4.jpg',limit='One date and observer; population geography unspecified; no continuing-absence claim.'),
 dict(id='RF-B02',entity='Newkirk roadside provision',date='1946',source_type='Contemporary guide',
      observation='More food and lodging provision than in the Cuervo entry.',locator='Rittenhouse p. 73',
      local_file=guide+'21978e4f91fb7dc4.jpg',limit='Comparative observation, not a controlled causal comparison.'),
 dict(id='RF-B03',entity='Santa Rosa roadside provision',date='1946',source_type='Contemporary guide',
      observation='Wider range of roadside and general services.',locator='Rittenhouse pp. 73-74',
      local_file=guide+'19e568a5727958a0.jpg',limit='Does not identify customer origins or spending.'),
 dict(id='RF-B04',entity="Willa's Beauty Shop",publication_date='2005-02-15',operating_interval=None,
      source_type='Family obituary',observation='Santa Rosa shop ownership reported without operating dates.',
      url='https://www.chavezfuneralhome.com/obituaries/813378',
      local_file='sources/pupil_links_and_holbrook_2026-09-21/willa_higgins_2005.html',
      limit='Does not date overlap with Cuervo residence. Preserved source rechecked; new web fetch failed.'),
 dict(id='RF-B05',entity="Elma's Beauty Shop",date='1950',source_type='Census occupation and industry entry',
      observation='Elma Jones, proprietor, named shop.',locator='ED 10-9, sheet 10, line 10',
      local_file='sources/03_census/1950_manuscripts/ed_10-9/43290879-New_Mexico-180133-0011.jpg',
      limit='Presence in schedule; opening and closure unknown.'),
 dict(id='RF-B06',entity='Regional telephone directory',date='1960-12',status='Catalog lead; volume not held',
      source_type='User-contributed catalog listing',
      observation='Mountain States directory includes Santa Rosa among six named regional communities.',
      url='https://www.librarything.com/nseries/371859/New-Mexico-Telephone-Directories',
      limit='Institutional holding and digitized copy unverified; no business listing read.'),
 dict(id='RF-B07',entity='Unnamed Cuervo gas station north of I-40',publication_date='2013-10-01',
      reported_visit_date='Recent trip; exact date unspecified',source_type='First-person travel account',
      author='K. Mennem',observation='Describes functioning fuel service north of I-40 alongside the older settlement to the south.',
      url='https://www.sandiegoreader.com/news/2013/oct/01/travel-new-mexico-ghost-towns/',
      local_file='sources/regional_functions_2026-09-21/mennem_2013_ghost_towns.html',
      limit='Single published observation; no named operator, receipt or continuous operating history.'),
]
for number,fid,name,address,ast,ust,page in [
    (8,'1927',"Tony's Texaco",'Exit 291 I-40, Cuervo',0,3,14),
    (9,'30531','Sena Station','Guadalupe, Cuervo',0,4,74),
    (10,'31151','Cuervo Gas Station','291 Exit I-40; frontage-road text truncated, Cuervo',3,3,83)]:
    observations.append(dict(id=f'RF-B{number:02}',entity=name,facility_id=fid,record_as_of='2020-11-19',
        source_type='NMED administrative tank inventory',status='Row and headers visually checked',
        address_as_recorded=address,removed_AST=ast,removed_UST=ust,in_use_AST=0,in_use_UST=0,pdf_page=page,
        local_file='sources/regional_functions_2026-09-21/nmed_all_storage_tanks_2020-11-19.pdf',
        limit='No removal or business-closure date; not yet reconciled to parcels or other registrations.'))
observations += [
 dict(id='RF-B11',entity='Later NMED name listing',record_as_of='2025-05-15',source_type='Administrative inventory',
      observation='FIDs 1927, 30531 and 31151 listed on PDF pages 30, 169 and 191.',
      status='762-page PDF held; facility names checked in web PDF text',
      local_file='sources/regional_functions_2026-09-21/nmed_all_storage_tanks_generated_2025-05-15.pdf',
      limit='Filename says May 14; printed generation date says May 15. Inclusion is not active operation.'),
 dict(id='RF-B12',entity='Whiting Brothers No. 75, west Cuervo',date=None,status='Unverified lead',
      source_type='Collector report of information received from another person',
      observation='Reported highway-department purchase and demolition for I-40.',
      url='https://rt66.x10host.com/wbros/gastable.html',
      limit='No acquisition instrument, plan or dated image verified the event. Not linked to NMED sites.'),
 dict(id='RF-B13',entity='Commercial/postal building fabric',metadata_date='1986-03',
      source_type='William J. Lucas photograph, UNM PICT-986-012',identifier='986-012-0009.tif',
      observation='Postal sign, commercial lettering, tires and barrels visible at standing building.',
      url='https://econtent.unm.edu/digital/collection/wjlr66/id/9/rec/1',
      local_file='sources/09_photographs/lucas_cuervo_1986-03_986-012-0009_access.jpg',
      limit='Visible signs and fabric do not establish business or postal operation.')]
(HERE/'business_observations.json').write_text(json.dumps({
    'method':'Publication dates, reported event dates, administrative status dates and unverified leads are distinct. Records are not unique establishments.',
    'observations':observations},indent=2)+'\n',encoding='utf-8')

manifest=json.loads((SRC/'download_manifest.json').read_text())
validated=[]
for entry in manifest:
    if entry.get('status') not in ['downloaded','downloaded_error_response']:continue
    p=ROOT/entry['local_file'];data=p.read_bytes()
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],p
    if p.suffix=='.json':
        obj=json.loads(data)
        if isinstance(obj,dict) and 'error' in obj:
            entry['status']='downloaded_error_response'
            entry['validation_status']='rejected_as_source'
            entry['validation_note']=obj['error']
            continue
    if p.suffix=='.pdf':
        assert data.startswith(b'%PDF'),p
        entry['pdf_pages']=len(PdfReader(p).pages)
    if p.name=='mennem_2013_ghost_towns.html':assert b'functional gas station' in data
    entry['validation_status']='file_checked'
    validated.append(entry['local_file'])
(SRC/'download_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

summary_text=(
    '**Latest follow-up:** [Regional work, business survival and population geography](research_evidence/regional_functions_2026-09-21.md) '
    "adds a first visual pass through all 87 Santa Rosa 1950 population sheets: 643 main occupation appearances plus one industry-only entry, "
    "compared with Cuervo's 56. Selected families combined agriculture, rail, retail and services. A 1946 guide documents different roadside "
    "provision; a 2013 visitor reports a working north-side Cuervo fuel station; NMED inventories supply three facility IDs without closure dates. "
    "Modern block analysis exposes the village/hinterland allocation problem and does not establish a precise 2010–2020 village trend. "
    "Willa's shop dates and the post-1950 historical population bridge remain open.\n\n")
p=ROOT/'SUMMARY.md';s=p.read_text(encoding='utf-8')
if 'Regional work, business survival and population geography' not in s:
    s=s.replace('**Latest follow-up:**','**Preceding follow-up:**',1)
    s=s.replace('## The project\n\n','## The project\n\n'+summary_text,1)
s=s.replace('The other five acquired census districts are not systematically transcribed.',
    "Santa Rosa EDs 10-8, 10-9 and 10-10 now have a complete first pass through main occupation fields, with relationship anchors and selected family checks; "
    "they do not yet have a reconciled full-person/household transcription. Newkirk ED 10-7 and rural Santa Rosa ED 10-11 remain untranscribed.")
p.write_text(s,encoding='utf-8')

update=("**Regional-functions follow-up, later September 21:** [the new report](research_evidence/regional_functions_2026-09-21.md) "
        "adds 643 Santa Rosa main occupation appearances from 87 sheets, selected mixed-occupation families, a 1946 roadside comparison, "
        "a 2013 fuel-service observation and three NMED facility IDs. The 2010/2020 block audit demonstrates the settlement/hinterland "
        "allocation problem; no precise village trend or business-closure dates are claimed. See RFG-01–05 and PJ-11.\n\n")
p=ROOT/'DOCUMENT-REGISTER.md';s=p.read_text(encoding='utf-8')
if 'RFG-01' not in s:
    s=s.replace('## ⚠ Read this first\n\n','## ⚠ Read this first\n\n'+update,1)
    lines=s.splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('| PJ-10 |'))
    lines.insert(idx+1,'| PJ-11 | Regional work, business survival and population-boundary study | COMPLETE FIRST PASS Sep 21; dates and geographic bridge remain OPEN | [Report](research_evidence/regional_functions_2026-09-21.md), two figures, 643 main occupation appearances, 13 business observations/leads, source hashes and reproducible geographic analysis. |')
    s='\n'.join(lines)+'\n'
    s+='''
## Regional-functions source additions, September 21

| ID | Document or dataset | Status | Evidence and limits |
|---|---|---|---|
| RFG-01 | Rittenhouse, *A guide book to highway 66* (1946), Newberry G89.747 | 24 reading-resolution spreads HELD; selected pages READ | [Reading index](research_evidence/regional_functions_2026-09-21/rittenhouse_reading_index.json). Printed pp. 73–74 compare roadside provision. Separate thumbnails do not count as reading copies. |
| RFG-02 | 1950 Santa Rosa main occupation inventory, EDs 10-8, 10-9, 10-10 | All 87 population sheets first-pass READ | [643 occupation entries plus one industry-only row](research_evidence/regional_functions_2026-09-21/occupation_entries_flat.json). Possible duplicates, faint readings and incompatible population denominators retained explicitly. |
| RFG-03 | 2010 block population/housing and 2020 block geometry joined to DHC | HELD and ANALYZED | [Geographic audit](research_evidence/regional_functions_2026-09-21/population_geometry_audit.json). County totals reconcile; 902/902 2020 blocks match DHC counts. Defined-window allocations cannot establish a precise village trend. |
| RFG-04 | NMED tank inventories, generated November 19, 2020 and May 15, 2025 | 108- and 762-page PDFs HELD; selected rows READ | FIDs 1927, 30531, 31151 provide targets for historical facility files. Removed-tank status is not a business-closing date; distinct sites unverified. [Reading locators](research_evidence/regional_functions_2026-09-21/nmed_facility_reading_locators.json). |
| RFG-05 | K. Mennem, “Ghost towns of New Mexico,” October 1, 2013 | HTML HELD; relevant passage READ | First-person report of functioning gas station north of I-40. Exact trip date and business identity unstated. [Observation RF-B07](research_evidence/regional_functions_2026-09-21/business_observations.json). |
'''
p.write_text(s,encoding='utf-8')

p=ROOT/'research_evidence/research_status_2026-09-21.md';s=p.read_text(encoding='utf-8')
if 'Regional-functions follow-up' not in s:
    u=update.replace('(research_evidence/regional_functions_2026-09-21.md)','(regional_functions_2026-09-21.md)').replace(' See RFG-01–05 and PJ-11.','')
    s=s.replace('## Where the project stands\n\n','## Where the project stands\n\n'+u,1)
p.write_text(s,encoding='utf-8')

# Validate actual deliverable links and structural arithmetic, without re-running the research.
report=ROOT/'research_evidence/regional_functions_2026-09-21.md'
local_links=re.findall(r'\]\((B:/[^)]+)\)',report.read_text(encoding='utf-8'))
missing=[x for x in local_links if not Path(x).exists()]
assert not missing,missing
comparison=json.loads((HERE/'occupation_comparison.json').read_text())
assert sum(r['santa_rosa'] for r in comparison['sectors'])==643
assert sum(r['cuervo'] for r in comparison['sectors'])==56
assert len(comparison['santa_rosa_industry_only_rows'])==1
geometry=json.loads((HERE/'population_geometry_audit.json').read_text())
assert geometry['tiger_dhc_different_blocks']==0
for region in geometry['study_areas']:
    assert region['population_lower']<=region['population_upper']
    assert region['housing_lower']<=region['housing_upper']
files=['business_observations.json','occupation_entries_flat.json','occupation_comparison.json',
       'santa_rosa_occupation_readings.json','population_geometry_audit.json','study_windows.geojson',
       'occupation_comparison.png','population_boundary_problem.png','analyze_occupations.py',
       'analyze_population_geometry.py','read_tank_inventories.py']
output_manifest=[{'path':(HERE/name).relative_to(ROOT).as_posix(),
                 'sha256':hashlib.sha256((HERE/name).read_bytes()).hexdigest()} for name in files]
output_manifest.append({'path':report.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(report.read_bytes()).hexdigest()})
(HERE/'output_manifest.json').write_text(json.dumps(output_manifest,indent=2)+'\n',encoding='utf-8')
validation={'local_report_links_checked':len(local_links),'missing_links':missing,
            'main_occupation_entries':{'Cuervo':56,'Santa_Rosa':643},'industry_only_extra':1,
            'Santa_Rosa_population_sheets':87,'independent_double_transcription':False,
            'business_observations_and_leads':len(observations),'source_files_hash_checked':validated,
            'visual_QA':['occupation comparison figure','population boundary figure','three 2020 NMED rows and headers'],
            'open_limits':['Possible census duplicates and faint readings','Private-household/population reconciliation',
                           'Willa shop dates','Facility identity and business closing dates',
                           '1960-2000 settlement population and geographic continuity']}
(HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
print(json.dumps(validation,indent=2))
