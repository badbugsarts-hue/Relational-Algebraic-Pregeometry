# Relational-Algebraic Pregeometry Programme (RAP) 

[![Status: Canonical Freeze](https://img.shields.io/badge/Status-Canonical%20Freeze-blue.svg)]()
[![Verification: Lean 4](https://img.shields.io/badge/Verification-Lean%204-purple.svg)]()
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)]()

## Mission Statement
This repository contains the formal architecture and manuscript source for **RAP v4.0** (formerly UIDT). The framework replaces continuous physical fields with a discrete, finite relational-algebraic kernel ($\mathcal{A}_F$). It is governed by a strict "falsification-first" discipline and explicitly rejects anthropocentric biases and unverified continuum assumptions.

## Governance & AI Audit Policy
All agents and contributors must adhere to the rules defined in `governance/AI_AUDIT_POLICY.md` and the `governance/AGENTS.md` steering baseline.
- **Rule:** Do not introduce physical constants, target cosmology values, Standard Model targets, or calibrated UIDT parameters into pregeometry growth rules, null ensembles, dashboards, or diagnostics unless a dedicated reviewed task explicitly requires it.
- **Rule:** Runtime artifacts must only be generated under `verification/data/pregeometry/`.

## Core Architecture
The physical passage from the finite kernel to apparent continuity is treated as an open thermodynamic limit. The formal separation is defined as:
`BlockPartition` $\to$ `FiniteAlgebraSignature` $\to$ `SpectralTriple`

*Note: Recent mathematical proofs regarding finite-time blow-ups in 3D fluid dynamics (Navier-Stokes) serve as the external validation for our postulate of Topological Condensation and Forgetful Functor Collapse at extreme relational densities.*

## Lean 4 Formalization
We enforce **Gap Localization before Construction (GLBC)**. Mathematical claims, specifically the *Staircase Conjecture* for the origin of the $G_{SM}$ block partition, are subjected to automated, blinded verification in Lean 4 to prevent target leakage. 

- **Current Snapshot:** `f1ae5486`
- **Proof State:** 18/18 reachable modules exit successfully. Open obligations (`sorry` tags) are explicitly registered as research gaps.

## Setup & Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Run the test suite: `py -m pytest verification/tests/ -q -p no:cacheprovider`

## Legacy Notice (UIDT)
Under PI Decision D19 & D20, the continuous real scalar field $S(x)$ and the "Unified Information-Density Theory" (UIDT) nomenclature have been demoted to a historical macroscopic effective-field description. Legacy scalar/EFT materials are quarantined in the `museum/` directory and are **not** active ontology.


