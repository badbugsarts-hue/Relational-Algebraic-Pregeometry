# Functional dependence and research provenance

**Status:** new RAP v4.0 working note, 27 October 2026; no PI approval or evidence upgrade.

P(x,t)=x^2 is independent of an accessible t; accessibility alone does not prove dependence. Conversely, finding two outputs at fixed x that differ when t changes refutes functional independence.

RAP's conservative audit policy is stronger: protected calibrated targets should remain outside blind solver paths. The new structural module imports only mathematical standard-library components and does not load the reference constants. A separate comparator is invoked only on explicit request.

The literal/import scan is not a proof of target-independent discovery. Input choice, detector design, stopping rules and earlier calibration may still encode targets. The historical formal target-shape audit remains open; it is not closed by a clean scan of the new Python module.
