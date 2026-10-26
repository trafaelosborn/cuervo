from pathlib import Path
from PIL import Image
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'tmp' / 'rebound_1940_1950'
OUT.mkdir(parents=True, exist_ok=True)
manifest = []
for year, folder, pattern in [(1940, '1940_manuscripts', 'm-t0627-02445-0065*.jpg'), (1950, '1950_manuscripts', '*.jpg')]:
    for path in sorted((ROOT / 'sources' / '03_census' / folder / 'ed_10-6').glob(pattern)):
        index = int(path.stem.split('-')[-1])
        if year == 1940 and index == 657:
            continue
        if year == 1950 and index == 1:
            continue
        im = Image.open(path)
        w, h = im.size
        regions = {'people': (.055, .215, .445, .792), 'work': (.58, .215, .91, .792)} if year == 1940 else {'people': (.087, .205, .574, .69), 'sample': (.086, .698, .95, .903)}
        for kind, box in regions.items():
            crop = im.crop(tuple(round(v * (w if i % 2 == 0 else h)) for i, v in enumerate(box)))
            for half in ['a', 'b'] if kind == 'people' and year == 1940 else ['all']:
                piece = crop
                if half == 'a': piece = crop.crop((0, 0, crop.width, round(crop.height*.525)))
                if half == 'b': piece = crop.crop((0, round(crop.height*.475), crop.width, crop.height))
                if piece.width > 1600:
                    piece = piece.resize((1600, round(piece.height * 1600 / piece.width)))
                dest = OUT / f'{year}_{index}_{kind}_{half}.jpg'
                piece.save(dest, quality=95)
                manifest.append({'source': str(path.relative_to(ROOT)), 'crop': str(dest.relative_to(ROOT)), 'region_fraction': box, 'half': half})
(OUT / 'crop_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(f'Prepared {len(manifest)} reading crops in {OUT}')
