"""Fetch public originals for the residential-cooling research sweep."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, urllib.request, datetime

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'sources' / 'home_cooling_2026-09-24'
OUT.mkdir(parents=True, exist_ok=True)
SOURCES = {
 'census_1960_nm_housing_equipment.pdf': 'https://usa.ipums.org/usa/resources/voliii/pubdocs/1960/Housing/42017038ch1.pdf',
 'census_1960_housing_definitions.pdf': 'https://www2.census.gov/library/publications/decennial/1960/housing-volume-1/41962442v1p4ch1.pdf',
 'glaeser_tobio_2007_sunbelt.pdf': 'https://www.nber.org/system/files/working_papers/w13071/w13071.pdf',
 'rappaport_2003_nice_weather.pdf': 'https://fmwww.bc.edu/repec/esNASM04/up.30923.1075143636.pdf',
 'leduc_wilson_2024_sunbelt.pdf': 'https://www.frbsf.org/wp-content/uploads/wp2024-21.pdf',
 'ghcnd_stations.txt': 'https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt',
 'ghcnd_inventory.txt': 'https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt',
 'census_1970_nm_housing_ch2.pdf': 'https://www2.census.gov/library/publications/decennial/1970/housing-volume-1/25809063v1p33ch2.pdf',
 'census_1970_nm_housing_appendix.pdf': 'https://www2.census.gov/library/publications/decennial/1970/housing-volume-1/25809063v1p33ch3.pdf',
 'rappaport_2006_nice_weather.pdf': 'https://www.kansascityfed.org/documents/5390/pdf-RWP03-07.pdf',
 'barreca_et_al_2015_mortality.pdf': 'https://impactlab.org/wp-content/uploads/2017/09/Barreca-2016-Adapting-to-Climate-Change.pdf',
 'santa_rosa_ghcnd.dly': 'https://www.ncei.noaa.gov/pub/data/ghcn/daily/all/USC00298107.dly',
 'ghcnd_readme.txt': 'https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt',
 'united_power_1940_opinion.html': 'https://calculators.law/caselaw/decisions/oeW8n71z53dM/in-re-united-power-co-taxes-for-1937',
 'farmers_electric_nm.html': 'https://www.fecnm.org/',
 'biddle_2008_researchgate.html': 'https://www.researchgate.net/publication/222777062_Explaining_the_spread_of_residential_air_conditioning_1955-1980',
 'biddle_2010_researchgate.html': 'https://www.researchgate.net/publication/241698792_Air_Conditioning_Migration_and_Climate-Related_Wage_and_Rent_Differentials',
 'census_1980_nm_summary_governmental.pdf': 'https://upload.wikimedia.org/wikipedia/commons/8/85/1980_Census_of_Population_and_Housing._Summary_Characteristics_for_Governmental_Units_and_SMSAs_New_Mexico_%28IA_1980censusofpopu80333unse%29.pdf',
 'doe_evaporative_coolers.html': 'https://www.energy.gov/energysaver/evaporative-coolers',
}

def fetch(item):
    name, url = item
    result = dict(file=name, url=url, retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        if (OUT/name).exists():
            data = (OUT/name).read_bytes()
            result.update(status='already_downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            return result
        req = urllib.request.Request(url, headers={'User-Agent':'CuervoHistoryResearch/1.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            result['resolved_url'] = response.url
        if name.endswith('.pdf') and not data.startswith(b'%PDF-'):
            raise ValueError('Response is not a PDF')
        (OUT/name).write_bytes(data)
        result.update(status='downloaded', bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        result.update(status='failed', error=str(exc))
    return result

if __name__ == '__main__':
    import sys
    manifest = Path(__file__).parent/'download_manifest.json'
    previous = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
    with ThreadPoolExecutor(max_workers=4) as pool:
        selected = [(n,u) for n,u in SOURCES.items() if not sys.argv[1:] or n in sys.argv[1:]]
        results = list(pool.map(fetch, selected))
    manifest.write_text(json.dumps(previous + [r for r in results if r['status'] != 'already_downloaded'], indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))
