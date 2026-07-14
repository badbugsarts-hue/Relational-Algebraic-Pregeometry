import Antigravit2.NCG.FiniteAlgebra

namespace Antigravit2.NCG

/-- Minimaler Datenträger für Moduli-Analyse:
    Bündelt alle Typen und Typklassen, die eine Signatur ausmachen. -/
structure ModuliDatum where
  A : Type
  H : Type
  addCommGroup : AddCommGroup H
  module : Module ℂ H
  realStruct : RealStructure H
  sig : @FiniteAlgebraSignature A H addCommGroup module realStruct

end Antigravit2.NCG
