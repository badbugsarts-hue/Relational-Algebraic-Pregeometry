# Relational-Algebraic Pregeometry — RAP v4.0

[![Status: Canonical Freeze](https://img.shields.io/badge/Status-Canonical%20Freeze-blue.svg)]()
[![Verification: Lean 4](https://img.shields.io/badge/Verification-Lean%204-purple.svg)]()
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)]()
[![CI: Python Checks](https://img.shields.io/badge/CI-Python%20Checks-green.svg)]()

**Working repository; physical programme [D]. No new PI freeze or publication.** This is the newly prepared RAP counterpart of the requested verification/ledger repository structure, not a renamed copy of the old UIDT data.

## Entry points

- [Data availability](DataAvailability.md)
- [Current generated status](STATUS.md)
- [Master verification](RAP_Master_Verification.py)
- [Conditional certificate / precision engine](rap_proof_engine.py)
- [Dockerfile](Dockerfile)
- [Full manuscript source and build instructions](manuscript/BUILD.md)
- [Research index: 12 actual notes](docs/research/INDEX.md)
- [Claim ledger](LEDGER/README.md)
- [CANONICAL reference layer](CANONICAL/README.md)
- [Evidence boundary](CANONICAL/EVIDENCE.md)
- [Recorded historical decisions](governance/README.md)

## Lean 4 Formalization

We enforce **Gap Localization before Construction (GLBC)**. Mathematical claims, specifically the *Staircase Conjecture* for the origin of the G_SM block partition, are subjected to automated, blinded verification in Lean 4 to prevent target leakage.

- **Current Snapshot:** `f1ae5486`
- **Proof State:** 18/18 reachable modules exit successfully. Open obligations (`sorry` tags) are explicitly registered as research gaps.
- **Source:** [`verification/antigravit2/`](verification/antigravit2/)

## Reproduce the Python checks

Use Python 3.12 and an isolated environment on your own machine. Install the supplied hash-locked requirements there. No network is used by the suite itself.

```sh
python -m pip install --require-hashes -r requirements.txt
python RAP_Master_Verification.py --output results/master-verification.json
python rap_proof_engine.py --n 6 --exhaustive --dps 100 --output results/core-engine-100.json
python scripts/run_tests.py
python scripts/export_partitions.py --n 6 --output results/partitions-N6.csv
python scripts/update_status.py
python scripts/verify_integrity.py
```

For explicitly separate post-hoc reference arithmetic, add `--include-reference-checks` to the master command or run `python scripts/reference_diagnostics.py`. The structural engine never imports these reference values. `--max-n` defaults to 40 and is restricted to 2–40 for exhaustive resource control; it is not a physical cutoff. The proof-engine `--n` is a declared input, never a derived spacetime or gauge dimension.

Re-running reports changes their hashes. Review the changed files and regenerate integrity material with `scripts/package_release.py` before redistributing. Do not present an old manifest as current after edits.

## What verification means

Exact integer/Fraction controls check the interval classification against independent finite enumeration and selected algebraic identities. A separate analytic proof explains the general interval statement. The 80-digit mpmath diagnostic has an observed residual criterion below 1e-40; the 100-digit diagnostic uses 1e-60. Cloned contexts avoid shared precision mutation. **Those residuals are consistency observations, not certified true-error bounds, a general Lean certificate, or a physical mass-gap proof.**

N=6 and H1/H2 remain declared assumptions. The engine does not construct a physical spectral triple, select a Standard-Model gauge group, derive gamma, generate a continuum or identify a glueball. Reported historical Lean results are not independently reproduced by this package.

## Repository structure

- `rap/`: new structural, numerical and validation modules.
- `tests/`, `scripts/`: regression tests, explicit comparator, status and integrity utilities.
- `LEDGER/`: 30 curated claims, schemas, tensions, proposed tasks and contribution rules.
- `CANONICAL/`: nine carried references and evidence/falsification/limitation documents; no new PI approval implied by the directory name.
- `docs/research/`: 12 newly written notes plus index, not the old 47-note UIDT collection.
- `manuscript/`: full corrected working source, repaired 124-record bibliography and bibliography-only diff.
- `results/`: actual Python reports and logs from preparation; not simulation data.
- `provenance/`, `governance/`: input identities and verbatim recorded D19–D25 boxes.
- `verification/`: Lean 4 formalization (antigravit2) and pregeometry numerical experiments.
- Root metadata: Zenodo JSON, English HTML/CommonMark description, 131-entry full bibliography, 49-entry guide subset, citation entries and license.

## Docker and CI

```sh
docker build -t rap-v4-checks .
docker run --rm rap-v4-checks
```

The container defaults to Python checks only. It is not a Lean/TeX image. The base manifest and CI actions are pinned, but neither Docker nor the remote CI workflow was executed during preparation. To keep container reports, mount an output directory writable by UID 10001; the example without a mount prints the result but does not persist its internal report after removal.

## Governance & AI Audit Policy

All agents and contributors must adhere to the rules defined in `governance/AI_AUDIT_POLICY.md` and the `governance/AGENTS.md` steering baseline.

- **Rule:** Do not introduce physical constants, target cosmology values, Standard Model targets, or calibrated UIDT parameters into pregeometry growth rules, null ensembles, dashboards, or diagnostics unless a dedicated reviewed task explicitly requires it.
- **Rule:** Runtime artifacts must only be generated under `verification/data/pregeometry/`.

## Manuscript, DOI and release limits

The original corrected working source body and historical decision boxes are retained. Bibliographic identity errors are repaired in the external manuscript bibliography. The full root bibliography includes seven additional guide comparisons; those are not silently imported into the manuscript. No final manuscript PDF is supplied: compilation and visual inspection are still required elsewhere.

The existing DOI 10.5281/zenodo.22731224 identifies the base version only. Confirm the actual date, version label and destination DOI for a new correction. `.zenodo.json` is a root override for GitHub integration; uploading it as an ordinary file does not import it. The wrapped legacy API body is in `metadata/zenodo-deposition.json`. No API write or publication is performed. The prior legacy-schema qualification for documented `version`/`language` fields remains applicable.

The stated CC BY 4.0 is retained for this working release material; review actual file rights and software licensing before publication. Dependencies and third-party works retain their own terms. No external cited full texts are bundled.

## Legacy Notice (UIDT)

Under PI Decision D19 & D20, the continuous real scalar field S(x) and the "Unified Information-Density Theory" (UIDT) nomenclature have been demoted to a historical macroscopic effective-field description. Legacy scalar/EFT materials are quarantined in the `museum/` directory and are **not** active ontology.
