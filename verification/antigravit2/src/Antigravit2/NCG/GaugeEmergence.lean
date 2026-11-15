import Mathlib

/-!
# Gauge emergence: relative central phases on candidate matter bimodules

Evidence: [A] for the abstract group-theoretic lemmas below;
[D] for any interpretation as a RAP matter representation or a physical gauge group.

We model the central phases of the three simple summands
  M₃(ℂ) ⊕ M₂(ℂ) ⊕ ℂ
by an arbitrary abelian phase group P.  The intended physical instance is
P = U(1), but the proofs do not depend on a particular construction of the
unit circle.

The two candidate off-diagonal bimodule sectors (3,2) and (2,1) carry the
relative characters p₃ p₂⁻¹ and p₂ p₁⁻¹.  This file proves that the joint
relative-phase map P³ → P² is surjective and that its kernel is the diagonal
subgroup.  It does NOT construct these bimodules from RAP axioms or select
them physically.  Thus it tests the highlighted central-phase mechanism
without assuming the Standard-Model gauge group.
-/

namespace Antigravit2.NCG.GaugeEmergence

universe u

variable (Phase : Type u) [CommGroup Phase]

/-- Central phases for the M₃, M₂ and scalar summands, in that order. -/
abbrev CentralPhases : Type u := Phase × (Phase × Phase)

/-- Relative phases seen by candidate off-diagonal matter sectors (3,2) and (2,1). -/
def relativeMatterCharacters (z : CentralPhases Phase) : Phase × Phase :=
  (z.1 * z.2.1⁻¹, z.2.1 * z.2.2⁻¹)

/-- The relative-phase map sends the identity central triple to the identity pair. -/
theorem relativeMatterCharacters_one :
    relativeMatterCharacters Phase (1 : CentralPhases Phase) = (1 : Phase × Phase) := by
  simp [relativeMatterCharacters]

/-- The relative-phase map is a group homomorphism: it preserves multiplication. -/
theorem relativeMatterCharacters_mul (x y : CentralPhases Phase) :
    relativeMatterCharacters Phase (x * y) =
      relativeMatterCharacters Phase x * relativeMatterCharacters Phase y := by
  rcases x with ⟨x₃, x₂₁⟩
  rcases x₂₁ with ⟨x₂, x₁⟩
  rcases y with ⟨y₃, y₂₁⟩
  rcases y₂₁ with ⟨y₂, y₁⟩
  apply Prod.ext
  · simp [relativeMatterCharacters, mul_assoc, mul_comm, mul_left_comm]
  · simp [relativeMatterCharacters, mul_assoc, mul_comm, mul_left_comm]

/-- Every pair of relative phases is realized by some central triple. -/
theorem relativeMatterCharacters_surjective :
    Function.Surjective (relativeMatterCharacters Phase) := by
  intro pq
  rcases pq with ⟨q₃₂, q₂₁⟩
  refine ⟨(q₃₂, (1, q₂₁⁻¹)), ?_⟩
  simp [relativeMatterCharacters]

/-- The joint relative-phase map has precisely the diagonal central subgroup as kernel. -/
theorem relativeMatterCharacters_eq_one_iff (z : CentralPhases Phase) :
    relativeMatterCharacters Phase z = (1 : Phase × Phase) ↔
      z.1 = z.2.1 ∧ z.2.1 = z.2.2 := by
  constructor
  · intro h
    have h₃₂ : z.1 * z.2.1⁻¹ = 1 := by
      have h' := congrArg Prod.fst h
      simpa [relativeMatterCharacters] using h'
    have h₂₁ : z.2.1 * z.2.2⁻¹ = 1 := by
      have h' := congrArg Prod.snd h
      simpa [relativeMatterCharacters] using h'
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
    simp [relativeMatterCharacters, h₃₂, h₂₁]

/-- A diagonal central phase acts trivially on both relative characters. -/
theorem diagonal_phase_is_neutral (p : Phase) :
    relativeMatterCharacters Phase (p, (p, p)) = (1, 1) := by
  simp [relativeMatterCharacters]

/-!
## Interpretation boundary

For P = U(1), the theorem gives a surjective map U(1)^3 → U(1)^2:
  (z₃,z₂,z₁) ↦ (z₃ z₂⁻¹, z₂ z₁⁻¹),
with diagonal U(1) as kernel.  Hence the *chosen pair* of off-diagonal
sectors detects two independent relative U(1) phases.  A single selected
sector detects one U(1) character.

This is a conditional representation-level result, not a derivation of
the physical Standard-Model gauge group.  The RAP algebra currently does
not select the matter bimodule, its multiplicities, a real structure J,
a unimodularity constraint, or a spacetime-local gauge action.  Those are
separate construction obligations.
-/

end Antigravit2.NCG.GaugeEmergence
