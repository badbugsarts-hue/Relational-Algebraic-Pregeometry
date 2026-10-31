#!/usr/bin/env python3
"""Export the declared finite candidate set and its filter verdicts, not empirical data."""
from pathlib import Path
import argparse,csv,json,sys
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
from rap.structural import partitions,admissible
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--n',type=int,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
if not 1<=a.n<=40:p.error('exhaustive export is restricted to 1<=n<=40')
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open('w',encoding='utf-8',newline='') as fp:
    w=csv.DictWriter(fp,fieldnames=['declared_n','parts','at_least_two_parts','distinct_parts_H1','adjacent_gap_H2','admissible','complex_algebra_dimension'])
    w.writeheader()
    for parts in partitions(a.n):
        w.writerow({'declared_n':a.n,'parts':json.dumps(parts),'at_least_two_parts':len(parts)>=2,
                    'distinct_parts_H1':len(set(parts))==len(parts),
                    'adjacent_gap_H2':all(x-y<=1 for x,y in zip(parts,parts[1:])),
                    'admissible':admissible(parts),'complex_algebra_dimension':sum(x*x for x in parts)})
print('Exported mathematical candidates to '+str(a.output)+'; no physical selection asserted.')
