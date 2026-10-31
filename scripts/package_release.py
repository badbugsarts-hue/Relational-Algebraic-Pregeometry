#!/usr/bin/env python3
"""Refresh hashes and package only the explicitly tracked release files.

Never sweeps a working directory for credentials or unrelated data. To add a new
file, review it and add its path/role to MANIFEST.json first. Existing hashes are
then recomputed; this operation is not an approval or evidence upgrade.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe(name):
    q=PurePosixPath(name);p=root/q
    if q.is_absolute() or '..' in q.parts or not p.resolve().is_relative_to(root):raise ValueError('unsafe manifest path')
    return p
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path('dist/RAP_v4_0_Repository.zip'))
a=parser.parse_args()
manifest=json.loads((root/'MANIFEST.json').read_text())
tracked={item['path']:item.get('role','reviewed release file') for item in manifest['files']}
if len(tracked)!=len(manifest['files']):raise ValueError('duplicate tracked path')
if set(tracked)&{'MANIFEST.json','SHA256SUMS'}:raise ValueError('circular manifest entry')
canonical=[]
for name in sorted(tracked):
    p=safe(name)
    if not p.is_file():raise FileNotFoundError(p)
    if name.startswith('CANONICAL/') and name!='CANONICAL/MANIFEST.json':
        canonical.append({'path':name,'sha256':digest(p)})
(root/'CANONICAL/MANIFEST.json').write_text(json.dumps({'authority':'package snapshot, not PI approval','files':canonical},indent=2)+'\n')
manifest['files']=[{'path':name,'bytes':safe(name).stat().st_size,'sha256':digest(safe(name)),'role':tracked[name]} for name in sorted(tracked)]
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
paths=sorted(list(tracked)+['MANIFEST.json'])
(root/'SHA256SUMS').write_text(''.join(digest(safe(name))+'  '+name+'\n' for name in paths))
a.output.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in sorted(paths+['SHA256SUMS']):
        info=zipfile.ZipInfo(name,date_time=(2026,10,27,0,0,0));info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,safe(name).read_bytes())
with zipfile.ZipFile(a.output) as z:
    if z.testzip() is not None:raise RuntimeError('ZIP CRC failure')
print(json.dumps({'archive':str(a.output),'members':len(paths)+1,'sha256':digest(a.output),
                  'new_approval_or_publication':False},indent=2))
