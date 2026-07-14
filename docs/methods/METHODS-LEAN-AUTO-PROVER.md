---
title: Methods – Lean Auto-Prover & External Benchmarks
id: METHODS-LEAN-AUTO-PROVER
version: 1.0.0
---

# Methods – Lean Auto-Prover & External Benchmarks

## 1. Externe Systeme

### 1.1 DeepMind AlphaProof & AlphaProof Nexus

- **AlphaProof:** Reinforcement-Learning-Agent für formale Beweise in Lean (IMO-ähnliche Aufgaben, Silver-Medal-Level).
- **AlphaProof Nexus (Mai 2026):** Erweiterte Version, die neun Erdős-Probleme und mehrere Dutzend OEIS-Konjekturen mit Lean-verifizierten Beweisen gelöst hat.

**Referenzen:**

- DeepMind, *Advancing Mathematics Research with AI-Driven Formal Proof Search*, arXiv 2605.xxxx.
- GitHub: `google-deepmind/alphaproof-nexus-results` (Lean-Beweise und Daten).

## 2. UIDT-Verwendungsgrenzen (GLBC / No-Leakage)

UIDT nutzt diese Systeme **ausschließlich** als methodische Referenzen:

- Kein direkter Import von AlphaProof- oder AlphaProof-Nexus-Modellen in UIDT-Code.
- Keine Nutzung von Erdős- oder OEIS-Ergebnissen als Validierung oder Ableitung von:
  - G1–G4 (Admissibility),
  - Origin-Gap (G2),
  - Spektralparametern ∆, γ, E_T,
  - Moduli- oder NCG-Claims.

Formale Beweise aus dem `alphaproof-nexus-results`-Repo dürfen als **Beweis-Engineering-Vorlagen** dienen (z.B. Taktik-Patterns, Proof-Search-Strukturen), aber nicht als semantische Stütze für UIDT-Physikclaims.

## 3. Interne Auto-Prover

- UIDT-interne Auto-Prover (falls implementiert) laufen immer **unter UIDT-Governance**:
  - Kein Zugriff auf fremde, nicht dokumentierte Trainingsdaten.
  - Ergebnisse gelten erst als Kandidaten, wenn Lean 4 sie vollständig verifiziert und AxiomAudit sie in der Ledger-Struktur führt.
