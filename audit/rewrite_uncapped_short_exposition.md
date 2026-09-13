# Short substitution exposition, 2026-09-13

Starting point: the author's abstract in commit 852a2f6. The abstract now
compares bounded long-run growth under complementarity with growth that
increases without bound across AI-dominated capped equilibria as the
efficiency upper bound rises. It no longer asserts a singularity.

## Editorial changes

- Preserve the author's abstract and all other introduction paragraphs.
- Replace the introduction's uncapped-economy paragraph by this comparison,
  retaining its statement about the proved unit-elastic equilibrium.
- Update the Section 5 overview so it does not promise the suppressed result.
- Replace Section 5.3 with the comparative-static implication and the dated
  return inequality, derived from the same production and pricing conditions.
- Preserve the entire previous subsection as line comments under explicit
  markers. Removing each "% " prefix (or "%" on an empty line) reconstructs
  the text exactly.
- Comment only the input of its proof in appendix.tex. The complete proof
  remains in its original file, unchanged; it is not printed without its
  proposition. Remaining proposition/equation numbers are automatic.

The archival subsection's LF-normalized SHA256 at 852a2f6 is
3ab95da79250719fc13f0170a3f6abf98cd5c4d52a97434ac84077145a4587b6.
An automated test checks exact preservation. Earlier tests still check the
preserved mathematical results but do not call those statements active.

## Mathematical scope

For sigma>1, R(B) is an infimum of the dated net return at fixed B over the
static monopoly allocations. Equality is attained only as s_X tends to one.
The dated inequality does not use an efficiency cap, a research-investment
floor, a BGP, or an assumption that B actually diverges.

If B does diverge, r and Y/K must diverge. Production then implies
Z/Y=(Y/K)^[alpha/(1-alpha)] -> infinity. Household Euler directly implies
unbounded consumption-per-person growth, not the same statement about the
dated output growth rate. No convergence of C/Y has been silently imposed.
The comparison across capped equilibria is not a proof of uncapped
equilibrium existence/nonexistence or a finite-time singularity.

At sigma<1 the analogous static comparison is reversed on the monopoly
domain e_X<1. At sigma=1 this power-form R(B) is undefined and the
Cobb-Douglas equations apply. Exact rational tests check the sign reversal.

The author's abstract remains unchanged. Suggested later copy edits:
"Hence ... therefore" duplicates the connector; "IA" should be "AI";
"growth is always bounded" should specify long-run output-per-worker growth,
because transitional growth can exceed gamma.

No simulation, parameter, model notation, or research law was changed.

Verification: all 74 tests in the ten-module analytical/source suite pass.
The PDF compiles with no undefined references or box warnings. Visual review
covers the abstract, introduction, new subsection, and appendix boundary.
