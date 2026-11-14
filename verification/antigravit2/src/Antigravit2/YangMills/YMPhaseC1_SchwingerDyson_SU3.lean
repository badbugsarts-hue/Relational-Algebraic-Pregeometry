/-
  YMPhaseC1_SchwingerDyson_SU3.lean — conditional Phase C1 interface

  This file proves scalar consequences of explicit Witten-gap and uniform
  susceptibility-bound inputs. It does not formalize SU(3) geometry,
  Makeenko–Migdal identities, Helffer–Sjöstrand, or a Combes–Thomas estimate.
  Those analytic inputs remain open research obligations.
-/

import Antigravit2.YangMills.YMPhaseB_SU3_Schur

namespace YMPhaseC1

/-- Explicit analytic inputs needed before the C1 scalar consequences apply.

`effectiveGap` is an assumed uniform lower bound for the relevant Witten
operator. `C_CT` is an assumed volume-uniform constant in an off-diagonal
resolvent estimate. Neither field is derived from the finite lattice action.
-/
structure AnalyticInputs where
  ricciLowerBound : ℝ
  sigmaSD : ℝ
  effectiveGap : ℝ
  C_CT : ℝ
  h_effectiveGap : effectiveGap = ricciLowerBound + sigmaSD
  h_effectiveGap_pos : 0 < effectiveGap
  h_C_CT_pos : 0 < C_CT

/-- Scalar upper bound proposed for a susceptibility row sum. -/
noncomputable def susceptibilityUpperBound (d : AnalyticInputs) : ℝ :=
  d.C_CT / d.effectiveGap

theorem susceptibilityUpperBound_pos (d : AnalyticInputs) :
    0 < susceptibilityUpperBound d := by
  unfold susceptibilityUpperBound
  exact div_pos d.h_C_CT_pos d.h_effectiveGap_pos

/-- A certificate connecting a concrete row-sum quantity to the proposed
resolvent upper bound. Establishing this certificate is the substantive C1
problem and is not proved in this module.
-/
structure UniformSusceptibilityCertificate (d : AnalyticInputs) where
  S_off : ℝ
  h_S_off_nonneg : 0 ≤ S_off
  h_S_off_le : S_off ≤ susceptibilityUpperBound d

/-- Choose the Phase B splitting parameter from the certified row-sum bound. -/
noncomputable def optimalSplittingParameter
    (d : AnalyticInputs) (c : UniformSusceptibilityCertificate d) : ℝ :=
  YMPhaseB.optimalAlpha c.S_off

theorem optimalSplittingParameter_bounds
    (d : AnalyticInputs) (c : UniformSusceptibilityCertificate d) :
    0 < optimalSplittingParameter d c ∧
      optimalSplittingParameter d c < 1 := by
  unfold optimalSplittingParameter
  rcases YMPhaseB.optimalAlpha_yields_kappa_half c.S_off c.h_S_off_nonneg with
    ⟨h_pos, h_lt_one, _⟩
  exact ⟨h_pos, h_lt_one⟩

theorem optimalSplittingParameter_kappa
    (d : AnalyticInputs) (c : UniformSusceptibilityCertificate d) :
    YMPhaseB.schurKappa (optimalSplittingParameter d c) c.S_off = 1 / 2 := by
  unfold optimalSplittingParameter
  exact (YMPhaseB.optimalAlpha_yields_kappa_half c.S_off c.h_S_off_nonneg).2.2

/-- If a numerical Ricci lower bound `rho` is independently established, then
any perturbation strictly larger than `-rho` preserves a positive scalar
curvature bound. This arithmetic lemma does not establish geometric `rho`.
-/
theorem positive_curvature_after_perturbation
    (rho perturbation : ℝ) (h_rho : 0 < rho)
    (h_perturbation : -rho < perturbation) :
    0 < rho + perturbation := by
  linarith

end YMPhaseC1
