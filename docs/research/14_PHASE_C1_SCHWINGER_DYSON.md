# Phase C1: Schwinger–Dyson and susceptibility bounds

**Status:** conditional research interface added after commit `55a01dd`; no physical evidence upgrade. The finite-volume geometric and analytic inputs below are not established by the Lean module.

The proposed target is a volume-uniform bound on the off-diagonal plaquette covariance row sum

\[
S_{\rm off}=\sup_{p\ge p_0}\sup_{\sigma,\square}
\sum_{\square'\ne\square}
\left|\operatorname{Cov}_{\sigma}(\Phi_{\square},\Phi_{\square'})\right|<\infty.
\]

The supplied argument sketches a possible route through geometry of a finite product of compact groups, a weighted Hodge/Bochner operator, and a spatial decay estimate for its inverse. These ingredients are not interchangeable: positive Ricci curvature of each link group does not by itself control the Hessian of the interacting plaquette potential, the inverse operator's off-diagonal decay, or the sum uniformly in volume.

## What follows from standard identities

For a smooth potential `V` and normalized Haar measure on a compact Lie group product, integration by parts gives

\[
\mathbb E_{e^{-V}}[-\Delta F+\langle\nabla V,\nabla F\rangle]=0.
\]

This is the Gibbs integration-by-parts / Schwinger–Dyson identity. Makeenko–Migdal loop equations are particular identities for Wilson-loop observables and include loop-dependent contact/splitting terms; the generic identity above is not itself the full loop equation. Existing lattice derivations work in specific settings and do not supply the proposed C1 covariance estimate automatically ([Shen, Smith & Zhu, 2026](https://doi.org/10.1515/ans-2023-0226)).

Under suitable smoothness and operator-domain conditions, Helffer–Sjöstrand represents covariance using the inverse of a weighted operator on gradients. On a Riemannian manifold the corresponding one-form operator includes the connection Laplacian, the Ricci endomorphism, and the potential Hessian. In the usual nonnegative convention the connection-Laplacian term is `∇*∇`; signs must be fixed consistently with the chosen Laplacian convention. Such a representation alone gives no off-diagonal decay or volume-uniform row-sum estimate. The Euclidean formulation and its required strict Hessian lower bound are stated explicitly in Bauerschmidt–Bodineau, Appendix A ([source](https://d-nb.info/1202686133/34)).

## Ricci normalization and the pointwise Hessian estimate

For `𝔤=su(N)` the Killing form is `B(X,Y)=2N Re Tr(XY)`. With a bi-invariant metric, `Ric=-B/4` as a `(0,2)` tensor. For the scaled metric

\[
g_c(X,Y)=-c\,\operatorname{ReTr}(XY),\qquad c>0,
\]

this gives

\[
\operatorname{Ric}(X,Y)=-\frac N2\operatorname{ReTr}(XY)
  =\frac{N}{2c}g_c(X,Y),\qquad
\kappa_c(\mathrm{SU}(N))=\frac{N}{2c}.
\]

Thus `−Re Tr(XY)` gives `κ=N/2`, while `−(1/N)Re Tr(XY)` gives `κ=N²/2`; for SU(3) these are `3/2` and `9/2`, respectively. The value `3/4` does not follow from either convention. This agrees with the cited curvature paper's `κ_SU(N)=N/2` for `−Tr(XY)` ([Theorem 5 and Table I](https://hexagonmath.org/pdf/2610.00341v4), lines 101–111, 130–146). This calculation assumes that the inner product supplied for the assessment is exactly `−(1/N)Re Tr(XY)`; the assessment PDF itself is not present here.

For the normalized plaquette `Φ□=N⁻¹ Re Tr(U□)` and the product metric made from `g₁=−Re Tr(XY)`, differentiating along product geodesics and applying Hilbert–Schmidt Cauchy–Schwarz gives the pointwise estimate

\[
|\nabla^2\Phi_\square(X,X)|
\le \frac4N\sum_{\ell\in\partial\square}\|X_\ell\|_{g_1}^2.
\]

For

\[
V_\sigma=-\sum_\square\left(\widetilde\beta_\square(\sigma)\Phi_\square-
  \frac\alpha2\Phi_\square^2\right),\qquad
\widetilde\beta_\square=\beta_{\rm ref}+\sqrt\alpha\,\sigma_\square,
\]

the Hessian is

\[
\nabla^2V_\sigma(X,X)=\sum_\square\left[-(\widetilde\beta_\square-\alpha\Phi_\square)
  \nabla^2\Phi_\square(X,X)+\alpha\bigl(X\Phi_\square\bigr)^2\right].
\]

Since `|Φ□|≤1`, each link belongs to six plaquettes in a standard 4D lattice, and the last term is nonnegative, this yields the lower bound

\[
\nabla^2V_\sigma(X,X)\ge -\frac{24}{N}
  \left(\sup_\square|\widetilde\beta_\square(\sigma)|+\alpha\right)
  \sum_\ell\|X_\ell\|_{g_1}^2.
\]

Consequently the pointwise Bakry–Émery tensor has the sufficient lower bound

\[
\operatorname{Ric}+\nabla^2V_\sigma\succeq
\left[\frac N2-\frac{24}{N}
  \left(\sup_\square|\widetilde\beta_\square(\sigma)|+\alpha\right)\right]I
\]

in the `g₁` convention. At `σ=0`, positivity by this estimate requires `β_ref+α<N²/48` (for SU(3), `β_ref+α<3/16`), not merely `β_ref<N²/48`.

This estimate still does not give a uniform-in-`σ` Bakry–Émery bound: the Gaussian HS field is unbounded and `sup_σ|β_ref+√α σ□|=∞`. It also does not prove the Witten spectral gap in expectation. The proposed `C_grad`, neighbor count, and `C_CT/γ_Witten` row-sum estimate need separate derivations with constants uniform in `p`, boundary conditions, and `σ`. A spectral gap controls the operator norm of an inverse; it does not alone prove exponential off-diagonal decay. A Combes–Thomas estimate would need its own hypotheses and proof, followed by a lattice shell-sum estimate.

## Lean interface added

[`YMPhaseC1_SchwingerDyson_SU3.lean`](../../verification/antigravit2/src/Antigravit2/YangMills/YMPhaseC1_SchwingerDyson_SU3.lean) formalizes only conditional scalar implications:

- given a positive effective Witten-gap input and a positive `C_CT`, the quotient `C_CT / effectiveGap` is positive;
- given a separate certificate that an actual `S_off` is nonnegative and lies below that quotient, the Phase B choice of `α` lies in `(0,1)` and yields `κ=1/2`;
- a positive scalar curvature lower bound remains positive under a perturbation larger than its negative.

The structure fields are explicit assumptions, not proofs that the Witten operator has a gap, that `C_CT` is uniform, or that any covariance row sum obeys the bound. The module does not formalize the Lie group, Haar geometry, Makeenko–Migdal identities, Helffer–Sjöstrand, Combes–Thomas decay, transfer contraction, or a Yang–Mills mass gap. The endpoint of Phase C1 is therefore still open.

## Next analytic obligations

1. Verify that the metric used in the source assessment matches the stated convention; the Ricci scaling is derived above conditionally on that convention.
2. Control the unbounded HS background or use an argument that does not require uniform pointwise convexity in `σ`; a negative Hessian contribution cannot be hidden inside a named `Σ_SD` without derivation.
3. Prove a Witten-operator gap in the intended coupling range.
4. Establish a Combes–Thomas or equivalent off-diagonal resolvent estimate with constants uniform in volume, then sum over plaquette shells.
5. Prove the link from the resulting concrete covariance certificate to the Phase B Hessian bound and separately justify any transfer-operator conclusions.

No claim is made that the Schwinger–Dyson self-energy is positive in the crossover regime. Naming such a term does not establish its sign.
