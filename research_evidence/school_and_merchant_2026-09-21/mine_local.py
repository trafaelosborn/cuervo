"""Extract search leads only; visual verification is separate."""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
pages=json.loads((ROOT/'research_evidence/full_life_chronology_2026-09-21/canonical_ocr_pages.json').read_text(encoding='utf-8'))
patterns={
 'enrollment':r'enroll|enrolm|attendance|pupils|scholars',
 'school_change':r'consolidat|school.{0,40}(?:clos|open|district|transport|wagon)|(?:school bus|school truck|high school)|(?:teach|school).{0,25}(?:resign|elect|employ|appoint)',
 'merchant_end':r'(?:Bond|Wiest|Armijo|Oklahoma Hotel|Rock Island Hotel).{0,100}(?:clos|sold|purchas|retir|liquidat|bankrupt|moved)|(?:clos|sold|purchas|retir|liquidat|bankrupt).{0,100}(?:Bond|Wiest|Armijo|Oklahoma Hotel|Rock Island Hotel)'
}
leads=[]
for page in pages:
    text=' '.join((ROOT/page['text_file']).read_text(encoding='utf-8').split())
    for category,pattern in patterns.items():
        for match in re.finditer(pattern,text,re.I):
            leads.append(dict(issue_date=page['issue_date'],page=page['content_page_ordinal'],page_id=page['page_id'],
                              category=category,match=match.group(),
                              context=text[max(0,match.start()-260):match.end()+520],
                              source_file=page['local_issue_file'],pdf_page=page['local_pdf_page_candidate'],
                              review='unverified OCR lead'))
(HERE/'targeted_ocr_leads.json').write_text(json.dumps(leads,indent=2,ensure_ascii=False),encoding='utf-8')
for item in leads:
    if item['page']==1 and item['category'] in ('enrollment','merchant_end'):
        print(json.dumps(item,ensure_ascii=True))
print('TOTAL_LEADS',len(leads))
