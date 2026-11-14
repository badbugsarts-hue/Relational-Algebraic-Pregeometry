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

## Metric normalization is unresolved

The proposed value `κ_Haar = N_c/4` needs a derivation in the exact metric convention before it can be encoded as an SU(3) theorem. For a compact simple group, `Ric = -B/4` as a tensor for a bi-invariant metric; the numerical lower-Ricci eigenvalue depends on the metric scale. A recent lattice-gauge curvature paper uses `⟨X,Y⟩=-Tr(XY)` and reports `κ_SU(N)=N/2` in that convention ([Theorem 5 and Table I](https://hexagonmath.org/pdf/2610.00341v4), lines 101–111, 130–146). Rescaling the metric changes the numerical curvature bound. Therefore this value cannot simply be transferred to `⟨X,Y⟩=-(1/N_c) Re Tr(XY)` or identified with a separately normalized gauge Casimir without checking the basis and normalization in the cited assessment document. That document is not present in this repository.

The proposed `C_grad`, neighbor count, and `C_CT/γ_Witten` row-sum bound also need proofs with constants uniform in `p`, boundary conditions, and `σ`. A spectral gap controls the operator norm of an inverse; it does not alone prove exponential off-diagonal decay. A Combes–Thomas estimate would need its own hypotheses and proof, followed by a lattice shell-sum estimate.

## Lean interface added

[`YMPhaseC1_SchwingerDyson_SU3.lean`](../../verification/antigravit2/src/Antigravit2/YangMills/YMPhaseC1_SchwingerDyson_SU3.lean) formalizes only conditional scalar implications:

- given a positive effective Witten-gap input and a positive `C_CT`, the quotient `C_CT / effectiveGap` is positive;
- given a separate certificate that an actual `S_off` is nonnegative and lies below that quotient, the Phase B choice of `α` lies in `(0,1)` and yields `κ=1/2`;
- a positive scalar curvature lower bound remains positive under a perturbation larger than its negative.

The structure fields are explicit assumptions, not proofs that the Witten operator has a gap, that `C_CT` is uniform, or that any covariance row sum obeys the bound. The module does not formalize the Lie group, Haar geometry, Makeenko–Migdal identities, Helffer–Sjöstrand, Combes–Thomas decay, transfer contraction, or a Yang–Mills mass gap. The endpoint of Phase C1 is therefore still open.

## Next analytic obligations

1. Fix and derive the SU(3) metric normalization and its Ricci lower bound from the chosen invariant inner product.
2. Compute or bound the Hessian of the damped plaquette potential uniformly over configurations and HS backgrounds; a negative Hessian contribution cannot be hidden inside a named `Σ_SD` without derivation.
3. Prove a Witten-operator gap in the intended coupling range.
4. Establish a Combes–Thomas or equivalent off-diagonal resolvent estimate with constants uniform in volume, then sum over plaquette shells.
5. Prove the link from the resulting concrete covariance certificate to the Phase B Hessian bound and separately justify any transfer-operator conclusions.

No claim is made that the Schwinger–Dyson self-energy is positive in the crossover regime. Naming such a term does not establish its sign.
