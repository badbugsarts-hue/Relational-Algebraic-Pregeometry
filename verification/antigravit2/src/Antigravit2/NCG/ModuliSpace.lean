import Antigravit2.NCG.ModuliData

namespace Antigravit2.NCG

/-- Ein Dirac-Operator, der zu einer gegebenen Signatur gehört. -/
@[reducible]
def DiracFor (d : ModuliDatum) : Type :=
  d.H → d.H

/-- G1-G4 Admissibility-Prädikat (Platzhalter). -/
axiom Admissible (d : ModuliDatum) (D : DiracFor d) : Prop

/-- Admissibilität eines Dirac-Operators relativ zu einem ModuliDatum. -/
structure AdmissibleDirac (d : ModuliDatum) where
  D      : DiracFor d
  adm_ok : Admissible d D

namespace AdmissibleDiracSpace

/-- Der "Raum" aller zulässigen Dirac-Operatoren für ein ModuliDatum. -/
def Space (d : ModuliDatum) : Type :=
  AdmissibleDirac d

/-- Prädikat: Zwei Moduli-Daten sind durch einen zulässigen Pfad verbunden. -/
axiom IsConnectedByAdmissiblePath (d₁ d₂ : ModuliDatum) : Prop

end AdmissibleDiracSpace

/-- Extrahiert die Blockpartition. -/
axiom blockPartition (d : ModuliDatum) : List Nat

/-- RNC: Relocation Necessity Conjecture
    In Lean als reine algebraische Lokalkonstanz formuliert. -/
axiom RNC_Conjecture :
  ∀ (d₁ d₂ : ModuliDatum),
    AdmissibleDiracSpace.IsConnectedByAdmissiblePath d₁ d₂ →
    blockPartition d₁ = blockPartition d₂

end Antigravit2.NCG
