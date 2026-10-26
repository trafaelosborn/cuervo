"""Curated, source-linked observations. OCR candidates are stored separately."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
audit=json.loads((ROOT/'sources/02_newspapers/cuervo_clipper/full_scan_audit_2026-09-17.json').read_text(encoding='utf-8'))
bydate={x['issue_date']:x for x in audit['issues']}
sources={}
dates=['1910-01-28','1910-02-04','1910-03-04','1910-06-10','1910-07-08','1910-09-30','1911-04-21','1911-09-14','1912-04-04','1918-02-15','1921-02-11','1921-03-11','1921-04-15','1922-09-29','1922-12-01']
for i,date in enumerate(dates,1):
    item=bydate[date]
    sources[f'C{i:02}']={'title':f'Cuervo Clipper, {date}, front page','file':item['file'],
                         'locator':'PDF page 2 (after repository cover)', 'url':item['catalog_url'],
                         'review':('Front page visually checked in the September 17 study; prior reading retained.' if date == '1922-12-01' else 'Relevant front page visually checked in this study.')}
def source(key,title,file,locator,url='',review='Existing project study; underlying primary-source locators retained there.'):
    sources[key]=dict(title=title,file=file,locator=locator,url=url,review=review)
source('D20','New Mexico State Business Directory, 1920, Part 1','sources/11_business_directories/newmexicostatebu01unse_0.pdf','Printed 190; PDF 305','https://archive.org/details/newmexicostatebu01unse_0','Complete Cuervo entry visually rechecked.')
source('D21','New Mexico State Business Directory, 1921, Part 1','sources/11_business_directories/newmexicostatebu01unse.pdf','Printed 186-187; PDF 289 and 291','https://archive.org/details/newmexicostatebu01unse','Complete Cuervo entry visually rechecked; PDF 290 is blank reverse.')
source('N47','State Line Tribune, January 2, 1947','sources/full_life_chronology_2026-09-21/state_line_tribune_bond_wiest.pdf','PDF 1 (date) and 3 (El Rancho advertisement and mill article)','https://newspapers.swco.ttu.edu/server/api/core/bitstreams/b7594ff9-73d9-44dc-bc81-8fa4829d50a3/content','New acquisition; date, advertisement and adjacent mill article visually checked.')
source('LC','Library of Congress newspaper catalog, sn92072379','sources/full_life_chronology_2026-09-21/loc_clipper_catalog.json','Notes and dates of publication','https://www.loc.gov/item/sn92072379/','Catalog metadata retrieved September 21; bibliographic evidence, not a surviving final issue.')
source('AR','Stephen S. Post, Las Campanas de Santa Fe, Archaeology Notes 193 (1996)','sources/full_life_chronology_2026-09-21/bond_archaeological_report_193.pdf','Printed 55; PDF 63','https://nmarchaeology.org/wp-content/uploads/2024/04/193.pdf','Secondary historical discussion checked visually; summarizes Grubbs (1960), not independently acquired here.')
source('P13','Discontinuance of Star Routes, Senate Document 460 (1914)','sources/05_postal/us_post_office_star_routes_curtailed_1914.pdf','Printed/PDF 33, New Mexico; route 67404',review='Previously checked September 18; Hanson-Cuervo route, not Cuervo post-office closure.')
source('P11','USPS Postal Bulletin 22323, November 3, 2011','sources/05_postal/usps_postal_bulletin_22323_2011-11-03.pdf','Printed/PDF 13','https://about.usps.com/postal-bulletin/2011/pb22323/pdf/pb22323.pdf','Cuervo row visually rechecked; administrative effective date distinguished from last counter-service date.')
source('A','Archives catalog pull list','research_evidence/archives_catalog_pull_list_2026-09-16.md','Town-company record; Bond & Wiest volumes 116, 114, 106, 200, 213, 207 and 208','https://nmarchives.unm.edu/repositories/22/resources/1391','Cataloged holdings; underlying merchant and company books not acquired.')
source('POP','Verified population series and later census study','research_evidence/population_series_verified.md','1910-1950 precinct observations; later town/county tables')
source('DEEP','September 17 primary-source deep dive','research_evidence/deep_dive_2026-09-17.md','Sections 3-7 and source index: 1902 railway, 1908 Sanborn, 1926 timetable, 1929 retail, 1950 occupations, highway chronology')
source('REB','1940-1950 rebound and agricultural context','research_evidence/rebound_1940_1950_2026-09-19.md','County cattle sales and household analysis; corrected 1950 ages')
source('PRICE','Real cattle prices study','research_evidence/real_cattle_prices_2026-09-19.md','USDA New Mexico prices, BLS CPI-U, 1913-1978')
source('RAIL','Cuervo railway functions study','research_evidence/rail_local_functions_2026-09-20.md','Dated observations and primary-source index; 1956-1958 office/passenger changes and 1967 siding')
source('F74','Rock Island 1974 freight accounting study','research_evidence/cuervo_freight_accounting_1974_2026-09-20.md','December 15 Station Book; Cuervo and code 8310')
source('CH','Church and supporting acquisitions','research_evidence/additional_acquisitions_2026-09-18.md','Church section; 2017 funeral announcement, 2018 directory, 2025 bulletin')
source('R26','Contemporary ranching verification','research_evidence/contemporary_ranching_2026-09-21.md','Rancho Armendariz; 2026 interview and conservation-award announcement')
source('PUB','Public narrative audit','research_evidence/popular_narrative_audit_2026-09-21.md','HistoryNet school-closure claim; unverified administrative date')
source('SR72','New Mexico Senate Memorial 17 (2025)','research_evidence/research_status_2026-09-21.md','Santa Rosa comparison; I-40 completion in 1972','https://www.nmlegis.gov/Sessions/25%20Regular/memorials/senate/SM017.html','Official retrospective statement; already inspected September 21.')

# Date is the observation/event interval, never an invented opening or closure date.
# Types: observed, reported, proposed, catalog, context, unresolved.
rows=[
('Before c.1901','unresolved','Ranching and settlement baseline','The exact pre-town ranching chronology and townsite creation remain unverified. Town-company records and 1892-1903 assessments are cataloged.','A','Do not turn broad catalog collection dates into dates for the town-company volume.'),
('1901-1902','context','Railway corridor forms','The contemporary 1902 railway report describes the connection at Santa Rosa. Cuervo\'s exact station-opening and plat dates are still missing.','DEEP','Regional railway context, not a Cuervo opening certificate.'),
('Early 1900s / 1904-1908','catalog','Early mercantile activity','A later historical report places Bond expansion to Cuervo in the early 1900s; the archive catalogs a Bond & Wiest ledger for 1904-1908.','AR,A','The ledger has not been read; no opening date, revenue or customer geography established.'),
('1908','context','Santa Rosa already has regional functions','Sanborn maps identify government, banking, wholesale premises and other services before Route 66.','DEEP','Comparison-town baseline; no inference that its customers all came from Cuervo.'),
('1908-1909? / by January 1910','catalog','Clipper origins','The LOC catalog says January 1909; the April 15, 1921 paper says it is entering its fourteenth year. Surviving local scans begin January 1910.','LC,C13','Founding accounts are inconsistent; the first surviving issue is not the first published issue.'),
('1910-01-28','reported','Telephone connection','The Clipper reports completion of the Cuervo-Montoya telephone line.','C01','Dated report of improved communication; no subscriber count.'),
('1910-01-28','reported','Passing cattle handled at Cuervo','Five carloads of cattle were unloaded the previous Sunday to feed and rest while en route to Kansas City; several reportedly died.','C01','Direct report of livestock handling, not evidence the cattle originated near Cuervo.'),
('1910-01-28','observed','Commercial and medical services','Advertisements name Bond & Wiest, Big Jo Lumber, Cuervo Drug Store, Rock Island Boarding House, two physicians and a visiting dentist.','C01','Advertisements establish offers at this date, not occupancy, receipts or full-time staffing.'),
('1910-02-04','reported','Livery exit and planned garage conversion','T. L. Lewis reportedly closed out his livery business and entered cattle dealing; Long Commission Company announced it would take over the livery barn and convert it to a garage.','C02','Owner exit and proposed reuse. Completion of the conversion is not established here.'),
('1910-03-04','reported','Sheep shipped and merchants traded','The paper reports fourteen cars of sheep loaded at Cuervo for Kansas, a separate purchase of over 4,000 sheep from Bond & Wiest, and produce unloaded for the merchant.','C03','Do not equate the fourteen cars with the separate 4,000-head purchase; the report does not explicitly link them.'),
('1910-06-10','reported','Townsite promotion','A list of purchasers of lots in the Thompson Townsite addition appears in the paper.','C04','A contemporary sales claim; deeds, occupancy and the original town plat remain unverified.'),
('1910-06-30; reported July 8','reported','School bonds approved','The Sixth (Cuervo) School District reportedly approved $4,000 in bonds with one opposing vote for a new stone school building.','C05','Vote authorizes investment; it is not a completion date.'),
('1910-09-30','reported','School draws families','Prof. Haight reports 67 enrolled pupils; the paper says families are moving into Cuervo from the surrounding country for schooling.','C06','Enrollment is reported, and the migration statement is qualitative. The forecast of 100 pupils is not an observed count.'),
('1910 and 1920 censuses','observed','Early population observations','Cuervo precinct totals are 545 and 438, respectively.','POP','The 1920 compendium warns of redistricting. These are not fixed-footprint town counts.'),
('1911-04-21','reported','School financing advances','The paper says bonds have been sold and the board is ready for bids on a stone school with four rooms.','C07','Stronger evidence of implementation than the earlier vote, but still not completion.'),
('1911-09-14','reported','School under construction','Contractor J. B. Colvin is identified as in charge of erecting the new school.','C08','Construction is underway by this report.'),
('1911-09-14','reported','Lumber stock being withdrawn','Big Jo Lumber is reported to be shipping out its stock and cutting prices on what remains.','C08','Evidence of stock withdrawal/liquidation activity; the final yard closure and reason are unverified.'),
('1911-09-14','reported','Depot platform improved','Section foreman Hanson reportedly widened and improved the depot platform.','C08','Railway facilities were receiving work alongside other commercial changes.'),
('1912-04-04','reported','New school in use','The paper describes a new two-story school, two employed teachers and an expectation of needing a third; it again reports seasonal moves into Cuervo for school.','C09','The third teacher is a forecast. Exact opening day and identity of today\'s surviving building require confirmation.'),
('1913-07-15','observed','Hanson-Cuervo mail route discontinued','The Post Office report records discontinuance of the 7.5-mile, three-round-trip-weekly route because Hanson lacked a suitable postmaster candidate.','P13','Loss of a feeder route; Cuervo\'s own post office did not close at this date.'),
('1918-02-15','reported','Oklahoma Hotel changes hands','S. P. Morison is reported to have purchased the Oklahoma Hotel from Mrs. Lizzie Mason the preceding Monday.','C10','A sale, not a closure. The buyer is listed as Morrison in later directories.'),
('1918-02-15','observed','Medical and automobile services','Dr. A. A. Sanford advertises at the Cuervo drugstore; S. P. Morison advertises the Ford Garage, repairs and gasoline.','C10','Dated service offers before Route 66 designation.'),
('1920','observed','Broad business directory baseline','The Cuervo entry lists two hotels, Golden Rule Garage, several merchants, a school principal, postmaster, railway/express/telegraph agent and stage/mail line to Lucille.','D20','A directory snapshot; neighborhood population 350 is not the census precinct count.'),
('1921-02-11','proposed','Pooled support for a doctor','W. B. Terry of Newkirk proposes $1 per family per month to attract a physician for the locality, believing 100 families would agree.','C11','Proposal and perceived access problem. No 100 actual subscribers or successful recruitment established.'),
('1921-02-11','observed','Santa Rosa competes for trade','Moise Bros. advertises that savings justify a trip even over a long distance; Santa Rosa Mercantile explicitly prints its Santa Rosa address.','C11','Evidence of solicitation across distance, not measured diversion of Cuervo spending.'),
('1921-03-11','reported','Garage reopens','The Cuervo garage reportedly reopens after several months closed, with Harrison Bros. as mechanics.','C12','Direct evidence that at least one closure was temporary.'),
('1921-03-11','reported','Physician called from Duran','Dr. A. A. Sanford of Duran is reported called to see a Cuervo child.','C12,C10','Matches the name advertised at Cuervo in 1918; suggests a changed practice base, not the disappearance of every local doctor.'),
('1921-04-15','observed','Garage and blacksmith service advertised','M. D. Harrison advertises gasoline, oils, accessories, engine work and blacksmithing at the old Ozark Trail Garage building.','C13','A named business and location clue; identity with the earlier Golden Rule or 1910 barn is unproved.'),
('1921','observed','Merchants and hotels persist','The directory still lists Armijo, Bond & Wiest, two hotels and other enterprises. It changes the Rock Island proprietor to J. L. Foster and the school principal to Alma E. Squire.','D21,D20','Proprietor and personnel turnover; omissions alone cannot date closures.'),
('1922-09-27; reported September 29','reported','Delayed train boosts trade','A westbound limited was held at Cuervo all Wednesday by a freight wreck toward Santa Rosa; the paper reports a busy day for local hotels and stores.','C14','Dated connection between a transport interruption and local commerce; no receipts or normal baseline.'),
('1922-12-01','reported','Clipper financial withdrawal','Katharine A. Hicks announces withdrawal from financial involvement, reports losses, and advocates concentration of newspaper support at the county seat.','C15','Political purpose and her associate\'s Santa Rosa paper also matter. This does not establish exact cessation.'),
('1923?','catalog','Possible newspaper cessation','The LOC catalog notes possible cessation in 1923, citing Pearce S. Grove\'s New Mexico newspapers.','LC','The question mark is material. No final issue or definitive closure notice obtained.'),
('1926','context','Route 66 era begins','Route 66 designation enters the chronology after the businesses, institutions and pressures documented above.','DEEP','Designation is not the beginning of road travel or all tourist trade.'),
('1926-01','observed','Passenger access is directional','The timetable offers a morning trip from Cuervo to Tucumcari and an evening return; the Santa Rosa pairing requires an overnight stay.','DEEP','A travel opportunity, not evidence that particular people shopped in either place.'),
('1929 retail / 1930 census','context','Santa Rosa commercial concentration','Santa Rosa reports 44.5% of county retail sales with 16.0% of county population; Cuervo precinct counts 287 residents in 1930.','DEEP,POP','Business and population refer to different reference years; Cuervo receipts are not separately known.'),
('1932','context','Southwest road realignment','The NRHP narrative identifies FAP 114-C and plans dated December 1, 1932.','DEEP','Historical highway documentation; parcel-level Cuervo effects remain open.'),
('1936','context','Paving east of Cuervo','The Montoya-Cuervo nomination dates hard surfacing to 1936, citing 1935 plans.','DEEP','Not a demonstrated date of economic collapse.'),
('1940','observed','Pre-interstate demographic contraction','Cuervo precinct has 188 residents, down from 287 in 1930.','POP','A 34.5% decline in the reported precinct; no exact within-decade turning point.'),
('1939-1949','context','County livestock sales expand','Guadalupe County cattle/calves sold rise from 7,399 in 1939 to 19,724 in 1944, then 17,595 in 1949.','REB','County cattle flows, not Cuervo shipments, profits or jobs.'),
('1947-01-02','observed','Cuervo feed dealer remains listed','An El Rancho Milling advertisement names Bond & Wiest of Cuervo among its dealers. The adjacent article describes the Clovis mill, rail spur and direct truck deliveries to ranches.','N47','Evidence of a dealer relationship; neither sales volume nor bypassing of a particular Cuervo merchant is measured.'),
('1950','observed','Working community and small rebound','Cuervo precinct counts 210 people, 22 more than 1940. Main occupation descriptions include ranching, railway work, retail, teaching, postal and food/service work.','DEEP,REB','Residents\' occupations do not locate every employer inside the settlement.'),
('1951-1956','context','Real cattle-price downturn','Statewide real beef-cattle prices fall 51.7% from the 1951 peak to 1956 in the project series.','PRICE','Potential economic pressure; local business losses have not been attributed to it.'),
('1952','context','Southwest highway relocated','The old alignment is superseded before the interstate project.','DEEP','Separate change in access; affected premises and business losses remain to be linked.'),
('September 1956-October 1958','observed','Train-order-office designation disappears','The designation is present in September 1956 and absent in the October 1958 operating timetable.','RAIL','Does not date the last employee or freight agency closure.'),
('April-October 1958','observed','Advertised passenger stops disappear','Stops are still advertised April 27; the October 26 operating timetable has no regular, flag or conditional stop marker at Cuervo.','RAIL','Bracket for scheduled passenger service; not the end of railway use or all cattle loading.'),
('1958, reported retrospectively','unresolved','School closure lead','A later published account dates school closure to 1958. Administrative records have not confirmed the date or reason.','PUB','Keep this as a lead, not a verified endpoint for the school.'),
('1963-1965','context','Documented interstate construction','NTSB describes project I-040-5(18)1283 near Cuervo, approximately mileposts 282.7-290.7.','DEEP','Exact coverage of Exit 291, property takings and local access changes still require project files.'),
('1967','observed','Siding remains listed','A railway timetable still lists the Cuervo siding.','RAIL','Physical/operating listing is not proof of livestock-loading use.'),
('1968','context','Through Golden State service ends','The through passenger train is discontinued after Cuervo\'s scheduled local stops had disappeared.','RAIL','Two distinct passenger-service events.'),
('1972','context','Santa Rosa interstate bypass','An official state memorial dates Santa Rosa\'s I-40 completion to 1972.','SR72','Its 1960-1970 growth precedes this event; the two towns\' exposure is not identical by assumption.'),
('1974-12-15','observed','Freight administration persists without local agent','Rock Island lists Cuervo with no agent, separate location/accounting codes and billing assigned to Tucumcari.','F74','Administrative identity persists; actual carloads, livestock acceptance and local payroll remain unverified.'),
('2011-09-10','observed','Post office formally discontinued','USPS records Cuervo\'s discontinuance and reassignment as a place name under Newkirk while retaining ZIP 88417.','P11','Administrative effective date, not necessarily the last date a staffed counter operated.'),
('2017-03-09','reported','Funeral Mass announced','Dorothy Chavez\'s funeral notice announces Mass at Santo Nino, Cuervo, and names her restoration involvement.','CH','An announced service and stewardship evidence; not a regular-service schedule.'),
('2018','observed','Catholic mission affiliation','The archdiocesan directory lists Santo Nino, Cuervo, as a mission of St. Rose of Lima, Santa Rosa.','CH','Administrative affiliation, not attendance or frequency of priest visits.'),
('2020 purchase; described in 2026','reported','Named ranch base outside Cuervo','Jim Armendariz says his father purchased the ranch outside Cuervo in 2020 and the operation works from there.','R26','A retrospective first-person account; other leases extend beyond Cuervo.'),
('2025-12','observed','Parish financial activity','A St. Rose bulletin records a Cuervo Function receipt of $170.','CH','Does not identify event location, attendance or regular Mass frequency.'),
('2026','observed','Ranching continues','A conservation-award announcement and ranch-family interview independently identify a current Cuervo-area operation.','R26','Contemporary ranching is established; historical continuity on every parcel and local spending shares are not.')
]
events=[]
for i,(date,kind,subject,observation,refs,limit) in enumerate(rows,1):
    events.append(dict(id=f'E{i:03}',date=date,evidence_type=kind,subject=subject,
                       observation=observation,source_ids=refs.split(','),limit=limit))

businesses=[
('Bond & Wiest','1910; 1920-1922; 1947','General merchandise, agricultural supplies, livestock dealing and later a listed feed dealership. March 1910 names a 4,000-plus sheep purchase from the firm.','C01,C03,D20,D21,C15,N47','Multiple dated observations, not proof of uninterrupted operation, stable ownership or a single premises.'),
('Big Jo Lumber Co.','1910; September 1911','Advertised lumber yard; later reported shipping out stock and cutting prices on the balance.','C01,C08','Final closing date and reason unresolved; later merchants also sold lumber.'),
('Cuervo Drug Store / medical practices','1910; 1912; 1918; 1921','Hawkins & Butler advertise in early 1910; Woodburn & Woodburn by September; J. C. Woodburn is identified as local railway surgeon in 1912. A. A. Sanford advertises at the drugstore in 1918 and is described as of Duran in 1921.','C01,C06,C09,C10,C12','Names and practice locations require person/property linkage; this is not an exact ownership or closure chain.'),
('T. L. Lewis livery / later livery service','1910; 1911','Lewis reportedly exits the livery trade in February 1910. Long Commission proposes a garage conversion. Emmor Taylor still advertises a livery and feed barn in September 1911.','C02,C08','One operator\'s exit did not establish the end of the town\'s livery function.'),
('Garage businesses','1918; 1920; 1921','Morison advertises a Ford Garage in 1918; Golden Rule Garage is listed in 1920. A Cuervo garage reopens in March 1921; M. D. Harrison advertises at the old Ozark Trail Garage building in April.','C10,D20,C12,C13','Do not automatically merge the three named garages or the 1910 conversion proposal.'),
('Rock Island lodging','1910; 1920; 1921-1922','Rock Island Boarding House: Margaret Kelly in 1910. Rock Island Hotel: Mrs. L. C. Bailey in 1920, J. L. Foster in 1921 and the September 1922 advertisement.','C01,D20,D21,C14','Similar names do not establish that every entry refers to the same building.'),
('Oklahoma Hotel','1912; 1918; 1920-1921','Advertises meals and beds in 1912; reported sale from Lizzie Mason to S. P. Morison in 1918; Morrison listed as proprietor in both directories.','C09,C10,D20,D21','Observed sale and later listings; closure date unknown.'),
('Armijo Mercantile','1920-1922','Elfino Armijo is printed as manager in the directories; Cuervo advertisements remain in 1922.','D20,D21,C14,C15','Directory management and dated advertisements; no closure established.'),
('Landers partnerships','1920-1921','Landers & Sanford: general merchandise, drugs and feed in 1920. Landers & Cain: groceries in 1921.','D20,D21','Changed directory name; exact partnership succession and premises unverified.'),
('S. J. T. Pepper & Co.','1920-1921','General merchandise listed in both directories.','D20,D21','No opening or closing date.'),
('Cuervo school','1910-1912; 1920-1921; 1950','Bond vote, construction and new building are documented in sequence; named principals in directories; teacher occupations in 1950 precinct.','C05,C06,C07,C08,C09,D20,D21,DEEP','The reported 1958 closure and regular enrollment series still need administrative verification.'),
('Postal and feeder service','1913; 1920-1921; 1950; 2011','Hanson feeder route ends in 1913; Cuervo retains a postmaster in the directories and 1950 census; administrative office discontinuance is 2011.','P13,D20,D21,DEEP,P11','Feeder-route withdrawal and office closure are different events.'),
('Railway agency / operating functions','1911; 1920-1921; 1950; 1958; 1974','Depot improvements and named agent precede 1950 jobs; passenger stops and office designation disappear by October 1958; 1974 billing is assigned to Tucumcari.','C08,D20,D21,DEEP,RAIL,F74','Final local payroll and last actual livestock shipment remain open.'),
('Outside competitors: Moise Bros. and Santa Rosa Mercantile','1921','Advertisements explicitly identify Santa Rosa and solicit readers\' trade; Moise says savings repay a long trip.','C11,C13','These are external commercial offers, not entries in a Cuervo establishment count.')
]
(HERE/'sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False),encoding='utf-8')
(HERE/'chronology.json').write_text(json.dumps(events,indent=2,ensure_ascii=False),encoding='utf-8')
(HERE/'business_register.json').write_text(json.dumps([dict(entity=a,observations=b,description=c,source_ids=d.split(','),limit=e) for a,b,c,d,e in businesses],indent=2),encoding='utf-8')
intro='''# Cuervo: formation, changing functions and decline

*A chronology from the town's beginnings through 2026. Research completed September 21, 2026. This is a source-based working reconstruction, with unresolved dates retained explicitly.*

## What this study changes

**Cuervo had already become a place to trade livestock, obtain supplies, receive medical care, attend school and connect with outside markets before Route 66. Its later decline needs to be explained function by function.** The new early sources show investment, commercial withdrawal, attempted recruitment and reopening within the same broad period. A simple sequence in which every service steadily disappeared does not fit them.

The most useful new evidence is:

- **Livestock and merchandise moved through Cuervo in 1910.** One report describes cattle unloaded to feed and rest en route to Kansas City; another reports fourteen carloads of sheep loaded for Kansas. Bond & Wiest bought and sold agricultural goods, including sheep. Sheep, wool and mixed farming belong alongside cattle in the economic history. [C01, C03, D21]
- **The school attracted families into Cuervo.** A September 1910 report gives 67 pupils and says households were moving in from the surrounding country to obtain schooling. A 1912 report again describes seasonal moves for school. Cuervo itself served as a small regional center. [C06, C09]
- **A commercial contraction appears as early as 1911, alongside investment.** Big Jo Lumber was reportedly shipping out stock while the new school was being erected and the depot platform improved. The stock notice does not establish the yard's last day or explain its decision. [C08]
- **Residents discussed the difficulty of supporting a doctor in 1921.** A Newkirk resident proposed pooling monthly payments from families to attract a physician for the locality. This is unusually direct evidence about maintaining a service with a dispersed customer base. [C11]
- **Some services recovered.** A garage reopened in March 1921 after several months closed. A named garage/blacksmith advertisement followed in April. [C12, C13]
- **Ranch-supply trade remained visible in 1947.** An El Rancho Milling advertisement lists Bond & Wiest of Cuervo as a dealer. This supplies a named commercial observation between the Clipper's last surviving year and the 1950 census. [N47]

We also now hold searchable repository OCR for **270 distinct Clipper issue dates and 1,167 nonempty page transcripts**, plus **19 newly downloaded source-page PDFs** filling the three missing catalog issues and seven additional pages of November 4, 1921. The dates span 1910-1922 with substantial gaps; this is not an unbroken weekly run or an exhaustive human reading.

## 1. Formation and early economic functions

### What can be said about the beginning

The familiar founding date around 1901 remains a starting hypothesis to anchor more precisely. The railway report establishes the formation of the regional connection at Santa Rosa; it does not furnish Cuervo's station-opening date. The original town plat, town-company record and early property assessments remain important. The catalog's broad 1884-1944 range for the A. A. Jones papers must not be assigned to the town-company book itself. [DEEP, A]

The early mercantile record is more tangible. UNM catalogs a Bond & Wiest ledger for 1904-1908. A 1996 historical discussion places Bond expansion to Cuervo in the early years of the century, but relies on an earlier study rather than reproducing a local opening record. These are strong routes into the formation period, not a license to invent an exact founding or store-opening date. [A, AR]

### A town participating in agricultural trade

The January 28, 1910 Clipper reports five carloads of passing cattle unloaded for feed and rest on their way to Kansas City. That establishes a livestock-handling function without establishing the cattle's origin. On March 4 the paper reports fourteen cars of sheep loaded out of Cuervo for Kansas. It separately reports a Kansas buyer purchasing more than 4,000 sheep from Bond & Wiest and an inbound car of potatoes, grain and dried fruit for the firm. The paper says the merchant unloaded one or two produce cars for customers each week. These are contemporary reports, not checked freight returns or accounts. [C01, C03]

The two March sheep statements cannot simply be combined into a single shipment of 4,000 animals. Nevertheless, the page provides direct evidence of a commercial intermediary dealing in livestock and goods before the highway designation. The 1921 directory explicitly lists hides, wool and pelts among Bond & Wiest's business. A cattle-price graph alone cannot explain the fortunes of this broader enterprise. [C03, D21]

### Adaptation was already happening

In February 1910, T. L. Lewis reportedly left the livery business for cattle dealing. Long Commission Company proposed taking over the barn and converting it to a garage. This is a change of operator and intended use. An Emmor Taylor livery/feed advertisement in September 1911 shows why it should not be called the end of livery service in Cuervo. [C02, C08]

The same early record includes a completed telephone connection to Montoya, physicians advertising in Cuervo, a visiting dentist, lodging, a lumber yard, grocers and a barber. It identifies services already present, not the amounts spent at them or their financial viability. [C01, C02]

## 2. The school brought people into town

The newspaper provides a sequence that is much stronger than a single building date:

- **June 30, 1910:** a reported vote for $4,000 in school bonds; one vote opposed. The July 8 article describes a planned stone building and says the site was not yet decided. [C05]
- **September 30, 1910:** reported enrollment of 67, with 100 anticipated; the newspaper says families are moving into town for school. Only 67 is an observation. It describes an existing stone school as too small and anticipates an enlarged service area extending into part of San Miguel County. [C06]
- **April 21, 1911:** bonds reportedly sold; bids sought for a four-room stone school. [C07]
- **September 14, 1911:** J. B. Colvin identified as the contractor erecting the new school. [C08]
- **April 4, 1912:** a new two-story school and two employed teachers reported, with a third expected the following year. Seasonal moves into Cuervo for schooling are reported again. [C09]

This supplies a concrete mechanism by which an institution could help sustain town residence. It also complicates the idea that Cuervo was only a victim of a larger center: it drew households from a surrounding rural area. The statements are qualitative newspaper reports and contain boosterism. They do not give a migration count, demonstrate permanent moves, or prove that every planned expansion occurred.

The school evidence prevents a careless reading of the early censuses. The precinct total falls from 545 in 1910 to 438 in 1920, but boundaries changed and both totals include countryside. We cannot assume the built settlement shrank continuously during a period when its school was attracting families. A town-versus-hinterland reconstruction is now more consequential. [POP]

## 3. Early strains were real, but differed by service

### Lumber stock withdrawal in 1911

The September 14 paper says Big Jo Lumber was shipping out stock and would reduce prices on the balance. That is a contemporary sign of commercial withdrawal, in the same issue that describes school construction and depot improvements. It may lead to an early business closure, but the last trading date, destination of the stock and reason remain unknown. Later Bond & Wiest advertisements include lumber, so the loss of a dedicated yard would not automatically mean that lumber became unobtainable locally. [C08, C11]

### The 1921 physician proposal

In the February 11 item headed **Doctor Wanted**, W. B. Terry of Newkirk proposed a monthly assessment of $1 per family for a physician who would establish headquarters in the locality. He believed 100 families would join whether or not they needed treatment that month. The implied proposed support was $100 a month, not a documented subscription total, salary or profit. The editor invited responses and offered to help secure a physician if enough people wanted one. [C11]

This is evidence of a perceived access problem and an attempt to spread the cost of sustaining a service. It is compatible with a minimum-customer-base explanation. It does not establish a universal town-size threshold, show that the plan succeeded, or prove that every resident lacked medical access. Terry came from Newkirk; the appeal must not be silently confined to Cuervo households.

There is also a named practitioner to trace. Dr. A. A. Sanford advertised at the Cuervo drugstore in February 1918. The March 11, 1921 paper describes Dr. A. A. Sanford **of Duran** being called to see a Cuervo child. The matching name suggests a change of practice base while some care remained available through travel. His exact move, reasons and relationship to the recruitment proposal are not established. [C10, C12]

### Garage reopening and competition for shoppers

On March 11, 1921, the paper reports that the Cuervo garage had reopened after several months closed, with Harrison Bros. as mechanics. On April 15, M. D. Harrison advertises the Cuervo Garage & Blacksmith Shop at the old Ozark Trail Garage building, offering gasoline, oils, repairs and blacksmithing. We have an actual temporary interruption followed by renewed service. The earlier Golden Rule Garage entry and the 1910 barn-conversion proposal cannot yet be linked to this building. [C12, C13, D20]

The April advertisement sits beside Moise Bros.' explicitly Santa Rosa advertisement claiming savings would repay a trip over a long distance. The February page carries the same appeal and a Santa Rosa Mercantile address. This proves that outside merchants solicited the readership and made travel cost part of their pitch. It does not reveal how many Cuervo customers went, how often, or how much local turnover they displaced. [C11, C13]

### The newspaper and hotels in 1922

The September 29 paper reports that a westbound limited was detained all Wednesday by a freight wreck between Cuervo and Santa Rosa, producing a busy day for local hotels and stores. The same page advertises the Rock Island Hotel under J. L. Foster and two Cuervo merchants. Passenger trade and local commerce were still connected just before Hicks's withdrawal announcement. There are no receipts or comparison days. [C14]

On December 1, Hicks explicitly reports financial loss and favors concentrating newspaper support at the county seat. Political objectives and her associate Charles Gerhardt's Santa Rosa Public Voice also shape the decision. We should preserve that mixed explanation. [C15]

**The exact Clipper closure remains unsettled.** The Library of Congress catalog gives possible cessation in 1923, with a question mark, citing Pearce S. Grove. Its January 1909 start also sits uneasily with the paper's 1921 claim to be entering its fourteenth year. The digitized run ending in December 1922 is a holdings endpoint. Neither that endpoint nor financial withdrawal establishes the last publication date. [LC, C13, C15]

## 4. Connecting the early town to its later condition

The important bridge is now a named business. **The January 2, 1947 State Line Tribune lists Bond & Wiest of Cuervo as an El Rancho feed dealer.** The same page describes a Clovis feed mill with a rail spur, its own trucks, ranch delivery and employment of roughly 50-60 people at full production. That employment statement concerns the mill, not Cuervo. [N47]

This supplies a concrete regional network to investigate: manufacturing in one center, dealers in several towns, and the possibility of direct delivery to ranches. It does not show that direct deliveries displaced Bond & Wiest. The dealer's presence is evidence that some ranch-supply intermediation remained locally in 1947. Clovis belongs in this part of the research alongside Santa Rosa and Tucumcari.

The 1950 census then finds ranching, railway, retail, educational, postal and food/service occupations among precinct residents. Later events remain separable: a 1952 road relocation; disappearance of scheduled passenger stops within 1958; the documented 1963-1965 interstate project; a 1974 freight-accounting listing with billing through Tucumcari; and formal postal discontinuance in 2011. Church stewardship and contemporary ranching continue much later. Each event needs its own effect assessed. [DEEP, RAIL, F74, P11, CH, R26]

**The revised question is why an established collection of businesses and institutions lost enough local activity to become difficult to sustain, while some agricultural activity survived.** The early evidence makes this question more specific. It has not yet apportioned the effects of population change, land use, merchant competition, trucking, railway staffing, schools or highways.

## 5. Full chronology

**Evidence types:** *observed* = a directly recorded listing/count; *reported* = an account of an event; *proposed* = an intention, not an outcome; *catalog* = bibliographic/archival description; *context* = a regional condition or previously reviewed historical account; *unresolved* = a lead still awaiting confirmation. A report date may be later than the event.

'''
timeline='| Date | Dated observation | Evidence and limit |\n|---|---|---|\n'
for e in events:
    timeline+=f"| {e['date']} | **{e['subject']}.** {e['observation']} [{', '.join(e['source_ids'])}] | *{e['evidence_type']}.* {e['limit']} |\n"
register='\n## 6. Business and institution register\n\nDates below are selected positive observations, not opening-to-closing lifespans. Entries identify names/functions; property identity and ownership succession need separate verification.\n\n| Entity | Dated observations and functions | Remaining limit |\n|---|---|---|\n'
for a,b,c,d,e in businesses:register+=f'| **{a}** ({b}) | {c} [{d.replace(",", ", ")}] | {e} |\n'
ending='''
## 7. What remains to test, in priority order

1. **School catchment and closure.** Link the 1910-1912 construction sequence to the surviving building, reconstruct annual enrollment and transport arrangements, and obtain the actual consolidation/closure decision. If it drew families into town, its withdrawal may have changed residence as well as schooling. The currently repeated 1958 date remains a secondary lead.
2. **Merchant revenue and customer geography.** Read the Bond & Wiest accounts across the early years, 1920s, Depression and war: not just totals, but customers, addresses, merchandise categories, credit and livestock transactions. The catalog identifies 1904-1908 and 1908-1911 ledgers, 1914-1916 inventories, 1919-1925 and 1925-1931 journals, 1930-1933 cash books and 1941-1943 cash books. Their contents remain unacquired. [A]
3. **Medical and newspaper transitions.** Trace Sanford's move, the outcome of Terry's proposal, Hicks/Gerhardt's publishing arrangements and the last Clipper issue. The mechanisms have named participants and dated leads now.
4. **Business closures after 1922.** Establish last positive observations and explicit closure/sale notices for the hotels, merchants, garages and lumber yard. The new 1947 dealership observation is a useful midpoint, not a terminal date. Search regional newspapers, telephone directories, tax rolls and property transfers.
5. **Which transport-dependent work disappeared?** Link the early livestock-handling and later freight-accounting evidence to actual station returns, stockyard use, car orders, trucking practices and payroll. Keep passenger loss separate from freight use. The last post-1958 Cuervo livestock shipment is still unlocated.
6. **Town versus countryside.** Reconstruct comparable boundaries and household locations before reading all precinct losses as town losses. Distinguish farm families leaving the district from rural households moving into Cuervo for school. Add sheep/wool and crop conditions to the economic tests.

The 1940s rebound remains a useful subsidiary question. Cattle-market expansion is plausible context, but it does not explain every local household change, nor can it explain the town's full century. Interstate harm also remains open: earlier difficulties do not rule out a severe later loss of passing trade.

## 8. Coverage, search method and limitations

This study retrieved UNM's existing CONTENTdm page metadata and OCR; it did not run a new OCR model or exhaustively correct newspaper text. The API returned 272 issue records covering 270 dates and 1,189 child-page records. Two pairs of issue records have identical OCR (eight duplicate pages); fourteen child records attached to August 26, 1921 have empty transcripts. Removing these leaves **1,167 nonempty page transcripts**, reconciled against the prior local scan audit.

The nonempty-page differences are exactly the three missing four-page issues (February 11, 1910; February 22, 1912; September 28, 1917) and seven additional pages of November 4, 1921. Those **19 source-page PDFs were downloaded separately**, parsed and visually checked for page integrity. The original 267 combined PDFs were preserved. We now hold scans corresponding to all 270 catalog dates, with those dates still separated by historical gaps. There are no held issue dates for 1914-1916, and only four for 1920.

Search patterns generated **9,288 unverified OCR leads** in seven subject categories. Many are syndicated stories, legal notices, advertisements repeated across issues or references to other places. They are not 9,288 historical events. The curated chronology and register use selected visual checks plus explicitly referenced prior studies. Their limits are attached to the entries.

New primary pages closely read in this pass include fourteen additional Clipper front pages, the complete 1920 and 1921 Cuervo directory entries, the 1947 dealer advertisement and adjacent mill article, and the 2011 USPS row. The December 1922 editorial and later rail/census/church findings draw on prior verified studies. The 1996 historical report and LOC catalog are labeled separately. Keyword searches found no conclusive outcome to the physician subscription proposal or exact final Clipper issue; that search result is not proof those records do not exist.

**Source-reading rules:** an advertisement establishes an offer at a date; its absence does not prove closure. A sale changes ownership. A plan is not completion. A seasonal school closing is not permanent shutdown. A catalog entry establishes a lead, not the contents of an unread book. A census resident's occupation does not identify a workplace parcel. Neither a siding nor an accounting code proves an actual livestock shipment.

### Reusable research files

- `chronology.json`: curated dated observations, evidence types, source IDs and limits.
- `business_register.json`: named businesses and institutions with dated observations.
- `sources.json`: source paths, page locators, catalog URLs and review status.
- `canonical_ocr_pages.json` and `issue_coverage.json`: source-page and issue mapping.
- `ocr_search_leads.jsonl`: unverified search leads, kept apart from curated evidence.
- `ocr_coverage_audit.json`: duplicate, empty-transcript and holdings reconciliation.
- Original page metadata, per-page OCR, per-issue text and retrieval checksums are in `sources/02_newspapers/cuervo_clipper/repository_ocr_2026-09-21/`.
- Supplemental source scans and their checksums are in `sources/02_newspapers/cuervo_clipper/supplemental_scans_2026-09-21/`.

## 9. Source key

PDF page numbers are one-based. Clipper front pages are PDF page 2 in the original combined downloads because page 1 is a repository cover. The detailed source JSON retains full local paths and the review status of every source.

'''
source_notes=''
for key,s in sources.items():
    local='../'+s['file'].replace('\\','/')
    source_notes+=f"- **[{key}]** [{s['title']}]({local.replace(' ','%20')}). {s['locator']}. {s['review']}"
    if s['url']:source_notes+=f" [Repository/source]({s['url']})."
    source_notes+='\n'
report=intro+timeline+register+ending+source_notes
# Derived counts must match the retained index, not an approximate narrative count.
coverage=json.loads((HERE/'ocr_coverage_audit.json').read_text(encoding='utf-8'))
lead_count=sum(coverage['search_leads_by_category'].values())
report=report.replace('9,288',f'{lead_count:,}')
(ROOT/'research_evidence/full_life_chronology_2026-09-21.md').write_text(report,encoding='utf-8')
assert all(s in sources for e in events for s in e['source_ids'])
assert all((ROOT/s['file']).is_file() for s in sources.values())
print(json.dumps({'events':len(events),'business_register_entries':len(businesses),'sources':len(sources),'ocr_leads':lead_count,'report_words':len(report.split())},indent=2))
