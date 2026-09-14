# Proposition 4: local equilibrium convergence

Date: 2026-09-13. Baseline: `359f6fc`.

Historical report for commit `ccfe608`. Its treatment of the two local
properties as additional assumptions is superseded by
`rewrite_proposition4_stability_from_primitives.md`, which proves both
from the existing parameter restrictions.

## Scope and result

The user requested that Proposition 4 cover equilibrium trajectories from
initial stocks near its balanced-growth path, not only the exact BGP.
The local result was already stated separately in Appendix C. It is now part
of Proposition 4, and the two proofs have been joined under its single proof
heading in Appendix A. Appendix C retains the normalized variables, allocation
ratios, local conditions, and calibration check, without another proposition.

The quantifiers are explicit: for every sufficiently small neighborhood of
the reference BGP in stationary coordinates, there is an open neighborhood
of its initial stocks such that each stock pair has an equilibrium remaining
in the chosen stationary neighborhood and converging to the reference BGP.
Initial consumption and the shadow price are selected as continuously
differentiable functions of the two stocks. They are not arbitrary initial
data. Local uniqueness concerns paths staying near and converging to this
BGP; neither global uniqueness nor convergence of every possible equilibrium
from those stocks is asserted.

The exact BGP growth equalities are preserved. The text now distinguishes
these dated equalities from the limits along nearby equilibrium trajectories.
Main-text notation remains unstarred; Appendix C retains its existing starred
reference paths and log deviations. Both historical proposition labels now
refer to Proposition 4, preserving cross-reference compatibility.

## What the proof requires

Besides the existing BGP parameter restrictions, the local result retains
two sufficient conditions, now explicitly numbered in Appendix C:

1. The normalized Jacobian is hyperbolic with a two-dimensional stable
   invariant subspace.
2. Projection of that subspace onto the two predetermined stocks has full
   rank.

These conditions are not asserted to follow from the BGP growth identities
or from the primitive restrictions for every calibration. They are verified
numerically at the paper's calibration: eigenvalues approximately
`(-0.098971, -0.003194, 0.040391, 0.149290)` and absolute state-projection
determinant `0.6037` using unit-length stable eigenvectors. An orthonormal
basis changes that determinant's numerical value but not its nonzero rank.

The stable-manifold theorem supplies converging trajectories. Full rank and
the inverse-function theorem give a graph over initial stocks. An exponential
bound on deviations supplies the nested-neighborhood statement. Convergence
of the vector field gives convergence of growth rates, not just levels.
The proof then checks both transversality conditions, finite objectives, and
global household and developer optimality. The latter uses the existing
concavity verification at the resulting price paths. No model equation or
financing assumption is added.

## Verification

The 11 tests in `test_rewrite_uncapped_unit` pass. Two new checks cover the
unified statement/proof structure and the tangent graph over independently
perturbed capital and AI-efficiency stocks. The latter checks Jacobian
invariance and the quadratic nonlinear defect of the tangent approximation;
it does not present that approximation as an equilibrium trajectory.

The broader ten-module suite runs 86 tests: 83 pass and three pre-existing
source-wording assertions fail. Running those same three tests against the
TeX sources at `359f6fc`, substituted in memory without touching files,
reproduces all three failures:

- `test_new_section_order_and_explicit_conditional_scope` expects the removed
  explanatory paragraph after Proposition 3.
- `test_upper_bound_terminology_preserves_other_frontiers` expects the phrase
  `technological frontier`.
- `test_abstract_and_intro_specify_long_run_growth_and_unit_benchmark` expects
  earlier abstract wording.

Those assertions and the author's corresponding text are outside this edit.
They were not changed to obtain a clean test count. No transition simulations
were run, and the simulation code, parameters, and results are unchanged.
Proposition 3, the title, abstract, introduction, and literature review are
also unchanged.

Tectonic compiles `main_rewrite.tex` successfully. The final log has no
undefined references/citations, duplicate labels, or overfull/underfull boxes.
The compiler needed a missing font downloaded; this did not require changing
the manuscript's typography. The printed proposition remains number 4.

Reproduce the focused checks from the repository root:

```powershell
python -B -X utf8 -c "import sys,unittest; sys.path[:0]=['.python-packages','tests']; r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_rewrite_uncapped_unit')); sys.exit(not r.wasSuccessful())"
```

The compiled PDF retains its existing local and public filenames.
Visual verification covered printed pages 20–21 (statement and interpretation),
62–63 (local convergence proof), and 69–70 (local conditions). The proposition
and its main proof link fit together on page 20. Both proposition-label aliases
resolve to number 4; the local proof anchor resolves inside its single proof.
