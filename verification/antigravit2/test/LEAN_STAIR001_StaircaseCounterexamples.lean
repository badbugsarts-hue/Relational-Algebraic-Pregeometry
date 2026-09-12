/-
  LEAN_STAIR001_StaircaseCounterexamples
  ========================================
  Regression tests for LEAN-STAIR-001: Retraction of the staircase-only
  conjecture.

  The falsified conjecture claimed that Phase-9-admissible partitions
  are exclusively complete staircases [k, k-1, ..., 1] with k(k+1)/2 = N.

  The three examples below demonstrate:
  1. [3, 2] is admissible (N=5 is NOT a triangular number; list does NOT
     end at 1). This is a non-staircase admissible partition.
  2. [4, 3, 2] is admissible (N=9 is NOT a triangular number; list does
     NOT end at 1). This is another non-staircase admissible partition.
  3. [3, 2, 1] is admissible (N=6, a complete staircase). This confirms
     staircases are a proper SUBSET of the admissible set, not the
     entire set.

  Together these show the admissible set is strictly larger than the
  set of complete staircases, falsifying the original conjecture.

  These tests must never be removed. If the definition of phase9Admissible
  changes in a way that would break them, the change must be reviewed
  against the replacement conjecture (consecutive intervals).

  Reference: Handout H-5, LEAN-STAIR-001
  Reference: EliminationN6.lean, RETRACTED block
-/

import Antigravit2.Filters.EliminationN6

open Antigravit2.Filters

-- ═══════════════════════════════════════════════════════════════
-- COUNTEREXAMPLES to the staircase-only conjecture
-- ═══════════════════════════════════════════════════════════════

/-- Counterexample 1: [3, 2] passes both H1 and H2.
    N = 5 is not a triangular number. The list does not end at 1.
    This is a non-staircase admissible partition. -/
example : phase9Admissible [3, 2] = true := rfl

/-- Counterexample 2: [4, 3, 2] passes both H1 and H2.
    N = 9 is not a triangular number. The list does not end at 1.
    This is a non-staircase admissible partition. -/
example : phase9Admissible [4, 3, 2] = true := rfl

-- ═══════════════════════════════════════════════════════════════
-- STAIRCASE CONFIRMATION (proper subset witness)
-- ═══════════════════════════════════════════════════════════════

/-- [3, 2, 1] is a complete staircase (k=3, N=6=3·4/2) and is
    admissible. Together with the counterexamples above, this shows
    that complete staircases are a proper subset of the admissible
    set — the admissible set is strictly larger. -/
example : phase9Admissible [3, 2, 1] = true := rfl
