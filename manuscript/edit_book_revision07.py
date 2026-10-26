"""Bounded editorial repairs; Revision 6 stays unchanged."""
from pathlib import Path
import json, re, shutil, hashlib
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'manuscript/book-revision-06'
NEW=ROOT/'manuscript/book-revision-07'
(NEW/'chapters').mkdir(parents=True,exist_ok=True)
texts={n:next((OLD/'chapters').glob(f'chapter-{n:02d}-*.md')).read_text(encoding='utf-8') for n in range(1,9)}
changes=[]
def para(n,start,replacement=''):
    blocks=texts[n].split('\n\n')
    ids=[i for i,b in enumerate(blocks) if b.startswith(start)]
    assert len(ids)==1,(n,start,ids)
    i=ids[0];changes.append({'chapter':n,'before':blocks[i],'after':replacement})
    blocks[i:i+1]=[replacement] if replacement else []
    texts[n]='\n\n'.join(blocks)

para(2,'Feed and handling earned income','Feed and handling earned income from animals whose journey began elsewhere. Cuervo supplied something the passing traffic needed.')
texts[2]=texts[2].replace(' Cuervo supplied feed and rest to cattle passing through from elsewhere.','')
para(3,'Credit also changes the interpretation','Credit affected customers’ choices as well as their access to supplies. An outstanding account, an expected advance or a livestock arrangement could influence where they bought goods. Continuing relationships helped organize the market alongside posted prices.')
para(3,'Credit also distributed power.','Those relationships also distributed power. Their value to customers depended on the attached obligations and access to alternatives. Evidence from the wider Bond network reveals how they could be used.')
para(3,'Handling without a separate fee benefited')
para(3,'The farm totals do not count households','Seasonal labor returns are also imperfectly comparable, as the source note explains.[^24]')
para(4,'An offering can depend on a minimum','A service can depend on one qualified worker. Sanchez’s offer was an attempt to restore instruction for pupils who remained.')
para(4,'The group had inspected the premises','The inspection turned local concern into recommendations for the board and teachers. The report records that organized effort; it leaves the individual repairs unconfirmed.')
para(4,'These were announced visits,','The announced visits offered a specific form of preventive care across several communities. A traveling worker could use each school as a venue and reach families without maintaining a full-time practice at every stop.')
para(4,'A school building, visiting worker')
para(4,'Her proposed county paper would carry','Her proposed county paper would carry smaller communities’ news and advertisements from a larger publishing base. Cuervo could remain a subject and market for journalism while losing the work of producing an independently supported paper.')
para(4,'Continued coverage in a county paper')
texts[4]=texts[4].replace('Financial withdrawal, publication location and the final issue are distinct questions.','Financial withdrawal, publication location and the final issue are distinct questions. Subsequent coverage in the proposed county paper has not been verified here.')
para(4,'In April, M. D. Harrison advertised','In April, M. D. Harrison advertised the Cuervo Garage & Blacksmith Shop at the old Ozark Trail Garage building. Fuel and oil sales, engine work and blacksmithing gave the operation several possible sources of income.')
para(4,'Combining sales and repairs at the advertised','Combining these tasks could spread the cost of premises and equipment across different kinds of work. The reopening shows that an interruption could be reversed.')
para(4,'The garage reopening establishes recovery')
texts[4]=texts[4].replace('The cause of the earlier closure and duration of renewed operation remain unknown.','The cause of the earlier closure and duration of renewed operation remain unknown. The advertisement supplies neither receipts by activity nor measured savings from shared premises or equipment.')
para(4,'The proposal cannot be turned into','Lewis’s departure did not end all livery provision: Emmor Taylor was still advertising a livery and feed barn in September 1911. One operator’s exit and the disappearance of a service were different events.')
para(6,'The NTSB report’s later traffic table','The NTSB report’s later traffic table records eastbound and westbound I-40 volumes near the accident site for 1993 through 2001. Although its heading names the Cuervo interchange, these are mainline counts. They measure passing traffic decades after construction, rather than exit use or the project’s immediate effect on local receipts.')
para(6,'These mainline counts, beginning')
para(6,'Rock Island’s own Station Book provides','Rock Island’s own Station Book, issued on December 15, 1974, retained Cuervo as a separately identified place. An asterisk marked it as having no agent; the entry supplied car-accounting, location and revenue identifiers. Billing was assigned to Tucumcari.[^17]')
para(6,'In 1974, Cuervo retained','Santa Rosa, Montoya and Newkirk shared that billing arrangement. Cuervo’s railway accounting identity survived the disappearance of its passenger stops, although the listing does not establish whether cattle were still being loaded there.[^17][^18]')
para(7,'The explanations can be ranked.','Cuervo’s decline was a loss of locally concentrated trade and services within a continuing regional economy. Ranch production endured, while the arrangements that brought customers, workers and institutional support to the village changed at different times. Continued use of the country did not ensure continued employment and services in the town.\n\nThe evidence supports different degrees of confidence. Relocation, staffing interruptions, Hicks’s withdrawal, road changes, passenger stops and billing assignments are documented. Their separate histories establish contraction without a single interstate turning point. Feedback and the costs of reopening help explain how losses might persist, but their local size and sequence remain less certain.')
para(8,'The ranch outside Cuervo was a base','The operation’s combined acreage and herd figures therefore cannot be assigned entirely to the village or historical precinct.')
texts[8]=texts[8].replace('December 6-7','December 6–7')
marker='<!-- FIGURE: trade-notices -->'
texts[2]=texts[2].replace(marker+'\n\n','').replace('The geography was correspondingly varied.',marker+'\n\nThe geography was correspondingly varied.')
photo='<!-- PHOTO: entrances -->'
texts[2]=texts[2].replace(photo+'\n\n','').replace('These services also complicate',photo+'\n\nThese services also complicate')
for n,s in texts.items():
    name=next((OLD/'chapters').glob(f'chapter-{n:02d}-*.md')).name
    (NEW/'chapters'/name).write_text(s,encoding='utf-8')
shutil.copy2(OLD/'bibliography.md',NEW/'bibliography.md')
(NEW/'editorial-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
protected={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in list((OLD/'chapters').glob('*.md'))+[ROOT/'output/pdf/cuervo-complete-reading-proof-revision-06.pdf']}
(NEW/'revision06-integrity.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
print(f'Applied {len(changes)} bounded paragraph edits; retained all note identities.')
