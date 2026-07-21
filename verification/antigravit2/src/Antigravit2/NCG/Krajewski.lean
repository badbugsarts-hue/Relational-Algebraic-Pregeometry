/-
  Antigravit2.NCG.Krajewski
  ==========================
  [D] — Krajewski Diagram Structure (re-export layer).

  Phase 10c consolidation: The combinatorial kernel (Bimodule, KrajewskiDiagram,
  noSelfLoops, admissibleDiagram) is now defined in KrajewskiCore without
  FiniteAlgebra dependencies, following the GLBC principle (gap localization
  before construction). This module re-exports KrajewskiCore for backward
  compatibility with AxiomAudit and other importers.

  The FiniteAlgebra-parameterized KrajewskiDiagram variant was an architectural
  over-complication: the combinatorial diagram structure does not require a
  FiniteAlgebraSignature. Physical algebra assignments enter only at the
  instance layer (Krajewski321, future candidates).

  LEAN-001 fix (2026-07-21): Removed duplicate Bimodule import and
  FiniteAlgebra-parameterized KrajewskiDiagram to resolve namespace collision.
-/

import Antigravit2.NCG.KrajewskiCore
import Antigravit2.NCG.FiniteAlgebra

-- Re-export: KrajewskiCore defines Bimodule, KrajewskiDiagram, noSelfLoops,
-- admissibleDiagram. All downstream importers of this module continue to
-- resolve those names via KrajewskiCore.

namespace Antigravit2.NCG

-- Forward compatibility alias: downstream code using `KrajewskiDiagram` without
-- type parameters resolves to the combinatorial KrajewskiCore definition.
-- The FiniteAlgebra-parameterized variant is intentionally removed; add it
-- as a separate `BridgedKrajewskiDiagram` in Bridge.lean when needed.

end Antigravit2.NCG
