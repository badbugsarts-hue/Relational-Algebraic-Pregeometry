# Building the manuscript

`RAP_v4_0.tex` is the full corrected working manuscript, not a newly deposited version. The sole new text operation in this repository copy is bibliography externalization/alignment; the body and D19–D25 boxes are unchanged. `bibliography-alignment.patch` records that operation. The original inline bibliography, including its documentary note, is retained under provenance for audit, not re-endorsed as verified.

The 124-record `references.bib` contains the 120 original publication units plus four component works. Seven additional guide-only comparisons remain outside this manuscript bibliography. Existing citation keys are preserved. Natbib/unsrtnat and `nocite{*}` retain the full manuscript reference set. Article-number records additionally receive a `pages` fallback where needed because classic BibTeX styles may ignore `eid`; bibliographic identity is unchanged.

On a separate machine with a suitable TeX installation and BibTeX, from the repository root:

```sh
latexmk -pdf -cd manuscript/RAP_v4_0.tex
```

Required packages are declared in the source, including natbib, tcolorbox, TikZ, physics, cleveref and the font packages. No external figure inclusion is required by the supplied source. Check bibliography Unicode handling, overfull boxes, equations, tables and all cross-references in the resulting PDF. If the local engine requires additional Unicode handling, resolve it in the TeX environment rather than declaring an uninspected PDF final.

No TeX engine was available for this package preparation. Compilation and visual inspection remain NOT_RUN. The old UIDT PDF and the uncorrected original RAP PDF are not substituted for a corrected result.
