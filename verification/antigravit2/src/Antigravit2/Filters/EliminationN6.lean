/-
  Antigravit2.Filters.EliminationN6
  ===================================
  [D] — Proposition under Hypotheses H1, H2. Not a universal NCG theorem.

  Phase 9: Complete N=6 admissibility classification with explicit
  elimination of all rival partitions under two stated hypotheses.

  ┌────────────────────┬────────────────────────────────────────────────────────┐
  │ Hypothesis         │ Content                                              │
  ├────────────────────┼────────────────────────────────────────────────────────┤
  │ H1 (DESIGN-LEVEL)  │ Intersection-Form Filter: consecutive block sizes   │
  │                    │ in a sorted partition differ by at most 1. Motivated │
  │                    │ by NCG intersection-form non-degeneracy              │
  │                    │ (arXiv:0706.3690) but not a general theorem.         │
  ├────────────────────┼────────────────────────────────────────────────────────┤
  │ H2 (HEURISTIC)     │ Combinatorial proxy: all block sizes are pairwise   │
  │                    │ distinct AND at least two blocks exist. No Yukawa   │
  │                    │ or mass relation is formalized.                     │
  └────────────────────┴────────────────────────────────────────────────────────┘

  PROPOSITION (Phase 9):
    Under H1 and H2, [3,2,1] is the unique admissible partition of N=6.

  FORMAL CHARACTERISATION:
    Sorted positive Phase-9-admissible lists are precisely finite decreasing
    consecutive intervals [a, a-1, ..., b] with 1 <= b < a.

  FALSIFICATION PATHS:
    (a) If H1 is weakened (larger block-difference tolerance), additional
        partitions (e.g. [4,2], [5,1]) become admissible.
    (b) If H2 is weakened (allowing repeated block sizes), additional
        partitions (e.g. [2,2,1,1]) become admissible.

  Anti-Target-Leakage: filter definitions are generic; [3,2,1] follows both
  from explicit elimination and from the general interval/arithmetic route,
  not from any hard-coded bias.

  Reference: Matrix-Thermodynamik session notes (Filter 1, Filter 2)
  Reference: arXiv:0706.3690 (Chamseddine-Connes-Marcolli)
  Reference: METHODOLOGY_GLBC_001
-/

import Antigravit2.Filters.Enumeration
import Mathlib.Tactic

namespace Antigravit2
namespace Filters

open MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- PHASE 9 FILTER DEFINITIONS (Bool-valued for decidability)
-- ═══════════════════════════════════════════════════════════════

/-- [DESIGN-LEVEL] H1: Intersection-Form Filter.
    For a sorted (decreasing) list of block sizes, each consecutive
    pair (a, b) satisfies a ≤ b + 1, i.e., the sizes decrease by
    at most 1 at each step.

    MOTIVATION: In NCG, the intersection form of a Krajewski diagram
    imposes constraints on which block-size pairs can have non-trivial
    fermionic multiplets. The condition |n_i - n_j| ≤ 1 for coupled
    blocks is a first-order proxy for this constraint.

    FORMALIZATION GAP: The precise derivation of this bound from the
    intersection-form axioms in full generality is not yet formalized.
    The NCG literature (arXiv:0706.3690, arXiv:1805.08582) motivates
    such constraints but does not prove a general dimension-jump theorem
    in exactly this form.

    UPGRADE PATH: Derive from SpectralTriple intersection-form axioms.
-/
def intersectionFilter : List ℕ → Bool
  | [] => true
  | [_] => true
  | a :: b :: rest =>
    if a ≤ b + 1 then intersectionFilter (b :: rest) else false

/-- Check that no element appears more than once (Bool version). -/
def nodupBool : List ℕ → Bool
  | [] => true
  | x :: xs => !(xs.contains x) && nodupBool xs

/-- Check that a list has at least two elements. -/
def atLeastTwo {α : Type} : List α → Bool
  | _ :: _ :: _ => true
  | _ => false

/-- [HEURISTIC] H2: Combinatorial Non-Degeneration Proxy.
    FORMAL CONTENT: The block list has at least two elements and no block
    size occurs more than once. The implementation is exactly
    `nodupBool xs && atLeastTwo xs`.

    INTERPRETATION: This Bool is only a modeling proxy for a possible
    physical non-degeneration assumption. The corpus contains no Yukawa
    structure, mass matrix, or theorem connecting repeated block sizes to
    fermion masses. Consequently H2 neither derives nor predicts a mass
    spectrum.

    FORMALIZATION GAP: Any physical interpretation requires a separately
    formalized bridge from spectral-triple Dirac/Yukawa data to this
    combinatorial predicate. That bridge is absent.

    UPGRADE PATH: Formalize and review such a bridge before assigning a
    physical mass interpretation.
-/
def massNondeg (xs : List ℕ) : Bool :=
  nodupBool xs && atLeastTwo xs

/-- Phase 9 admissibility: H1 ∧ H2.
    A partition is Phase-9-admissible if it satisfies both the
    intersection-form filter (H1) and the combinatorial proxy (H2).

    STATUS: Definitional conjunction. Inherits epistemic status from
    H1 [DESIGN-LEVEL] and H2 [HEURISTIC].
-/
def phase9Admissible (xs : List ℕ) : Bool :=
  intersectionFilter xs && massNondeg xs

/-- `xs` is a positive consecutive descending interval with at least two entries. -/
def isConsecInterval (xs : List ℕ) : Bool :=
  decide (2 ≤ xs.length)
    && xs.all (fun x => decide (1 ≤ x))
    && (List.zip xs xs.tail).all (fun p => decide (p.1 = p.2 + 1))

private theorem atLeastTwo_eq_true_iff (xs : List ℕ) :
    atLeastTwo xs = true ↔ 2 ≤ xs.length := by
  cases xs with
  | nil => simp [atLeastTwo]
  | cons _ xs =>
      cases xs <;> simp [atLeastTwo]

private theorem nodupBool_eq_true_iff (xs : List ℕ) :
    nodupBool xs = true ↔ xs.Nodup := by
  induction xs with
  | nil => simp [nodupBool]
  | cons x xs ih => simp [nodupBool, ih, List.nodup_cons]

private theorem intersectionFilter_of_consecutiveSteps (xs : List ℕ)
    (h : (List.zip xs xs.tail).all
      (fun p => decide (p.1 = p.2 + 1)) = true) :
    intersectionFilter xs = true := by
  induction xs with
  | nil => simp [intersectionFilter]
  | cons a xs ih =>
      cases xs with
      | nil => simp [intersectionFilter]
      | cons b rest =>
          simp only [List.tail_cons, List.zip_cons_cons, List.all_cons,
            Bool.and_eq_true, decide_eq_true_eq] at h
          rw [intersectionFilter, if_pos (h.1.le)]
          exact ih h.2

private theorem pairwise_gt_of_consecutiveSteps (xs : List ℕ)
    (h : (List.zip xs xs.tail).all
      (fun p => decide (p.1 = p.2 + 1)) = true) :
    xs.Pairwise (· > ·) := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      cases xs with
      | nil => simp
      | cons b rest =>
          simp only [List.tail_cons, List.zip_cons_cons, List.all_cons,
            Bool.and_eq_true, decide_eq_true_eq] at h
          have htail : (b :: rest).Pairwise (· > ·) := ih h.2
          rw [List.pairwise_cons]
          constructor
          · intro y hy
            rcases List.mem_cons.mp hy with hEq | hy
            · subst y
              omega
            · have hby : b > y := (List.pairwise_cons.mp htail).1 y hy
              omega
          · exact htail

private theorem consecutiveSteps_of_sorted_filter (xs : List ℕ)
    (hsort : xs.Sorted (· ≥ ·)) (hnodup : xs.Nodup)
    (hfilter : intersectionFilter xs = true) :
    (List.zip xs xs.tail).all
      (fun p => decide (p.1 = p.2 + 1)) = true := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      cases xs with
      | nil => simp
      | cons b rest =>
          have hsortTail : (b :: rest).Sorted (· ≥ ·) :=
            (List.pairwise_cons.mp hsort).2
          have hnodupTail : (b :: rest).Nodup :=
            (List.nodup_cons.mp hnodup).2
          rw [intersectionFilter] at hfilter
          split at hfilter
          next hab =>
            have hge : a ≥ b := (List.pairwise_cons.mp hsort).1 b (by simp)
            have hne : a ≠ b := by
              intro heq
              apply (List.nodup_cons.mp hnodup).1
              simp [heq]
            have heq : a = b + 1 := by omega
            simp only [List.tail_cons, List.zip_cons_cons, List.all_cons,
              Bool.and_eq_true, decide_eq_true_eq]
            exact ⟨heq, ih hsortTail hnodupTail hfilter⟩
          next => contradiction

/-- Every positive consecutive interval satisfies the Phase-9 filters. -/
theorem interval_admissible (xs : List ℕ)
    (h : isConsecInterval xs = true) :
    phase9Admissible xs = true := by
  simp only [isConsecInterval, Bool.and_eq_true, decide_eq_true_eq] at h
  have hfilter := intersectionFilter_of_consecutiveSteps xs h.2
  have hnodup : xs.Nodup :=
    (pairwise_gt_of_consecutiveSteps xs h.2).imp (fun hxy => Nat.ne_of_gt hxy)
  simp [phase9Admissible, massNondeg, hfilter,
    (nodupBool_eq_true_iff xs).2 hnodup,
    (atLeastTwo_eq_true_iff xs).2 h.1.1]

/-- Every sorted positive Phase-9-admissible list is a consecutive interval. -/
theorem admissible_interval (xs : List ℕ)
    (hsort : xs.Sorted (· ≥ ·))
    (hpos : xs.Forall (fun x => 1 ≤ x))
    (h : phase9Admissible xs = true) :
    isConsecInterval xs = true := by
  simp only [phase9Admissible, massNondeg, Bool.and_eq_true] at h
  have hnodup : xs.Nodup := (nodupBool_eq_true_iff xs).1 h.2.1
  have hlength : 2 ≤ xs.length := (atLeastTwo_eq_true_iff xs).1 h.2.2
  have hsteps := consecutiveSteps_of_sorted_filter xs hsort hnodup h.1
  have hallPos : xs.all (fun x => decide (1 ≤ x)) = true := by
    simp only [List.all_eq_true, decide_eq_true_eq]
    exact List.forall_iff_forall_mem.mp hpos
  simp [isConsecInterval, hlength, hallPos, hsteps]

example : isConsecInterval [3, 2] = true := by decide
example : isConsecInterval [4, 3, 2] = true := by decide
example : isConsecInterval [3, 1] = false := by decide
example : isConsecInterval [2, 1, 0] = false := by decide

private theorem consecutiveSteps_eq_reverse_range (a : ℕ) (xs : List ℕ)
    (h : (List.zip (a :: xs) (a :: xs).tail).all
      (fun p => decide (p.1 = p.2 + 1)) = true) :
    ∃ b : ℕ, b ≤ a ∧
      a :: xs = (List.range' b (a - b + 1)).reverse := by
  induction xs generalizing a with
  | nil =>
      exact ⟨a, by simp, by simp⟩
  | cons b rest ih =>
      simp only [List.tail_cons, List.zip_cons_cons, List.all_cons,
        Bool.and_eq_true, decide_eq_true_eq] at h
      obtain ⟨c, hca, htail⟩ := ih b h.2
      refine ⟨c, by omega, ?_⟩
      have hlen : a - c + 1 = (b - c + 1) + 1 := by omega
      have hend : c + (b - c + 1) = a := by
        calc
          c + (b - c + 1) = (c + (b - c)) + 1 := by simp [Nat.add_assoc]
          _ = b + 1 := by rw [Nat.add_sub_of_le hca]
          _ = a := h.1.symm
      have hrange : (List.range' c (a - c + 1)).reverse =
          a :: (List.range' c (b - c + 1)).reverse := by
        rw [hlen, List.range'_1_concat, List.reverse_append,
          List.reverse_singleton, List.singleton_append, hend]
      calc
        a :: b :: rest = a :: (List.range' c (b - c + 1)).reverse := by rw [htail]
        _ = (List.range' c (a - c + 1)).reverse := hrange.symm

private theorem reverse_range_consecutiveSteps (b n : ℕ) :
    (List.zip (List.range' b n).reverse (List.range' b n).reverse.tail).all
      (fun p => decide (p.1 = p.2 + 1)) = true := by
  induction n with
  | zero => simp
  | succ n ih =>
      cases n with
      | zero => simp
      | succ n =>
          simp only [List.range'_1_concat, List.reverse_append, List.reverse_singleton,
            List.singleton_append, List.tail_cons, List.zip_cons_cons, List.all_cons,
            Bool.and_eq_true, decide_eq_true_eq]
          constructor
          · omega
          · simpa only [List.range'_1_concat, List.reverse_append,
              List.reverse_singleton, List.singleton_append,
              List.tail_cons] using ih

/-- The Boolean interval predicate is equivalent to an explicit descending range. -/
theorem isConsecInterval_iff_exists_range (xs : List ℕ) :
    isConsecInterval xs = true ↔
      ∃ a b : ℕ, 1 ≤ b ∧ b < a ∧
        xs = (List.range' b (a - b + 1)).reverse := by
  constructor
  · intro h
    simp only [isConsecInterval, Bool.and_eq_true, decide_eq_true_eq] at h
    cases xs with
    | nil => simp at h
    | cons a rest =>
        obtain ⟨b, hba, hxs⟩ := consecutiveSteps_eq_reverse_range a rest h.2
        have hpos : ∀ x ∈ a :: rest, 1 ≤ x := by
          simpa only [List.all_eq_true, decide_eq_true_eq] using h.1.2
        have hbmem : b ∈ a :: rest := by
          rw [hxs, List.mem_reverse]
          simp only [List.mem_range'_1]
          omega
        have hlt : b < a := by
          have hlength := h.1.1
          rw [hxs, List.length_reverse, List.length_range'] at hlength
          omega
        exact ⟨a, b, hpos b hbmem, hlt, hxs⟩
  · rintro ⟨a, b, hb, hab, rfl⟩
    have hlength : 2 ≤ (List.range' b (a - b + 1)).reverse.length := by
      simp only [List.length_reverse, List.length_range']
      omega
    have hallPos : (List.range' b (a - b + 1)).reverse.all
        (fun x => decide (1 ≤ x)) = true := by
      simp only [List.all_eq_true, decide_eq_true_eq]
      intro x hx
      rw [List.mem_reverse, List.mem_range'_1] at hx
      omega
    simp only [isConsecInterval, Bool.and_eq_true, decide_eq_true_eq]
    exact ⟨⟨hlength, hallPos⟩,
      reverse_range_consecutiveSteps b (a - b + 1)⟩

private theorem sum_range'_mul_two (b n : ℕ) :
    (List.range' b n).sum * 2 = n * (2 * b + n - 1) := by
  induction n generalizing b with
  | zero => simp
  | succ n ih =>
      cases n with
      | zero => simp [Nat.mul_comm]
      | succ n =>
          rw [List.range'_succ, List.sum_cons, Nat.add_mul, ih (b + 1)]
          have hleft : 2 * (b + 1) + (n + 1) - 1 = 2 * b + n + 2 := by omega
          have hright : 2 * b + (n + 2) - 1 = 2 * b + n + 1 := by omega
          rw [hleft, hright]
          ring

/-- Closed form for the sum of a descending interval. -/
theorem interval_sum (a b : ℕ) (hab : b ≤ a) :
    (List.range' b (a - b + 1)).reverse.sum * 2 =
      (a + b) * (a - b + 1) := by
  rw [List.sum_reverse, sum_range'_mul_two]
  have hinner : 2 * b + (a - b + 1) - 1 = a + b := by omega
  rw [hinner, Nat.mul_comm]

/-- The only positive nontrivial consecutive interval summing to six has endpoints 3 and 1. -/
theorem interval_sum_six (a b : ℕ)
    (hb : 1 ≤ b) (hab : b < a) (ha : a ≤ 6)
    (hsum : (a + b) * (a - b + 1) = 12) :
    a = 3 ∧ b = 1 := by
  interval_cases a <;> interval_cases b <;> simp_all

/-- N=6 uniqueness over every sorted positive admissible list, independent of `partitions6`. -/
theorem unique_321_N6_all_sorted (xs : List ℕ)
    (hsort : xs.Sorted (· ≥ ·))
    (hpos : xs.Forall (fun x => 1 ≤ x))
    (hsum : xs.sum = 6)
    (hadm : phase9Admissible xs = true) :
    xs = [3, 2, 1] := by
  have hinterval := admissible_interval xs hsort hpos hadm
  obtain ⟨a, b, hb, hab, hxs⟩ :=
    (isConsecInterval_iff_exists_range xs).1 hinterval
  subst xs
  have hamem : a ∈ (List.range' b (a - b + 1)).reverse := by
    rw [List.mem_reverse, List.mem_range'_1]
    omega
  have ha : a ≤ 6 := by
    have := List.le_sum_of_mem hamem
    omega
  have hproduct : (a + b) * (a - b + 1) = 12 := by
    calc
      (a + b) * (a - b + 1) =
          (List.range' b (a - b + 1)).reverse.sum * 2 :=
        (interval_sum a b hab.le).symm
      _ = 12 := by omega
  obtain ⟨rfl, rfl⟩ := interval_sum_six a b hb hab ha hproduct
  decide

-- ═══════════════════════════════════════════════════════════════
-- INDIVIDUAL FILTER VERDICTS — H1 (Intersection Filter)
-- ═══════════════════════════════════════════════════════════════

-- Partitions PASSING H1 (consecutive diffs ≤ 1):
-- [6], [3,3], [3,2,1], [2,2,2], [2,2,1,1], [2,1,1,1,1], [1,1,1,1,1,1]
example : intersectionFilter [6] = true := rfl
example : intersectionFilter [3, 3] = true := rfl
example : intersectionFilter [3, 2, 1] = true := rfl
example : intersectionFilter [2, 2, 2] = true := rfl
example : intersectionFilter [2, 2, 1, 1] = true := rfl
example : intersectionFilter [2, 1, 1, 1, 1] = true := rfl
example : intersectionFilter [1, 1, 1, 1, 1, 1] = true := rfl

-- Partitions FAILING H1 (have consecutive diff > 1):
-- [5,1] (diff 4), [4,2] (diff 2), [4,1,1] (diff 3), [3,1,1,1] (diff 2)
example : intersectionFilter [5, 1] = false := rfl
example : intersectionFilter [4, 2] = false := rfl
example : intersectionFilter [4, 1, 1] = false := rfl
example : intersectionFilter [3, 1, 1, 1] = false := rfl

-- ═══════════════════════════════════════════════════════════════
-- INDIVIDUAL FILTER VERDICTS — H2 (Combinatorial Proxy)
-- ═══════════════════════════════════════════════════════════════

-- Partitions PASSING H2 (all distinct, ≥2 blocks):
-- [5,1], [4,2], [3,2,1]
example : massNondeg [5, 1] = true := rfl
example : massNondeg [4, 2] = true := rfl
example : massNondeg [3, 2, 1] = true := rfl

-- Partitions FAILING H2:
-- [6] (single block), [4,1,1] (repeated 1), [3,3] (repeated 3),
-- [3,1,1,1] (repeated 1), [2,2,2] (repeated 2), [2,2,1,1] (repeated),
-- [2,1,1,1,1] (repeated 1), [1,1,1,1,1,1] (all equal)
example : massNondeg [6] = false := rfl
example : massNondeg [4, 1, 1] = false := rfl
example : massNondeg [3, 3] = false := rfl
example : massNondeg [3, 1, 1, 1] = false := rfl
example : massNondeg [2, 2, 2] = false := rfl
example : massNondeg [2, 2, 1, 1] = false := rfl
example : massNondeg [2, 1, 1, 1, 1] = false := rfl
example : massNondeg [1, 1, 1, 1, 1, 1] = false := rfl

-- ═══════════════════════════════════════════════════════════════
-- COMBINED VERDICTS — Phase 9 Admissibility
-- ═══════════════════════════════════════════════════════════════

-- Only [3,2,1] passes both H1 AND H2:
example : phase9Admissible [3, 2, 1] = true := rfl

-- All others fail at least one filter:
example : phase9Admissible [6] = false := rfl
example : phase9Admissible [5, 1] = false := rfl
example : phase9Admissible [4, 2] = false := rfl
example : phase9Admissible [4, 1, 1] = false := rfl
example : phase9Admissible [3, 3] = false := rfl
example : phase9Admissible [3, 1, 1, 1] = false := rfl
example : phase9Admissible [2, 2, 2] = false := rfl
example : phase9Admissible [2, 2, 1, 1] = false := rfl
example : phase9Admissible [2, 1, 1, 1, 1] = false := rfl
example : phase9Admissible [1, 1, 1, 1, 1, 1] = false := rfl

-- ═══════════════════════════════════════════════════════════════
-- PROPOSITION: UNIQUENESS OF [3,2,1] UNDER H1 ∧ H2
-- ═══════════════════════════════════════════════════════════════

/-- [D] Proposition (Phase 9).

    Under hypotheses H1 (intersection-form filter) and H2 (combinatorial
    non-degeneration proxy), [3,2,1] is the only admissible entry in the
    explicit reference list `partitions6`.

    STATUS: The logical derivation is [A] within the formal system
    (exhaustive relative to the reference list `partitions6`; see PROOF
    METHOD below for what is and is not machine-verified). The physical
    validity depends on the epistemic status of H1 [DESIGN-LEVEL] and
    H2 [HEURISTIC].

    PROOF METHOD: Filtering of the reference partition list `partitions6`.
    Each of the 10 non-[3,2,1] entries is eliminated by at least one filter.

    SCOPE OF "EXHAUSTIVE": `partitions6` is an explicit reference list, not a
    generated enumeration, and its completeness is NOT machine-verified at
    this commit. Verified by `decide` in Enumeration.lean: element sums (= 6),
    positivity, decreasing sortedness, cardinality (= 11), and `Nodup`.
    Enumeration.lean is sorry-free. Those properties still do not independently
    prove that every partition of 6 occurs in the reference list. The regression
    `enumPartitions 6 = partitions6` is commented out because
    `enumPartitionsBounded` is a `partial def` and therefore not reducible by
    `decide`.

    Consequently this statement is exhaustive relative to `partitions6` as
    given, not relative to an independently verified enumeration of the
    partitions of 6. The separate theorem `unique_321_N6_all_sorted` proves
    the N=6 result for arbitrary sorted positive lists and does not depend on
    completeness of `partitions6`.

    ELIMINATION PROTOCOL:
    ┌─────────────────────┬──────┬──────┬─────────┬───────────────────┐
    │ Partition           │  H1  │  H2  │ Verdict │ Eliminating filter│
    ├─────────────────────┼──────┼──────┼─────────┼───────────────────┤
    │ [6]                 │  ✓   │  ✗   │  FAIL   │ H2 (simple alg.) │
    │ [5,1]               │  ✗   │  ✓   │  FAIL   │ H1 (diff=4)      │
    │ [4,2]               │  ✗   │  ✓   │  FAIL   │ H1 (diff=2)      │
    │ [4,1,1]             │  ✗   │  ✗   │  FAIL   │ H1+H2            │
    │ [3,3]               │  ✓   │  ✗   │  FAIL   │ H2 (repeated 3)  │
    │ [3,2,1]             │  ✓   │  ✓   │  PASS   │ —                │
    │ [3,1,1,1]           │  ✗   │  ✗   │  FAIL   │ H1+H2            │
    │ [2,2,2]             │  ✓   │  ✗   │  FAIL   │ H2 (repeated 2)  │
    │ [2,2,1,1]           │  ✓   │  ✗   │  FAIL   │ H2 (repeated)    │
    │ [2,1,1,1,1]         │  ✓   │  ✗   │  FAIL   │ H2 (repeated 1)  │
    │ [1,1,1,1,1,1]       │  ✓   │  ✗   │  FAIL   │ H2 (all equal)   │
    └─────────────────────┴──────┴──────┴─────────┴───────────────────┘

    FALSIFICATION: If either H1 or H2 is weakened, additional partitions
    become admissible and the uniqueness claim is lost.
-/
theorem unique_321_N6 :
    partitions6.filter phase9Admissible = [[3, 2, 1]] := rfl

-- ═══════════════════════════════════════════════════════════════
-- WITHDRAWN CONJECTURE [D] (LEAN-STAIR-001)
--
-- The former claim that Phase-9-admissible partitions consist exclusively
-- of complete staircases [k, k-1, ..., 1], and hence occur only at triangular
-- total dimensions, is false. Definitional regression checks establish that
-- [3, 2] and [4, 3, 2] are admissible non-complete staircases, while the
-- complete staircase [3, 2, 1] remains admissible.
--
-- FORMALLY ESTABLISHED REPLACEMENT: `admissible_interval` and
-- `interval_admissible` identify sorted positive Phase-9-admissible lists with
-- finite decreasing consecutive intervals. `isConsecInterval_iff_exists_range`
-- gives the explicit range representation. This is a logical [A] result about
-- the definitions; its physical interpretation still inherits the unchanged
-- DESIGN-LEVEL/HEURISTIC status of H1 and H2.
-- ═══════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════
-- Phase 9 epistemic status summary
--
-- ┌──────────────────────────┬───────────────┬─────────────────────────┐
-- │ Entity                   │ Status        │ Upgrade path            │
-- ├──────────────────────────┼───────────────┼─────────────────────────┤
-- │ intersectionFilter (H1)  │ DESIGN-LEVEL  │ Derive from NCG axioms  │
-- │ massNondeg (H2)          │ HEURISTIC     │ Requires missing bridge │
-- │ phase9Admissible         │ DEFINITIONAL  │ Inherits from H1/H2    │
-- │ unique_321_N6            │ [A] formal    │ Reference-list theorem  │
-- │ Staircase conjecture     │ [D] withdrawn │ Replaced formally       │
-- └──────────────────────────┴───────────────┴─────────────────────────┘
-- ═══════════════════════════════════════════════════════════════

end Filters
end Antigravit2
