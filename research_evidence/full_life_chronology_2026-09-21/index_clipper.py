"""Audit and index downloaded OCR. Hits are leads, not verified historical events."""
from pathlib import Path
import collections, hashlib, json, re
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'sources/02_newspapers/cuervo_clipper/repository_ocr_2026-09-21'
OUT=Path(__file__).resolve().parent
pages=json.loads((BASE/'ocr_page_index.json').read_text(encoding='utf-8'))
old=json.loads((ROOT/'sources/02_newspapers/cuervo_clipper/full_scan_audit_2026-09-17.json').read_text(encoding='utf-8'))['issues']
old_by_date={x['issue_date']:x for x in old}
by_date=collections.defaultdict(lambda:collections.defaultdict(list))
for p in pages: by_date[p['issue_date']][p['parent_id']].append(p)
canonical,duplicates,coverage=[],[],[]
for date,parents in sorted(by_date.items()):
    selected=min(parents,key=int)
    chosen=parents[selected]
    def combined(rows): return '\n'.join((ROOT/x['text_file']).read_text(encoding='utf-8') for x in rows)
    for ident,rows in parents.items():
        if ident != selected:
            duplicates.append({'issue_date':date,'retained_parent':selected,'duplicate_parent':ident,
                               'ocr_identical':combined(rows)==combined(chosen),'pages':len(rows)})
    nonempty=[x for x in chosen if x['characters']]
    for n,x in enumerate(nonempty,1):
        x=dict(x,content_page_ordinal=n,local_issue_file=old_by_date.get(date,{}).get('file'),
               local_pdf_page_candidate=n+1 if date in old_by_date else None,
               local_mapping_note='Ordinal candidate only; visually verify before citation.')
        canonical.append(x)
    target=BASE/'issues'/f'{date}.txt'; target.parent.mkdir(exist_ok=True)
    text='\n\n'.join(f"[ISSUE {date}; CONTENT PAGE {i+1}; REPOSITORY PAGE ID {x['page_id']}; SCAN ORDINAL {x['scan_ordinal']}]\n"+(ROOT/x['text_file']).read_text(encoding='utf-8') for i,x in enumerate(nonempty))
    target.write_text(text,encoding='utf-8')
    coverage.append({'issue_date':date,'canonical_parent':selected,'repository_child_objects':len(chosen),
                     'nonempty_ocr_pages':len(nonempty),'local_pdf_scan_pages':old_by_date.get(date,{}).get('scan_pages_after_cover',0),
                     'issue_text':str(target.relative_to(ROOT))})
(OUT/'canonical_ocr_pages.json').write_text(json.dumps(canonical,indent=2),encoding='utf-8')
patterns={
 'business_change':r'clos(?:ed|ing)|re.?open|chang.{0,12}hand|sold.{0,30}(?:store|hotel|business)|purchas.{0,35}(?:store|hotel|business)|new (?:hotel|store|garage)|mov.{0,20}(?:plant|office)',
 'school':r'school.{0,15}(?:build|house|bond|enroll|teach|clos)|new.{0,15}school',
 'transport_freight':r'depot|station agent|railroad|railway|car.?load|stock.?yard|cattle.{0,40}ship|ship.{0,40}cattle|garage|telephone',
 'medical_church_post':r'doctor|physician|church|preach|post.?office|postmaster|mail (?:line|route)',
 'land_agriculture':r'town.?site|homestead|(?:sheep|cattle|wool).{0,35}(?:sold|sale|ship)|droug?ht|dry weather|crop fail|abandon',
 'newspaper':r'Clipper.{0,35}(?:sold|purchas|mov|plant|clos)|(?:sold|purchas).{0,35}Clipper|financial.{0,20}(?:connect|loss)|Public Voice|Gerhardt|Hicks',
 'trade_geography':r'long distance|trade at home|buy at home|mail.?order|trading.{0,30}(?:Santa Rosa|Tucumcari)|(?:Santa Rosa|Tucumcari).{0,30}trad'
}
hits=[]
for p in canonical:
    raw=(ROOT/p['text_file']).read_text(encoding='utf-8')
    flat=' '.join(raw.split())
    for category,pattern in patterns.items():
        for m in re.finditer(pattern,flat,re.I):
            hits.append({'issue_date':p['issue_date'],'content_page_ordinal':p['content_page_ordinal'],
                         'page_id':p['page_id'],'category':category,'match':m.group(),
                         'snippet':flat[max(0,m.start()-200):m.end()+300],
                         'scan_url':p['scan_url'],'review_status':'unverified_ocr_lead'})
(OUT/'ocr_search_leads.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in hits),encoding='utf-8')
summary={'raw_parent_records':len({x['parent_id'] for x in pages}),'distinct_issue_dates':len(by_date),
         'raw_page_objects':len(pages),'raw_empty_transcripts':sum(not x['characters'] for x in pages),
         'duplicate_issue_records':duplicates,'canonical_nonempty_pages':len(canonical),
         'coverage_differences':[x for x in coverage if x['nonempty_ocr_pages']!=x['local_pdf_scan_pages']],
         'issue_counts_by_year':dict(sorted(collections.Counter(x['issue_date'][:4] for x in coverage).items())),
         'search_leads_by_category':dict(collections.Counter(x['category'] for x in hits)),
         'limits':'Repository OCR retrieved, not newly generated or exhaustively corrected. Text is a search aid. The run has calendar gaps. Scan-page mapping must be verified visually.'}
(OUT/'ocr_coverage_audit.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(OUT/'issue_coverage.json').write_text(json.dumps(coverage,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
