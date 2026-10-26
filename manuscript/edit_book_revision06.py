"""Apply the agreed final editorial pass without changing Revision 5."""
from pathlib import Path
import re, json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT/'manuscript/book-revision-05'
NEW = ROOT/'manuscript/book-revision-06'
BODIES, NOTES, NAMES, CHANGES = {}, {}, {}, []
for n in range(1, 9):
    p = next((OLD/'chapters').glob(f'chapter-{n:02d}-*.md'))
    body, notes = p.read_text(encoding='utf-8').split('\n---\n', 1)
    BODIES[n] = body.strip()
    NOTES[n] = {int(k): v.strip() for k, v in re.findall(r'^\[\^(\d+)\]: (.*?)(?=\n\n\[\^|\Z)', notes, re.M|re.S)}
    NAMES[n] = p.name

def edit(n, start, replacement='', end=None):
    """Replace one paragraph, or the span before another exact paragraph start."""
    blocks = BODIES[n].split('\n\n')
    matches = [i for i, b in enumerate(blocks) if b.startswith(start)]
    assert len(matches)==1, (n,start,matches)
    a=matches[0]
    if end:
        targets=[i for i,b in enumerate(blocks) if i>a and b.startswith(end)]
        assert len(targets)==1, (n,end,targets)
        z=targets[0]
    else: z=a+1
    CHANGES.append({'chapter':n,'before':'\n\n'.join(blocks[a:z]),'after':replacement})
    blocks[a:z]=[replacement] if replacement else []
    BODIES[n]='\n\n'.join(blocks)

def sub(n, old, new):
    assert old in BODIES[n], (n,old)
    BODIES[n]=BODIES[n].replace(old,new)
    CHANGES.append({'chapter':n,'before':old,'after':new})

# Chapter 1: a clear promise, short previews, one introduction.
edit(1,'Cuervo was expanding','Cuervo was expanding and contracting at once.')
edit(1,'Today, Cuervo','Today, Cuervo is commonly described as a Route 66 ghost town. Its surviving buildings help explain the label. The surrounding land, however, still supports ranching.[^2]')
edit(1,'Grubbs’s reconstruction of the early accounts','Grubbs found the merchant still operating in 1958.[^5] A firm serving ranch country could outlast other local undertakings without generating a large town around it.',end='## What kept a service open?')
edit(1,'The school gave families','Schooling also drew families into Cuervo from the surrounding country in 1910 and 1912.[^7] Its ability to attract residents depended on maintaining instruction, premises and staff.',end='The newspaper depended')
edit(1,'The newspaper depended','The newspaper relied on a backer who valued a political return as well as commercial receipts. Katharine A. Hicks’s December 1922 withdrawal of financial support changed that arrangement.[^8] A service could lose its sponsor while some of its users remained.',end='## Which Cuervo')
edit(1,'Railway administration provides','Different services had different centers. Santa Rosa supplied some needs; Tucumcari supplied others. Following those connections reveals overlapping markets and institutions, rather than one town simply absorbing another.',end='This also changes')
edit(1,'Adam Smith linked','A specialist needs enough work to cover the cost of maintaining a separate operation. A firm facing scattered demand may instead combine tasks or reach customers over a wider territory.[^11] Cuervo’s merchant did both. Its market extended beyond the village, so the local population was a poor measure of the trade available.',end='Transport can change')
edit(1,'Home air conditioning',end='Services can also support')
edit(1,'The chapters that follow',end='<!-- PHOTO: window-inscription -->')
edit(1,'This book’s contribution','The records are fullest for Cuervo’s formation and early services. They document several later withdrawals but leave other closures undated. This book follows the work that gathered at Cuervo, the support that sustained it, and the changes that reduced its role while ranching continued. It begins with the question of why that work gathered here.',end=None)
edit(1,'Cuervo lost many of the activities')
NOTES[1][11]='Adam Smith, *An Inquiry into the Nature and Causes of the Wealth of Nations* (1776), Book I, chapter III, on market extent and specialization. The distinction between a settlement’s residents and the customers available to its firms guides the application here. Wider reach alone does not demonstrate declining average costs, and joint operation alone does not measure savings from shared resources.'

# Chapter 2: bring the reader to the relocation sooner.
edit(2,'The original investment should')
edit(2,'A livestock economy','Livestock production occupied land beyond the streets where commerce gathered. A merchant serving that country could handle substantial trade with relatively few people living beside its store.')
edit(2,'The store’s purpose','The branch combined merchandise, credit, sheep interests and wool buying. A producer might need supplies before receiving payment for a sale, while the firm needed information about the flocks in which it had invested.')
edit(2,'The railway changed the relative',end='## The first location')
edit(2,'The Wagon Mound business financed','Outside finance bought stock before the branch earned receipts, while the parent business supplied commercial relationships an independent entrant would have had to establish.')
edit(2,'A profit share gave','Wiest’s profit share linked his return to the business he managed. The arrangement joined the Bonds’ capital and connections to his work at the branch.',end='The surviving reconstruction')
edit(2,'Relocation carried an established')
edit(2,'Storage let the firm')
edit(2,'Formation proceeded in stages')
edit(2,'Railway access distributed',end='## Santa Rosa already')
edit(2,'Both centers could serve')
edit(2,'That episode identifies','Feed and handling earned income from animals whose journey began elsewhere. The stop mattered because Cuervo supplied something the traffic needed.')
edit(2,'The Kansas feeding destination','The Kansas destination locates a limit to the work retained at Cuervo. Loading gathered trade there; feeding the sheep supported a later stage of production elsewhere.')
edit(2,'A consignment divided work')
edit(2,'A trading place becomes','Schooling provided a reason to gather independent of a freight shipment. The *Clipper* reported families moving into Cuervo for their children’s education in September 1910, and again in April 1912.[^15][^16] Some came for the school term while keeping their rural connections. Chapter 4 follows the staffing, finance and maintenance that made instruction possible.',end='Medical provision supplies')
edit(2,'Woodburn’s choice adds')
edit(2,'By 1920, the business','By 1920, the business directory listed Armijo Mercantile as well as Bond & Wiest, the Golden Rule Garage, and the Oklahoma and Rock Island hotels. It also named a school principal, a postmaster, a railway agent and a stage and mail line to Lucille. Cuervo combined trade, lodging, repairs, public services and communications.[^17]',end='These services also')
edit(2,'Different expectations were','More farm households promised customers and pupils, but could threaten the grazing on which stockmen depended. The newspaper’s optimism and the ranchers’ objections expressed different interests in the same land.',end='Grubbs’s account preserves')
edit(2,'A town has no common')
edit(2,'The correction separates','Passenger access, freight handling, staffing and shipment administration followed different histories, examined in Chapter 6. Losing one function would not establish the end of the others.',end='More generally, access')
edit(2,'Wiest’s letter identifies')
edit(2,'Cuervo’s formation can now','The railway gave an established merchant a reason to move from Cabra. Capital, premises, management and customer relationships made that location usable; schooling and other services gave additional reasons to gather. Santa Rosa already performed a wider range of work, but Cuervo did not need to reproduce it to serve a useful market.',end='The more demanding question')

# Chapter 3: keep the commercial evidence; reduce repeated lessons.
edit(3,'The store and warehouse therefore')
edit(3,'The railway contributed to both')
edit(3,'A book account represented','Book accounts recorded money owed to the firm. Sales and cash collection could occur at different times: households needed supplies, and producers incurred costs, before the next livestock or wool sale.',end='For the merchant, credit')
edit(3,'For that reason, a merchant’s')
edit(3,'That makes a general store')
edit(3,'The court described a proposed','The ranchers assigned leases and other interests as security for company finance, and agreed to handle their business through the corporation while the loan remained unpaid. Credit, grazing access, livestock and purchasing obligations reinforced one another.[^11]',end='That combination could matter')
edit(3,'Economists describe these','When one contract changes the choices available under another, the markets are interlinked. A sheep owner’s control over livestock could affect a rancher’s choice of merchant; credit obligations could restrict the same choice.[^12] These are specific interactions to investigate, beyond the fact that one firm carried several lines of business.')
edit(3,'Combining lots secured better','Combining consignments secured a reported freight-rate saving: here the source identifies how aggregation reduced a cost. Shared management, premises or information might also have made joint operation economical, but the accounts do not measure those savings.')
edit(3,'Cooperation also helps','Handling without a separate fee benefited the related firms through the combined shipment.',end='The same function could')
edit(3,'The arrangement also helps explain how the enterprise')
sub(3,'The two streams should not be collapsed into a single estimate of the manager’s income.','The records do not establish comparable amounts actually received from both sources in each year.')
edit(3,'Branch accounts followed')
edit(3,'Customer loyalty was being contested')
sub(3,'It recorded 596 farms in 1930 and 297 in 1959.','It recorded 596 farms in 1930, 851 in 1935 and 297 in 1959. The long-term decline followed an intervening increase.')
edit(3,'The labor returns require','The farm totals do not count households or annual jobs. Seasonal labor returns are also imperfectly comparable, as the source note explains.[^24]',end='Motor transport was already')
sub(3,'The farm count had risen from 596 in 1930 before its later decline; the long-term endpoints conceal that intervening rise. ','')
edit(3,'Paid work away from the farm was')
sub(3,'The project’s statewide series','The statewide price series')
edit(3,'Nor does a rise in the selling price')
edit(3,'A possible explanation lies','After a closure, customers may establish accounts elsewhere, so rising incomes need not bring trade back to its former location. Chapter 7 considers that possible obstacle to reopening; the price series does not document it for a named Cuervo store.',end='## What an export can support')
edit(3,'The broader problem has','Douglass North’s account of agricultural growth turns on what exports require locally and where their income is spent.[^29] Sales beyond the region can sustain local services, but the location of supporting work and purchases determines how much employment they create nearby. Cuervo’s merchant supplied handling, finance and trade. Sheep feeding in Kansas, wool buying in Boston and feed manufacture in Clovis placed other work elsewhere.',end='The firm itself is')
NOTES[3][11]+=' The proposed 1932 corporate loan was $90,000, about $2.1 million in 2025 consumer purchasing power. The courts refused to enforce a promised cancellation of the ranchers’ remaining debts because the manager lacked authority and the corporation had not ratified the promise.'
NOTES[3][24]+=' Family-worker estimates were 593 in 1954 and 413 in 1959; hired-worker estimates were 292 and 121. The first observations concern late September and early October, the second the week before enumeration, typically in November locally. Their difference is not a comparable annual job-loss estimate.'

# Chapter 4: let decisions and material details carry the institutional history.
edit(4,'Simmons’s departure exposed','An offering can depend on a minimum amount of qualified staff time. Losing one essential worker may interrupt instruction even when pupils remain. Sanchez’s announcement proposed a replacement; the record does not establish its implementation.',end='A separate administrative record')
edit(4,'Both services depended')
edit(4,'The distinction between permanent and seasonal residence',end='The institution and settlement')
edit(4,'Volunteer teaching still required')
edit(4,'Residents were working out')
edit(4,'The survey also cites deeds','The survey cites deeds from 1913 and 1943, but does not establish when the mapped building was constructed. The early newspaper’s school and the structure recorded in 2010 have not been shown to be the same building.',end='<!-- FIGURE: school-parcel -->')
edit(4,'The later disposal record','The property’s later sale belongs to the history of continuing use in Chapter 8. The often-repeated 1958 school closure date remains unconfirmed by a contemporary record of instruction.',end='<!-- PHOTO: building-fabric -->')
edit(4,'The payment interval, contribution','Terry wrote from Newkirk and sought support across the newspaper’s locality. His hundred families were prospective contributors, not a count of Cuervo households or a measured minimum for a village practice. The notice leaves subscriptions, recruitment and the relationship between monthly contributions and treatment fees unconfirmed.',end='<!-- FIGURE: doctor-support -->')
edit(4,'Regular contributions could','The proposal addressed reliability of income between calls. Whether the sum would attract a doctor depended on expenses, additional fees and the practitioner’s alternatives.',end='## Care across')
edit(4,'The schoolhouse had a role','A school building, visiting worker and published schedule could bring care to families without maintaining a full-time practice at each stop.',end='The distinction is relevant')
edit(4,'Hicks supplied both a reason',end='Her comparison was also')
edit(4,'That proposal illustrates','Producing one weekly for several communities could spread editorial and printing costs over more readers and advertisers. Hicks judged that arrangement preferable; her announcement supplies no measured cost comparison.',end='The proposed location')
edit(4,'Hicks also intended','Hicks promised continued contributions to the Santa Rosa paper. Her withdrawal from one enterprise accompanied participation in another.')
edit(4,'The newspaper earned a political')
edit(4,'Hicks’s withdrawal brought','Hicks’s decision joined losses, a political purpose fulfilled and an alternative county paper. She allowed that denser settlement might support a different arrangement later. Her statement explains the withdrawal of her backing, while leaving the *Clipper*’s final publication date open.',end='## Local readers')
edit(4,'This possibility matters','Continued coverage in a county paper could preserve local news while moving publishing work and responsibility elsewhere. Whether the proposed paper supplied that coverage would require its subsequent issues.')
edit(4,'The rival advertisements')
edit(4,'The hotel sale transferred')
edit(4,'Together, these episodes','Reopening, reuse and changes of ownership could preserve a service under a different arrangement. Fuel or repairs might remain available without preserving the same proprietor or employment. The notices distinguish those outcomes without providing a count of jobs.',end='## What size alone')
edit(4,'## What size alone','## Different requirements for staying open\n\nThe merchant’s wide market and the garage’s combined tasks helped make local business possible. The school, doctor proposal and newspaper reveal additional requirements: an essential worker, dependable receipts and a backer’s willingness to pay. Their sponsors also cared about what was offered. Hicks wanted a first-class weekly; school supporters wanted practical instruction and considered high-school accreditation. A count of potential users could not resolve those decisions.\n\nThese commitments could change at different times. A political purpose might be fulfilled while pupils still needed instruction; a new mechanic could reopen a garage while another enterprise lost support. Their uneven histories help explain why no single population count marks the point at which Cuervo’s services became untenable.\n\nThe next chapter follows the people within that changing provision. Schooling, work and residence could connect a household to different places, with each connection changing on its own schedule.',end='---' if False else None)
# Replace the old concluding sections, following the substituted heading block.
edit(4,'These cases put a familiar',end=None) if 'These cases put a familiar' in BODIES[4] else None
start=BODIES[4].index('\n\nMarket size explains part')
BODIES[4]=BODIES[4][:start]

# Chapter 5: stronger census opening and bounded household interpretation.
edit(5,'John Higgins Jr. graduated','Cuervo precinct gained twenty-two residents between 1940 and 1950, rising from 188 to 210. The schedules show a larger change in how they lived: household groups increased from forty-two to fifty-nine, with most of the additional groups containing only one or two people. A modest population rebound concealed a substantial change in household structure.[^2][^8]\n\nThe counts covered countryside as well as the village. Following the people within them reveals arrivals, changing families, and several kinds of work under one roof. Later family histories trace a different set of connections: where people went to school, earned a living, and made a home.',end='## The population inside')
edit(5,'The geographic distinction suits')
edit(5,'Across the five enumerations')
edit(5,'The smaller population remained young')
sub(5,' Calling the whole population too young to serve would overlook them.','')
edit(5,'The children supply another','The 1950 schedules contain fifty-one children under ten, nearly the same as the fifty-two known in 1940. Young children helped sustain the later total, but their count includes any who had arrived from elsewhere; it is not a measure of local births.[^9]',end='The rebound warrants')
edit(5,'The large Bailey family','Twenty-four households in 1950 contained at least one recorded ranching occupation. They included ninety-one people and eighteen children under ten: roughly forty-three percent of all residents and thirty-five percent of the youngest children.[^11] Large families also appeared alongside railway, construction and postal work. The work recorded at the census need not be the work done when a child was born.',end='## Arrivals in a declining')
edit(5,'Movement crossed the boundary')
edit(5,'The six answers naming','The answers occurred in six households with a combined membership of twenty-five. That gives a sense of scale beside the precinct’s twenty-two-person net gain, but does not establish twenty-five migrants: the question was asked of selected individuals, whose answers cannot be assigned to everyone sharing the home.[^12]',end='## Several kinds')
sub(5,'It documents two people’s retail work within the household, without requiring the uncertain later biographical link to identify their employer.','It documents two people’s retail work without identifying their employer.')
edit(5,'Her documented roles span')
edit(5,'John Jr.’s reported','John Higgins Jr.’s family account dates his Santa Rosa High School graduation to 1969 and a move from Cuervo to Santa Rosa to 2006. It also describes ranch work in New Mexico and Oklahoma, leaving his intervening residence incomplete.[^1] The schooling and the recorded residential move were different events.')
edit(5,'These selected histories','Rudolpho, or Rudy, Chavez’s family account likewise names schooling in Cuervo and Santa Rosa, and places his married home in Cuervo after his 1965 marriage. It does not date the educational transition or establish uninterrupted residence.[^25] These histories trace different school, work and home connections; attendance elsewhere cannot by itself be coded as permanent departure.')
edit(5,'The economic implication','Household location brings these decisions together. Earnings, available housing, family ties, amenities and the practical cost of reaching work or services all affect where a home is useful.[^26] Travel to an outside school could make remaining near ranch land possible while reducing the village’s own service role. The histories identify some connections; they do not reveal the weight each household placed on them.')
edit(5,'## The Los Lunas comparison','<!-- FIGURE: regional-households -->',end='## What can be counted later')
edit(5,'Modern census blocks','A fixed study window around the settlement produces overlapping population-allocation ranges: zero to seventeen in 2010 and five to twenty-seven in 2020.[^24] Some census blocks cross its boundary, so their residents cannot all be placed inside or outside it. The zero is a lower allocation bound, not a claim that nobody lived there. These ranges cannot establish village growth, and the window cannot be joined to the larger historical precinct as one population series.',end='Cuervo’s earlier contraction')
edit(5,'These findings connect the institutions',end='The next chapter follows')
NOTES[5][16]=NOTES[5][16].split(' Identification with')[0]
NOTES[5][25]=NOTES[4][21]
NOTES[5][26]='Edward L. Glaeser and Joshua D. Gottlieb, “The Wealth of Cities: Agglomeration Economies and Spatial Equilibrium in the United States,” NBER Working Paper 14806 (2009), [paper record](https://www.nber.org/papers/w14806). The spatial-equilibrium framework considers earnings, housing prices and amenities together. Here it organizes questions about household location; it supplies neither estimated preferences nor a fitted equilibrium for Cuervo.'

# Chapter 6: retain distinct dates and practical journeys, shorten tutorials.
edit(6,'Distance therefore needs','The timetable translates distance into usable time. A shorter ride that requires an overnight stay may cost more in time and lodging than a longer journey with a same-day return. The advertised schedule establishes that difference without counting actual trips or purchases.',end='Automobile travel offered')
edit(6,'A larger assortment could','A larger assortment and several errands could make a longer trip worthwhile. Better connections could also help Cuervo traders replenish goods and reach customers. The same reduction in travel cost enlarged the alternatives available to both merchant and customer; actual spending would determine who gained.',end='The retail census fixes')
edit(6,'A business serving motorists','A roadside business could draw customers from passing traffic even as nearby residence declined. Rittenhouse’s entries show why the range of services mattered: travelers could attend to several needs at one stop.',end='Rittenhouse’s recommendations')
edit(6,'These were different interventions','Paving and repairs improved an existing approach; realignment changed which premises stood beside it.')
edit(6,'For a business, the exact','The old gas-station frontage makes the distinction concrete. A local road could remain usable after through traffic moved, leaving a business dependent on deliberate visits instead of drivers passing its entrance. Access and exposure were different advantages.')
edit(6,'That persistence is relevant')
edit(6,'Livestock shipping did not','Passenger stops and freight service were separate functions. Loading livestock required equipment, facilities and arrangements with the freight carrier; a passenger timetable could not establish whether those were available.')
edit(6,'The directory’s blank','Southern Pacific’s restrictions therefore leave Rock Island’s local service unresolved. The siding’s presence alone does not establish a usable cattle-loading facility.')
edit(6,'Cuervo’s own revenue','In 1974, Cuervo retained a separate railway accounting identity, with no agent listed and billing assigned to Tucumcari. Santa Rosa, Montoya and Newkirk shared that arrangement. The record documents administration after Cuervo’s passenger stops had disappeared; it does not establish whether cattle were still being loaded there.[^17][^18]',end='The 1950 census had recorded')
edit(6,'A 1947 newspaper page','The 1947 feed-dealer listing discussed in Chapter 3 places Bond & Wiest in a system combining a Clovis mill, rail access and truck delivery.[^20] A local dealer could participate in distribution while manufacture and some transport work occurred elsewhere. The page does not identify deliveries to particular ranches or show whether they displaced the Cuervo merchant.\n\nLower delivery costs could let a ranch buy farther afield, while a dealer retained ordering, credit or small urgent sales. That is a possible adjustment in the work performed locally, not evidence that every outside delivery removed a local sale. The documented finding is that several supply channels were available before Cuervo’s passenger stop disappeared.',end='## Passing traffic')
edit(6,'A controlled-access highway','An interstate generally requires a driver to leave the main road at an interchange before reaching nearby premises. Signs, visibility and the return route influence that decision. A reachable business can lose incidental stops, while a station near the exit gains them. The exact frontage and ramp arrangements therefore matter to any local business account.',end='The NTSB report’s later traffic')
edit(6,'Mainline counts measure','These mainline counts, beginning decades after construction, describe passing traffic. They measure neither exit use nor the project’s immediate effect on local receipts.',end='A published visitor account')
edit(6,'A broader economy could still','Several sources of demand gave Santa Rosa potential alternatives when one weakened, though the available counts do not measure that protection or track individual firms. Its household persistence cannot establish the success of every motel or shop.',end='Santa Rosa could also')
edit(6,'The chronology now contains','The 1952 road relocation, local passenger withdrawal within 1958 and nearby 1963–1965 interstate project changed different opportunities. The Golden State was discontinued in March 1968; Cuervo’s separate billing identity remained in 1974. A later state rail plan still described an active freight corridor.[^25] Through movement and local railway work followed different histories.\n\nThe early-1950s cattle-price collapse overlapped with some of these changes.[^26] The sequence establishes several pressures on local trade, with their timing clearer than their individual contributions to closure. Better connections could also help ranch households remain while obtaining more supplies and services elsewhere. The next chapter brings those relationships together.',end=None)
start=BODIES[6].index('\n\nThrough passenger service ended later.')
BODIES[6]=BODIES[6][:start]

# Chapter 7 is rebuilt as synthesis, not a second telling of the evidence.
BODIES[7]=(ROOT/'manuscript/revision06-chapter07-body.md').read_text(encoding='utf-8').strip()
CHANGES.append({'chapter':7,'action':'Rebuilt synthesis; retained AC and Los Lunas; removed hypothetical feedback plate.'})

# Chapter 8: later evidence and one ending.
edit(8,'The later locality remained useful')
edit(8,'The purchase records a recent commitment')
edit(8,'The townsite remained a place')
edit(8,'The school provides','The school property acquired a later owner with a personal connection to the institution. After the 2010 survey, the school board reportedly accepted Flora Page’s purchase offer in September 2012. Her later obituary described schooling in Cuervo and Santa Rosa.[^5] Land transactions continued even though the final date of teaching remained uncertain.',end='The January 1983 assessor')
edit(8,'Restoration and parish affiliation')
edit(8,'## People whose lives crossed','## Connections beyond residence\n\nThe family histories in Chapter 5 show how schooling, work and home could belong to different places.[^10] A resident could obtain services elsewhere; someone who moved could retain land, relatives or a church connection. The modern census supplies bounds for a chosen study window rather than a secure village count.[^11] Continued use is better established here through the named ranch, parcels and institutional ties than through a claim about the number of people remaining.',end='## The photograph')
edit(8,'Photographs record','The photographs record materials and spatial relationships: the road embankment above adjoining land in Figure 8.2, the opening into damaged fabric in Figure 8.3.[^12] The sources supply dates and uses that the views alone cannot. A frame filled with vacant premises can also leave working land outside it. Read together, the images and records show the loss of a commercial concentration within a locality still being used.',end='<!-- FIGURE: road -->')
edit(8,'## Several outcomes','## A locality still in use\n\n“Ghost town” describes Cuervo’s visible losses more readily than its whole economy. Agricultural production, property transactions and institutional ties had requirements different from those of a daily shop or staffed school. Work on abandonment and reuse elsewhere makes the same distinction between a place’s appearance and the ways people continue to use it.[^13]\n\nA usable building remains a resource, but reopening its former business would also require staff, finance and customers with a reason to come. The ranch and church demonstrate continued usefulness on their own terms. Neither needs to reproduce the town’s earlier concentration of services to belong to its history.\n\nCuervo’s surviving buildings record a real loss: fewer places to work, trade, and obtain services. Ranching, land transactions, and ties to Santo Niño record a locality still in use. These histories belong together. The country remained productive while much of the work that had gathered a town around it was gone.',end=None)
start=BODIES[8].index('\n\n“Ghost town” describes the visible')
BODIES[8]=BODIES[8][:start]

def save_working():
    """Preserve stable note IDs while the prose and cross-references are reviewed."""
    (NEW/'chapters').mkdir(parents=True,exist_ok=True)
    for n in range(1,9):
        # Further source additions and note remapping happen in the finalizer.
        note_text='\n\n'.join(f'[^{k}]: {v}' for k,v in NOTES[n].items())
        (NEW/'chapters'/NAMES[n]).write_text(BODIES[n]+'\n\n---\n\n## Source notes\n\n'+note_text+'\n',encoding='utf-8')
    (NEW/'editorial-changes.json').write_text(json.dumps(CHANGES,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__': save_working()
