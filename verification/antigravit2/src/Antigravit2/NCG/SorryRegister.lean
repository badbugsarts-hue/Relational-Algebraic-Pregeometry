/-
  Antigravit2.NCG.SorryRegister
  ================================
  SORRY REGISTER — Phase 7
  
  Jeder Eintrag referenziert die Datei, das Lemma, den Grund und die Zielphase
  für die Auflösung des `sorry`-Markers. Dies stellt sicher, dass kein `sorry` 
  "stumm" im Code überlebt und unbeabsichtigte axiomatische Lücken reißt.

  [ALLOWED-P8] canonicalBlocks Regression (SpectralTriple.lean)
    Reason: `canonicalBlocks` basiert auf `List.mergeSort`. Der Elaborator 
            reduziert dies nicht rein strukturell in endlicher Zeit (non-computable 
            oder sehr tiefe rekursive Reduktion ohne simp/decide lemmas). 
    Scope:  Isolation in `Enumeration.lean`. `canonicalBlocks` taucht in 
            keinem Prop der NCG-Hierarchie (`toTrivialTriple`, `SpectralTriple`) auf. 
            (Transitiv verifiziert via `#print axioms toTrivialTriple` -> no `sorryAx`).
    Target: Phase 8 (Entwicklung spezifischer Decidability-Lemmas für Partitionen).

  [CLOSED-P10] unique_321_N6 and its supporting decidability lemmas
    Reason: The Phase 9 uniqueness statement `unique_321_N6` and its supporting
            33 per-partition checks were successfully discharged via `by decide` and
            `rfl`. They are now completely sorry-free.
            The statement evaluates to [A] under the stated assumptions: H1 (intersectionFilter,
            DESIGN-LEVEL) and H2 (massNondeg, HEURISTIC) as defined in EliminationN6.lean.
            The [A] covers the formal implication, not the physical adequacy of the filters.
            The 2026-07-13 history is retained for auditing.
    Scope:  Axiom audit verifies this closure:
            `info: src/Antigravit2/NCG/AxiomAudit.lean:35:0: 'Antigravit2.Filters.unique_321_N6' depends on axioms: [propext]`
    Target: Completed.

  [CLOSED-P10] List.Sorted Enumeration Regression (Enumeration.lean)
    Reason: SUPERSEDED 2026-08-03. The earlier reason -- that `List.Sorted (· ≥ ·)`
            decidability hangs the elaborator infinitely without `native_decide` --
            does not hold at lean v4.32.0-rc1 / mathlib ba1e3bb. The statement for
            `partitions6` discharges with plain `by decide`, with no `native_decide`
            and hence no `Lean.ofReduceBool`. Measured: all three statements (4/5/6)
            elaborate together in 35 s, and the Decidable instance is obtained by
            `infer_instance`.
    Scope:  0 instances remaining. Enumeration.lean is sorry-free.
            Line 79 (partitions6) was discharged on 2026-08-03.
            Lines 77-78 (partitions4, partitions5) were closed on 2026-08-03 by PI
            decision, by the identical one-token change (`sorry` -> `by decide`).
            No `native_decide` was used, hence no `Lean.ofReduceBool` was introduced.
    Target: Completed.

  [NONE] All RealStructure.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All Bridge.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All BlockPartition.lean lemmas — sorry-free as of 2026-06-30
-/

namespace Antigravit2
namespace NCG

-- Status: 5 instances in SpectralTriple.lean lines 98-103.

end NCG
end Antigravit2
