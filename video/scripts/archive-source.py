from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import subprocess
ROOT=Path(__file__).resolve().parents[1]
excluded={'node_modules','output','deliverables','.git','.audio-venv','.npm-cache','__pycache__'}
with ZipFile(ROOT/'deliverables/job-ledger-source.zip','w',compression=ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted(ROOT.rglob('*')):
  rel=f.relative_to(ROOT)
  if f.is_file() and not any(p in excluded for p in rel.parts):z.write(f,Path('cubbie-video')/rel)
print('Complete editable source archived without dependencies or render caches.')
