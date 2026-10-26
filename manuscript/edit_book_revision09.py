"""A bounded editorial pass over Revision 8; retain a complete before/after log."""
from pathlib import Path
import hashlib, json, re, shutil

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'manuscript/book-revision-08'
NEW = ROOT / 'manuscript/book-revision-09'
NEW.mkdir(exist_ok=True)
(NEW / 'chapters').mkdir(exist_ok=True)
paths = {n: next((OLD / 'chapters').glob(f'chapter-{n:02}-*.md')) for n in range(1, 9)}
original = {n: p.read_text(encoding='utf-8') for n, p in paths.items()}
bodies = {n: s.split('\n---\n', 1)[0].split('\n\n') for n, s in original.items()}
notes = {n: s.split('\n---\n', 1)[1] for n, s in original.items()}
changes = []

def replace(n, i, text):
    before = bodies[n][i]
    assert before and before != text, (n, i)
    changes.append({'chapter': n, 'original_paragraph': i, 'before': before, 'after': text})
    bodies[n][i] = text

def cut(n, i, text, replacement=''):
    assert text in bodies[n][i], (n, i, text)
    replace(n, i, bodies[n][i].replace(text, replacement).strip())

# Chapter 1: introduce the scope once, without anticipating every later caveat.
cut(1, 9, 'An interchange keeps a place connected to the road, but it cannot guarantee customers for each business.',
    'The value of an interchange depends on which customers a business needs.')
replace(1, 23, 'The published population of Cuervo election precinct 6 was 287 in 1930, 188 in 1940 and 210 in 1950. The precinct included the village and surrounding country. Comparisons with earlier censuses face further problems because reporting areas changed.[^9]')
cut(1, 25, ' A population total records the balance of those movements, not their causes.')
cut(1, 28, ' Continued access to a service does not mean that its departure left the town unaffected.')
replace(1, 33, 'Services can also support one another. The Cuervo record documents families moving for schooling, creating potential demand for housing and trade. Losses could work in the other direction, weakening reasons to maintain other activities. Chapter 7 assesses that possibility.')
replace(1, 37, 'The surviving buildings are an important part of the evidence. Photographs show their materials, condition and position in the landscape. Establishing when and why a business closed requires other records.')

# Chapter 2: describe the scale and the observation directly.
replace(2, 8, 'The merchant connected dispersed grazing country with a concentrated point of exchange. Distance from a ranch to the store mattered alongside distance from the store to an outside buyer. The business had to offer producers and customers enough advantage to keep using it.')
cut(2, 9, 'Nor does the presence of a profitable merchant tell us how large the surrounding settlement should become. ')
cut(2, 18, 'He suggested 1902 as the likely year, but did not establish an exact opening day.', 'He suggested 1902 as the likely year.')
replace(2, 20, 'An undated town map places the Bond & Wiest warehouse beside the railway, close to the depot. Later ownership markings add a separate layer to the sheet. Its layout shows how storage and the transport connection occupied the same corridor, linking rail freight with trade in the town.[^7]')
replace(2, 38, 'In March the paper reported fourteen cars of sheep loaded at Cuervo for Kansas. A separate notice in the same issue described a Kansas buyer purchasing more than 4,000 sheep from Bond & Wiest. The reports document outbound loading and a commercial relationship with an outside buyer.[^11]')
cut(2, 57, 'They were responses to particular prospects and obligations, rather than votes in a single referendum on the town’s future.', 'They answered particular prospects and obligations.')
cut(2, 62, ' Losing one function would not establish the end of the others.')
cut(2, 63, 'More generally, access does not amount to a promise of local prosperity. ')

# Chapter 3: retain accounting distinctions; remove the repeated disclaimer after examples.
cut(3, 8, 'This is one part of the early business change, but it is not an annual sales series.',
    'Sales followed their own course.')
cut(3, 11, ' That is a direct contemporary reason to keep sales and profits separate.')
replace(3, 16, 'Repeated dealings could give the merchant information about a borrower’s prospects, while livestock and produce transactions supplied additional knowledge. Combining trade and finance could make that knowledge useful across the business.')
cut(3, 17, ' The amount alone does not choose among them.')
cut(3, 18, 'The comparison illustrates a financial problem within the wider organization; it does not substitute for Cuervo’s missing cash-flow records.',
    'Its cash strain illustrates a financial problem within the wider organization.')
replace(3, 25, 'The company could reduce stock on the shelves while expanding its stake in sheep. Those investments had different implications for retail work and premises in Cuervo.')
cut(3, 31, 'The figures show different contributions to the enterprise without supplying a fully reconcilable modern income statement.',
    'These historical categories cannot be fully reconciled as a modern income statement.')
cut(3, 32, 'Annual returns for the intervening decades remain unavailable, but the institution’s durability is clear.',
    'The institution proved durable.')
cut(3, 40, ' Its effect depended on the terms, rather than on the simple fact that the relationship existed.')
cut(3, 44, ' These are specific interactions to investigate, beyond the fact that one firm carried several lines of business.')
replace(3, 48, 'Combining consignments secured a reported freight-rate saving: assembling a carload reduced the cost of sending goods to market.')
cut(3, 49, ' The Encino arrangement shows why combining shipments had once been useful.')
cut(3, 56, ' The records do not establish comparable amounts actually received from both sources in each year.')
cut(3, 68, ' The change is substantial, although the two counts are not equivalent measures of output, income or grazing demand.')
cut(3, 73, 'They show why the amount of product entering trade must be distinguished from the stock of livestock at a particular moment.',
    'They measure the product entering trade.')
replace(3, 76, '')
replace(3, 80, 'The figures are consistent with fewer, larger recorded operations. Coverage and definitions changed, and land could be assigned to an operation’s headquarters even when it crossed county lines.')
cut(3, 81, 'That leaves a material difference, but the remainder is not a list of identified closures or departed families.',
    'The revised definition explains part of the fall.')
replace(3, 83, 'An operation could involve owners, family labor and hired workers across several households.')
replace(3, 84, '')
cut(3, 87, ', although their workplaces and occupations are unspecified')
replace(3, 90, 'Stronger cattle conditions could help explain Cuervo’s small population rebound from 188 in 1940 to 210 in 1950. The price rise supplied a favorable setting for those twenty-two additional residents, though its contribution cannot be measured from the two series.[^27]')
replace(3, 91, 'Prices measured in consumer purchasing power are not ranch profits. Receipts also depend on the quantity and weight sold; earnings depend on feed, labor, transport, finance and other costs. The statewide beef-cattle series excludes calves.')
cut(3, 92, ' These are large changes even after allowing for the limits of using a consumer-price index to describe a ranching business.')
cut(3, 94, ' The proximity of the dates cannot establish how much each contributed, or which enterprises were affected.')
cut(3, 96, 'Chapter 7 considers that possible obstacle to reopening; the price series does not document it for a named Cuervo store.',
    'Chapter 7 considers that possible obstacle to reopening.')
cut(3, 99, ' Its eventual ending is not dated by those observations.')

# Chapter 4: keep proposals visibly prospective, then let their implications stand.
replace(4, 8, 'The missing appointment was at Hanson. The decision removed its route to Cuervo without closing Cuervo’s own post office. The network depended on maintaining its local offices as well as carrying mail between them.')
replace(4, 11, 'Enrollment and staffing grew within one autumn. The school served families who could change where they stayed during the term, extending its constituency beyond permanent village residents.')
replace(4, 12, 'On February 8, 1912, the paper reported 132 children enrolled since the term began and 106 currently enrolled.[^4] The first figure includes everyone entering during the term; the second counts those still on the roll.')
cut(4, 15, ' The reports document the moves without measuring that additional trade.')
cut(4, 18, 'Its account concerned the resumption and improvement of schooling, not permanent closure.',
    'The meeting looked ahead to the next school year.')
replace(4, 25, 'The inspection turned local concern into recommendations for the board and teachers; the individual repairs remain unconfirmed.')
cut(4, 33, 'These equivalents help indicate the scale of the commitment. The hundred families and the resulting fund were expectations, not collected subscriptions.',
    'Terry still had to recruit those contributors.')
replace(4, 36, 'Terry sought support across the newspaper’s locality, beyond Cuervo’s resident households. The notice records a proposal; subscriptions, recruitment and treatment fees remain unconfirmed.')
replace(4, 42, 'Visiting care required somebody to arrange a journey, with distance and the practitioner’s other commitments affecting availability.')
cut(4, 43, 'It named no intended recruit, so Sanford’s history provides context rather than an identification of the proposed doctor.',
    'He named no intended recruit.')
cut(4, 50, 'Hicks judged that arrangement preferable; her announcement supplies no measured cost comparison.',
    'Hicks judged that arrangement preferable.')
replace(4, 60, 'Hicks was reorganizing one institution within an already connected market.')
cut(4, 62, 'Other commercial notices show why an operator’s difficulty should not automatically be treated as the permanent loss of a function. ',
    'Commercial services could also return. ')
cut(4, 66, ' One operator’s exit and the disappearance of a service were different events.')
cut(4, 70, ' The notices distinguish those outcomes without providing a count of jobs.')

# Chapter 5: maintain the geography and units, avoiding a second methodological ending.
replace(5, 5, 'The precinct included the settlement and surrounding ranch country. Families living some distance from the commercial center could therefore appear in the population reported under Cuervo’s name.')
replace(5, 9, 'Rural households could precede the town’s commercial concentration and later appear under its name. The 1900 records use different precinct and locality labels.[^3]')
replace(5, 24, 'The reconstruction groups each listed head with the associated household members. Two such groups could share a dwelling, and either could include relatives or other residents beyond a married couple and children.')
cut(5, 27, ' The schedules establish the regrouping; spending effects remain unmeasured.')
cut(5, 37, ' The work recorded at the census need not be the work done when a child was born.')
cut(5, 41, ' These are associations between recent residence changes and work recorded at the later date.')
cut(5, 42, 'The entries connect recent arrivals with ranching and railway occupations. They leave the motive for each move unstated:',
    'The motive for each move is unstated:')
replace(5, 50, 'The household brought agricultural and public employment together.')
replace(5, 55, 'Stuart Holbrook and his wife Blanche supplied another combination: general-merchandise manager and store clerk in the 1950 Cuervo schedules. Their employer was unnamed.[^15]')
replace(5, 56, 'The inventory counts written occupations. Household care and other unrecorded activities also sustained the community; a blank occupation entry cannot be counted as unemployment.')
cut(5, 58, 'It describes the populations rather than measuring a transfer of jobs between them.',
    'Its units are resident populations, not workplaces.')
cut(5, 63, ' The later high-school destination cannot automatically be attributed to one mid-century closure of the Cuervo school.')
cut(5, 64, ' The schooling and the recorded residential move were different events.')
cut(5, 65, ' Santa Rosa schooling and a later Tucumcari home belong to different parts of the account.')
cut(5, 66, ' It does not provide a school-transfer or departure date.')
cut(5, 68, ' The histories identify some connections; they do not reveal the weight each household placed on them.')
cut(5, 71, 'Santa Rosa’s own population history requires more precision than a continuous upward line.',
    'Santa Rosa’s population also fluctuated.')
cut(5, 76, ' It should not be interpreted as hundreds of additional people establishing ordinary households in the town.')
replace(5, 80, 'Municipal expansion can change these reporting areas. Across the published counts, Santa Rosa’s household population persisted amid contraction elsewhere in the county.')

# Chapter 6: distinguish the functions once; captions retain their own necessary reading keys.
cut(6, 11, ' The advertised schedule establishes that difference without counting actual trips or purchases.')
cut(6, 13, ' It did not sever every regional relationship.')
replace(6, 16, 'Santa Rosa’s customers could include residents, rural households, travelers and other businesses. The rest of the county also included Vaughn and other trading places. The census does not identify how much Cuervo residents spent in Santa Rosa.')
cut(6, 23, ' Neither source identifies the purchases of Cuervo households.')
cut(6, 32, ' These records describe separate observations; they do not establish one continuously operating firm.')
cut(6, 35, ' Its usefulness cannot be read solely from the number of vehicles passing its edge.')
cut(6, 45, 'Its condition had deteriorated, but its usefulness had not disappeared altogether. The word abandoned, used to classify the historic highway section, did not mean that nobody traveled on it.',
    'Its condition had deteriorated, but it remained part of local circulation.')
cut(6, 46, ' It does not provide a dated balance sheet for every establishment affected by the road.')
cut(6, 51, ' The condition matters, but it does not turn the stop into a mere passing time.')
cut(6, 55, ', although the surviving observations do not establish the last employee’s workday')
replace(6, 56, 'By October 1958, both advertised passenger stops and the train-order-office designation had disappeared from the inspected schedule. Their exact sequence remains unresolved.')
replace(6, 59, 'The Golden State continued along the corridor after Cuervo’s advertised stops disappeared. The April 25, 1968 Congressional Record reported its discontinuance that March, a decade after the withdrawal of Cuervo’s local passenger stops.[^14]')
replace(6, 65, 'Rock Island’s local freight service, including the availability of cattle-loading facilities, remains unresolved.')
cut(6, 67, ', although the listing does not establish whether cattle were still being loaded there')
cut(6, 69, ' A payroll series would be needed to measure the associated employment loss.')
cut(6, 71, ' The page does not identify deliveries to particular ranches or show whether they displaced the Cuervo merchant.')
replace(6, 72, 'Lower delivery costs could let a ranch buy farther afield, while a dealer retained ordering, credit or small urgent sales. These were possible adjustments within a supply system that offered several channels before Cuervo’s passenger stop disappeared.')
replace(6, 77, 'Earlier contraction therefore remains part of the explanation, alongside the interstate’s later intervention. The plans specify changes and clearance work; individual removal dates, openings and trade losses require other evidence.[^21]')
replace(6, 82, 'In an account published in 2013, K. Mennem described an operating gas station north of I-40 while discussing the older settlement to the south as a ghost town. The traveler named neither the business nor an exact visit date.[^22]')
replace(6, 86, 'A 2025 New Mexico Senate memorial dates the interstate’s completion at Santa Rosa to 1972. This retrospective account places it later than the documented 1963–1965 Cuervo-area project.[^23]')
replace(6, 87, 'Santa Rosa’s increase from 2,220 residents in 1960 to 2,485 in 1970 preceded that reported completion. Its 1970–1980 count then slipped slightly, to 2,469. The 1960s increase belongs before the reported bypass date; these census intervals cannot establish the interstate’s demographic effect.[^24]')
replace(6, 90, 'Several sources of demand could give Santa Rosa alternatives when one weakened.')

# Chapter 7: reserve the general limits for the synthesis, not every example.
replace(7, 3, 'Together, the records show local services diminishing within an economy that still used the surrounding land. Some decisions can be explained directly. Economic mechanisms help account for the broader result.')
replace(7, 8, 'Joint operation gave Bond & Wiest several sources of business and could save costs through shared premises, management and knowledge of customers. Combined hide shipments provide a specific example: assembling a carload secured better freight terms. The broader savings remain unmeasured.')
cut(7, 12, 'Figure 7.2 compares these requirements without treating a proposal as an operating institution.',
    'Figure 7.2 compares these requirements.')
replace(7, 18, 'Agricultural conditions could alter both the volume and the kind of demand. The county’s mid-century shift toward cattle affected the market around a merchant with a substantial history in sheep and wool. The early-1950s fall in real cattle prices could constrain producers’ spending while road access was changing.[^11]')
replace(7, 19, 'Higher prices later in the series need not restore an earlier supplier’s customers: income could support established alternatives elsewhere. That offers one explanation for why a town might fail to recover alongside its agricultural market.')
replace(7, 23, 'Serving users from farther away changes the costs of maintaining a nearby establishment and of reaching its replacement.[^14] A household with a car and a worker dependent on a local employer could experience the same change differently. Time, fares and the availability of rides mattered alongside distance.')
replace(7, 27, 'Its fit to Cuervo is weaker. The town’s early withdrawals and precinct population loss preceded widespread cooling. A broad movement into the Southwest also cannot explain why work should concentrate in Santa Rosa rather than Cuervo. Santa Rosa had widespread air conditioning by 1980, alongside a slightly lower population than in 1970.[^17] Cooling may have made remaining more comfortable, but the available local evidence does not identify it as a cause of migration between the two places.')
replace(7, 30, 'A residential growth path requires housing people can obtain and worthwhile work, services or amenities they can reach. Los Lunas combined metropolitan connections with employers and services of its own. Cuervo’s proximity to Santa Rosa offered a different set of opportunities. The shared ranching background makes Los Lunas a useful comparison, but differences in employment, housing and journeys prevent it from serving as a controlled test of Cuervo’s prospects.')
replace(7, 32, 'Interdependence is directly visible in the early school-related moves: an institution helped determine where families stayed.[^20] A later loss could work in reverse if households left and their reduced spending weakened other services. Travel or replacement provision could interrupt that reinforcing process, as the family histories suggest.[^21]')
replace(7, 34, 'The local record identifies relevant commitments: merchant capital and premises, managers, qualified staff and financial backers. Reassembling them could make reopening difficult. The 1921 garage reopening shows that such obstacles could also be overcome.')
replace(7, 38, 'Relocation, staffing interruptions, Hicks’s withdrawal, road changes, passenger stops and billing assignments establish contraction without a single interstate turning point. The record leaves some final closures undated. Feedback and the costs of reopening explain how losses could persist, but their local size and sequence remain unmeasured. They are mechanisms consistent with the history, rather than a demonstrated chain accounting for every closure.')
cut(7, 39, 'The demographic evidence fits this account without proving every mechanism. ')
cut(7, 40, ' The records establish a contraction of local work, not its net benefit or cost to everyone affected.')

# Chapter 8: let the closing argument end on what remained.
cut(8, 13, 'These are documents of later property arrangements, rather than evidence that the town had ceased to matter to its owners.',
    'The old divisions continued to organize new property arrangements.')
cut(8, 14, 'The property retained value long after the teaching whose final date remains uncertain.',
    'The property retained value long after teaching had ended.')
cut(8, 18, ' The parish’s reported totals cannot be treated as attendance figures for Cuervo.')
cut(8, 19, ' The entry leaves the venue and frequency of services unspecified.')
cut(8, 20, 'Their separate dates leave the frequency of services unresolved.',
    'The later service schedule remains unresolved.')

# Source-note cleanup is deliberately narrow: remove a literal repeated explanation.
note24 = re.search(r'^\[\^24\]: (.*?)(?=\n\n\[\^|\Z)', notes[3], re.M | re.S)
assert note24
note_before = note24.group(0)
note_after = note_before.replace(' The first observations concern late September and early October, the second the week before enumeration, typically in November locally. Their difference is not a comparable annual job-loss estimate.', '')
assert note_before != note_after
notes[3] = notes[3].replace(note_before, note_after)
changes.append({'chapter': 3, 'note': 24, 'before': note_before, 'after': note_after})

# Move figures a few paragraphs earlier, placing interpretation after the visual.
# This keeps abbreviated passages from stranding a short page before a full-page plate.
layout_moves = [(5, 26, 24), (5, 54, 49), (7, 14, 12)]
for n, marker, before in layout_moves:
    assert bodies[n][marker].startswith('<!-- FIGURE:')
    bodies[n][before] = bodies[n][marker] + '\n\n' + bodies[n][before]
    bodies[n][marker] = ''
(NEW / 'layout-adjustments.json').write_text(json.dumps([
    {'chapter': n, 'original_marker_paragraph': marker, 'moved_before_original_paragraph': before}
    for n, marker, before in layout_moves
], indent=2), encoding='utf-8')

for n, p in paths.items():
    body = '\n\n'.join(b for b in bodies[n] if b != '')
    text = body + '\n---\n' + notes[n]
    old_refs = re.findall(r'\[\^(\d+)\]', original[n].split('\n---\n', 1)[0])
    new_refs = re.findall(r'\[\^(\d+)\]', body)
    # The repeated note-24 call in a deleted methodological aside is the sole removed call.
    expected_refs = old_refs.copy()
    if n == 3: expected_refs.remove('24')
    assert expected_refs == new_refs, ('citation sequence changed', n)
    assert re.findall(r'<!-- (?:FIGURE|PHOTO):.*?-->', original[n]) == re.findall(r'<!-- (?:FIGURE|PHOTO):.*?-->', text)
    (NEW / 'chapters' / p.name).write_text(text, encoding='utf-8')

for filename in ['bibliography.md', 'revision06-integrity.json', 'revision07-integrity.json']:
    shutil.copyfile(OLD / filename, NEW / filename)
protected = list(OLD.rglob('*')) + [ROOT / 'output/pdf/cuervo-complete-reading-proof-revision-08.pdf', ROOT / 'manuscript/build_book_revision08.py', ROOT / 'manuscript/check_book_revision08.py', ROOT / 'manuscript/book_visuals_revision08.py']
integrity = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
(NEW / 'revision08-integrity.json').write_text(json.dumps(integrity, indent=2), encoding='utf-8')
(NEW / 'editorial-changes.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding='utf-8')
print('PASSAGES_EDITED', len(changes))
