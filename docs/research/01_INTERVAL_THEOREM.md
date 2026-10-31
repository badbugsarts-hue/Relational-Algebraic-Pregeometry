# Conditional interval theorem

**Status:** new RAP v4.0 working note, 27 October 2026; no PI approval or evidence upgrade.

Let a descending partition of N have k>=2 positive integer parts. H1 requires distinctness; H2 bounds each successive gap by one. Distinct descending integer neighbours have gap at least one. Combining the two bounds makes every gap exactly one. If the last part is m, induction gives the list [m+k-1,...,m], with m>=1. Summation gives N=k*m+k*(k-1)/2. Conversely every such interval is a descending positive partition satisfying both predicates.

This is a general conditional analytic argument. The Python engine solves the divisibility equation independently of its partition enumerator; comparing both implementations through N=40 is a finite regression check, not a general formal certificate. At N=6 the only admissible interval is [3,2,1]. At N=7, [4,3] refutes the old inference that the smallest part must be one; at N=15 there are three intervals.

Neither the proof nor the finite certificate derives N=6, H1 or H2 from physics. No physical partition-selection or gauge-origin conclusion is licensed.
