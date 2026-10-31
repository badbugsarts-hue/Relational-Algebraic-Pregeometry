# RAP claim ledger

This newly written release registry is grounded in the corrected manuscript, not migrated wholesale from UIDT claims. It is a curated set, not a count of every evidence tag. `CLAIMS.json` separates class, evidence kind, method, input, uncertainty, and scope. Validation checks its structure, source anchors, unique identifiers and dependency closure. It does not certify scientific truth.

`reproduction_command: null` means no executed reproduction is offered for that claim. Unknown empirical uncertainty remains null, never silently zero. Reported Lean and MC summaries remain reported, not independently reproduced. New task IDs are proposals, not new PI decisions. Historical decisions are preserved separately in `governance/RECORDED_PI_DECISIONS.json` and in the manuscript.

The nine reference constants have one machine-readable source: `../CANONICAL/constants.json`. The structural engine does not import it. Run the explicit post-hoc comparator separately if desired.
