# Archived uncapped asymptotic result

These two files preserve the exact sources at commit `819142e`, before the
2026-09-12 adoption of the persistent-investment version of Proposition 5:

- `uncapped_section_before_persistent_investment.tex`: the prior Section 5,
  including the original conditional asymptotic statement.
- `uncapped_asymptotic_explosion_proof.tex`: its proof, including the
  normalized growth coefficient and logistic reduction.

They are not inputs to `main_rewrite.tex` and must not be compiled alongside
the active sources: their labels intentionally duplicate historical labels.
The archive does not reverse any author edits or alter simulations. The old
asymptotic algebra remains tested in `tests/test_rewrite_uncapped_substitutes.py`.
The active theorem is tested in `tests/test_rewrite_davidson_route.py`.

The replacement derives unbounded AI efficiency from persistent investment
rather than assuming it. General equilibrium nonexistence for eta <= alpha
remains unproved. See `audit/rewrite_davidson_route.md` for the exact scope.
