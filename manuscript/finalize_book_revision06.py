"""Finish source notes, migrate note locators, and record the applied edit list."""
import re, json
from collections import defaultdict
from edit_book_revision06 import ROOT, OLD, NEW, BODIES, NOTES, NAMES, CHANGES, sub, edit
from edit_book_revision01 import words

# Retain the distinctive school-finance sequence at its principal institutional home.
school='The school’s expansion required finance before it required a larger building. In July 1910, the newspaper reported a vote for $4,000 in school bonds, about $140,000 in 2025 consumer purchasing power. The site was still undecided. The following April brought the reported sale of the bonds and a call for bids; construction was under way by September.[^22] Those successive commitments precede the April 1912 description of the completed two-story school.'
sub(4,'By April 1912, the paper described',school+'\n\nBy April 1912, the paper described')
NOTES[4][22]=NOTES[2][16].replace('in note 5','in Chapter 2, note 5')
edit(4,'Combining repair and other tasks','Combining sales and repairs at the advertised premises supplied several possible sources of receipts. Sharing equipment or spreading premises costs across tasks could also help, but the advertisement does not measure those savings.')
# Keep the formation chapter's explanation of the wider market, without another Smith introduction.
old2=next((OLD/'chapters').glob('chapter-02-*.md')).read_text(encoding='utf-8').split('\n---\n')[0]
keep2=[b for b in old2.split('\n\n') if b.startswith(('The same distinction applies to land.','Nor does the presence of a profitable merchant'))]
sub(2,'## The first location','\n\n'.join(keep2)+'\n\n## The first location')
edit(2,'The railway gave an established','The railway gave an established merchant a reason to move from Cabra. Capital, premises, management and customer relationships made the location usable; schooling and other services gave additional reasons to gather. Santa Rosa already performed a wider range of work, but Cuervo did not need to reproduce it to serve ranch country.\n\nThe question was how much of that country’s business Cuervo could retain. Ranching did not require every purchase, loan or shipment to pass through the village. Bond & Wiest retained a role for decades. The next chapter examines what it held, sold and financed, and how it earned its money.',end='Bond & Wiest did so')
edit(2,'Bond & Wiest did so')

# Put full-page plates at paragraph boundaries that do not strand a short tail.
def move_plate(n,key,anchor,after=False,kind='FIGURE'):
    marker=f'<!-- {kind}: {key} -->';blocks=BODIES[n].split('\n\n')
    assert blocks.count(marker)==1;blocks.remove(marker)
    matches=[i for i,b in enumerate(blocks) if b.startswith(anchor)];assert len(matches)==1,(n,key,anchor)
    blocks.insert(matches[0]+int(after),marker);BODIES[n]='\n\n'.join(blocks)
    CHANGES.append({'chapter':n,'plate':key,'placement':('after ' if after else 'before ')+anchor})
move_plate(3,'trade-connections','The 1910 newspaper reports show')
move_plate(3,'prices-and-population','The timing complicates')
move_plate(4,'school-staff-and-care','The committee examining')
move_plate(4,'school-parcel','The property’s later sale',after=True)
move_plate(4,'doctor-support','The proposal addressed reliability',after=True)
move_plate(4,'newspaper-purpose','The political explanation')
move_plate(6,'retail','The census’s definition')
move_plate(6,'station-book','Southern Pacific’s restrictions')
move_plate(6,'chronology','The early-1950s cattle-price collapse',after=True)
move_plate(7,'support','The responses also differed',after=True)
# Preserve household details as the place where occupations, earnings and residence meet.
sub(5,'A population total cannot', 'A population total cannot') if 'A population total cannot' in BODIES[5] else None

NOTES[1][3]='National Trust for Historic Preservation, [“7 Ghost Towns on Route 66”](https://savingplaces.org/guides/ghost-towns-on-route-66), Cuervo section; Jim Winnerman, [“Ghost Towns: Cuervo, New Mexico”](https://historynet.com/ghost-towns-cuervo-new-mexico/), *Wild West*, June 2022; HistoryNet web publication July 11, 2022, updated July 20, 2022. These examples illustrate the published ghost-town narrative available in September 2026. The web page identifies its magazine origin and June issue; a print page number has not been supplied.'
NOTES[3][9]=NOTES[3][9].replace(' His speculation about Tucumcari’s scouring works is not adopted as a verified shipment route.','')
NOTES[3][11]=NOTES[3][11].replace(' The proposed 1932 corporate loan was $90,000, about $2.1 million in 2025 consumer purchasing power.','')
NOTES[7][18]=NOTES[7][18].split(' Figure 7.3')[0]+' The model formalizes reciprocal effects between manufacturing location and demand under specified assumptions. School-related moves at Cuervo do not validate that manufacturing mechanism or establish a later cascade of closures.'
NOTES[7][19]=NOTES[7][19].replace('note 7 above','note 7')
NOTES[7][22]=NOTES[1][12]+' Adoption and population observations do not identify a cooling effect: the alternative population path without air conditioning is unobserved.'
NOTES[7][23]='Sylvain Leduc and Daniel J. Wilson, [“Snow Belt to Sun Belt Migration: End of an Era?”](https://www.frbsf.org/wp-content/uploads/wp2024-21.pdf), Federal Reserve Bank of San Francisco Working Paper 2024-21 (July 2024), pp. 1–2, describe the post-1960s acceleration toward the South and Southwest and regard widespread cooling as a likely contributor; their county correlations do not isolate its causal effect. Edward L. Glaeser and Kristina Tobio, [“The Rise of the Sunbelt”](https://www.nber.org/papers/w13071), NBER Working Paper 13071 (2007), pp. 2–5, weigh productivity, amenities and housing supply; their findings favor productivity before 1980 and housing supply increasingly afterward. Neither paper estimates migration between Cuervo and Santa Rosa. The household-location framework is discussed in Chapter 5, note 26.'
NOTES[7][24]='Village of Los Lunas, [*2040 Comprehensive Plan*](https://www.loslunasnm.gov/DocumentCenter/View/11100/Village-of-Los-Lunas-2040-Comprehensive-Plan), approved July 2022, pp. 4–5 (agricultural and ranching settlement and railway history), 16–18 (regional location, economy and housing), 23 (Rail Runner connection) and 36 (local employers). The travel time is the plan’s description, not a measured historical commute. Its retrospective account establishes similarities and differences in setting; later employers and transit cannot be assigned the whole cause of 1990–2020 growth. The plan’s resident occupational estimates are not treated as workplace job counts.'
NOTES[7][15]=NOTES[5][22].replace('note 20','Chapter 5, note 20')+' Santa Rosa’s household totals and institutional population are examined in Chapter 5. These municipal series do not estimate a counterfactual Cuervo path.'
NOTES[8][5]=NOTES[8][5].replace('See Chapter 4, notes 7–8 and Figure 4.2.','See Chapter 4, note 7 and Figure 4.2.')+' Chavez Funeral Home, [Flora S. Page obituary, 2023](https://www.chavezfuneralhome.com/obituaries/flora-page), records schooling in Cuervo and Santa Rosa without dates.'
NOTES[8][10]='Chavez Funeral Home family accounts cited in Chapter 5, notes 1, 17–18 and 25. These selected histories distinguish dated residence, education and work; they do not establish a general commuting or migration pattern.'
NOTES[8][12]='Taylor Osborn, Cuervo photographic collection. See the photograph credits and concordance at the end of the book. Images retain the photographed scene, with orientation corrected and no retouching. Conflicting folder and embedded dates prevent assigning exact capture dates. Visible features alone supply no historical building identity or road-construction date.'
NOTES[2][16]=NOTES[2][16].split(' The $4,000 bond equivalent')[0]+' School finance and the building sequence are treated in Chapter 4, note 22.'
# Remove obsolete source locators before migrating all remaining references.
NOTES[6][24]=NOTES[6][24].replace('notes 19–22','notes 19–21')
NOTES[7][16]=NOTES[7][16].replace('See Chapter 2, notes 15–16, and Chapter 4, notes 3 and 5.','See Chapter 4, notes 3 and 5.')
NOTES[7][6]=NOTES[7][6].replace(' The purchasing-power equivalent follows Chapter 2, note 5, and Chapter 4, note 10.','')

# Migration targets use Revision-5 identities (plus explicitly added notes).
MOVED={(1,10):(6,17),(1,12):(7,22),(2,3):(1,11),(4,8):(8,5),
       (4,19):(1,11),(4,20):(7,12),(4,21):(5,25),(5,22):(7,15),
       (7,1):(1,11),(7,4):(3,19)}
MAPS={}
for n,body in BODIES.items():
    refs=list(dict.fromkeys(int(x) for x in re.findall(r'\[\^(\d+)\]',body)))
    assert all(k in NOTES[n] for k in refs),(n,refs)
    MAPS[n]={old:new for new,old in enumerate(refs,1)}

def target(ch,num):
    while (ch,num) in MOVED: ch,num=MOVED[ch,num]
    assert num in MAPS[ch],f'Missing note target {ch}:{num}'
    return ch,MAPS[ch][num]

def number_list(s):
    vals=[]
    for a,b in re.findall(r'(\d+)(?:[–-](\d+))?',s):
        vals.extend(range(int(a),int(b)+1) if b else [int(a)])
    return vals

def compressed(nums):
    nums=sorted(set(nums)); groups=[];i=0
    while i<len(nums):
        j=i
        while j+1<len(nums) and nums[j+1]==nums[j]+1:j+=1
        if j-i>=2:groups.append(f'{nums[i]}–{nums[j]}')
        else:groups.extend(str(x) for x in nums[i:j+1])
        i=j+1
    return groups[0] if len(groups)==1 else ', '.join(groups[:-1])+' and '+groups[-1]

PAT=re.compile(r'(?:(Chapter\s+(\d+),\s+)|(chapter\s+))?(notes?)\s+(\d+(?:[–-]\d+)?(?:(?:,\s*(?:and\s+)?|\s+and\s+)\d+(?:[–-]\d+)?)*)',re.I)
def remap_refs(text,current):
    def replace(m):
        explicit,chnum,localword,word,numbers=m.groups()
        original=int(chnum) if chnum else current
        destinations=defaultdict(list)
        for old in number_list(numbers):
            ch,num=target(original,old);destinations[ch].append(num)
        chunks=[]
        for ch,nums in destinations.items():
            prefix=f'Chapter {ch}, ' if explicit or ch!=current else ('chapter ' if localword else '')
            chunks.append(prefix+('note ' if len(set(nums))==1 else 'notes ')+compressed(nums))
        return '; '.join(chunks)
    return PAT.sub(replace,text)

def main():
    (NEW/'chapters').mkdir(parents=True,exist_ok=True)
    stats=[]
    for n,body in BODIES.items():
        body=re.sub(r'\[\^(\d+)\]',lambda m:f'[^{MAPS[n][int(m[1])]}]',body)
        body=remap_refs(body,n)
        notes=[]
        for old,new in MAPS[n].items():
            value=remap_refs(NOTES[n][old],n)
            notes.append(f'[^{new}]: {value}')
        full=body+'\n\n---\n\n## Source notes\n\n'+'\n\n'.join(notes)+'\n'
        (NEW/'chapters'/NAMES[n]).write_text(full,encoding='utf-8')
        stats.append({'chapter':n,'before':words(next((OLD/'chapters').glob(f'chapter-{n:02d}-*.md')).read_text(encoding='utf-8').split('\n---\n')[0]),'after':words(body),'notes':len(notes)})
    (NEW/'note-map.json').write_text(json.dumps(MAPS,indent=2),encoding='utf-8')
    (NEW/'editorial-changes.json').write_text(json.dumps(CHANGES,ensure_ascii=False,indent=2),encoding='utf-8')
    (NEW/'edit-statistics.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
