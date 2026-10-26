from pathlib import Path
from collections import Counter
import json

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
old = json.loads((ROOT / 'research_evidence/census_full_history_2026-09-18/person_age_observations.json').read_text(encoding='utf-8-sig'))
people = {year: [dict(r) for r in old if r['year'] == year] for year in (1940,1950)}
for fix in json.loads((BASE/'age_reading_corrections.json').read_text(encoding='utf-8')):
    row = next(r for r in people[fix['year']] if str(r['sheet'])==fix['sheet'] and r['line']==fix['line'])
    assert row['age_completed_years']==fix['previous_age']
    row['previous_age_completed_years']=row['age_completed_years']
    row['age_completed_years']=fix['revised_age']
    row['age_status']='rechecked-2026-09-19'
groups = []
for line in (BASE / 'household_readings.txt').read_text(encoding='utf-8').splitlines():
    if not line.strip() or line.startswith('#'): continue
    year, loc, surname, members = line.split(';')
    sheet, row = loc.split(':')
    groups.append({'year':int(year), 'sheet':sheet, 'line':int(row), 'default_surname':surname, 'names':members.split('|')})
households = []
for year, rows in people.items():
    k = 0
    for group in [g for g in groups if g['year']==year]:
        assert str(rows[k]['sheet']) == group['sheet'] and rows[k]['line']==group['line'], (group, rows[k])
        hh_id = f"{year}-{group['sheet']}-{group['line']}"
        members = []
        for name in group['names']:
            row = rows[k]
            surname, given = name.split(',',1) if ',' in name else (group['default_surname'],name)
            row.update(id=f"{year}-{row['sheet']}-{row['line']}", household=hh_id, surname_read=surname, given_read=given, name_uncertain=('?' in name or '?' in surname))
            members.append(row['id'])
            k += 1
        hhrows = rows[k-len(members):k]
        households.append({'id':hh_id,'year':year,'head_name_read':group['names'][0]+' '+group['default_surname'], 'members':members,'count':len(members),'under10_known':sum(r['age_completed_years'] is not None and r['age_completed_years']<10 for r in hhrows),'under18_known':sum(r['age_completed_years'] is not None and r['age_completed_years']<18 for r in hhrows)})
    assert k == len(rows), (year,k,len(rows))
allrows = [r for rows in people.values() for r in rows]
for name,data in [('people_name_age_readings.json',allrows), ('households.json',households)]:
    (BASE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False), encoding='utf-8')
for year in people:
    hh = [h for h in households if h['year']==year]
    print(year, 'people',len(people[year]),'households',len(hh),'mean size',len(people[year])/len(hh),'sizes',dict(sorted(Counter(h['count'] for h in hh).items())))
