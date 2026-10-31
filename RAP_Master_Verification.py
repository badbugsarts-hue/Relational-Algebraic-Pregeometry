#!/usr/bin/env python3
"""RAP v4.0 release checks: exact finite mathematics, numerical diagnostics and file audits.

PASS means the listed checks passed. It never means RAP, continuum emergence,
physical filter selection, or the Yang-Mills mass gap has been proved.
"""
from __future__ import annotations
import argparse,json,platform,subprocess,sys,time
from datetime import datetime,timezone
from fractions import Fraction as F
from pathlib import Path
from rap.structural import (partitions,admissible,interval_solutions,interval_certificate,
                            verify_interval_certificate,algebra_signature,equal_block_action_ratio)
from rap.numerics import precision_diagnostics
from rap.validation import validate_repository


def run(root: Path, max_n: int = 40, include_reference_checks: bool = False) -> dict:
    if isinstance(max_n,bool) or not 2 <= max_n <= 40:
        raise ValueError('max_n must be between 2 and 40; this is a resource bound, not a physical cutoff')
    start=time.monotonic();checks=[]
    def check(name,ok,scope='exact finite mathematics'):
        checks.append({'name':name,'passed':bool(ok),'scope':scope})
    check('all_N6_partitions',len(list(partitions(6)))==11)
    check('N6_conditional_unique',[p for p in partitions(6) if admissible(p)]==[(3,2,1)])
    check('N7_counterexample',interval_solutions(7)==[(4,3)])
    check('N15_nonuniqueness',interval_solutions(15)==[(8,7),(6,5,4),(5,4,3,2,1)])
    tested_partitions=0
    for n in range(2,max_n+1):
        all_parts=list(partitions(n));tested_partitions+=len(all_parts)
        check('interval_enumeration_N_'+str(n),[p for p in all_parts if admissible(p)]==interval_solutions(n))
        for p in interval_solutions(n):
            c=interval_certificate(p);check('certificate_'+str(n)+'_'+str(c['k']),verify_interval_certificate(c))
    c=interval_certificate((4,3));c['n']=8
    check('reject_tampered_certificate',not verify_interval_certificate(c))
    check('signature_dimensions',algebra_signature((3,2,1))['complex_algebra_dimension']==14)
    check('signature_does_not_construct_spectral_triple',not algebra_signature((3,2,1))['spectral_triple_constructed'],'explicit formal/physical boundary')
    for n in range(2,65):
        for k in range(1,n+1):
            if n%k==0:
                check('equal_block_ratio_'+str(n)+'_'+str(k),equal_block_action_ratio(n,k)==F(n*n-k*k,k*k*(n*n-1)))
    # Charges are imposed external inputs in this control, not a RAP derivation.
    Y={'Q':F(1,6),'u':F(-2,3),'d':F(1,3),'L':F(-1,2),'e':F(1)}
    anomaly={'SU3_squared_Y':2*Y['Q']+Y['u']+Y['d'],
             'SU2_squared_Y':3*Y['Q']+Y['L'],
             'gravity_Y':6*Y['Q']+3*Y['u']+3*Y['d']+2*Y['L']+Y['e'],
             'Y_cubed':6*Y['Q']**3+3*Y['u']**3+3*Y['d']**3+2*Y['L']**3+Y['e']**3}
    for name,value in anomaly.items():check('imposed_charge_control_'+name,value==0,'exact cancellation for supplied charges; no endogenous charge selection')
    numeric=[precision_diagnostics(80),precision_diagnostics(100)]
    for data in numeric:
        d=data['working_decimal_digits']
        check('precision_context_'+str(d),data['global_context_unchanged'],'software context check')
        check('log_consistency_'+str(d),data['log_identity']['observed_consistency'],'observed numerical residual, not certified error')
        check('rational_control_'+str(d),data['rational_control']['observed_consistency'],'observed consistency; exact Fraction control separate')
        check('rounding_warning_'+str(d),data['rounding_counterexample']['shows_loss_of_exactness'],'counterexample to residual-only exactness claims')
    checks.extend(validate_repository(root))
    posthoc={'status':'NOT_REQUESTED','scope':'separate comparator; never solver input'}
    if include_reference_checks:
        result=subprocess.run([sys.executable,str(root/'scripts/reference_diagnostics.py')],capture_output=True,text=True,cwd=root)
        if result.returncode:
            check('posthoc_comparator_execution',False,'reference arithmetic only')
            posthoc={'status':'FAILED','stderr':result.stderr}
        else:
            posthoc=json.loads(result.stdout);check('posthoc_comparator_execution',True,'reference arithmetic only')
    return {'programme':'RAP','programme_version':'4.0','release_state':'working-draft',
            'run_utc':datetime.now(timezone.utc).isoformat(),
            'runtime':{'python':platform.python_version(),'platform':platform.platform()},
            'suite_status':'PASS' if all(c['passed'] for c in checks) else 'FAIL',
            'scientific_status':'OPEN; no physical selection, continuum or Yang-Mills proof certified',
            'verification_scope':{'exhaustive_integer_partition_n':[2,max_n],
                                  'partitions_visited':tested_partitions,
                                  'general_theorem_formal_Lean_verification':'NOT_RUN'},
            'checks':checks,'check_count':len(checks),'passed_count':sum(c['passed'] for c in checks),
            'precision_diagnostics':numeric,'posthoc_reference_diagnostics':posthoc,
            'anomaly_control':{'inputs':'externally imposed hypercharges',
                               'exact_residuals':{k:str(v) for k,v in anomaly.items()}},
            'not_run':['Docker build/run','LaTeX compilation and PDF visual inspection','Lean build/axiom inventory',
                       'Monte Carlo/lattice replication','independent external scientific validation'],
            'elapsed_seconds':round(time.monotonic()-start,3)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n',type=int,default=40)
    parser.add_argument('--include-reference-checks',action='store_true')
    parser.add_argument('--output',type=Path,default=Path('results/master-verification.json'))
    args=parser.parse_args();root=Path(__file__).resolve().parent
    try:report=run(root,args.max_n,args.include_reference_checks)
    except (ValueError,ImportError,FileNotFoundError) as exc:parser.error(str(exc))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('RAP v4.0: '+report['suite_status']+' — '+str(report['passed_count'])+'/'+str(report['check_count'])+' listed checks')
    print('80-digit diagnostic: observed residual criterion < 1e-40; 100-digit: < 1e-60')
    print('These are mathematical/software diagnostics, NOT mass-gap or physical proofs.')
    print('Scientific status: OPEN. Lean / Docker / PDF / lattice reproduction: NOT_RUN.')
    print('Report: '+str(args.output))
    return 0 if report['suite_status']=='PASS' else 1

if __name__=='__main__':sys.exit(main())
