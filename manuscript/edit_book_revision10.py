"""Apply the reader-led clarity and distance sweep without altering earlier proofs."""
from pathlib import Path
import json, hashlib, shutil

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'manuscript/book-revision-09'
REV=ROOT/'manuscript/book-revision-10'
(REV/'chapters').mkdir(parents=True,exist_ok=True)
changes=[]
texts={int(p.name[8:10]):p.read_text(encoding='utf-8') for p in (OLD/'chapters').glob('*.md')}

def edit(n,old,new,reason='Explicit reference and accessible prose'):
    assert texts[n].count(old)==1,(n,old,texts[n].count(old))
    texts[n]=texts[n].replace(old,new)
    changes.append({'chapter':n,'reason':reason,'before':old,'after':new})

edit(1,'Today, Cuervo is commonly described as a Route 66 ghost town.','Cuervo, in eastern New Mexico, is commonly described as a Route 66 ghost town.','Locate the subject before developing the argument')
start=texts[1].index('## A store with a wide reach')
end=texts[1].index('## Which Cuervo is being counted?')
edit(1,texts[1][start:end],'''## Serving the surrounding country

Bond & Wiest, a general-merchandise business, sold supplies, extended credit and traded in sheep and wool.[^5] Its railway shipments connected the surrounding ranch country with distant markets.[^6] Much of the work supporting this trade took place outside the village. The people living beside the store were only part of its market.

Other services drew on different support. Schooling attracted families from the surrounding country in 1910 and 1912.[^7] The *Cuervo Clipper* relied on financial backing from an owner who valued its political influence as well as its receipts. Katharine A. Hicks withdrew that backing in December 1922.[^8] A service could lose its sponsor while some of its users remained.

These businesses and institutions gave people reasons to come to Cuervo. Keeping them there required customers, staff and continuing support. Their requirements explain why one could grow or survive while another withdrew.

''','Make Chapter 1 general; reserve merchant origins, relocation and shipment detail for Chapters 2–3')
edit(1,'Cuervo’s merchant did both. Its market extended beyond the village, so the local population was a poor measure of the trade available.','A small resident population can therefore support a business whose customers live farther afield.','Avoid an unidentified or apparently exclusive merchant; keep the introductory economic principle')
edit(1,'An assessor card prepared in January 1983 classified a Cuervo property as a gas station, rated its condition poor and used a salvage basis for valuation. A later entry recorded no change in December 2008. The assessment records the property’s condition, leaving its trading history open.','A 1983 assessor card classified a Cuervo property as a gas station while recording poor condition and a salvage basis for valuation. That description identifies a former use without establishing when fuel sales ended.','Keep the introductory example brief; detailed record history remains in Chapter 8')
edit(1,'This book follows the work that gathered at Cuervo, the support that sustained it, and the changes that reduced its role while ranching continued. It begins with the question of why that work gathered here.','The chapters move from the formation of its businesses to the services and households they supported, then follow changes in transport and access to competing centers. Together, those histories explain how the town’s role diminished while the surrounding country remained in use. The first question is why work gathered here.','Give readers a clear progression into the rest of the book')

edit(2,'Its merchant supplied, financed and marketed production; the railway made a different location attractive for that business.','The Bond business supplied goods, extended credit and helped market livestock and wool. The railway made a different location attractive for that work.')
edit(2,'Like Cuervo’s merchant, it linked the railway to a wider territory,','Like Bond & Wiest, it linked the railway to a wider territory,')
edit(2,'The map also records limitations. Santa Rosa lacked a public water supply, public lights and a fire department or apparatus at the time of the survey. Streets were unpaved.','The December 1908 Sanborn survey also recorded limited municipal services: no public water-supply system, public lighting, fire department or fire apparatus. The water entry concerned public provision, not the presence of natural water sources. Streets were unpaved.','Distinguish a dated public-service observation from natural water availability')
edit(2,'Cuervo’s merchant did not need to reproduce all those functions to operate successfully.','Bond & Wiest did not need to reproduce all those functions to operate successfully.')
edit(2,'In March 1910, Wiest and Holbrook were reported in Santa Rosa receiving cattle for the firm.','In March 1910, the *Clipper* reported Wiest and an associate, Holbrook, receiving cattle for Bond & Wiest in Santa Rosa.','Identify the business without assigning an undocumented job title or identity to the newspaper’s surname')
edit(2,'By 1920, the business directory listed Armijo Mercantile as well as Bond & Wiest, the Golden Rule Garage, and the Oklahoma and Rock Island hotels.','The 1920 business directory listed two named mercantile firms, Armijo Mercantile and Bond & Wiest, alongside the Golden Rule Garage and the Oklahoma and Rock Island hotels.','Make multiple merchants explicit without claiming the directory is exhaustive')

edit(1,'The relevant requirements belong to activities. A missing teacher or withdrawn subsidy can matter more immediately than a change in the population total. Replacements, new funding and different ways of operating can restore provision, as Cuervo’s reopenings show.\n\n','','Remove a repeated introductory conclusion and its stray spillover page; earlier service examples retain the point')
edit(2,'The wider early record includes physicians’ advertisements, a visiting dentist, lodging, groceries, a lumber yard and a barber. A telephone connection to Montoya was reported complete in January 1910. These were different ways of making the locality more useful, and they depended on different customers and arrangements.','Other early reports and advertisements record physicians, a visiting dentist, lodging, groceries, a lumber yard and a barber. A telephone connection to Montoya was reported complete in January 1910.','Tighten a repeated explanation while preserving the evidence')
edit(2,'The 1920 business directory listed two named mercantile firms, Armijo Mercantile and Bond & Wiest, alongside the Golden Rule Garage and the Oklahoma and Rock Island hotels. It also named a school principal, a postmaster, a railway agent and a stage and mail line to Lucille. Cuervo combined trade, lodging, repairs, public services and communications.','The 1920 directory listed two mercantile firms, Armijo Mercantile and Bond & Wiest, alongside the Golden Rule Garage and the Oklahoma and Rock Island hotels. It also named a principal, postmaster, railway agent and a stage and mail line to Lucille.','Keep named services while removing a redundant summary and spillover')

edit(3,'There is, however, a useful later observation of the merchant’s role.','A 1947 advertisement provides a later observation of Bond & Wiest’s role.')
edit(3,'Cuervo’s business remained connected with the supply side of livestock production.','Bond & Wiest remained connected with the supply side of livestock production.')
edit(3,'Cuervo’s merchant supplied handling, finance and trade.','Bond & Wiest supplied handling, finance and trade.')
edit(3,'Grubbs found J. S. Holbrook operating the Cuervo business in 1958.','Grubbs found J. S. Holbrook, son of the earlier manager Joe Holbrook Jr., operating the Cuervo business in 1958.','Distinguish two generations on first mention; Grubbs p. 115 visually rechecked')
edit(3,'He described Holbrook’s irritation at the position enjoyed by a Boston buyer and his reluctance to accept it without alternatives.','He described Joe Holbrook Jr.’s irritation with a Boston wool buyer in 1913 and his reluctance to accept the buyer’s terms without alternatives.','Identify the earlier Holbrook and date the correspondence; Grubbs pp. 102, 109 and 115 visually rechecked')
edit(3,'Grubbs, pp. 108–109, drawing on correspondence about eastern wool buyers and Holbrook’s bargaining.','Grubbs, pp. 108–109, drawing on correspondence about eastern wool buyers, including the July 10, 1913 letter cited in p. 109, note 43; pp. 102 and 115 identify the Holbrook generations.','Add exact locator for the clarified identity and correspondence date')

edit(4,'A neighbor proposed regular payments to attract a doctor.','A proposal from nearby Newkirk called for regular payments to attract a doctor.')
edit(4,'Its reason was the discontinuance of Hanson because there was no suitable candidate for postmaster.','The department was closing Hanson’s post office because no suitable candidate for postmaster was available.','Specify closure of the post office rather than of the settlement')
edit(4,'seven and a half miles','about 12 kilometers (7.5 miles)','Kilometers first; source precision retained in parentheses')
edit(4,'7.50 miles','12.07 kilometers (7.50 miles)','Convert the cited route length using 1 mile = 1.609344 kilometers')
edit(4,'## Building a school constituency','## How the school attracted families','Replace an abstract heading with its concrete subject')
edit(4,'the preceding school closing','the end of the preceding school term','Distinguish the term’s end from permanent school closure')
edit(4,'Dr. A. A. Sanford advertised at the Cuervo drugstore in February 1918.','Dr. A. A. Sanford advertised at a drugstore in Cuervo in February 1918.')
edit(4,'The December 1, 1922 paper advertised another way of distributing care.','The December 1, 1922 *Clipper* advertised another way of distributing care.')
edit(4,'The newspaper that published these appeals depended on an arrangement of its own.','The *Cuervo Clipper*, which published these appeals, depended on an arrangement of its own.')
edit(4,'the *Clipper* reported that the Cuervo garage had opened again','the *Clipper* reported that a garage in Cuervo had opened again','Avoid implying that several distinct garage notices describe one exclusive business')
edit(4,'The merchant’s wide market and the garage’s combined tasks helped make local business possible.','Bond & Wiest’s wide market and Harrison’s combined repair, blacksmithing and fuel business helped make local trade possible.','Name the businesses and their work in the chapter conclusion')

edit(5,'The schedules show a larger change in how they lived:','The individual census returns show a larger change in how they lived:','Introduce the source in familiar language')
edit(5,'The original household schedules add a useful check.','The original census forms, called schedules, add a useful check.','Define the term before using it throughout the chapter')
edit(5,'Seven retained answers name an outside place or state.','Seven answers in the inspected forms name an outside place or state.','Replace internal research terminology')
edit(5,'643 main occupation appearances','643 main occupation entries','Use a concrete description of the counted unit')
edit(5,'The later Higgins accounts extend the distinction beyond one census.','The Higgins family’s later obituaries extend the distinction beyond one census.','Identify the source genre')
edit(5,'John Sr.’s later account describes ranching northeast of Cuervo','John Sr.’s obituary describes ranching northeast of Cuervo','Do not imply a first-person account')
edit(5,'Willa’s account adds a business in another place.','Willa’s obituary adds a business in another place.','Identify the source genre')
edit(5,'John Sr.’s account also says that he was reared in Cuervo and schooled in Santa Rosa. The connection therefore preceded the son’s 1969 graduation. Education outside the smaller settlement appears across two generations.','John Sr.’s obituary also says that he was reared in Cuervo and schooled in Santa Rosa. Schooling outside the smaller settlement continued into the next generation.','Remove a forward reference to an as-yet-unintroduced son and graduation')
edit(5,'John Higgins Jr.’s family account dates his Santa Rosa High School graduation','His son John Higgins Jr.’s obituary dates his Santa Rosa High School graduation','Identify both the relationship and the source')
edit(5,'Other family accounts widen the map.','Other obituaries widen the map.')
edit(5,'Tito Vigil’s account likewise names','Tito Vigil’s obituary likewise names')
edit(5,'Rudolpho, or Rudy, Chavez’s family account likewise names','Rudolpho, or Rudy, Chavez’s obituary likewise names')
edit(5,'6.28 square kilometers','6.28 square kilometers (2.42 square miles)','Pair the study-window area units')
edit(5,'A fixed study window around the settlement produces overlapping population-allocation ranges: zero to seventeen in 2010 and five to twenty-seven in 2020.','Allocating census blocks to a fixed study area around the settlement gives overlapping ranges: zero to seventeen people in 2010 and five to twenty-seven in 2020.','Explain the procedure in familiar language; the following sentences retain its limits')

edit(6,'The local newspaper reported a busy day for hotels and stores.','The *Cuervo Clipper* reported a busy day for hotels and stores.')
edit(6,'Rock Island’s public timetable placed Santa Rosa 17 railway miles from Cuervo and Tucumcari 42 miles away.','The Rock Island railway’s public timetable placed Santa Rosa about 27 kilometers (17 miles) from Cuervo by rail and Tucumcari about 68 kilometers (42 miles) away.','Name the railway and standardize route distances')
edit(6,'a 6.9-mile section','an 11.1-kilometer (6.9-mile) section','Paired distance units')
edit(6,'the original E-Federal Aid Project 114-C title sheet now confirms that approval date.','the original E-Federal Aid Project 114-C title sheet bears that approval date.','Remove working-draft language')
edit(6,'climbed roughly two hundred feet','climbed roughly 60 meters (200 feet)','Paired elevation units with approximate source precision')
edit(6,'an employee timetable showed the Imperial stopping','a timetable for railway staff showed the Imperial passenger train stopping','Define the source and train on first mention')
edit(6,'The Golden State continued along the corridor','The Golden State passenger train continued along the corridor')
edit(6,'The NTSB’s investigation of a 2002 accident','The National Transportation Safety Board’s (NTSB) investigation of a 2002 accident','Expand the acronym on first use in this chapter')
edit(6,'The 17 and 42 miles are railway distances.','The approximate 27-kilometer (17-mile) and 68-kilometer (42-mile) lengths are railway distances.','Pair both distances in the shared-unit source-note expression')

edit(7,'The merchant connected scattered producers to supplies, finance and outside buyers.','Bond & Wiest connected scattered producers to supplies, finance and outside buyers.')
edit(7,'Hicks explained her financial withdrawal through losses, a fulfilled political purpose and an alternative county paper.','Katharine A. Hicks explained her withdrawal of backing from the *Clipper* through losses, a fulfilled political purpose and an alternative county paper.')
edit(7,'Terry’s medical fund instead records a proposed remedy:','W. B. Terry’s proposed medical fund offered a different remedy:')
edit(7,'The early merchant already relied on distant buyers and suppliers.','Bond & Wiest already relied on distant buyers and suppliers.')
edit(7,'from 6.1 to about 18.73 square miles','from 15.8 square kilometers (6.1 square miles) to about 48.5 square kilometers (18.73 square miles)','Pair the municipal land-area comparison')

edit(8,'The supplied town map combines a printed base with subsequent coloring.','The undated Cuervo parcel map combines a printed base with subsequent coloring.','Identify the source without relying on conversation context')
edit(8,'In December 2011, the school board chose Flora Page’s $10,250 offer from four bids.','In December 2011, the Santa Rosa Consolidated Schools board chose Flora Page’s $10,250 offer from four bids.','Name the public body')

edit(1,'That description identifies a former use without establishing when fuel sales ended.','The card describes the property, but does not establish whether fuel was still being sold.','Preserve the distinction between an assessed classification and verified trading activity')

# Remaining distance expressions are in source notes, with exact source values retained.
for old,new in [('7.678 project miles','a project length of 12.36 kilometers (7.678 miles)'),('6.9-mile','11.1-kilometer (6.9-mile)'),('6.8 miles','10.9 kilometers (6.8 miles)')]:
    body,notes=texts[6].split('\n---\n',1)
    if old in notes:
        changes.append({'chapter':6,'reason':'Paired distance units in source notes','before':old,'after':new,'occurrences':notes.count(old)})
        notes=notes.replace(old,new)
        texts[6]=body+'\n---\n'+notes

for p in (OLD/'chapters').glob('*.md'):
    (REV/'chapters'/p.name).write_text(texts[int(p.name[8:10])],encoding='utf-8')
for name in ['bibliography.md','revision06-integrity.json','revision07-integrity.json','revision08-integrity.json']:
    shutil.copy2(OLD/name,REV/name)
protected=list(OLD.rglob('*'))+[ROOT/'output/pdf/cuervo-complete-reading-proof-revision-09.pdf']
protected += [ROOT/'manuscript'/p for p in ['build_book_revision09.py','check_book_revision09.py','edit_book_revision09.py','revision09_captions.py']]
(REV/'revision09-integrity.json').write_text(json.dumps({p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()},indent=2),encoding='utf-8')
(REV/'editorial-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(changes)} recorded editorial changes; eight chapters prepared.')
