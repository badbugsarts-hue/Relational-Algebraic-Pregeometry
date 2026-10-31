# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v4.0.1] - 2026-10-27 — Repository support preparation

### Added
- Newly wrote RAP verification entry points, exact structural engine, precision diagnostics, tests, data-availability text, status generation, ledger/schema files and CANONICAL documents.
- Added 12 actual research notes and a generated navigation index; no fictional 47-note collection.
- Added locked dependency artefact hashes, a digest-pinned Python Dockerfile and pinned CI actions. Docker, Lean and manuscript compilation were not executed.
- Added `rap/` Python package with structural, numerical and validation modules.
- Added `results/` directory with verification outputs, execution receipts and partition data.
- Added `provenance/` directory with container-pin, dependency-lock, source-snapshot and previous manuscript input.
- Added `metadata/` directory with format-validation and Zenodo deposition records.

### Changed
- Kept calibrated values out of the structural solver; reference arithmetic is an explicit separate comparator.
- Preserved the previous corrected manuscript body and D19–D25 boxes. Externalized the corrected 124-record manuscript bibliography and retained the old inline bibliography for provenance.
- Upgraded LEDGER/CLAIMS.json from 1 stub claim to 30 curated claims with full schema validation.

### Fixed
- Removed `.lake/` Lean build artifacts from git tracking (126 files).
- Removed `scratch/` test files from git tracking.
- Merged `.gitignore` to properly exclude `.lake/`, `.venv/`, `dist/`, IDE configs.

### Not included
- No new PI decision, numerical lattice/MC evidence, physics proof, DOI assignment, canonical author freeze or online publication.

## [v4.0.0] - 2026-09-13

### Added
- Finalized manuscript for `Relational_Algebraic_Pregeometry_v4_0.tex` for the v4.0 Release.
- Updated `CHANGELOG.md` to track release.
- Added LaTeX intermediate files to `.gitignore`.

## [Unreleased]

### Added
- Initial project documentation: `README.md`, `ROADMAP.md`, `CONTRIBUTING.md`, `requirements.txt`.
- Agentic IDE steering baselines (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`, `.windsurfrules`).
- AI skills configurations (`.ai/skills/pregeometry-harness.md`, etc.).

### Changed
- Clarified workspace scope as purely experimental pregeometry benchmark workspace, strictly isolated from canonical UIDT physics targets.
