"""Evidence ledger of named transactions, movement and institutional links.
Selection is purposeful, not an exhaustive census of commercial activity.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent
index=json.loads((ROOT/'research_evidence/full_life_chronology_2026-09-21/canonical_ocr_pages.json').read_text(encoding='utf-8-sig'))
pages={x['page_id']:x for x in index}
rows=[]
def add(date,source,target,kind,description,page=None,printed=None,pdf=None,limit=None):
 r={'id':'N%02d'%(len(rows)+1),'date':date,'source_actor':source,'target_actor_or_place':target,'relation_type':kind,'observation':description,'limit':limit}
 if page:
  x=pages[str(page)];r.update(source_class='Contemporary newspaper report, original page visually inspected',issue_date=x['issue_date'],page_id=x['page_id'],source_url=x['source_url'],local_file=x['local_issue_file'],pdf_page=x['local_pdf_page_candidate'])
 else:r.update(source_class='Grubbs 1958: secondary analysis or quoted original correspondence; manuscript not inspected',local_file='sources/origins_followup_2026-09-23/grubbs_bond_thesis_1958.pdf',printed_page=printed,pdf_page=pdf)
 rows.append(r)
add('1910-03-04','Cuervo loading point','Kansas','reported shipment','Fourteen cars of sheep loaded at Cuervo; destination Kansas.',2482,limit='Shipper not named. Do not merge automatically with the nearby Mertz sale or sum as independent sheep totals.')
add('1910-03-04','Bond & Wiest','Sherman Mertz, reported of Waubansee, Kansas','reported sale','Over 4,000 sheep purchased from Bond & Wiest.',2482,limit='Destination affiliation is reported; precise ranch origin and identity with a similarly named Albuquerque visitor are not resolved.')
add('1910-03-04','Wiest and Holbrook for Bond & Wiest','Santa Rosa','reported business activity','Managers were in Santa Rosa receiving a bunch of cattle for the firm.',2482,limit='Does not establish seller, animal origin, subsequent destination or route.')
add('1910-03-04','Unidentified suppliers','Bond & Wiest, Cuervo','reported inbound freight','A carload of potatoes, grain and dried fruit unloaded; newspaper describes unloading one to two cars of produce weekly.',2482,limit='Weekly rate is the newspaper claim, not a counted shipment series; suppliers unknown.')
add('1910-03-04','A. W. Wiest','Mr. Goldenburg, Tucumcari','reported motorcar sale','Wiest sold a new Ford to a Tucumcari buyer during a visit there.',2482,limit='Do not assign this transaction to Bond & Wiest merchandise accounts or infer its price.')
add('1910-03-11','Bond & Wiest, Cuervo','Unspecified destination','reported shipment','One car of hides and pelts shipped.',2477,limit='Destination unknown; not proof of Boston routing.')
add('1910-03-11','Unidentified suppliers','Bond & Wiest, Cuervo','reported inbound freight','A car each of flour, sugar and grain unloaded.',2477,limit='Supplier locations and quantities within each car unknown.')
add('1910-07-15','Surrounding producers','Bond & Wiest, Cuervo','reported wool marketing','Paper describes wool coming from surrounding country and promotes the firm\'s prices.',2601,limit='No catchment boundary, complete volume or independent price comparison.')
add('1910-07-15','Dr. J. C. Woodburn','Cuervo drug business','reported entry/acquisition','Physician selected Cuervo after looking at other New Mexico locations and took over the drug business.',2601,limit='An existing business changed hands; not evidence the first drugstore opened then or of later profitability.')
add('1910-10-21','Bond & Wiest, Cuervo','Waubanse, Kansas (source spelling)','reported shipment/sale','6,000 sheep, described as lambs and wethers, shipped for feeding for mutton.',2654,limit='Car count withheld because scan reading remains uncertain; this is neither wool processing nor proof of local slaughter.')
add('1910-10-21','John Hicks, Cuervo','Unspecified destination','reported shipment','Four cars of cattle shipped on the same day as the sheep shipment.',2654,limit='Do not attach the sheep shipment\'s Kansas destination to these cattle.')
add('1910-12-02','Bond & Wiest','Wm. Keys, Quay County','reported sale','Named Quay County customer bought a bunch of sheep.',2686,limit='Quantity unknown. The locality is printed as Lochney; modern spelling/location is not resolved.')
add('1910-12-02','Cuervo shipment; Tom Lewis accompanied trip','Los Angeles; Lewis returned from El Paso','reported shipment/travel','Cattle shipped from Cuervo to Los Angeles; Lewis returned from an accompanying trip to El Paso.',2686,limit='Final buyer, ranch origin and exact rail itinerary unknown; Lewis is not assumed to own all the cattle.')
add('1910-12-02','Mr. Handshaw','Santa Rosa','reported farm-product delivery','Report says Handshaw hauled two loads of hay to Santa Rosa that week.',2686,limit='Residence appears in Haile news; exact farm and buyer unknown. Not a Cuervo-store transaction.')
add('1911-01-20','W. R. Harvey and another reported cattle buyer','Cuervo, from Amarillo','reported buyer visit','Two Amarillo cattle buyers reported arriving by train.',2713,limit='Visit does not itself prove a completed sale or shipment.')
add('1899','Wagon Mound Bond business','Cabra predecessor of Bond & Wiest','capital/organizational link','Grubbs traces the Cabra branch and its capital to Wagon Mound.',printed=98,pdf=231,limit='Company history, not an independently inspected original ledger.')
add('Early Cuervo operations','Bond & Wiest wool business','Brown & Adams, Boston; later Hallowell, Jones & Donald','reported marketing relationship','Grubbs identifies eastern wool buyers.',printed=109,pdf=257,limit='Specific quantities and routes not assigned. His suggested Tucumcari shipping route is explicitly excluded as inference.')
add('1905 and 1907','Encino and Bond & Wiest','Cuervo freight consolidation','reported pooling arrangement','Grubbs describes combining hides/pelts for carload shipment and freight-rate advantages.',printed=110,pdf=259,limit='Original correspondence required to establish actual frequency and savings.')
add('1911-1912','A. W. Wiest at Cuervo','Wagon Mound management; Holbrook at Cuervo','manager transfer','Wiest took charge at Wagon Mound in 1911 during MacArthur\'s illness; Holbrook was formally appointed Cuervo assistant manager in 1912.',printed=103,pdf=245,limit='A personnel transfer is not evidence that Cuervo ceased trading.')
add('1915-06','Porfirio Gallegos / A. H. Long','Rosa Mercantile and an unnamed competitor','contested customer loyalty','Grubbs quotes Bond advising Long against withdrawing sheep from Gallegos for trading with a competitor.',printed=228,pdf=499,limit='Rosa in Rio Arriba County, NOT Santa Rosa or Cuervo. Letters June 24 and 29, 1915, Book 58 pp.590,652; originals unread.')
data={'selection':'Selected local reports and branch links, not exhaustive; repeated ads are not transaction counts.','date_note':'Newspaper dates are publication dates, not necessarily event dates.','observations':rows}
(OUT/'trade_network_observations.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
verified=[]
for pid in ['2482','2477','2654','2686']:
 x=dict(pages[pid]); x.update(visually_verified=True,local_mapping_note='Physical PDF page mapping confirmed by visual comparison with the rendered original page.',render='research_evidence/economic_synthesis_2026-09-23/network_renders/'+x['issue_date']+'.png',sha256=hashlib.sha256((ROOT/x['local_issue_file']).read_bytes()).hexdigest());verified.append(x)
(OUT/'newspaper_verification.json').write_text(json.dumps(verified,indent=2),encoding='utf-8')
print('Saved',len(rows),'observations, including four newly inspected front pages.')
