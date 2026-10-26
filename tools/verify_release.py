"""Verify downloaded release files against the published checksums."""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--directory',type=Path,default=ROOT/'output/pdf')
args=parser.parse_args()
manifest=json.loads((ROOT/'releases/v1.0.0-files.json').read_text())
for row in manifest['files']:
    p=args.directory/row['filename']
    assert p.stat().st_size==row['bytes'],f'File size differs: {p.name}'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],f'Checksum differs: {p.name}'
    print('Verified:',p.name)
