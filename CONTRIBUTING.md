# Contributing

> **Disclaimer:** This is an experimental benchmark workspace. Strict adherence to `AI_AUDIT_POLICY.md` and the `governance/AGENTS.md` steering baseline is required for all contributions.

## Scientific Governance

Keep exact mathematics, observed numerics, input definitions, external evidence, software reports and governance policies separate. Supply a source anchor and executable reproduction where applicable. Do not insert calibrated targets into the structural module or redefine a reference as a prediction. Do not replace null uncertainty with zero.

Report failed and null results, dependency changes and unexecuted checks. Do not commit credentials, private data or generated claims of independent approval.

## Workflow Rules

1. **Ticket-Branch Git Workflow:** All changes must occur on dedicated feature branches. No direct pushes to main.
2. **Mandatory Test Suite Execution:** Before any commit, run both suites:
   ```bash
   # RAP v4.0 verification suite
   python RAP_Master_Verification.py --output results/master-verification.json
   python scripts/run_tests.py

   # Pregeometry tests
   py -m pytest verification/tests/ -q -p no:cacheprovider --basetemp verification/data/pregeometry/pytest-tmp-agent-config --tb=short
   ```
3. **No Target Leakage:** Do not introduce physical constants, target cosmology values, Standard Model targets, or calibrated UIDT parameters into pregeometry growth rules, null ensembles, dashboards, diagnostics or tests unless a dedicated reviewed task explicitly requires it.
4. **Artifact Management:** No root-level runtime artifacts are allowed. All runtime data must go to `verification/data/pregeometry/`.
5. **PI Records:** Preserve existing PI records; propose any new decision separately. A clean scan or successful CI job does not close the target-shape or physics audit.
6. **Integrity:** Re-running reports changes their hashes. Regenerate integrity material with `scripts/package_release.py` before redistributing.
