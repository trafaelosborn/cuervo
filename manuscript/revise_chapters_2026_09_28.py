"""Apply the bounded September 28 editorial revision to preserved draft sources."""
from pathlib import Path
import re
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'manuscript/revisions/chapters01-03-before-2026-09-28'
EVIDENCE = ROOT / 'research_evidence/monetary_revision_2026-09-28'
EVIDENCE.mkdir(parents=True, exist_ok=True)
CPI = {1899:25,1900:25,1901:25,1902:26,1903:27,1904:27,1905:27,
       1906:27,1907:28,1908:27,1909:27,1910:28,1911:28,1912:29,
       1913:29.7,1914:30.1,1915:30.4,1932:41,2025:967.5}
source = ROOT/'research_evidence/origins_followup_2026-09-23/financial_transcription.json'
original = json.loads(source.read_text(encoding='utf-8'))
converted = {key:[{'year':r[0], 'nominal_thousands':r[1],
                         'constant_2025_thousands':r[1]*CPI[2025]/CPI[r[0]]}
                        for r in original[key]['rows']]
             for key in ['table_32','table_33','table_34','table_35']}
examples = [{'year':y,'nominal_dollars':n,'constant_2025_dollars':n*CPI[2025]/CPI[y]}
            for y,n in [(1899,10000),(1910,4000),(1911,5300),(1915,16700),(1904,75),(1907,125),(1932,90000)]]
manifest = {'checked':'2026-09-28','base_year':2025,
 'cpi_source':'https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1800-',
 'cpi_basis':'Published historical table, 1967 basis; all ratios use this same series.',
 'cpi_selected_years':CPI,'method':'nominal amount * CPI(2025) / CPI(year)',
 'limits':'Consumer purchasing power, not business valuation, asset replacement cost, local prices or ranch input costs. Pre-1913 reconstructed historical index. Annual-average index also used for year-end balances. Historical amounts already rounded in Grubbs.',
 'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'series':converted,'selected_equivalents':examples,
 'profit_change_1911_1915_nominal_pct':(16700/5300-1)*100,
 'profit_change_1911_1915_real_pct':((16700/CPI[1915])/(5300/CPI[1911])-1)*100}
(EVIDENCE/'calculations.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

money_note = ('Monetary convention: unqualified sums retain their historical dollar values. Selected parentheticals and the financial chart express approximate 2025 consumer purchasing power, calculated as the historical amount multiplied by the 2025 annual index and divided by the index for the original year. '
 '[Federal Reserve Bank of Minneapolis historical CPI table](https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1800-), checked September 28, 2026; '
 '[BLS explanation of constant dollars](https://www.bls.gov/cpi/factsheets/purchasing-power-constant-dollars.htm); '
 '[inputs and calculations](B:/Meridian/Cuervo/research_evidence/monetary_revision_2026-09-28/calculations.json). '
 'The historical table uses reconstructed price estimates before 1913. Equivalents are rounded and do not estimate current business value, replacement cost or local purchasing conditions. The same annual-average deflator is applied to year-end balances; it does not revalue their physical contents.')

def change(text, old, new):
    assert text.count(old)==1, (text.count(old),old[:90])
    return text.replace(old,new)

def renumber(text):
    body, notes = text.split('\n---\n',1)
    order=list(dict.fromkeys(re.findall(r'\[\^(\d+)\]',body)))
    definitions=dict(re.findall(r'^\[\^(\d+)\]: (.*?)(?=\n\n\[\^|\Z)',notes,re.M|re.S))
    assert set(order)==set(definitions)
    mapping={old:str(n) for n,old in enumerate(order,1)}
    body=re.sub(r'\[\^(\d+)\]',lambda m:'[^'+mapping[m[1]]+']',body)
    notes='\n## Working source notes\n\n'+'\n\n'.join('[^'+mapping[n]+']: '+definitions[n].strip() for n in order)+'\n'
    return body+'\n---\n'+notes,mapping

maps={}
name='chapter-01-reading-cuervo.md'
t=(OLD/name).read_text(encoding='utf-8')
t=change(t,'DRAFT 6 | 2026-09-25. Accessible institutional prose; proportionate assessment of household cooling.',
           'DRAFT 7 | 2026-09-28. Accessible institutional prose; source plates and assessor evidence integrated.')
t=change(t,'The school was expanding while the lumber firm was withdrawing stock. The railway was improving its facilities, but that offered no guarantee to nearby businesses. Even this small settlement could grow in one respect and shrink in another.',
           'The three notices describe different decisions made in the same place. The school project drew investment while the lumber firm withdrew stock. Improvements at the depot did not guarantee trade for every neighboring business. Even this small settlement could grow in one respect and shrink in another.')
t=change(t,'## Roads and roadside trade','<!-- FIGURE: simultaneous-change -->\n\n## Roads and roadside trade')
t=change(t,'The photographs therefore need to be read alongside other records. School reports document investment and arrivals. Merchant accounts connect a building to customers and distant markets. Current ranching records establish work beyond the village. Together, these sources describe more of the place than its buildings alone can reveal.',
           'Property records make the same distinction necessary. An assessor card prepared in January 1983 classified a Cuervo property as a gas station, rated its condition poor and used a salvage basis for valuation. A later entry recorded no change in December 2008. The card documents an assessed building and its condition. It does not date the last sale of petrol or explain why the business stopped.[^14]\n\nEach kind of record answers a different question. School reports document investment and arrivals. Merchant accounts connect premises to customers and distant markets. Current ranching records establish work beyond the village. Read together, they show how commercial activity could retreat while buildings and rural production remained.')
t += '\n[^14]: Guadalupe County assessor packet, Cuervo townsite, old-town Block 20, lots 8-12, [property-card scan](B:/Meridian/Cuervo/Cuervo/Cuervo/Cuervo Townsite/scan_20260922144438405.pdf), PDF pp. 1-2. The building card on p. 2 is marked prepared January 1983; a subsequent entry is dated December 15, 2008. Classification, condition and valuation treatment are dated administrative observations. The effective-age field is not a construction date. No operator or closing date is established. [Packet reading record](B:/Meridian/Cuervo/research_evidence/county_packet_2026-09-27.md).\n'
t,maps['1']=renumber(t)
(ROOT/'manuscript'/name).write_text(t,encoding='utf-8')

name='chapter-02-why-a-town-here.md'
t=(OLD/name).read_text(encoding='utf-8')
t=t.replace('DRAFT 1 | 2026-09-26.','DRAFT 2 | 2026-09-28.',1)
t=change(t,'which supplied its initial $10,000. The branch began with financial backing and commercial connections beyond its immediate locality.[^4]',
           'which supplied its initial $10,000 (about $390,000 in 2025 consumer purchasing power).[^4][^24] The branch began with financial backing and commercial connections beyond its immediate locality.')
t=change(t,'The investment also committed the business to a place.',
           'An annotated town map places the Bond & Wiest warehouse beside the railway, close to the depot. Its layout makes the commercial relationship visible: storage and the transport connection occupied the same corridor. The map is undated and carries later ownership markings, so it cannot supply an exact plan of the premises in 1903. It does show how the merchant was positioned to link rail freight with trade in the town.[^25]\n\nThe investment also committed the business to a place.')
t=change(t,'The railway connection itself is independently documented at the regional level.',
           '<!-- FIGURE: cuervo-map -->\n\nThe railway connection itself is independently documented at the regional level.')
t=change(t,'The incoming trade appears alongside it. The March 11 issue reported Bond & Wiest unloading separate cars of flour, sugar and grain, as well as sending out hides and pelts. In July, wool was reported arriving from the surrounding country while the firm received cars of grain, flour and fruit. The town joined movements that ran in both directions.[^10][^11]',
           'Supplies moved the other way. The March 4 issue reported a carload of potatoes, grain and dried fruit unloaded for Bond & Wiest. The firm\'s advertisement on the same page offered groceries and farming equipment while soliciting hides and pelts. A week later, the paper reported separate cars of flour, sugar and grain arriving, and hides and pelts going out. In July, wool came in from the surrounding country while the firm received further merchandise by rail.[^10][^11]\n\n<!-- FIGURE: trade-notices -->')
t=change(t,'$4,000','$4,000 (about $140,000 in 2025 purchasing power)')
t=change(t,'Monetary amounts are nominal historical dollars.','The initial financing is placed in the 1899 founding context; the price index is the same for 1899 and 1900. Other unqualified sums retain historical dollar values.')
t=change(t,'Plans for a third teacher are not treated as completed appointments.',
           'Plans for a third teacher are not treated as completed appointments. The later [2010 school survey](B:/Meridian/Cuervo/Cuervo/Cuervo/Cuervo Plats/C-232.pdf) identifies the school parcel and cites deeds from 1913 and 1943. Those are references to instruments, not independently inspected deeds or proof of a school relocation or a date for the surviving building. The newspaper construction sequence is retained on its own evidence.')
t+='\n[^24]: '+money_note+'\n'
t+='\n[^25]: Guadalupe County packet, [City of Cuervo parcel map](B:/Meridian/Cuervo/Cuervo/Cuervo/Parcel Map/City of Cuervo.pdf), one sheet, undated. The printed rail corridor identifies the depot, section house and Bond & Wiest warehouse; colored ownership annotations form a separate layer of uncertain date. Figure 2.1 reproduces a sheet overview and an enlarged detail, retaining those markings. Platted lots are not counted as occupied buildings, and the title does not establish municipal incorporation. [Intake and reading record](B:/Meridian/Cuervo/research_evidence/county_packet_2026-09-27.md).\n'
t,maps['2']=renumber(t)
(ROOT/'manuscript'/name).write_text(t,encoding='utf-8')

name='chapter-03-the-business-of-ranch-country.md'
t=(OLD/name).read_text(encoding='utf-8')
t=t.replace('DRAFT 1 | 2026-09-26.','DRAFT 2 | 2026-09-28.',1)
t=change(t,'The accounts make Cuervo\'s economic history more concrete.',
           'In approximate 2025 consumer purchasing power, the two profits were $180,000 and $530,000. Inflation reduces the size of the recovery, but leaves the finding intact: reported profit nearly tripled in real terms.[^29]\n\nThe accounts make Cuervo\'s economic history more concrete.')
t=change(t,'<!-- FIGURE: merchant-finance -->\n\nThe recovery should change the narrative, but it should not be made to do too much. These are nominal historical figures from a later reconstruction, using the accounting categories available to Grubbs. They show reported earnings and their direction. They do not measure the owners\' return against every alternative investment, or the welfare of everyone who lived in Cuervo.\n\nWithin those limits, the conclusion is substantial. Bond & Wiest was capable of earning money after the early setbacks. A description of the town as already undergoing inevitable commercial extinction cannot rest on this firm\'s uninterrupted failure. Its own figures contain both contraction and recovery.',
           'Adjusting for inflation preserves the pattern. In 2025 purchasing power, reported profit rose by about 190% between 1911 and 1915, compared with about 215% in the original dollar figures. The chart applies the same adjustment to each year\'s balances and profits. Sheep still overtook merchandise, and the recovery remains substantial.[^29]\n\n<!-- FIGURE: merchant-finance -->\n\nThese accounts come through Grubbs\'s later reconstruction, with the categories and rounding he supplied. They establish reported earnings, rather than a modern audit or a measure of every resident\'s welfare. On that evidence, Bond & Wiest remained capable of earning money after the early setbacks. Its contraction and recovery both belong in the town\'s history.')
t=change(t,'The court described a proposed $90,000 corporate loan sought in 1932.',
           'The court described a proposed $90,000 corporate loan sought in 1932 (about $2.1 million in 2025 purchasing power).')
t=change(t,'He reported a monthly managerial salary of $75 beginning in 1904, rising to $100 in 1905 and $125 in 1907.',
           'He reported a monthly managerial salary of $75 beginning in 1904 (about $2,700 in 2025 purchasing power). The historical salary rose to $100 in 1905 and $125 in 1907.')
t=change(t,'This also limits the conclusions that can be drawn from positive company profits. Money could be retained, credited against obligations or used to sustain the enterprise. It need not appear immediately as additional local household spending. The path from a firm\'s earnings to demand for another Cuervo shop included decisions about finance and distribution.\n\nThe same point applies in the other direction. A modest cash payment to an owner would not necessarily indicate a failing business if earnings were being used within it. Evaluating the enterprise requires attention to what happened to its resources, rather than assuming that every profitable year translated directly into money circulating through the settlement.',
           'Profits could consequently support the enterprise without immediately becoming household spending in Cuervo. Money might remain in the business or be credited against an owner\'s debt. A modest cash distribution could coexist with a profitable year. To understand what the merchant supported locally, the use of its earnings matters as much as their amount.')
t=change(t,'One possible mechanism is straightforward. During a closure, customers establish accounts and habits elsewhere.',
           '<!-- FIGURE: cattle-price-cycle -->\n\nA possible explanation lies in what customers do after a closure. They establish accounts and habits elsewhere.')
t+='\n[^29]: '+money_note+' The 1911-1915 net-profit comparison uses unrounded converted values: approximately +190.2% in consumer purchasing power, against +215.1% nominally. The cattle-price chart uses a separate index with 1951 = 100, calculated within its own consistent CPI series; the two published CPI bases are never divided across series.\n'
t,maps['3']=renumber(t)
(ROOT/'manuscript'/name).write_text(t,encoding='utf-8')
(EVIDENCE/'note-renumbering.json').write_text(json.dumps(maps,indent=2),encoding='utf-8')
print(json.dumps({'note_maps':maps,'real_profit_recovery_pct':manifest['profit_change_1911_1915_real_pct']},indent=2))
