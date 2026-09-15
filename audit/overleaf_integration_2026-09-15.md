# Approved Overleaf integration, September 15, 2026

Baseline: `a81f46b` (local main and origin/main matched before editing).

## Changes

- Integrated the author's Section 6.1 opening: four elasticities, common
  remaining parameters and exogenous initial values, elasticity-specific
  pre-RSI capital stocks, and the upper bound between the 1.5 and 1.1 thresholds.
- Preserved the distinction between chi=0 and zero inference compute, all
  subsequent initial-condition equations, and the classical-growth citations
  recently added in Sections 2 and 4.2.
- Applied the approved grammatical corrections in Section 5.3, commented its
  monotonicity footnote as requested, and distinguished unbounded discounted
  net profit across research plans from a path attaining infinity in finite time.
- Matched the proof to Proposition 5's single eta>alpha finite-horizon claim.
  Preserved the entire previous, broader proof as comments, including eta<alpha,
  the equality case, finite-upper-bound existence, and the infinite-horizon
  deviation argument. The surviving research-burst payoff equation is unchanged.
- Removed the obsolete reference to Proposition 5(i) from the shared parameter
  table; no parameter value or simulation input changed.

## Verification

- Tectonic compiled `main_rewrite.tex`: 71 pages. No undefined references,
  multiply defined labels, overfull/underfull boxes, or bibliography warnings
  appear in the final log. Tectonic emits the existing nonfatal Fontconfig notice.
- Four new source-scope regression tests passed, along with the three terminology
  and seven simulation-selection tests (14 focused tests total). These are
  manuscript checks, not a new numerical equilibrium audit.
- Extracted text confirms the single-result Proposition 5 on page 23, its proof
  on page 51, and the updated design on pages 23-24.
- Rendered pages 22, 23, 24, 26, 32, and 51 were visually checked; equations,
  proof links, headings, and both parameter tables are legible and unclipped.
- Title, abstract, introduction, simulation programs, computed trajectories,
  and numerical figures are unchanged. No simulations were rerun.
