# UIDT Phase 9 – Handout

_Falsifikations-orientierte Konsolidierung von Matrix-Thermodynamik, NCG-Filtern und G1–G4-Moduliprogramm im Lichte der v4.0-Ontologie und GLBC-Disziplin._

## 1. Zweck und Einbettung von Phase 9

Phase 9 bündelt die in der v3.9-Auditphase gewonnenen negativen Resultate, den Matrix‑Thermodynamik‑Kern und die NCG‑Filterarchitektur zu einem explizit als **D‑Klasse Forschungsprogramm** markierten Block innerhalb der UIDT v4.0‑Ontologie.
Sie ersetzt keine Resultate der v3.9‑Ontologie, sondern **lokalisiert** die verbleibenden Struktur‑Lücken (G1–G4, RNC, Auswahlprobleme) schärfer, ohne sie als gelöst auszugeben.

Konkret dient Phase 9 vier Funktionen:

- Explizite Formulierung des Matrix‑Thermodynamik‑Kerns als notwendige, aber nicht hinreichende Strukturbedingung.
- Präzise Fassung der **bedingten** N=6‑Selektionsaussage (3,2,1 unter H1/H2), mit transparenten Hypothesen.
- Einordnung des G1–G4‑Moduliprogramms und der **Relocation Necessity Conjecture (RNC)** als eigenständige Forschungsziele.
- Verankerung dieser Inhalte in der v4.0‑Evidenzarchitektur (GLBC, D19, Claims‑Register), ohne jegliche Evidence‑Klassen‑Upgrades.

## 2. Eingänge aus früheren Phasen

Phase 9 baut explizit auf folgenden Artefakten auf:

- **UIDT Ontology v3.9.9 (-006)** als kanonische Referenz für alle numerischen Ledger‑Werte und G1–G4‑Analyse.
- **v4.0 DRAFT-001** (D19‑Entscheidung): Demotion der kontinuierlichen Skalarfeld‑Variante $S(x)$ zu einer effektiven Feldgrösse und Einführung eines endlichen spektralen Kerns als Kandidaten‑Primitive.
- **Matrix‑Thermodynamik‑Kern** (Phase 7/8): $S = \sum_i n_i^2$ plus Off‑Diagonal‑Penalty als glasklares, aber interpretativ begrenztes Auswahl‑Funktional.
- **Lean‑4‑Formalisierungslayer** (Realstruktur, First‑Order‑Condition, Krajewski‑Kern, Auswahlmodul), auditiert auf statische Konsistenz, nicht als geschlossener Theorem‑Korpus.

## 3. Modul 1 – Thermodynamischer Kern und Filterstatus

### 3.1 Kernformel und Rolle

Der thermodynamische Kern arbeitet mit einer blockweisen Kondensationsgrösse
$$
S_\text{core} = \sum_i n_i^2 + S_\text{offdiag}(\{n_i\})
$$
mit einem strikt positiven Off‑Diagonal‑Beitrag, der zu ungleichen Blockgrössen hin tendiert.
Diese Struktur ist numerisch robust und hochpräzise auditiert, bleibt aber konzeptuell ein **Ranking‑Funktional über Partitionen**, nicht ein NCG‑Theorem über spektrale Tripel.

### 3.2 Filter H1/H2 als Hypothesen

Phase 9 kodiert zwei Filter explizit als Hypothesen, nicht als abgeleitete Sätze:

- **H1 (Intersection‑Filter)**: In sortierten Partitionen unterscheiden sich benachbarte Blockgrössen höchstens um 1; motiviert durch Intersection‑Form‑Beschränkungen, aber noch nicht aus den NCG‑Axiomen abgeleitet.
- **H2 (Massendegenerations‑Filter)**: Mindestens zwei Summanden, alle paarweise verschieden; motiviert durch empirische Nicht‑Entartung des Fermionspektrums, aber nur als kombinatorischer Proxy implementiert.

Beide Filter werden im Handout und in der Ontologie klar als **D‑Klasse Designentscheidungen** geführt; jede spätere Ableitung aus Stratum‑II‑Mathematik wäre eine genuine Evidence‑Erhöhung und muss separat dokumentiert werden.

## 4. Modul 2 – N=6-Partition und bedingte Auswahl

### 4.1 Endlicher Eliminationsraum

Für $N=6$ existieren genau elf sortierte ganzzahlige Partitionen; Phase 9 betrachtet diese als endlichen, maschinen‑enumerierbaren Suchraum.
Unter den Filtern H1 und H2 werden zehn dieser Partitionen eliminiert; übrig bleibt allein $3,2,1$ (in Lean‑Notation `[3,2,1]`).

### 4.2 Proposition und Grade

Die entsprechende Aussage wird bewusst **mehrschichtig** formuliert:

- **Formale Proposition (logischer Gehalt):**
  > Unter H1 und H2 ist $3,2,1$ die einzige zulässige Partition von $N=6$.

  Diese Aussage ist prinzipiell entscheidbar und soll langfristig als $A$‑Klasse‑Satz innerhalb des Lean‑Systems erscheinen, sobald alle Beweisbausteine geschlossen sind.

- **Physikalische und ontologische Bewertung:**
  Wegen der Hypothesen H1/H2 bleibt die Selektionsaussage in der Ontologie **fest auf D**; selbst ein abgeschlossener Lean‑Beweis ändert nichts an dieser Einstufung, solange H1/H2 nicht aus strengeren Annahmen hergeleitet werden.

- **Falsifikationspfad:**
  - Auf logischer Ebene genügt ein expliziter Gegenbeleg im $N=6$-Raum, der H1 und H2 erfüllt und nicht $3,2,1$ ist.
  - Auf physikalischer Ebene führt jede Abschwächung von H1 oder H2 zu neu zugelassenen Partitionen (z. B. 5,1 oder 2,2,2) und zerstört damit die Einzigkeit.

Phase 9 dokumentiert beide Ebenen; das Handout stellt klar, dass „Einzigkeit von 3,2,1“ ohne Hypothesenangabe ein Evidence‑Fehler wäre.

## 5. Modul 3 – G1–G4, Moduli und Relocation Necessity Conjecture (RNC)

### 5.1 G1–G4 als lokalisierte Obstruktionen

Die v3.9/v4.0‑Ontologie isoliert die GSM‑Origin‑Lücke in vier gemeinsam unerfüllten Bedingungen auf Multiplicität, Wedderburn‑Invarianten, Realstruktur und Chiralität (G1–G4).
Diese werden in Phase 9 nicht neu interpretiert, sondern als **benannte Constraints** mit klaren Lower‑Bounds für jede Kandidaten‑Algebra zusammengefasst.

### 5.2 RNC als eigenständige Forschungsaufgabe

Die **Relocation Necessity Conjecture (RNC)** formuliert die Vermutung, dass Wedderburn‑Invarianten und KO‑Dimension in zulässigen Moduli‑Räumen realer spektraler Tripel **lokal konstant** sind, d. h. unter kontinuierlichen $D$‑Deformationen nicht springen.

In Phase 9 hat RNC folgende Rolle:

- Sie macht explizit, dass viele „Kontinuumsargumente“ bestenfalls die GSM‑Lücke **verlagern**, nicht auflösen.
- Sie eröffnet ein streng mathematisches, von UIDT unabhängiges Forschungsproblem, dessen Lösung (positiv oder negativ) publikationsfähig ist.
- Sie koppelt natürlich an kombinatorische Fragen wie die „Staircase‑Conjecture“ (dreieckszahlige zulässige Dimensionen) an.

Phase 9 dokumentiert RNC als **Open Question Klasse D** mit klaren Falsifikationsbedingungen, ohne jegliche Andeutung eines Beweises.

## 6. Modul 4 – Governance, GLBC und Evidence-Disziplin

### 6.1 GLBC im v4.0-Rahmen

Die v4.0‑Ontologie hebt das „Gap Localization before Construction“ (GLBC)–Prinzip explizit auf Governance‑Ebene an und kennzeichnet es als **methodologische Disziplin (Klasse E)**, nicht als Theorem.
Für Phase 9 bedeutet das konkret:

- Kein physikalischer Target‑Wert ($\Delta$, $\gamma$, $E_T$) und kein Blockmuster (insb. $3,2,1$) darf in Kernstrukturen als Loss, Startwert oder Abbruchbedingung erscheinen.
- Kandidaten‑Partitionen dürfen nur als **eingesetzte Instanzen** in dedizierten Modulen vorkommen; jede definitorische Verankerung (z. B. „admissible := (partition = )“) gilt als Target‑Leakage und wird dokumentiert.

### 6.2 D19 und die Demotion von $S(x)$

PI‑Entscheidung D19 demotiert das kontinuierliche Skalarfeld $S(x)$ von einem ontologischen Primitive zur effektiven Makroskopik und registriert den endlichen spektralen Kern als **D‑Klasse‑Kandidat**.
Phase 9 ist der Ort, an dem diese Demotion operationalisiert wird:

- Alle Aussagen über „Emergenz des Kontinuums“ oder „thermodynamische Passage“ werden strikt in Part II der Ontologie gehalten und mit E/C‑Kappen versehen.
- Der Phase‑9‑Block darf keine Umdeutung dieser Kappen vornehmen.

### 6.3 Claims-Register und Open Obligations

Das v4.0‑Claims‑Register listet für Part I/II/III alle Claims mit Evidenzklasse, Falsifikationsbedingung und Downgrade‑Trigger.
Phase‑9‑spezifische Einträge betreffen insbesondere:

- Den **bedingten N=6‑Selektionssatz** (D, Falsifikation über Schwächung von H1/H2 oder explizite Gegenbeispiele).
- Die **Staircase‑Conjecture** (D, Falsifikation durch nicht‑staircase Partition mit H1/H2).
- Die **RNC‑Conjecture** (D, Falsifikation durch kontinuierliche Änderung eines diskreten Invariants in einem gut definierten Moduli‑Raum).

Das Handout referenziert diese Einträge explizit, ist aber selbst **kein** Claims‑Register; es dient als Leseführung und Integrationsskizze.

## 7. GitHub-Integration und Ablageempfehlung

Für die Integration in das GitHub‑Repository wird folgende Ablagestruktur empfohlen:

- Ablage unter `docs/architecture/phase-9-kernel-and-moduli.md`.
- Querverweise im v4.0‑README und in `docs/architecture/ontology-code-bridge.md`, damit der Zusammenhang zu D19, GLBC und dem Lean‑Formalisierungslayer klar sichtbar bleibt.
- Kein automatischer Export in Part I/II/III der LaTeX‑Ontologie; das Handout ist ein **nicht‑kanonisches Hilfsdokument** für Reviewer:innen und für Pull‑Request‑Gatekeeping.
