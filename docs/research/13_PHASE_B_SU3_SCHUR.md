# Phase B: SU(3), Schur-Schranke und Intervallzertifikat

**Status:** Arbeitsnotiz zu Commit `55a01dd` (13 November 2026); formale Aussagen beziehen sich auf die im Modul genannten Lean-Deklarationen. Keine physikalische Evidenzaufwertung.

Das Modul [YMPhaseB_SU3_Schur.lean](../../verification/antigravit2/src/Antigravit2/YangMills/YMPhaseB_SU3_Schur.lean) bündelt drei Teile der Phase B: die arithmetische Spezialisierung auf den Farbblock `N_c = 3`, eine bedingte Zeilensummen-Schranke für die Kovarianzform und ein Intervalllemma für `Γ_YM`.

## B3: Spezialisierung auf `N_c = 3`

Aus der im Modul gesetzten Partition `(3, 2, 1)` folgen per Rechnung

\[
\dim_{\mathbb R}\mathfrak{su}(3)=3^2-1=8,\qquad C_g=3,
\qquad 3\dim_{\mathbb R}\mathfrak{su}(3)=24.
\]

`su3_openai_constants_exact` prüft diese Definitionen und `su3_traceAnomalyAmplitude_pos` zeigt die Positivität der dort definierten Größe `24 / π⁴`. `su3_beta_bridge` prüft für die im Modul definierte Konversionsregel `β_submission = N_c · β_lgt` den Spezialfall `N_c = 3`.

Diese Deklarationen sind arithmetische Spezialisierungen der eingeführten Definitionen. Sie formalisieren für sich genommen weder die Lie-Algebra `su(3)` noch die Gültigkeit einer externen Konvention, eines Casimir-Werts, einer RG-Gleichung oder eines Werts aus `assessment-1.pdf`. Insbesondere wird die angegebene Konventionsbrücke hier als Definition verwendet.

## B1: Bedingte Schur-Zeilensummen-Schranke

Für eine reelle symmetrische Matrix `C` mit Zeilensummen

\[
\sum_j |C_{ij}| \le 1+S_{\rm off}
\]

liefert der symmetrische Schur-Test

\[
v^T C v \le (1+S_{\rm off})\,\|v\|^2.
\]

Der diagonale Anteil wird dabei durch `Var(Φᵢ) ≤ 1` beschränkt; der Rest ist die angenommene gleichmäßige Schranke `S_off` der absoluten Off-Diagonal-Zeilensumme. Das Modul beweist die elementare gewichtete Paarungleichung `weighted_pair_am_gm`, formalisiert aber derzeit nicht den Übergang von einer endlichen Kovarianzmatrix und ihrer Zeilensumme zur obigen quadratischen Form. `schur_hessian_lower_bound` nimmt diese quadratische Formschranke als Hypothese entgegen.

Mit `κ(α,S_off) = α(1+S_off)` zeigt `schurKappa_in_unit_interval`, dass `α > 0`, `S_off ≥ 0` und `S_off < 1/α - 1` `0 < κ < 1` implizieren. Die Definition

\[
\alpha(S_{\rm off})=\frac{1}{2(1+S_{\rm off})}
\]

ergibt unter `S_off ≥ 0` exakt `κ = 1/2`, wie `optimalAlpha_yields_kappa_half` zeigt. Das gilt für jeden reellen endlichen Eingabewert `S_off`; es beweist nicht, dass die physikalische Suszeptibilität endlich oder gleichmäßig im Volumen beschränkt ist. Eine positive uniforme Krümmungs- oder Spektrallücke folgt erst, wenn die weiteren Voraussetzungen des jeweiligen Transfer- bzw. Bakry–Émery-Arguments erfüllt und dessen Konstante kontrolliert sind.

## B2: Intervalllemma

`VerifiedIntervalBounds` kodiert rationale oder reelle Grenzen in der Form

\[
0\le κ_{\rm lo}\le κ_{\rm hi}<1,\quad
0<C_{\rm lo}\le C_{\rm hi},\quad
0<M_{\rm lo}\le M_{\rm hi}.
\]

`gammaInterval_valid` leitet daraus die Positivität und Ordnung der definierten Schranken

\[
\frac{1-κ_{\rm hi}}{C_{\rm hi}M_{\rm hi}}
\le
\frac{1-κ_{\rm lo}}{C_{\rm lo}M_{\rm lo}}.
\]

Das ist ein Ordnungslemma für die Definitionen der Intervallenden. Es setzt zertifizierte Eingangsintervalle voraus und enthält noch keine numerische Auswertung, keinen Algorithmus für rationale Einschließungen und keinen Nachweis, dass ein konkretes `Γ_YM` in diesem Intervall liegt. Dafür braucht es zusätzlich einen formalisierten Zusammenhang zwischen `Γ_YM` und den eingeschlossenen Größen sowie nachprüfbare Eingabedaten.

## Offene Arbeit: C1

Die zentrale offene Voraussetzung bleibt eine gleichmäßige Schranke für

\[
S_{\rm off}=\sup_{p,\,σ,\,\square}
\sum_{\square'\ne\square}
\left|\operatorname{Cov}_{σ}(Φ_{\square},Φ_{\square'})\right|.
\]

Eine exponentielle Korrelationsschranke plus kontrolliertes Schalenwachstum würde die Reihe konvergieren lassen, sofern beide Schranken bewiesen sind. Das vorliegende Modul beweist weder diese Voraussetzungen noch sie aus Schwinger–Dyson-/Makeenko–Migdal-Gleichungen oder einer Brascamp–Lieb-Ungleichung auf `SU(3)`. C1 bleibt daher eine analytische Forschungsaufgabe; die in B1 gezeigte freie Wahl von `α` ersetzt diesen Nachweis nicht.

## Einordnung

Der Lean-Status „axiom- und sorry-frei“ ist deklarations- und build-spezifisch. Die Ergebnisse dieses Moduls sind formale Aussagen über seine Definitionen und Hypothesen. Sie sind keine Konstruktion der Yang–Mills-Theorie, kein Kontinuumsgrenzwert und kein Beweis einer physikalischen Masselücke oder Operatoridentifikation; siehe auch [Gap und Operator-Matching](06_GAP_AND_OPERATOR_MATCHING.md).
