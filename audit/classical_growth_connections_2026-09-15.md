# Classical growth connections

## Scope and baseline

- User request: make the connection to Rebelo explicit and use other classical
  endogenous-growth references only when directly relevant.
- Baseline: user commit `2b0b5a6`, fast-forwarded before editing.
- Existing bibliography entries already contain Rebelo (1991), Jones and
  Manuelli (1990), and Romer (1990). No duplicate entries were added.
- Title, abstract, introduction, equations, numerical code, parameters, and
  stored simulation results are outside this edit.

## Sources checked

Previously downloaded full texts remain in the ignored directory
`tmp/related_literature_audit_2026-09-13/`. This audit checked the passages
listed below against the claims being added, not every theorem in each paper.
The earlier download provenance is in
`audit/related_literature_2026-09-13/source_manifest.json`.

1. Sergio Rebelo (1991), *Long-Run Policy Analysis and Long-Run Growth*,
   Journal of Political Economy 99(3), 500-521.
   DOI: https://doi.org/10.1086/261764.
   Consulted the NBER working-paper version (1990, w3325), PDF pages 2-8:
   reproducible inputs, nonreproducible factors, and the linear investment
   technology. The author's publication list confirms the published citation:
   https://www.kellogg.northwestern.edu/faculty/rebelo/htm/papers.html.
   Cached full text:
   https://www.nber.org/system/files/working_papers/w3325/w3325.pdf.

2. Larry E. Jones and Rodolfo E. Manuelli (1990), *A Convex Model of Equilibrium
   Growth: Theory and Policy Implications*, Journal of Political Economy
   98(5, Part 1), 1008-1038. DOI: https://doi.org/10.1086/261717.
   Consulted the NBER working-paper version (w3241), PDF pages 2-8:
   fixed factors can remain in production; the limiting marginal product of
   capital need not vanish; the growth condition compares returns with
   preferences and depreciation, not merely with zero.
   Published metadata checked against the journal record.
   Cached full text:
   https://www.nber.org/system/files/working_papers/w3241/w3241.pdf.

3. Paul M. Romer (1990), *Endogenous Technological Change*, Journal of Political
   Economy 98(5, Part 2), S71-S102. DOI: https://doi.org/10.1086/261725.
   Consulted the published article, PDF pages 2-5 (printed S71-S74):
   intentional research, nonrival and partially excludable knowledge, and
   markups on differentiated intermediates financing design costs.
   Full text: https://web.stanford.edu/~klenow/Romer_1990.pdf.
   Free entry and multiple differentiated producers distinguish Romer's market
   structure from the present integrated developer. No claim of identical
   institutions or strictly positive present-value entry profits is added.

## Placement and economic distinctions

- Section 2: spell out Romer's research-financing mechanism and the distinct
  accumulation mechanisms in Rebelo and Jones-Manuelli.
- Section 4.2, after Proposition 1's proof pointer: interpret the already
  derived positive limiting output-capital ratio as an asymptotically linear
  production structure. This explains growth with asymptotically constant B.
- Section 6.1: distinguish shutting down efficiency improvements (chi=0) from
  shutting down the expansion of AI services. Inference compute is a costly
  flow, not a capital stock. The calibrated pre-RSI labor bottleneck depends
  on B0 and the remaining parameters, not on chi=0 alone.

## Limits on the claims

- The classic papers are mechanism precedents, not proofs of equilibrium
  existence for this monopoly model.
- The capped positive-chi existence proposition is not extended mechanically
  to chi=0, nor is arbitrary-initial-state existence newly asserted.
- A positive limiting return alone is not sufficient for growth above gamma;
  the threshold comparison already in Section 4 remains essential.
- No new named proposition, notation, research technology, calibration, or
  simulation was introduced. Other classics were not added as a generic list.

## Verification

- Tectonic compiled `main_rewrite.tex` successfully (73 pages); no undefined
  references, multiply defined labels, overfull/underfull boxes, or BibTeX
  warnings were reported.
- Ten focused tests passed: three AI-terminology tests and seven simulation
  selection/preservation tests. No new numerical simulations were run.
- Extracted PDF text contains all four new explanatory passages.
- Visual review of PDF pages 1, 4, 5, 18, and 23 found no layout defects.
- The updated abstract on page 1 is the user's version, not a restoration of
  an earlier assistant draft.

## Separate issue noticed in the user's baseline

The new Proposition 5 in Section 5.3 states only the eta > alpha result, while
Section 6.1 still motivates eta < alpha by citing Proposition 5(i). This
cross-reference no longer matches the proposition's stated content. It is not
caused by these citation edits and was left unchanged for author review.
