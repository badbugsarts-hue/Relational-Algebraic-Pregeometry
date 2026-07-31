# Manuscript Provenance — Relational-Algebraic Pregeometry v4.0

**Why this file exists.** The manuscript `.tex` deliberately states no commit identity of its own.
A file cannot contain its own Git blob: the blob is the hash of its content, header included, so
any commit or blob written into the header names a superseded state as soon as the next commit
lands. Earlier headers tried to carry `APPLIED COMMIT` / `APPLIED GIT BLOB` and went stale three
times in four days. This file carries the chain instead. It is **not** part of the hashed
manuscript, so it is permitted to lag without making the manuscript self-contradictory.

**Authoritative source:** the Git commit graph of
`manuscript/Relational_Algebraic_Pregeometry_v4_0_DRAFT-001.tex` on branch `mss000-rebase-v2`.
Where this file and the commit graph disagree, the commit graph wins.

**Scope of this record.** This file is a narrative projection of the commit graph, not a substitute
for it. It states no SHA of its own containing commit — that would reintroduce the self-reference
D-2' removed.

```yaml
provenance_scope:
  covers_through_parent: b58ca6a      # last commit fully recorded below
  containing_commit: resolved_from_git_graph
  current_manuscript_identity: resolved_from_git_tree
  self_sha_embedded: false
  may_lag_behind_head: true           # by design; not a defect
```

**This file may lag the branch head.** That is intended: it is external to the hashed manuscript,
so a lag here never makes the manuscript self-contradictory. Resolve the current identity from the
tree, not from this table.

**Not merged.** Nothing below authorizes a merge. Build statements remain environment-qualified
while PROV-002 is open.

---

## Chain on `mss000-rebase-v2`

| Commit | Blob | What landed |
|---|---|---|
| `513cd2e` | — | P-A: Diophantine construction argument replaces invalid primality entailment |
| `550c88c` | — | MSS-000: Phase-6 architectural rebase under PI Decision D20 |
| `dc1cef4` | — | NORM-01: juxtaposed evidence tags decomposed into single-class claims |
| `c11b76e` | `be257b70` | P02: Matrix Arena, exact finite-N block ratio |
| `f010545` | — | CTX-001: scientific context, reciprocal demarcation, research-gap atlas |
| `11172a2` | — | GAP-23 marked closed (NORM-01 had landed in dc1cef4) |
| `77ed7b4` | `7962e5e7` | Museum watermark: visual firewall on the Historical Appendix |
| `c8daae1` | `c3197df2` | RAP finalization: D19/D21–D25 closure records, E_T scoping, name migration |
| `1cafaf6` | `b7fec339` | Patch A: Krajewski completeness boundary, stabilizer boundary, L8–L11 |
| `5af0c2f` | `8098be57` | Header: stale self-description corrected (first attempt; see note below) |
| `d0bf762` | `2790067a` | GAP-22: commit-scoped Lean reconciliation, `61bc24da` alongside `f1ae5486` |
| `8d2bfc7` | `9b4faf49` | D-1: each CI run bound to its own commit |
| `b58ca6a` | `6bdf26eb` | D-2': self-referential commit/blob removed from the header; this file added |

Blob column lists the file blob **after** that commit where recorded. Absent entries were not
captured at the time; the commit graph remains authoritative in every case.

## Note on the two header corrections

`5af0c2f` corrected a real defect — the applied manuscript described itself as an unapplied
candidate — but did so by writing concrete SHAs into the header. That converted a one-off
contradiction into a recurring one: three commits later the header again named a superseded state.
`D-2'` removes the self-reference entirely rather than chasing it.

**Precise scope of what D-2' fixed.** The header no longer contains self-referential Git identity;
commit and blob provenance are delegated to the commit graph and to this file. That specific class
of unavoidable staleness is closed. Other header fields can still go stale and are not covered:
the branch name, the file path, the `not merged` declaration, the PROV-002 qualification, and the
licence/DOI metadata all remain ordinary facts that a future change could invalidate. An earlier
summary of this work claimed the header "can no longer go stale by construction"; that was too
broad and is corrected here.

## Open gates at the time of writing

| Gate | Status |
|---|---|
| GAP-22 Lean reconciliation | closed for `f1ae5486` only; every later head needs a new five-part snapshot |
| F1 | closed at `f1ae5486` as a documentation/formal-software discrepancy; H1/H2 conditionality unchanged |
| F2 | **open** — no target-shape scan was supplied |
| F3 | register defect closed; 8 registered proof debts remain |
| PROV-002 | **open** — no pinned TeX environment; all build statements environment-qualified |
| GOV-001b | **open** — CI gates cannot be shown to inspect a real diff |
| GitHub Actions | **blocked at account level**; runs return `runner_id: 0`, zero steps executed |
| `master` root build | **broken** at `61bc24da` and `07ef753b` (Issue #25); PR #18 repairs it |
| Final freeze | **HOLD** |

## Rule for future patches

The base of any patch is the file **as it exists in a named commit**, obtained from the repository.
Pasted chat text is never a patch base: a byte audit on 2026-07-31 showed a pasted copy differing
from the committed blob in both CRLF and LF-normalized form.
