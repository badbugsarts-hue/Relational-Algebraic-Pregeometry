import Antigravit2.NCG.GaugeEmergence
import Antigravit2.NCG.Krajewski321

/-!
# Gauge test on the existing RAP [3,2,1] Krajewski graph

Evidence boundary:
* [A]: the finite list calculations and group identities proved here.
* [D]: assigning a relative central character to an edge of the RAP graph.
* Not established: actual complex bimodule fibres, left/right *-representations,
  a Hilbert-space completion, a nontrivial real structure on that space,
  unimodularity, or a local gauge group.

This file deliberately consumes `SM.smDiagram321`; it does not introduce a
new graph or assume a Standard-Model gauge group.  The current Krajewski
record contains only natural-number block labels and multiplicities, so
the character assignment below is an explicitly labelled diagnostic.
-/

namespace Antigravit2.NCG.GaugeEmergence

universe u

variable (Phase : Type u) [CommGroup Phase]

/-- Read the central phase assigned to one of the three RAP block labels. -/
def phaseAt321Block (z : CentralPhases Phase) (block : ℕ) : Phase :=
  if block = 3 then z.1 else
  if block = 2 then z.2.1 else
  if block = 1 then z.2.2 else 1

/-- Relative phase attached diagnostically to an oriented Krajewski edge. -/
def edgeRelativePhase321 (z : CentralPhases Phase) (edge : Bimodule) : Phase :=
  phaseAt321Block Phase z edge.leftBlock *
    (phaseAt321Block Phase z edge.rightBlock)⁻¹

/-- Relative phases on the actual edge list stored in smDiagram321. -/
def sm321EdgePhaseVector (z : CentralPhases Phase) : List Phase :=
  SM.smDiagram321.edges.map (edgeRelativePhase321 Phase z)

/-- The current RAP graph is exactly the three labelled, unit-multiplicity edges. -/
theorem sm321_edge_data :
    SM.smDiagram321.edges.map
      (fun e => (e.leftBlock, e.rightBlock, e.multiplicity)) =
        [(3, 2, 1), (2, 1, 1), (3, 1, 1)] := by
  rfl

/-- Evaluate the relative-character diagnostic on all three actual RAP edges. -/
theorem sm321_edge_phase_vector (z : CentralPhases Phase) :
    sm321EdgePhaseVector Phase z =
      [z.1 * z.2.1⁻¹, z.2.1 * z.2.2⁻¹, z.1 * z.2.2⁻¹] := by
  simp [sm321EdgePhaseVector, edgeRelativePhase321, phaseAt321Block,
    SM.smDiagram321]

/-- The long edge (3,1) is the composite of the two adjacent edge characters. -/
theorem sm321_triangle_character_relation (z : CentralPhases Phase) :
    z.1 * z.2.2⁻¹ =
      (z.1 * z.2.1⁻¹) * (z.2.1 * z.2.2⁻¹) := by
  group

/-- Therefore the third edge carries no independent relative central phase. -/
theorem sm321_edge_phase_vector_rank_two (z : CentralPhases Phase) :
    sm321EdgePhaseVector Phase z =
      [z.1 * z.2.1⁻¹,
       z.2.1 * z.2.2⁻¹,
       (z.1 * z.2.1⁻¹) * (z.2.1 * z.2.2⁻¹)] := by
  rw [sm321_edge_phase_vector]
  have h := sm321_triangle_character_relation Phase z
  rw [h]

/-- The graph-level diagnostic has the same diagonal kernel as the two-edge map. -/
theorem sm321_edge_characters_trivial_iff (z : CentralPhases Phase) :
    (∀ q ∈ sm321EdgePhaseVector Phase z, q = 1) ↔
      z.1 = z.2.1 ∧ z.2.1 = z.2.2 := by
  rw [sm321_edge_phase_vector]
  constructor
  · intro h
    have h₃₂ : z.1 * z.2.1⁻¹ = 1 := h _ (by simp)
    have h₂₁ : z.2.1 * z.2.2⁻¹ = 1 := h _ (by simp)
    constructor
    · calc
        z.1 = (z.1 * z.2.1⁻¹) * z.2.1 := by group
        _ = 1 * z.2.1 := by rw [h₃₂]
        _ = z.2.1 := by simp
    · calc
        z.2.1 = (z.2.1 * z.2.2⁻¹) * z.2.2 := by group
        _ = 1 * z.2.2 := by rw [h₂₁]
        _ = z.2.2 := by simp
  · rintro ⟨h₃₂, h₂₁⟩
    simp [h₃₂, h₂₁]

/-!
## What this test has and has not connected

Connected:
* the exact three edge labels and multiplicities in `SM.smDiagram321`;
* a conditional assignment of relative central characters to those edges;
* the triangle relation showing the (3,1) character is dependent on (3,2)
  and (2,1).

Not connected:
* `KrajewskiCore.Bimodule` has only `leftBlock`, `rightBlock` and
  `multiplicity`; it has no fibre space or algebra actions;
* `Dirac321.spectralTriple321` still uses the trivial algebra/Hilbert space
  `ℂ`, with identity Dirac precursor;
* `RealStructure` currently defines an anti-linear map and an involutivity
  relation, but not unitarity/isometry on a constructed matter Hilbert space;
* no unimodularity constraint or local spacetime-dependent gauge action is
  present in this chain.

So this is the first graph-attached group-character test, not yet a
representation-theoretic gauge-emergence theorem.
-/

end Antigravit2.NCG.GaugeEmergence
