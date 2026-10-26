"""Curated observations and source locators; no unreviewed OCR promoted to findings."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE=ROOT/'sources/school_and_merchant_2026-09-21'
pages=json.loads((ROOT/'research_evidence/full_life_chronology_2026-09-21/canonical_ocr_pages.json').read_text(encoding='utf-8'))
sources=[]
def source(id,title,path=None,url=None,level='',locator='',note=''):
    r=dict(id=id,title=title,evidence_level=level,locator=locator,note=note)
    if path:
        p=ROOT/path;r['local_file']=str(p.relative_to(ROOT)).replace('\\','/');r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    if url:r['url']=url
    sources.append(r)

dates=['1910-09-30','1910-10-07','1910-11-18','1911-01-27','1912-02-08','1919-01-10','1921-02-11','1921-09-09','1922-07-07']
for i,date in enumerate(dates,1):
    p=next(x for x in pages if x['issue_date']==date and x['content_page_ordinal']==1)
    source(f'S{i:02}',f'The Cuervo Clipper, {date}',p['local_issue_file'],
           f"https://econtent.unm.edu/digital/collection/dignews/id/{p['page_id']}",
           'contemporary newspaper; source image inspected','Printed front page / combined PDF page 2',
           'January 1911 numerical readings withheld; February 1921 pupil figures refer to Newkirk.' if i in (4,7) else '')
for id,title,file,url,level,note in [
 ('S10','Flora S. Page obituary (2023)','flora_page_obituary_2023.html','https://www.chavezfuneralhome.com/obituaries/flora-page','retrospective family account','Born 1931; attended Cuervo and Santa Rosa. No attendance dates.'),
 ('S11','Roy Kenneth Bailey obituary (2024)','roy_bailey_obituary_2024.html','https://www.chavezfuneralhome.com/obituaries/roy-bailey','retrospective family account','Born 1939; Santa Rosa High School class of 1958; named ranch employers, assignment dates unspecified.'),
 ('S12','Rudolpho (Rudy) Chavez obituary (2023)','rudy_chavez_obituary_2023.html','https://www.chavezfuneralhome.com/obituaries/rudolpho-rudy-chavez','retrospective family account','Born 1942; Cuervo and Santa Rosa schools; made home in Cuervo after 1965 marriage.'),
 ('S13','Tito S. Vigil obituary (2025)','tito_vigil_obituary_2025.html','https://www.chavezfuneralhome.com/obituaries/tito-vigil','retrospective family account','Born 1949; attended Cuervo schools; Santa Rosa High School class of 1967.'),
 ('S14','Fred L. Higgins obituary (2016)','fred_higgins_obituary_2016.html','https://www.chavezfuneralhome.com/obituaries/3943534','retrospective family account','Born 1952; grew up in Cuervo; Santa Rosa graduation in 1970. Does not state Cuervo-school attendance.'),
 ('S15','Old Cuervo school bid reported, December 11, 2011','cuervo_sale_2011_route66news.html','https://www.route66news.com/2011/12/11/elderly-woman-may-be-new-owner-of-old-cuervo-school/','secondary contemporary news report','Recounts print Guadalupe County Communicator coverage; bid/proposed acceptance, not proof of completed conveyance.'),
 ('S16','Cuervo school bid accepted, reported September 17, 2012','cuervo_sale_2012_route66news.html','https://www.route66news.com/2012/09/17/cuervo-school-building-has-a-new-owner/','secondary contemporary news report','Reports school-board acceptance of $10,250 bid; original minutes and deed not held.'),
 ('S17','Santa Rosa Consolidated Schools acknowledgment, September 16, 2026','santa_rosa_schools_acknowledgment_2026-09-16.pdf',None,'primary administrative correspondence','User-provided three-page letter, signed Marilyn Dodge; acknowledges gathering records, supplies no historical findings.')]:
    source(id,title,str((BASE/file).relative_to(ROOT)),url,level,'Entire relevant article; letter all three pages',note)
source('S18','Frank Bond & Son Records, MSS-133-BC: prior verified catalog leads',
       'research_evidence/archives_catalog_pull_list_2026-09-16.md','https://nmarchives.unm.edu/repositories/22/resources/1391',
       'catalog descriptions verified September 16; underlying books not held','Section 2',
       'September 21 direct fetch returned a bot-check page. No new catalog verification or account-book images.')
source('S19','Guadalupe County Records, 1974-020: prior verified school-record leads',
       'research_evidence/archives_catalog_pull_list_2026-09-16.md','https://nmarchives.unm.edu/repositories/32/archival_objects/842712',
       'catalog descriptions verified September 16; underlying records not held','SRCA_45408, folders 1, 2, 3, 5, 6',
       'School-series references extend through 1942, not through the alleged 1958 closure.')
source('S20','Full-life chronology, September 21, 2026','research_evidence/full_life_chronology_2026-09-21.md',
       level='prior project synthesis with primary-source locators',locator='School and merchant entries',
       note='Original 57 observations remain a dated release; this follow-up is an addendum.')
source('S21','Cuervo 1950 schedule, sheet 4',
       'sources/03_census/1950_manuscripts/ed_10-6/43290879-New_Mexico-180130-0005.jpg',
       level='primary census; previously manually read',locator='Lines 6 and 8',
       note='Prior name/occupation readings identify Joe Gallegos and Pearl Margaret Romero as resident schoolteachers. Census residence does not locate their schools.')
source('S22','J. Stuart Holbrook newspaper obituary lead',url='https://www.familysearch.org/patron/v2/TH-300-44997-73-40/dist.pdf?ctx=ArtCtxPublic',
       level='unverified cached OCR lead; scan not obtained',locator='Albuquerque Tribune, apparently A-2; exact issue date unverified',
       note='Cached OCR mentions Bond-Wiest association in Cuervo. Direct download HTTP 403; screenshot unavailable. June 1965 suggested by adjacent Gemini 4 news, not verified from masthead. Excluded as a dated operating-business observation.')

observations=[
 dict(id='E01',date='1910-09-30',subject='Cuervo school',measure='reported enrollment',value=67,unit='pupils',source='S01',new_this_pass=False,note='Prior verified baseline; paper also reports school-related moves into town.'),
 dict(id='E02',date='1910-10-07',subject='Cuervo school',measure='reported enrollment',value=75,unit='pupils',source='S02',new_this_pass=True,note='Visual reading corrects OCR 76; Mrs. Dr. Baker accepts teaching position.'),
 dict(id='E03',date='1910-11-18',subject='Cuervo school',measure='reported enrollment',value=93,unit='pupils',source='S03',new_this_pass=True,note='Snapshot, not annual enrollment or average attendance.'),
 dict(id='E04',date='1912-02-08',subject='Cuervo school',measure='cumulative enrollment since term began',value=132,unit='pupils',source='S05',new_this_pass=True,note='Do not mix with present enrollment; visual reading corrects OCR 131.'),
 dict(id='E05',date='1912-02-08',subject='Cuervo school',measure='present enrollment',value=106,unit='pupils',source='S05',new_this_pass=True,note='Reported current enrollment; not average daily attendance.'),
 dict(id='E06',date='1919-01-10',subject='Cuervo ninth-grade instruction',measure='interruption and announced replacement',value=None,unit=None,source='S06',new_this_pass=True,note='Pupils reportedly out of school because Prof. Simmons left; Miss Sanchez announces she will teach. Duration and actual resumption unknown.'),
 dict(id='E07',date='1921-09-09',subject='Cuervo school',measure='community support and proposed repairs/curriculum',value=None,unit=None,source='S08',new_this_pass=True,note='School Opens describes September 2 organization meeting, proposed volunteer help for practical subjects, and building/sanitation recommendations. Proposals are not proof of implementation.'),
 dict(id='E08',date='1922-07-07',subject='Easley garage',measure='reported business purchase',value=None,unit=None,source='S09',new_this_pass=True,note='Mr. Hamilton and Mr. Collier reportedly purchased J. F. Easley garage; purchase is not a closure.'),
 dict(id='E09',date='1922-07-07',subject='Bond & Wiest',measure='reported gasoline sales, interval unspecified',value=15,unit='barrels',source='S09',new_this_pass=True,note='Paper reports fifteen barrels sold to traveling public; no daily, weekly, or annual interval supplied. Do not convert to gallons without capacity evidence.'),
 dict(id='E10',date='2011-12-11',subject='Old Cuervo school property',measure='reported highest bid',value=10250,unit='nominal USD',source='S15',new_this_pass=True,note='Flora Page bid; report date, not exact bid or transfer date.'),
 dict(id='E11',date='2012-09-17',subject='Old Cuervo school property',measure='reported board acceptance of bid',value=10250,unit='nominal USD',source='S16',new_this_pass=True,note='Secondary report of Communicator article. Not exact board-meeting or deed date.'),
 dict(id='E12',date='2026-09-16',subject='School records request',measure='acknowledgment received as user-provided attachment',value=None,unit=None,source='S17',new_this_pass=False,note='Located and registered this pass. No historical records supplied in this letter; no live inbox checked.')
]
people=[
 dict(person='Flora S. Page',birth_year=1931,source='S10',school_path='Cuervo and Santa Rosa schools',graduation_year=None,limit='No attendance or transfer date. Eighth-grade graduation at stone building reported separately in S16.'),
 dict(person='Roy Kenneth Bailey',birth_year=1939,source='S11',school_path='Raised in Cuervo; Santa Rosa High School',graduation_year=1958,limit='No stated Cuervo-school attendance or bus route. High-school destination is not a school-closure date.'),
 dict(person='Rudolpho (Rudy) Chavez',birth_year=1942,source='S12',school_path='Cuervo school and Santa Rosa High School',graduation_year=None,limit='No dated transition. Made home in Cuervo after marrying in 1965, so school attendance elsewhere does not establish permanent migration.'),
 dict(person='Tito S. Vigil',birth_year=1949,source='S13',school_path='Cuervo schools and Santa Rosa High School',graduation_year=1967,limit='Elementary attendance dates unstated; age-based mid-1950s attendance would be an inference.'),
 dict(person='Fred L. Higgins',birth_year=1952,source='S14',school_path='Grew up in Cuervo; Santa Rosa schools',graduation_year=1970,limit='Does not state attendance at Cuervo school or year of reassignment.')
]
for filename,data in [('source_index.json',sources),('observations.json',observations),('pupil_paths.json',people)]:
    (HERE/filename).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'sources':len(sources),'observations':len(observations),'pupil_paths':len(people)}))
