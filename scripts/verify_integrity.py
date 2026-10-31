#!/usr/bin/env python3
"""Verify listed snapshot files. Hashes are not author signatures or scientific validation."""
from pathlib import Path,PurePosixPath
import hashlib,json,sys
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'MANIFEST.json').read_text());errors=[]
for item in manifest['files']:
    path=PurePosixPath(item['path'])
    p=root/path
    if path.is_absolute() or '..' in path.parts or not p.resolve().is_relative_to(root):
        errors.append(item['path']+': unsafe path');continue
    if not p.is_file():errors.append(item['path']+': missing');continue
    if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256'] or p.stat().st_size!=item['bytes']:
        errors.append(item['path']+': changed')
for line in (root/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1);p=root/name
    if not p.resolve().is_relative_to(root) or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
        errors.append(name+': checksum mismatch')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','files_checked':len(manifest['files']),
                  'errors':errors,'scope':'listed file integrity only; not authenticity or scientific truth'},indent=2))
sys.exit(1 if errors else 0)
