"""Build a deterministic V5-only ZIP; no source files or previous versions."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'tools/build_standalone.py')],check=True)
name='Automation-Academy-V5.html'
out=ROOT/'dist/Automation-Academy-V5.zip';out.parent.mkdir(exist_ok=True)
info=ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
with ZipFile(out,'w') as z:z.writestr(info,(ROOT/name).read_bytes())
with ZipFile(out) as z:assert z.namelist()==[name] and z.read(name)==(ROOT/name).read_bytes()
print(f'Packaged only {name}: {out.stat().st_size:,} bytes')
