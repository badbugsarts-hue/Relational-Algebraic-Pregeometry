# RAP v4.0 repository preparation — observed checks

**Python checks passed; scientific programme remains OPEN.** No author approval, physical proof, new DOI or publication is implied.

- **Master suite:** 436/436 individually listed conditions passed.
- **Independent finite enumeration:** N=2–40, 215306 partition instances visited; conditional N=6 result and N=7/N=15 controls included.
- **Regression tests:** 25 actually executed, 0 failures, 0 errors, 0 skipped.
- **Precision:** mpmath 1.3.0, separate cloned 80- and 100-digit contexts. Observed log-identity residuals: 1.6867516709168837158957718482032030412335938211789612080124420840173030865551615e-80 and 0.0. Acceptance criteria are 1e-40 and 1e-60, not rigorous error certificates.
- **Reference separation:** default master run leaves the post-hoc comparator unrequested; a separate explicit run exercises reference arithmetic. No calibrated constants are loaded by the structural solver.
- **Data/schema integrity:** 30 curated release claims, nine scoped reference constants, unique IDs, acyclic dependencies, source anchors and unknown uncertainties preserved.
- **Manuscript:** body and seven recorded PI boxes preserved; bibliography externalized and aligned in a new repository copy. All 79 used citation keys are covered. The predecessor is retained under provenance, not substituted for the new working source.
- **Bibliographies independently parsed:** 131 full records, 124 manuscript records, 49 guide records and two version-specific citation entries.
- **Research index:** 12 newly written notes, not an inherited count of 47.
- **Markdown:** 36 existing Markdown files parsed as CommonMark and relative links checked before this report was added. External URL availability is not certified.
- **Dependency/container inputs:** runtime versions and PyPI artefact hashes locked; public Python image manifest and CI actions pinned. No Docker build or remote CI run was performed.

## Not performed

No Lean build or declaration-level axiom inventory; no LaTeX compilation or final PDF inspection; no raw MC/HMC/lattice replication; no independent physical validation; no PI signature, canonical approval, DOI assignment or online publication. The numerical tests are mathematical diagnostics, not an implementation of the old UIDT mass-gap proof claim.

## Detailed records

Read `results/master-verification.json`, `results/unit-tests.json`, `results/core-engine-100.json`, `results/partitions-N6.csv` and `results/execution-receipt.json`. `STATUS.md` is generated from those reports. The release manifest and SHA256SUMS cover the delivered snapshot; hashes are integrity checks, not authenticity signatures.
