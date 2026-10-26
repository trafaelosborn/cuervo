"""Build a publication figure from the checked, held USDA/CPI transcription."""
from pathlib import Path
import hashlib
import json
import math
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tmp/chapter-build-deps'))
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/pdfs/matplotlib-config'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

SOURCE = ROOT / 'research_evidence/real_cattle_prices_2026-09-19/annual_prices_and_cpi.json'
OUT = ROOT / 'manuscript/figures/visual-expansion-2026-09-27'
OUT.mkdir(parents=True, exist_ok=True)
data = json.loads(SOURCE.read_text(encoding='utf-8'))
rows = sorted(data['observations'], key=lambda r: r['year'])
assert [r['year'] for r in rows] == list(range(1913, 1979))
by_year = {r['year']: r for r in rows}
for row in rows:
    expected = row['nominal_usd_per_cwt'] * 24.1 / row['cpi_u_annual']
    assert math.isclose(expected, row['real_1950_usd_per_cwt'], rel_tol=1e-10)
base = by_year[1951]['real_1950_usd_per_cwt']
indexed = [r['real_1950_usd_per_cwt'] / base * 100 for r in rows]
assert math.isclose(indexed[1951 - 1913], 100)
rise = (by_year[1949]['real_1950_usd_per_cwt'] / by_year[1939]['real_1950_usd_per_cwt'] - 1) * 100
fall = (by_year[1956]['real_1950_usd_per_cwt'] / base - 1) * 100
assert round(rise) == 81 and round(fall) == -52

NAVY, INK, GRAY, RULE = '#1b3558', '#242528', '#756e65', '#d8d2c9'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                     'svg.fonttype': 'none', 'axes.unicode_minus': False})
title_font = FontProperties(fname='C:/Windows/Fonts/GARAIT.TTF', size=26)
fig = plt.figure(figsize=(9, 6.8), facecolor='white')
fig.text(.10, .945, 'The cattle-price cycle', fontproperties=title_font, color=NAVY)
fig.text(.10, .898, 'New Mexico prices received for beef cattle, 1913-1978', color=INK, fontsize=11)
fig.text(.10, .860, 'Consumer-price-adjusted index; 1951 = 100', color=GRAY, fontsize=9.5)
ax = fig.add_axes([.10, .31, .85, .49])
ax.plot([r['year'] for r in rows], indexed, color=NAVY, linewidth=2.1)
ax.set_xlim(1912, 1980)
ax.set_ylim(0, 117)
ax.set_xticks([1920, 1930, 1940, 1950, 1960, 1970, 1978])
ax.set_yticks([0, 25, 50, 75, 100])
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color(RULE)
ax.tick_params(axis='both', length=0, pad=7, colors=GRAY, labelsize=9)
ax.grid(axis='y', color='#e9e5e0', linewidth=.7)
ax.set_axisbelow(True)
for year, offset, align in [(1951, (-12, 14), 'right'), (1956, (8, -23), 'left'), (1973, (0, 14), 'center')]:
    val = by_year[year]['real_1950_usd_per_cwt'] / base * 100
    ax.scatter([year], [val], s=25, color=NAVY, zorder=3)
    ax.annotate(f'{year}: {val:.0f}', (year, val), xytext=offset,
                textcoords='offset points', ha=align, color=NAVY, fontsize=10,
                bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 2})

fig.text(.10, .205, '+81%', color=NAVY, fontsize=22)
fig.text(.10, .170, '1939 to 1949', color=GRAY, fontsize=10)
fig.text(.40, .205, '-52%', color=NAVY, fontsize=22)
fig.text(.40, .170, '1951 to 1956', color=GRAY, fontsize=10)
fig.text(.69, .205, '96%', color=NAVY, fontsize=22)
fig.text(.69, .170, '1973, relative to 1951', color=GRAY, fontsize=10)

fig.text(.10, .105, 'State averages per 100 lb of liveweight, excluding calves; 66 annual observations.', fontsize=8, color=GRAY)
fig.text(.10, .080, 'The index measures consumer purchasing power per unit sold, not ranch profits or local spending.', fontsize=8, color=GRAY)
fig.text(.10, .043, 'Sources: USDA Statistical Bulletins 265 and 680; BLS annual CPI-U. Calculations: Meridian.', fontsize=8, color=GRAY)
stem = OUT / 'real-cattle-price-cycle'
fig.savefig(stem.with_suffix('.png'), dpi=200, facecolor='white')
fig.savefig(stem.with_suffix('.svg'), facecolor='white')
plt.close(fig)

manifest = {
    'status': 'draft figure for next Chapter 3 proof; not yet inserted',
    'title': 'The cattle-price cycle',
    'input': str(SOURCE),
    'input_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'source_record': data['sources'],
    'method': '100 * (nominal_price(year)/CPI(year)) / (nominal_price(1951)/CPI(1951)).',
    'years': [1913, 1978], 'observations': 66,
    'scope': 'New Mexico live beef cattle, excluding calves, per 100 lb; state observations, not Cuervo transactions.',
    'limits': 'Consumer purchasing power is not ranch profitability. Annual averages reflect the sale mix. No population overlay or causal estimate.',
    'annotations': {'real_change_1939_1949_pct': rise, 'real_change_1951_1956_pct': fall,
                    'index_1973': by_year[1973]['real_1950_usd_per_cwt']/base*100},
    'series': [{'year': r['year'], 'index_1951_100': v} for r, v in zip(rows, indexed)],
    'outputs': [str(stem.with_suffix(ext)) for ext in ['.png', '.svg']],
    'visual_review': 'pending'
}
(OUT / 'real-cattle-price-cycle-sources.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps({'outputs': manifest['outputs'], 'observations': 66, 'annotations': manifest['annotations']}, indent=2))
