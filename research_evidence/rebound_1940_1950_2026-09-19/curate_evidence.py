"""Source-addressable observations; manual readings, not inferred vital events."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding='utf-8')

sources = {
    'C40': {'title':'1940 population census, Cuervo precinct, Guadalupe County, ED 10-6',
        'local':'sources/03_census/1940_manuscripts/ed_10-6/',
        'url':'https://nara-1940-census.s3.us-east-2.amazonaws.com/population-schedules/nm/guadalupe-county/ed/10-6/m-t0627-02445-00652.jpg',
        'locator':'Images 00652-00656; sheets 1A-3A. Exact image/sheet/line in person observations.'},
    'C50': {'title':'1950 population census, Cuervo precinct, Guadalupe County, ED 10-6',
        'local':'sources/03_census/1950_manuscripts/ed_10-6/',
        'url':'https://1950census.archives.gov/search/?county=Guadalupe&ed=10-6&page=1&state=NM',
        'locator':'Images 0002-0010; sheets 1-8 and 71. Supplementary questions 21-24 and 33a.'},
    'A45': {'title':'1945 Census of Agriculture, New Mexico',
        'local':'sources/03_census/agriculture_rebound_2026-09-19/1945_nm_agriculture_full.pdf',
        'url':'https://www.nass.usda.gov/AgCensus/archive/files/1945-New_Mexico-1945-01-full.pdf',
        'locator':'County Table I, printed 20 / PDF 37; County Table III, printed 54 / PDF 71.'},
    'A50': {'title':'1950 Census of Agriculture, New Mexico county tables',
        'local':'sources/03_census/agriculture_rebound_2026-09-19/1950_nm_agriculture_counties.pdf',
        'url':'https://www.nass.usda.gov/AgCensus/archive/files/1950-New_Mexico_and_Arizona-Table_of_Contents-1809-Table-03.pdf',
        'locator':'Table 1, printed 40-41 / PDF 3-4; Table 4, printed 52 and 54-55 / PDF 15 and 17-18.'},
    'A50D': {'title':'1950 Census of Agriculture, introduction and definitions',
        'local':'sources/03_census/agriculture_rebound_2026-09-19/1950_nm_az_agriculture_introduction.pdf',
        'url':'https://www.nass.usda.gov/AgCensus/archive/files/1950-New_Mexico_and_Arizona-Table_of_Contents-1809-Table-01.pdf',
        'locator':'Printed XI-XII / PDF 10-11: dates, farm definition, comparability, cross-county operations.'}
}
save('source_index.json', sources)

agri = []
def add(metric, year, value, unit, src, page, pdf, row, period):
    agri.append(dict(geography='Guadalupe County, New Mexico', metric=metric, reference_year=year,
        value=value, unit=unit, source_id=src, printed_page=page, pdf_page=pdf, row=row, reference_period=period))
for year,value in [(1940,19227),(1945,27047)]:
    add('cattle_and_calves_inventory',year,value,'head','A45','54',71,'9', 'April 1, 1940' if year==1940 else 'January 1, 1945')
add('cattle_and_calves_inventory',1950,41276,'head','A50','52',15,'16','Approximately April 1; county average enumeration falls April 15-28, 1950')
for year,value in [(1939,7399),(1944,19724)]:
    add('cattle_and_calves_sold_alive',year,value,'head','A45','54',71,'35',f'Calendar year {year}')
add('cattle_and_calves_sold_alive',1949,17595,'head','A50','55 (labels on 54)',18,'31','Calendar year 1949')
for year,value in [(1940,370),(1945,481)]:
    add('farms_reporting_cattle_inventory',year,value,'farms','A45','54',71,'8','Inventory census date')
add('farms_reporting_cattle_inventory',1950,325,'farms','A50','52',15,'14','Inventory census date')
for year,value in [(1940,476),(1945,640)]:
    add('farms',year,value,'farms','A45','20',37,'1','Census year; definitions differ from 1950')
add('farms',1950,381,'farms','A50','41 (labels on 40)',4,'1','Census year; revised definition')
for year,value in [(1940,963025),(1945,1517361)]:
    add('land_in_farms',year,value,'acres','A45','20',37,'4','Census year')
add('land_in_farms',1950,1827287,'acres','A50','41 (labels on 40)',4,'10','Census year')
for year,value in [(1940,2023.2),(1945,2370.9)]:
    add('average_farm_size',year,value,'acres','A45','20',37,'7','Census year')
add('average_farm_size',1950,4796.0,'acres','A50','41 (labels on 40)',4,'12','Census year')
save('agriculture_observations.json', {
    'method':'Manual visual readings of the Guadalupe County columns; row labels and footnotes checked. Not Cuervo-level statistics.',
    'cautions':['Inventories use different seasons; sales are full calendar-year head counts, not prices, profits, local rail shipments, or unique locally raised animals.',
        '1950 farm definition is less inclusive for many small places. Do not interpret the entire farm-count fall as consolidation.',
        'Cross-county operations could be assigned wholly to one county under the published rules.',
        'The 1940 cattle inventory is 19,227, confirmed in an enlarged crop; an unpublished preliminary reading of 15,227 was rejected.'],
    'observations':agri})

residence = [
    ('1950-1-3','California; county/place blank','out_of_county','No box emphasized; earlier Yes mark also visible.'),
    ('1950-1-8','Tatum, Lea County, New Mexico','out_of_county','No in same-house question; address clear.'),
    ('1950-1-13','Tatum, Lea County, New Mexico','out_of_county','Same-house checkbox overwritten; retained because address is explicit. Do not treat checkbox as independently clean.'),
    ('1950-1-18','Texas; county/place unresolved','out_of_county','County/place heavily overwritten. Earlier working guess Houston is not accepted.'),
    ('1950-6-11','Tucumcari, Quay County, New Mexico','out_of_county','No in same-house question; address clear.'),
    ('1950-6-16','Tucumcari, Quay County, New Mexico','out_of_county','Same-house checkbox overwritten; address explicit.'),
    ('1950-7-5','Santa Rosa, Guadalupe County, New Mexico','within_county','Same-house No; county/place written despite same-county boxes being blank.')]
people = {p['id']:p for p in json.loads((HERE/'people_name_age_readings.json').read_text())}
readings=[]
for pid,address,kind,note in residence:
    p=people[pid]
    readings.append(dict(person_id=pid,name_read=p['given_read']+' '+p['surname_read'],age=p['age_completed_years'],
        household=p['household'],source_id='C50',sheet=p['sheet'],line=p['line'],prior_residence_read=address,
        reference='one year before the 1950 census, approximately April 1949',movement_type=kind,note=note))
save('prior_residence_readings.json', {'method':'Screened all retained supplementary blocks for written prior-residence places. These are selected sample-line observations, not a complete migration census. Blank, same-house, vacant, and less-than-one-year entries are not migration observations. Do not multiply by five.', 'observations':readings})

vets=[]
for pid,prior in [('1950-1-23','1940-3A-12'),('1950-3-1','1940-1A-38'),('1950-5-14','1940-2A-30'),('1950-6-11',None),('1950-71-2',None)]:
    p=people[pid]
    vets.append(dict(person_id=pid,name_read=p['given_read']+' '+p['surname_read'],age=p['age_completed_years'],
        source_id='C50',sheet=p['sheet'],line=p['line'],question='33a, service during World War II',answer_read='Yes',
        candidate_1940_person=prior,linkage_status='strong candidate; not externally verified' if prior else 'not linked in this pass'))
save('wwii_service_readings.json',{'method':'Five affirmative boxes read in the supplementary questions. This is a minimum observed count of self-reported veterans in 1950, not total enlistments, draftees, wartime absences, casualties, or a service rate. Non-sample residents generally lack these answers.', 'observations':vets})

links = [
    {'case':'Gonzales','status':'strong household candidate; head given name uncertain','1940_households':['1940-2A-35'],'1950_households':['1950-4-10'],
     'evidence':'Parents approximately age ten years; Arcenio, Josefina, and Gloria recur. Two younger children appear; Elena and Noe are absent from this 1950 household.',
     'limit':'7 to 7 does not mean no demographic change; no destination or death inferred for absent children.'},
    {'case':'Bailey','status':'strong parent/household candidate; some child names differ','1940_households':['1940-2B-78'],'1950_households':['1950-7-11'],
     'evidence':'Paul E. 41 to 51 and Mildred May 28 to 38; households of 9 and 12. Three children under ten appear in 1950.',
     'limit':'Do not claim all older children are fully linked or births occurred in Cuervo.'},
    {'case':'Yates','status':'strong family candidate','1940_households':['1940-3A-7'],'1950_households':['1950-7-24','1950-1-23'],
     'evidence':'James, Minnie, Mary and Henry recur with plausible ages. Henry 24 to 34 is separately head-listed in 1950 and reports WWII service.',
     'limit':'The two 1950 households include Virginia Yates, Leo Ballard and Jimmy Boyle; they are not seven linked original residents. Continuous residence not established.'},
    {'case':'Trujillo','status':'strong couple candidate','1940_households':['1940-2A-3'],'1950_households':['1950-3-16'],
     'evidence':'Juan B. and Reyes recur, ages 57/41 to 66/50. Household 8 to 3; six listed sons replaced in this household by one grandson.',
     'limit':'Absence from this household does not establish death, military service, or migration destination.'},
    {'case':'Maestas','status':'strong couple candidate','1940_households':['1940-2A-22'],'1950_households':['1950-5-16'],
     'evidence':'Antonio/Gilberta 23/18 to 33/28, plus Tony Jr. age 8; household 2 to 3.',
     'limit':'No birthplace within the precinct or uninterrupted residence established.'},
    {'case':'Duran','status':'strong couple candidate','1940_households':['1940-3A-28'],'1950_households':['1950-2-27'],
     'evidence':'Jose Maria/Jose M. and Antonia recur at 50/41 and 60/52; two people at both endpoints.',
     'limit':'Antonia age differs from exact ten-year progression.'},
    {'case':'Alfonso Chavez and Lucy Gomez','status':'probable, needs external marriage/identity check','1940_households':['1940-1A-1','1940-2B-63'],'1950_households':['1950-6-20'],
     'evidence':'Alfonso 27 and Lucy Gomez 19 in separate 1940 families plausibly become Alfonso 38 and Lucy 30 in 1950; six children under ten and Mary Frances Gomez, sister-in-law, in their household.',
     'limit':'Common names; family link probable, not proved. Do not subtract the entirety of the two parent households to obtain a family change.'},
    {'case':'Felix Marez / Felix Sierra','status':'ambiguous, not accepted','1940_households':['1940-2A-27'],'1950_households':['1950-5-2'],
     'evidence':'Given names, spouse Eva and ages resemble each other, but the surnames differ.',
     'limit':'No identity link used in calculations or conclusions.'}
]
save('household_linkage_examples.json', {'method':'Selected manually reviewed candidates. Not exhaustive person linkage, and no automatic string match is treated as proof.', 'cases':links})
print('Saved source index, agricultural observations, residence readings, service readings, and eight linkage cases.')
