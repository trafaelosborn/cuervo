"""Apply the first editor's pass, preserving Revision 4 and its research trails."""
from pathlib import Path
import re, json, hashlib
from revision05_notes import NOTES

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT/'manuscript/book-revision-04'
NEW = ROOT/'manuscript/book-revision-05'
CHANGES = []

def typography(text):
    # Leave link targets, HTML attributes, and figure/photo instructions unchanged.
    parts = re.split(r'(\]\([^\n]*?\)|<!--.*?-->|<[^>]+>)', text, flags=re.S)
    for i in range(0, len(parts), 2):
        s=parts[i].replace("'", '’')
        s=re.sub(r'"([^"\n]+)"', r'“\1”', s)
        s=re.sub(r'\b((?:18|19|20)\d{2})-((?:18|19|20)\d{2})\b', r'\1–\2', s)
        parts[i]=s
    return ''.join(parts)

def replace(body, old, new, n, category='cadence'):
    assert body.count(old)==1, (n, old, body.count(old))
    CHANGES.append(dict(chapter=n,category=category,before=old,after=new))
    return body.replace(old,new)

EDITS={
1:[
('That July, Rancho Armendariz','In July 2026, Rancho Armendariz','factual clarity'),
("about two-thirds of its year-round housing reportedly had air conditioning, yet its population", "about two-thirds of Santa Rosa's year-round housing reportedly had air conditioning, yet the town's population",'factual clarity'),
("The card documents an assessed building and its condition. It does not date the last sale of gasoline or explain why the business stopped.","The assessment records the property's condition, leaving its trading history open."),
],
2:[
('Grubbs dated the Cabra store to the fall of 1899.','Grubbs traced the Cabra store to 1899.','source discrepancy'),
('His reconstruction establishes the business there before its move to the new rail connection.','The business was already operating there before its move to the new rail connection.'),
('The animals were passing through; the report does not identify them as local production. Cuervo nevertheless performed work for their journey.','Cuervo supplied feed and rest to cattle passing through from elsewhere.'),
('The newspaper reports do not measure the resulting purchases. They do establish a reason for people to gather that was independent of the arrival of a particular freight train.','Schooling gave families a reason to gather in town throughout the term.'),
("The two services were related, but one record of a buyer's arrival does not tell the whole history of shipments. Each part needs to be followed on its own terms.","Passenger and freight services could support different stages of the same trade."),
('Those findings belong to the next chapter, but they establish a necessary boundary here: the railway opportunity did not collapse into immediate commercial failure.','The railway opportunity supported a business that survived its early setbacks.'),
],
3:[
(' His figures describe an early rise, a setback and a partial recovery. They do not describe an uninterrupted collapse after the first difficulty.',' His figures describe an early rise, a setback and a partial recovery.'),
('The reported earnings establish recovery after the early setback. Grubbs reconstructed them from older accounts, retaining historical categories and rounding. On that basis, Bond & Wiest continued to earn money as the balance of its business changed.','Bond & Wiest recovered from the early setback and continued to earn money as the balance of its business changed. Grubbs reconstructed those earnings from older accounts, retaining their historical categories and rounding.'),
('The Encino arrangement establishes the earlier advantage; it does not date its disappearance.','The Encino arrangement shows why combining shipments had once been useful.'),
('The figures establish broad ownership, but do not show a rising rate across those years or reveal the destinations of the trucks.','Truck ownership was already common in both years.'),
('The equipment figures establish that capacity; its local effects depend on the journeys and commercial arrangements producers chose.','The local effects depended on which journeys and commercial arrangements producers chose.'),
('That was 45.8% of the 1935 farm count. The observation does not identify where they worked or what they did, but it establishes a substantial overlap between operating a farm and obtaining earnings elsewhere.','That was 45.8% of the 851 farms counted in 1935. The farm count had risen from 596 in 1930 before its later decline; the long-term endpoints conceal that intervening rise. Off-farm earnings were already common among operators, although their workplaces and occupations are unspecified.','denominator clarity'),
('The evidence establishes dispersed production and trade, with several functions brought together in a local merchant. It leaves the share of ranch income spent in Cuervo unmeasured.','The local merchant brought several functions together within a dispersed economy of production and trade.'),
],
4:[
('Filling a role could determine whether provision continued. The school and postal records establish that requirement directly, while leaving the reasons for the vacancies open.','Both services depended on someone being available to fill a particular role.'),
('The matching name suggests a changed practice base while care continued through travel. The reports do not date the move or explain it. They do identify a form of access different from maintaining a practitioner in Cuervo: the doctor could come from another place to perform a particular service.','The matching name suggests a changed practice base while care continued through travel. A doctor based elsewhere could still visit Cuervo, though the reports leave the move’s date and reason open.'),
("The advertisements record competition for readers' custom. Actual purchases remain unmeasured, but the rival offers establish a commercial audience extending across town boundaries.","The rival advertisements sought customers across town boundaries."),
('This is where service history meets demographic history. The school reports of 1910 and 1912 show households coming into Cuervo for education. Later accounts show education linking local people with other places. Neither observation licenses a simple reversal in which every lost service automatically removes its former users from the population.\n\nService history leads to a demographic question: who remained, and how did their lives connect the available institutions? The next chapter follows household composition, work and selected residential histories. It separates the people counted at Cuervo from the destinations serving them.','Schooling drew families into Cuervo in 1910 and 1912. Later accounts link local people to schools elsewhere. Changes in services and residence could follow different schedules. The next chapter follows households, work and residential histories to distinguish the people living at Cuervo from the places serving them.'),
],
5:[
('These selected histories establish distinct routes through the region: schooling, ranch work and later homes had different destinations and dates. They illustrate the available arrangements without measuring their prevalence.','These selected histories follow different routes through the region. Schooling, ranch work and later homes had different destinations and dates.'),
(' The arithmetic does not identify the destinations of people missing from the county\'s later count.',''),
],
6:[
('The timetable establishes a practical advantage for the longer trip: useful daytime hours at the destination. It describes offered rail journeys, leaving passengers, purchases and alternative road travel outside its coverage.','The longer rail trip offered a practical advantage: useful daytime hours at the destination.'),
('The notices establish changing provision; the guide records one later view. Together they leave little support for assuming a large, stable tourist economy that remained intact until interstate construction.','The notices and guide show services changing over time, well before interstate construction.'),
('The siding continued to appear. Its listed capacity was 103 cars in the late-1950s operating tables. A 1967 timetable still identified a Cuervo siding, with a capacity of 92. Those figures should not be read as proof that the track was shortened. Changes in car length or the basis of a capacity figure could alter the count. They do establish that a siding remained in the operating description.','The siding continued to appear. Its listed capacity was 103 cars in the October 1958 and September 1959 operating tables, and 92 in a 1967 timetable. Changes in car length or capacity conventions could alter that count without a change in track length.[^13]','source locator'),
("Its discontinuance came in 1968, documented in the contemporary regulatory discussion.","The April 25, 1968 Congressional Record reported that it had been discontinued that March.",'source precision'),
('The evidence establishes several supply channels before Cuervo\'s passenger stop disappeared. It leaves the division of local purchases among those channels unmeasured.','Several supply channels were available before Cuervo\'s passenger stop disappeared.'),
],
7:[
('Those observations establish an operating business with more than a roadside clientele. They also place its early commercial success before the designation of Route 66.','Its early commercial success preceded the designation of Route 66.'),
('The accounts establish joint operation without measuring its savings.','The company operated these activities together.'),
('The agricultural series establishes changing conditions for producers. County inventories and state prices have different geographic coverage from the village, so they frame the pressures on local trade without measuring individual closures or ranch margins.','County inventories and state prices describe the wider conditions facing local producers and traders.'),
('The evidence identifies particular outside connections; it does not measure the share of ranch income once retained locally or its later change.','The documented outside connections show how producers could obtain support beyond the town.'),
('Retail evidence establishes Santa Rosa\'s importance without identifying every customer.','Santa Rosa served a wider retail market.'),
('They give the region a more accurate shape than a single relationship in which the larger neighbor absorbed every activity.','Different services drew the two towns into different regional relationships.'),
('These overlapping conditions set the scale of the explanation. The evidence identifies changes in access, agricultural returns and institutional support. It establishes some decisions directly, while leaving their respective shares of the later contraction unmeasured.','Access, agricultural returns and institutional support changed on overlapping schedules. Together they altered the conditions for maintaining services at Cuervo.'),
('Relocation is best described at the scale at which it is observed: a publication, a billing responsibility or a named household. The regional history contains those movements without establishing that Cuervo transferred to one destination as a unit.','Relocation took several forms: a publication, a billing responsibility or a named household could move to a different destination.'),
],
8:[
("The announcement establishes that activity without measuring its profit or Cuervo employment. Trade associated with the locality continued beyond the old storefronts.","Trade associated with the locality continued beyond the old storefronts."),
('Boundaries and transactions still required decisions. The continuing property record establishes that use of the townsite without implying a general redevelopment program.','The townsite remained a place where owners negotiated boundaries and exchanged land.'),
('A December 2025 parish bulletin supplies a later observation.','A parish bulletin dated December 21, 2025 supplies a later observation.','date clarity'),
('The entry documents money reported under Cuervo\'s name. It does not identify where the event occurred or how often services were held.','The entry leaves the venue and frequency of services unspecified.'),
]}

def main():
    (NEW/'chapters').mkdir(parents=True,exist_ok=True)
    for n in range(1,9):
        src=next((OLD/'chapters').glob(f'chapter-{n:02d}-*.md'))
        body,oldnotes=src.read_text(encoding='utf-8').split('\n---\n',1)
        for edit in EDITS[n]: body=replace(body,*edit[:2],n,*edit[2:])
        notes=NOTES[n].strip()
        olddefs=re.findall(r'^\[\^(\d+)\]:',oldnotes,re.M)
        defs=re.findall(r'^\[\^(\d+)\]:',notes,re.M)
        assert olddefs==defs,(n,olddefs,defs)
        assert set(re.findall(r'\[\^(\d+)\]',body))==set(defs)
        result=typography(body)+'\n---\n\n## Source notes\n\n'+typography(notes)+'\n'
        assert not re.search(r'B:/|research_evidence|Working source|source.register|prior source pass|held PDF',result)
        (NEW/'chapters'/src.name).write_text(result,encoding='utf-8')
    (NEW/'editorial-changes.json').write_text(json.dumps(CHANGES,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'body_edits':len(CHANGES),'cadence_edits':sum(x['category']=='cadence' for x in CHANGES),'notes_rewritten':sum(len(re.findall(r'^\[\^',s,re.M)) for s in NOTES.values())}))

if __name__=='__main__':main()
