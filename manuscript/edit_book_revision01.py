"""Reproduce the first whole-book prose edit without changing chapter releases."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'manuscript/book-revision-01'
CUTS={
1:['This helps explain why the size of a town can be a poor guide','The merchant also did more than sell finished goods','This is a useful starting point, but the history adds other forms of support.','Each kind of record answers a different question.'],
2:['No single investor had to intend all the consequences.','It also establishes why the later decline must be explained with more than a photograph'],
3:['This makes the company a useful warning against judging a small town through one indicator.','Those advantages need not be permanent to be valuable.'],
4:['This is a more useful account of fragility than assuming every service shared a common minimum population.','The consequences depend on the choices available.','For the town, their effects would also differ.'],
5:['Their contribution is nevertheless substantial.','For the Cuervo narrative, the consequence is to replace a single regional success-and-failure ranking'],
6:['Cuervo\'s regional position was consequently more complicated than a small town facing one larger neighbor.','The railway had thus changed its relationship with the settlement while continuing to carry traffic through it.','That limit does not reduce the value of the administrative finding.','Cuervo\'s position in that network could therefore change without the ranches losing every outside connection.'],
7:['The early evidence changes the question from why an implausibly small town briefly existed','That distinction does not leave the book without an explanation.'],
8:[]}
REPLACE={1:[('last sale of petrol','last sale of gasoline')],3:[('It also clarifies the meaning of survival.','The later evidence also clarifies the meaning of survival.')],5:[('Population counts describe the people present within a reporting area.','Population counts describe the people enumerated within a reporting area.')]}
def words(body):
    body=re.sub(r'<!--.*?-->','',body,flags=re.S)
    body=re.sub(r'^#+.*$','',body,flags=re.M)
    return len(re.sub(r'\[\^\d+\]','',body).split())

def main():
    log=[];stats=[]
    (DEST/'chapters').mkdir(parents=True,exist_ok=True)
    for n in range(1,9):
        src=next((ROOT/'manuscript').glob(f'chapter-{n:02d}-*.md'))
        # Exclude editorial records through the required chapter-note separator.
        if '\n---\n' not in src.read_text(encoding='utf-8'):
            src=next(p for p in (ROOT/'manuscript').glob(f'chapter-{n:02d}-*.md') if '\n---\n' in p.read_text(encoding='utf-8'))
        original=src.read_text(encoding='utf-8');body,notes=original.split('\n---\n',1)
        before=words(body)
        blocks=body.split('\n\n')
        for prefix in CUTS[n]:
            matches=[b for b in blocks if b.startswith(prefix)]
            assert len(matches)==1,(n,prefix,len(matches))
            paragraph=matches[0];assert '[^' not in paragraph
            i=blocks.index(paragraph)
            log.append({'chapter':n,'action':'remove_repeated_recap','before':paragraph,'preceding':blocks[i-1],'following':blocks[i+1]})
            blocks.remove(paragraph)
        body='\n\n'.join(blocks)
        for old,new in REPLACE.get(n,[]):
            assert body.count(old)==1,(n,old)
            body=body.replace(old,new)
            log.append({'chapter':n,'action':'wording','before':old,'after':new})
        body=re.sub(r'<!--(?! FIGURE:).*?-->','',body,flags=re.S)
        body=re.sub(r'\n{3,}','\n\n',body).strip()
        text=body+'\n\n---\n'+notes
        assert re.findall(r'\[\^\d+\]',original)==re.findall(r'\[\^\d+\]',text)
        out=DEST/'chapters'/src.name;out.write_text(text,encoding='utf-8')
        stats.append({'chapter':n,'source':src.relative_to(ROOT).as_posix(),'edited':out.relative_to(ROOT).as_posix(),
            'original_body_words':before,'edited_body_words':words(body),'removed_words':before-words(body),
            'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'edited_sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
    report={'date':'2026-09-28','coverage':'Bodies of all eight chapters read; targeted continuity and repetition edit; source definitions retained. Not a fresh exhaustive source audit or external review.',
        'original_body_words':sum(r['original_body_words'] for r in stats),'edited_body_words':sum(r['edited_body_words'] for r in stats),'chapters':stats,'edits':log}
    (DEST/'edits.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='edits'},indent=2))
if __name__=='__main__':main()
