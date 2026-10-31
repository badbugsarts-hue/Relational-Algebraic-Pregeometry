#!/usr/bin/env python3
"""Exact finite-domain certificates and isolated numerical diagnostics.

The historical filename 'proof engine' is not a claim of a general formal or physical proof.
N is a declared input. H1/H2 are filters, not physically derived laws.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from rap.structural import interval_solutions,interval_certificate,algebra_signature,partitions,admissible


def run(n: int, exhaustive: bool = False, dps: int = 100) -> dict:
    solutions=interval_solutions(n)
    result={'engine':'RAP finite conditional certificate engine','declared_n':n,'n_is_declared_input':True,
            'hypotheses':{'H1':'at least two distinct descending positive integer parts',
                          'H2':'successive gaps at most one'},
            'interval_certificates':[interval_certificate(p) for p in solutions],
            'algebra_signatures':[algebra_signature(p) for p in solutions],
            'exhaustive_comparison':{'status':'NOT_REQUESTED'},
            'general_analytic_argument':'docs/research/01_INTERVAL_THEOREM.md',
            'lean_build':'NOT_RUN','physical_selection':'OPEN',
            'calibrated_parameter_derivation':False,'yang_mills_mass_gap_proof':False}
    if exhaustive:
        if n > 40:
            raise ValueError('exhaustive enumeration is capped at n=40; interval certificates remain general')
        actual=[p for p in partitions(n) if admissible(p)]
        result['exhaustive_comparison']={'status':'PASS' if actual==solutions else 'FAIL',
                                        'domain_n':n,'all_partitions':sum(1 for _ in partitions(n))}
    from rap.numerics import precision_diagnostics
    result['precision_diagnostics']=precision_diagnostics(dps)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,required=True,help='declared positive integer; not derived from physics')
    parser.add_argument('--exhaustive',action='store_true')
    parser.add_argument('--dps',type=int,default=100)
    parser.add_argument('--output',type=Path)
    a=parser.parse_args()
    try:result=run(a.n,a.exhaustive,a.dps)
    except (ValueError,ImportError) as exc:parser.error(str(exc))
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8')
    print(text,end='')
    numerical=result['precision_diagnostics']
    ok=(result['exhaustive_comparison']['status']!='FAIL' and numerical['global_context_unchanged']
        and numerical['log_identity']['observed_consistency'] and numerical['rational_control']['observed_consistency'])
    return 0 if ok else 1

if __name__=='__main__':sys.exit(main())
