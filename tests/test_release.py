from __future__ import annotations
import concurrent.futures,copy,json,unittest
from pathlib import Path
from fractions import Fraction as F
import mpmath,jsonschema
from rap.structural import *
from rap.numerics import precision_diagnostics
from rap.validation import validate_repository,dependencies_acyclic
ROOT=Path(__file__).resolve().parents[1]

class StructuralTests(unittest.TestCase):
    def test_partitions_six(self):self.assertEqual(len(list(partitions(6))),11)
    def test_positive_inputs(self):
        for x in [True,False,0,-1,1.5,'6',None]:
            with self.assertRaises(ValueError):list(partitions(x))
    def test_no_duplicates(self):
        for n in range(1,19):
            p=list(partitions(n));self.assertEqual(len(p),len(set(p)))
            self.assertTrue(all(valid_partition(x,n) for x in p))
    def test_declared_filters(self):
        self.assertFalse(admissible((2,2,2)));self.assertFalse(admissible((5,3,1)))
        self.assertFalse(admissible((6,)));self.assertFalse(admissible((1,2,3)))
        self.assertFalse(admissible(()));self.assertFalse(admissible((True,)))
    def test_n6(self):self.assertEqual(interval_solutions(6),[(3,2,1)])
    def test_counterexample_to_staircase(self):self.assertEqual(interval_solutions(7),[(4,3)])
    def test_nonunique_n15(self):self.assertEqual(len(interval_solutions(15)),3)
    def test_small_domains(self):
        for n in range(1,21):self.assertEqual([x for x in partitions(n) if admissible(x)],interval_solutions(n))
    def test_certificate_roundtrip(self):
        for n in range(2,41):
            for p in interval_solutions(n):self.assertTrue(verify_interval_certificate(interval_certificate(p)))
    def test_certificate_mutation(self):
        c=interval_certificate((4,3))
        for field in ['n','k','m','sum_formula_rhs']:
            bad=copy.deepcopy(c);bad[field]+=1;self.assertFalse(verify_interval_certificate(bad))
            bad[field]=True;self.assertFalse(verify_interval_certificate(bad))
        bad=copy.deepcopy(c);bad['scope']='physical proof';self.assertFalse(verify_interval_certificate(bad))
        bad=copy.deepcopy(c);bad['unexpected']=1;self.assertFalse(verify_interval_certificate(bad))
    def test_certificate_rejects_invalid_input(self):
        with self.assertRaises(ValueError):interval_certificate((2,2,2))
    def test_signature_is_not_spectral_triple(self):
        s=algebra_signature((3,2,1));self.assertEqual(s['complex_algebra_dimension'],14)
        self.assertEqual(s['off_diagonal_count'],8);self.assertFalse(s['spectral_triple_constructed'])
    def test_action_ratio(self):self.assertEqual(equal_block_action_ratio(6,2),F(8,35))
    def test_action_ratio_invalid(self):
        for n,k in [(1,1),(5,2),(4,0),(True,1)]:
            with self.assertRaises(ValueError):equal_block_action_ratio(n,k)

class PrecisionTests(unittest.TestCase):
    def test_context_preservation(self):
        before=mpmath.mp.dps
        a=precision_diagnostics(80);b=precision_diagnostics(100)
        self.assertEqual(mpmath.mp.dps,before);self.assertTrue(a['global_context_unchanged']);self.assertTrue(b['global_context_unchanged'])
    def test_thresholds_are_observations(self):
        for d in [80,100]:
            r=precision_diagnostics(d);self.assertTrue(r['log_identity']['observed_consistency'])
            self.assertIsNone(r['certified_error_bound']);self.assertFalse(r['physical_validation'])
    def test_rounding_warning(self):self.assertTrue(precision_diagnostics(80)['rounding_counterexample']['shows_loss_of_exactness'])
    def test_independent_concurrent_contexts(self):
        before=mpmath.mp.dps
        with concurrent.futures.ThreadPoolExecutor(2) as pool:res=list(pool.map(precision_diagnostics,[80,100]))
        self.assertEqual([x['working_decimal_digits'] for x in res],[80,100]);self.assertEqual(mpmath.mp.dps,before)
    def test_invalid_precision(self):
        for d in [True,20,79,80.5]:
            with self.assertRaises(ValueError):precision_diagnostics(d)

class LedgerTests(unittest.TestCase):
    def test_release_checks(self):
        failed=[x for x in validate_repository(ROOT) if not x['passed']];self.assertEqual(failed,[])
    def test_evidence_schema_rejects_upgrade_alias(self):
        x=json.loads((ROOT/'LEDGER/CLAIMS.json').read_text());schema=json.loads((ROOT/'LEDGER/claims.schema.json').read_text())
        x['claims'][0]['evidence_class']='A+'
        with self.assertRaises(jsonschema.ValidationError):jsonschema.Draft202012Validator(schema).validate(x)
    def test_cycles_are_rejected(self):
        self.assertFalse(dependencies_acyclic([{'id':'a','dependencies':['b']},{'id':'b','dependencies':['a']}]))
        self.assertFalse(dependencies_acyclic([{'id':'a','dependencies':['missing']}]))
        self.assertTrue(dependencies_acyclic([{'id':'a','dependencies':[]},{'id':'b','dependencies':['a']}]))
    def test_no_approval_manufactured(self):
        x=json.loads((ROOT/'LEDGER/CLAIMS.json').read_text());self.assertIsNone(x['metadata']['new_pi_approval'])
    def test_uncertainty_not_silently_zero(self):
        c=json.loads((ROOT/'CANONICAL/constants.json').read_text())['constants']
        for x in c:
            if x['id'] in ['gamma_calibrated','scalar_vev_reference','torsion_reference']:self.assertIsNone(x['uncertainty']['value'])
    def test_seven_recorded_decisions_only(self):
        d=json.loads((ROOT/'governance/RECORDED_PI_DECISIONS.json').read_text())
        self.assertEqual([x['id'] for x in d['decisions']],['D'+str(i) for i in range(19,26)])

if __name__=='__main__':unittest.main()
