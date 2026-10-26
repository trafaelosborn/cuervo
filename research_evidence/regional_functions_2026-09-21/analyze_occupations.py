"""Summarize the manually read schedules; retain appearances and uncertainty."""
from pathlib import Path
from collections import Counter, defaultdict
import json, sys, os

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tmp/regional_python'))
os.environ['MPLCONFIGDIR'] = str(ROOT / 'tmp/matplotlib_config')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sr = json.loads((HERE/'santa_rosa_occupation_readings.json').read_text())
# Corrections from reinspection of the original page reading views.
for p in sr['pages']:
    if p['ed'] == '10-9' and p['sheet'] == 5:
        for row in p['rows']:
            if row[0] == 6:
                row[1] = ''  # Blank in source; the old wording was an editorial placeholder.
    if p['ed'] == '10-8' and p['sheet'] == 5:
        p['heads'] = sorted(set(p['heads'] + [1]))
        p.pop('needs_top_check', None)
        p['review_notes'] = 'Top rechecked: line 1 is a head, with no main occupation.'
    if p['ed'] == '10-8' and p['sheet'] == 3:
        p.pop('needs_bottom_check', None)
        p['review_notes'] = 'Bottom rechecked: line 30 is wife Flora Dimas, no main occupation.'
sr['method'] = ('First-pass visual inventory of main occupation/industry fields on all 87 '
    'population sheets of EDs 10-8, 10-9 and 10-10. One industry-only row is retained '
    'separately from occupation counts. Supplementary-only prior jobs excluded. '
    'These are schedule appearances, not deduplicated employed people, labor-force '
    'rates, private-household counts or establishments. Residence is not workplace. '
    'Head anchors are provisional; hotel groups and individual census reports need '
    'reconciliation before household statistics. Normalized readings, not diplomatic '
    'transcription. Worker class is copied but not used to infer industry or work status.')
sr['review_status'] = {
    'all_population_sheets_first_pass_read': True,
    'independent_double_transcription': False,
    'possible_duplicate_pairs': [
        {'locations': ['10-8:22:16', '10-8:74:1'],
         'reason': 'Natividad Garcia, dishwasher, Jacks Cafe; ages/status and dwelling references differ.'},
        {'locations': ['10-10:81:11', '10-10:81:16'],
         'reason': 'George M. Clayborn, nightclub musician; ages 50/30 and marital status differ.'}
    ],
    'faint_reading_pages': ['10-8:76', '10-9:78', '10-10:81'],
    'denominator': 'Main occupation appearances; not published town population.'
}
(HERE/'santa_rosa_occupation_readings.json').write_text(json.dumps(sr, indent=2)+'\n', encoding='utf-8')
manifest = {m['id']:m for m in json.loads((HERE/'census_view_manifest.json').read_text())}
entries = []
seen = set()
for p in sr['pages']:
    assert (p['ed'],p['image']) not in seen
    seen.add((p['ed'],p['image']))
    used = set()
    for row in p['rows']:
        assert len(row) == 6, (p, row)
        line, occupation, industry, sector, worker, note = row
        assert 1 <= line <= 30 and line not in used
        assert line not in p['nonperson_lines'], (p['ed'], p['sheet'], line)
        assert sector in sr['sector_key']
        used.add(line)
        m = manifest[f"{p['ed']}_{p['image']:04}"]
        entries.append(dict(ed=p['ed'], image=p['image'], sheet=p['sheet'], line=line,
            occupation=occupation, industry=industry, sector=sector, worker_class=worker,
            note=note, source=m['source'], source_sha256=m['source_sha256'],
            count_in_main_occupation_inventory=bool(occupation.strip())))
assert len(seen) == 87
main = [r for r in entries if r['count_in_main_occupation_inventory']]
extra = [r for r in entries if not r['count_in_main_occupation_inventory']]
scount = Counter(r['sector'] for r in main)
cuervo = json.loads((ROOT/'research_evidence/deep_dive_2026-09-17/cuervo_1950_occupation_readings.json').read_text())
crosswalk = {'Ranching':'AG','Retail':'RETAIL','Construction':'BUILD',
    'Government inspection':'GOV','Education / instruction':'EDU','Railroad':'RAIL',
    'Postal':'GOV','Bookkeeping':'OTHER','Fuel service':'AUTO','Food / drink':'FOOD',
    'Personal service':'PERS'}
ccount = Counter(crosswalk[r['sector']] for r in cuervo['entries'])
assert sum(ccount.values()) == 56
table = [dict(sector=k, label=label, cuervo=ccount[k], santa_rosa=scount[k],
              cuervo_share_pct=round(ccount[k]/56*100,2),
              santa_rosa_share_pct=round(scount[k]/len(main)*100,2))
         for k,label in sr['sector_key'].items()]
summary = {
    'method': sr['method'],
    'main_occupation_appearances': {'Cuervo_ED_10_6':56, 'Santa_Rosa_EDs_10_8_9_10':len(main)},
    'santa_rosa_total_job_field_rows': len(entries),
    'santa_rosa_industry_only_rows': extra,
    'santa_rosa_by_ed': {ed:dict(Counter(r['sector'] for r in main if r['ed']==ed))
                         for ed in ['10-8','10-9','10-10']},
    'sectors': table, 'cuervo_crosswalk': crosswalk,
    'santa_rosa_beauty_entries': [r for r in main if 'beaut' in (r['occupation']+' '+r['industry']).lower()],
    'santa_rosa_ambiguity_flags': [r for r in main if any(w in r['note'].lower()
        for w in ['uncertain','inferred','provisional','faint','unresolved'])],
    'unresolved_population_denominators': {'published_1950_Santa_Rosa':2199,
         'ED_cover_field_counts_sum':2184, 'ED_cover_Washington_counts_sum':2205},
    'limitations': [
        'Cuervo is precinct/ED geography including ranches; Santa Rosa is three municipal EDs.',
        'Main job entries may describe absent workers or people seeking work.',
        'Possible duplicate appearances retained; no unique-worker or employment-rate estimate.',
        'Broad analytical sectors use industry, with uncertain or spouse-inferred cases flagged.',
        'Blank occupation fields are not evidence of unemployment or absence of an enterprise.',
        'Unpaid family labor is included when an occupation is recorded; omissions remain possible.',
        'A single year cannot date structural change or isolate construction-cycle effects.'
    ]}
(HERE/'occupation_entries_flat.json').write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
(HERE/'occupation_comparison.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')

# Compare shares of the inventory, not incompatible population denominators.
groups = [('AG','Agriculture / ranching'),('RAIL','Railroad'),
          (('AUTO','FOOD','LODG'),'Motor, food and lodging'),
          (('GOV','EDU'),'Government and education'),
          ('RETAIL','Other retail / wholesale'),('BUILD','Construction / trades'),
          (('UTIL','PERS','PRO','OTHER'),'Other services / unresolved')]
def count_group(counter,key):
    return sum(counter[k] for k in key) if isinstance(key,tuple) else counter[key]
fig,ax=plt.subplots(figsize=(11,6.6),layout='constrained')
ys=list(range(len(groups)))
cv=[count_group(ccount,k)/56*100 for k,_ in groups]
sv=[count_group(scount,k)/len(main)*100 for k,_ in groups]
ax.barh([y-.18 for y in ys],cv,height=.33,color='#aa5935',label='Cuervo precinct: 56 entries')
ax.barh([y+.18 for y in ys],sv,height=.33,color='#246b79',label=f'Santa Rosa town: {len(main)} entries')
for y,v,n in zip(ys,cv,[count_group(ccount,k) for k,_ in groups]):
    ax.text(v+.5,y-.18,f'{v:.1f}% ({n})',va='center',fontsize=9)
for y,v,n in zip(ys,sv,[count_group(scount,k) for k,_ in groups]):
    ax.text(v+.5,y+.18,f'{v:.1f}% ({n})',va='center',fontsize=9)
ax.set_yticks(ys,[label for _,label in groups]);ax.invert_yaxis();ax.set_xlim(0,60)
ax.set_xlabel('Share of recorded main occupation appearances (%)')
fig.suptitle('1950: contrasting work recorded at residents\' homes',fontweight='bold',fontsize=15)
ax.spines[['top','right','left']].set_visible(False);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
ax.legend(loc='lower right',frameon=False)
fig.get_layout_engine().set(rect=(0,.105,1,.94))
fig.text(.018,.02,'Different geography: rural precinct versus municipal EDs. First-pass readings; possible duplicates retained.\n'
         'Includes recorded jobs of some absent or job-seeking people. Residence is not workplace.\n'
         'Source: NARA 1950 schedules, ED 10-6 and EDs 10-8, 10-9, 10-10; auditable sheet/line inventory.',fontsize=9,color='#444')
fig.savefig(HERE/'occupation_comparison.png',dpi=180)
people=json.loads((ROOT/'research_evidence/rebound_1940_1950_2026-09-19/people_name_age_readings.json').read_text())
lookup={(int(r['sheet']),r['line']):r for r in people if r['year']==1950}
housejobs=defaultdict(list)
for r in cuervo['entries']:
    person=lookup[(r['sheet'],r['line'])]
    housejobs[person['household']].append({**r,'name':person['given_read']+' '+person['surname_read']})
mixed={h:rows for h,rows in housejobs.items() if len({r['sector'] for r in rows})>1}
(HERE/'cuervo_mixed_job_group_leads.json').write_text(json.dumps(mixed,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sectors':table,'main':len(main),'industry_only':extra,'beauty':summary['santa_rosa_beauty_entries'],
                  'mixed_cuervo':{h:[(r['name'],r['occupation_normalized']) for r in rs] for h,rs in mixed.items()}},indent=2))
