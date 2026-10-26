"""Descriptive Santa Rosa July temperatures; not official normals or a town comparison."""
from pathlib import Path
import csv, json, statistics, math

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'sources/home_cooling_2026-09-24'
OUT = Path(__file__).parent
rows=[]
for line in (SOURCE/'santa_rosa_ghcnd.dly').read_text().splitlines():
    station,year,month,element=line[:11],int(line[11:15]),int(line[15:17]),line[17:21]
    if month != 7 or element not in ('TMAX','TMIN') or not 1931 <= year <= 1990:
        continue
    values=[]
    for day in range(31):
        field=line[21+day*8:29+day*8]
        value=int(field[:5]); quality=field[6]
        if value != -9999 and quality == ' ':
            values.append(value/10*9/5+32)
    rows.append(dict(station=station,year=year,month=month,element=element,
                     valid_days=len(values),included=len(values)>=28,
                     mean_f=statistics.mean(values) if values else None))
with (OUT/'santa_rosa_july_months.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary=[]
for start,end in [(1931,1960),(1961,1990)]:
    for element in ('TMAX','TMIN'):
        selected=[r for r in rows if start<=r['year']<=end and r['element']==element and r['included']]
        summary.append(dict(period=f'{start}-{end}',element=element,qualifying_julys=len(selected),
                            mean_f=round(statistics.mean(r['mean_f'] for r in selected),2),
                            omitted_years=[y for y in range(start,end+1) if y not in [r['year'] for r in selected]]))
result={'method':'GHCN-Daily USC00298107. July only; nonmissing TMAX/TMIN, blank quality flag; at least 28 valid days per July and element. Mean of qualifying monthly means, equal year weight. Celsius tenths converted to Fahrenheit. No homogenization, station-move adjustment, humidity estimate, or Cuervo imputation. Not official NOAA normals.', 'summaries':summary}
(OUT/'climate_summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
