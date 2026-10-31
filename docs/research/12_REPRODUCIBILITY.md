# Precision, dependency locks and execution scope

**Status:** new RAP v4.0 working note, 27 October 2026; no PI approval or evidence upgrade.

The master suite uses exact integers and Fraction where possible. Separate cloned mpmath contexts run at 80 and 100 decimal digits without mutating shared precision. The observed residual criteria are respectively 1e-40 and 1e-60 for mathematical consistency diagnostics, not certified physical or true-error bounds.

A cancellation counterexample demonstrates why zero at finite precision need not mean exact zero. Dependency versions and allowed artefact hashes are locked. The public base image is pinned by manifest digest, but Docker was not executed in this environment.

The final manuscript PDF is not included because no LaTeX engine was available. The repository working source externalizes the corrected bibliography; original manuscript body and historical PI boxes are preserved. Schema checks, hashes and test counts are scoped observations, not independent scientific replication.
