#!/usr/bin/env python3
"""Regenerate a dated dashboard from actual reports, without upgrading scientific claims."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
def load(name):
    p=root/name
    return json.loads(p.read_text()) if p.exists() else None
master=load('results/master-verification.json');tests=load('results/unit-tests.json');engine=load('results/core-engine-100.json')
lines=['# RAP v4.0 — generated verification status','',
 '**This is a generated snapshot, not a live external verification service.**',
 'Regenerate with `python scripts/update_status.py` after running the actual checks.','',
 '## Executed Python checks','']
if master:
    lines.extend(['- **Run UTC** — '+master['run_utc']+'.',
      '- **Master suite** — '+master['suite_status']+': '+str(master['passed_count'])+'/'+str(master['check_count'])+' listed checks.',
      '- **Exhaustive domain** — N='+str(master['verification_scope']['exhaustive_integer_partition_n'][0])+'–'+str(master['verification_scope']['exhaustive_integer_partition_n'][1])+'; '+str(master['verification_scope']['partitions_visited'])+' partition instances visited.',
      '- **Precision diagnostics** — separate 80/100-digit contexts; observed residual criteria 1e-40 / 1e-60, not certified error bounds.',
      '- **Scientific status** — '+master['scientific_status']+'.'])
else:lines.append('- **Master suite** — NOT_RUN; no report found.')
if tests:lines.append('- **Regression tests** — '+tests['status']+': '+str(tests['tests_run'])+' run, '+str(tests['failures'])+' failures, '+str(tests['errors'])+' errors, '+str(tests['skipped'])+' skipped.')
else:lines.append('- **Regression tests** — NOT_RUN.')
if engine:lines.append('- **Core engine** — exact finite certificates at declared N='+str(engine['declared_n'])+'; physical selection remains OPEN.')
else:lines.append('- **Core engine** — NOT_RUN.')
lines.extend(['','## Not executed / not established','',
 '- **Docker and CI** — files prepared and inputs pinned; no Docker build/run or remote CI execution claimed.',
 '- **Manuscript PDF** — full working source and corrected bibliography provided; compilation and visual inspection NOT_RUN; final PDF absent.',
 '- **Lean** — named historical result reported only; no new build or declaration-level axiom audit.',
 '- **Raw data** — no new Monte Carlo, HMC, lattice or experimental replication; FSS/P2 remains quarantined.',
 '- **Physical bridges** — H1/H2 origin, gauge emergence, continuum, operator matching and Born-rule bridge remain OPEN.',
 '- **Approval and publication** — no new PI approval, canonical freeze, DOI assignment, upload or publication.','',
 'PASS is limited to the listed mathematical/software checks. It does not mean that RAP or the Yang–Mills mass gap has been proved.'])
(root/'STATUS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('STATUS.md refreshed from observed reports; scientific status remains OPEN.')
