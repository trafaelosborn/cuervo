"""Build the current monograph from included text and reproduction assets."""
from pathlib import Path
import argparse,os,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--compact',action='store_true',help='Also build the PDF below 9.8 MB.')
args=parser.parse_args()
env=os.environ.copy();env['CUERVO_PORTABLE_FONTS']='1'
for folder in ['output/pdf','tmp/pdfs']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
scripts=['manuscript/build_cuervo_monograph.py','manuscript/make_print_monograph.py']
if args.compact:scripts.append('manuscript/make_compact_monograph.py')
scripts.append('tools/check_build.py')
for script in scripts:
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,env=env,check=True)
print('Built',ROOT/'output/pdf/cuervo-monograph-print-letter.pdf')
