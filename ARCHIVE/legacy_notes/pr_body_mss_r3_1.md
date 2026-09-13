# mss-r3-1: Add UIDT Ontology v4.0 DRAFT-007-R3-1 (108 pp canonical manuscript)

## Summary
Adds `manuscript/UIDT_Ontology_v4_0_DRAFT-007-R3-1.tex` — the current canonical v4.0 manuscript
(4841 lines, 108 pp, three-part architecture: Part I Pregeometric Kernel [D] · Part II Continuous
Limit [E]-capped · Part III Effective Information Field). This is the O-4-gated, compile-clean,
cross-ref-clean output of the 2026-07-13 audit cycle (Sonnet extraction -> Fable adjudication ->
Opus gatekeeping). It replaces the previously committed 2.2 KB placeholder
`manuscript/UIDT_Ontology_v4_0_0.tex` as the active working manuscript — **the stub is left in
place in this PR** (not deleted) pending an explicit PI decision on repo cleanup.

This PR is advisory scaffolding only. It authorizes no evidence-class change, no freeze, no
release. Governance status of open items (FSS-monodromy module refusal, O-1 tension rows, PBH
exclusion, Part III-vs-Part-IV architecture) is tracked separately in the manuscript hub and is
**unaffected by this PR** — this PR only lands the file.

## Claims Table
| Claim ID | Proposition | Stratum | Evidence Class |
|---|---|---|---|
| PR-MSS-R3-1-01 | The attached .tex compiles with pdflatex, 3 passes, 0 errors, 0 warnings | III (repo-state fact) | [B] (verifiable by Reproduction Note) |
| PR-MSS-R3-1-02 | All \ref/\cite in the attached .tex resolve (173 labels/75 refs; 99 bibitems/60 cited) | III (repo-state fact) | [B] (verifiable by Reproduction Note) |
| PR-MSS-R3-1-03 | No forbidden target literal (16.339, 49/3, 17/3000, K_S=Δ/γ, (2,3), (3,2,1)) appears as a computational target/loss/gate in this file | III (repo-state fact) | [B] (grep-verifiable) |
| PR-MSS-R3-1-04 | Physics content of the manuscript itself (evidence classes on individual claims) | I/II/III (mixed, per-claim) | unchanged by this PR — inherited from the source file, not asserted here |

## Reproduction Note
```
cd manuscript
pdflatex -interaction=nonstopmode UIDT_Ontology_v4_0_DRAFT-007-R3-1.tex
pdflatex -interaction=nonstopmode UIDT_Ontology_v4_0_DRAFT-007-R3-1.tex
pdflatex -interaction=nonstopmode UIDT_Ontology_v4_0_DRAFT-007-R3-1.tex
grep -c "Undefined" UIDT_Ontology_v4_0_DRAFT-007-R3-1.log   # expect 0
grep -nE "16\.339|49/3|17/3000|K_S *= *.Delta */ *.gamma" UIDT_Ontology_v4_0_DRAFT-007-R3-1.tex   # review only, none as a code-target
```
Deterministic; no simulation; LaTeX compilation and grep are static checks, not a simulation run.

## DOI Check
Not applicable to this PR — no new citations are introduced; the file's existing bibliography
(99 \bibitem, 60 cited) is unchanged from the source draft. A full DOI/arXiv sweep of that
bibliography is tracked as a separate work package (PLAN_HAIKU45.md / WP H0) and is **not**
represented as complete by this PR.

## What this PR does NOT do
- Does not merge (PI-only).
- Does not delete or modify `manuscript/UIDT_Ontology_v4_0_0.tex` (the prior stub).
- Does not resolve the FSS-monodromy refusal (O-0), the PBH exclusion (O-2/O-3), or the Part
  III-vs-Part-IV architecture question — these remain open PI decisions tracked in the hub.
- Does not touch any protected path other than `manuscript/`.

## PI sign-off required before merge
Per AI_AUDIT_POLICY.md: CI green, explicit PI sign-off, and (for any [A]/[A-]/[B] claim change)
external counter-signature. This PR changes only which manuscript file is present in the repo; it
does not itself assert any evidence-class upgrade.
