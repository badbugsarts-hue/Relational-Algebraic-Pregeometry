# Data availability — RAP v4.0 working repository

## Available in this package

- **Manuscript source** — `manuscript/RAP_v4_0.tex`; the corrected working text, with the bibliography externalized and repaired in this repository copy. Its body and seven historical PI boxes are preserved. No newly compiled PDF is included.
- **Bibliographies** — 131 full reference records, 124 manuscript records and 49 guide records. Source-to-output identity information is in `bibliography_provenance.csv`. This is not a full-text verification of every cited paper.
- **Mathematical code** — new generic interval/partition algorithms, certificate checks, exact Fraction controls and isolated numerical diagnostics. Inputs and scope are documented in the entry-point help and research notes.
- **Finite candidate table** — `results/partitions-N6.csv` lists all eleven partitions and the separate filter verdicts. It is generated mathematical data, not an experimental dataset.
- **Reference data** — nine carried constants and 30 curated release claims, with units, missing uncertainty explicitly null, source anchors and incoming evidence classes.
- **Executed reports** — `results/master-verification.json`, `results/core-engine-100.json`, `results/unit-tests.json` and logs from this environment. Their status refers only to the listed checks.
- **Integrity material** — source provenance, dependency lock, manifest and SHA-256 file list. Checksums are not signatures or independent approvals.

## Not available or not reproduced

No raw MC/HMC chains, lattice ensembles, seeds/configuration for quarantined FSS/P2, topology continuum data or new experimental measurements are supplied. The historical gamma MC summary is a reference, not a reproduced run. No complete independent Lean build or axiom inventory was executed or bundled as a new verification. No Docker run, final PDF compilation or publication is asserted.

No statistical uncertainty, covariance or raw data is reconstructed from a quoted central value. The missing material is tracked by open ledger tickets; it is not replaced with synthetic “experimental” data.

## Access and versioning

The delivered repository is a working submission-support snapshot. The old DOI 10.5281/zenodo.22731224 identifies the base publication only; no new dataset or correction DOI is assigned here. The historical UIDT repository was an organizational quality reference only, not a source of active results. Actual release files and their destination DOI require author review.

See `README.md` for reproduction commands and `CANONICAL/EVIDENCE.md` for what the reports do and do not establish.
