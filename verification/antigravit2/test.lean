import Antigravit2.Filters.EliminationN6

open Antigravit2.Filters

example : ∀ n ∈ [2, 1], n > 0 := by decide

-- LEAN-STAIR-001: permanent definitional regressions for the withdrawn
-- complete-staircase exclusivity conjecture.
example : phase9Admissible [3, 2] = true := rfl
example : phase9Admissible [4, 3, 2] = true := rfl
example : phase9Admissible [3, 2, 1] = true := rfl
