"""Apply the recorded voice and compression edit without altering revision 1."""
from pathlib import Path
import hashlib, json, re
from edit_book_revision01 import words

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'manuscript/book-revision-01'
REV=ROOT/'manuscript/book-revision-02'

def apply():
    edits=json.loads((REV/'editorial-edits.json').read_text(encoding='utf-8'))
    records=[]
    (REV/'chapters').mkdir(parents=True,exist_ok=True)
    for n in range(1,9):
        src=next((OLD/'chapters').glob(f'chapter-{n:02d}-*.md'))
        original=src.read_text(encoding='utf-8')
        body,notes=original.split('\n---\n',1)
        blocks=body.split('\n\n')
        changes=[]
        for index,value in edits[str(n)].items():
            i=int(index)
            before=blocks[i]
            assert not before.startswith('<!-- FIGURE:')
            blocks[i]=value
            changes.append({'block':i,'before':before,'after':value})
        # Move two existing plates closer to their data to avoid short overflow pages.
        figure_moves=[]
        for source,target in {2:[(32,29)],5:[(102,99)]}.get(n,[]):
            marker=blocks[source]
            assert marker.startswith('<!-- FIGURE:')
            blocks[source]=''
            blocks[target]+='\n\n'+marker
            figure_moves.append({'from_original_block':source,'after_original_block':target,'marker':marker})
        revised='\n\n'.join(b for b in blocks if b.strip())+'\n---\n'+notes
        newbody=revised.split('\n---\n',1)[0]
        assert re.findall(r'<!-- FIGURE:.*?-->',body)==re.findall(r'<!-- FIGURE:.*?-->',newbody)
        assert set(re.findall(r'\[\^(\d+)\]',newbody))==set(re.findall(r'^\[\^(\d+)\]:',notes,re.M)),n
        target=REV/'chapters'/src.name
        target.write_text(revised,encoding='utf-8')
        records.append({'chapter':n,'source':src.relative_to(ROOT).as_posix(),'output':target.relative_to(ROOT).as_posix(),
          'before_words':words(body),'after_words':words(newbody),'before_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
          'after_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'notes_unchanged':True,'figure_moves':figure_moves,'changes':changes})
    (REV/'edits.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'before_words':sum(r['before_words'] for r in records),'after_words':sum(r['after_words'] for r in records),
      'edited_blocks':sum(len(r['changes']) for r in records),'chapters':[{'n':r['chapter'],'words':r['after_words']} for r in records]},indent=2))

if __name__=='__main__':apply()
