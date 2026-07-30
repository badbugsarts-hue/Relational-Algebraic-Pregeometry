# CENSUS-001 Erratum

## Locked source

- Commit: `c8daae119b8699e665c462c06e8580b6e34f831a`
- Path: `manuscript/Relational_Algebraic_Pregeometry_v4_0_DRAFT-001.tex`
- Git blob: `c3197df2b927dd4dd76296bafe21ffea1283d03a`
- Blob SHA-256: `f9d0c1a19c754c83dd425c5b9f7792159cb5ed5bda8b6f81facf1da89f139e35`

## Correction

The previous execution handout's count of 144 semantic class-E evidence
markers and one `E pending` qualifier applies to the supplied watermarked
baseline:

```text
Git blob: 7962e5e74fb504416565f276512da12e4eaaf5b5
Blob SHA-256: 2e72d1cdd32e1bea25d077b3dfe9b769251f795796d6109f762e462e4ecdedab
semantic \catmark calls: 592
class E: 144
E pending qualifier: 1
```

Two independent scans of the locked final Git blob identified above find:

```text
semantic \catmark calls: 586
class E: 143
E pending qualifier: 0
```

The `\catmark{E\,pending}` occurrence belongs to the baseline blob and is
absent from the locked final blob. The two census results therefore describe
different revisions and do not conflict. No synthetic marker or manuscript
edit is introduced to make either result satisfy the other revision's
expectation.

The correction concerns census provenance only. It does not adjudicate the
scientific correctness of any marked claim and does not upgrade evidence.

[TENSION ALERT — ATTRIBUTION CORRECTED] The earlier `E = 144` assertion
applies to baseline blob `7962e5e74fb504416565f276512da12e4eaaf5b5`;
the locked final blob `c3197df2b927dd4dd76296bafe21ffea1283d03a`
yields `E = 143`.

NO DIRECT MANUSCRIPT APPLY
NO MERGE
NO EVIDENCE UPGRADE
