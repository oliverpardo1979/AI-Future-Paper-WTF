# Proposition 4: local stability follows from the primitives

Date: 2026-09-13. Baseline: `ccfe608`.

## Statement and scope

The main proposition now has two parts: (i) existence of an equilibrium
trajectory with the existing BGP growth rates, interest rate, and labor share;
(ii) existence of a convergent equilibrium from every initial condition in
an open neighborhood of that BGP's initial condition `(A0,N0,K0,B0)`.
The four displayed economic equations and parameter restrictions are unchanged.
No separate spectral or projection assumptions appear in the statement.

For perturbed A0 and N0, convergence is to the corresponding reference BGP,
whose levels depend smoothly on those exogenous initial values. The statement
does not assert convergence to unchanged absolute levels when effective labor
changes. The appendix retains precise local uniqueness, jump-variable selection,
and normalized convergence, without claiming global uniqueness or convergence
from arbitrary initial consumption and shadow prices.

## Analytic argument

The proof retains the original four-dimensional Jacobian and makes an
invertible linear change of its log deviations. All new scalar abbreviations
are confined to this matrix algebra; economic notation, timing, and simulation
coordinates are unchanged.

1. The existing restriction `eta + omega_X < 1` implies that the sum of the
   two transformed reduced-production elasticities is strictly less than one.
2. The characteristic polynomial is positive at zero and at negative infinity,
   and negative at a particular negative root of one quadratic factor.
   There are therefore two distinct negative roots. Descartes' rule shows
   that there cannot be further negative roots or repeated negative roots.
3. The other two roots have positive sum and product. They are either both
   positive or a conjugate pair with positive real parts. Hyperbolicity and
   exactly two stable directions follow for every admissible parameter set.
4. Normalize the transformed AI-state component of each stable eigenvector
   to one. The capital component is negative at the first stable root and
   positive at the second. Their projections onto the two states are
   linearly independent, proving full rank without an additional assumption.
5. The stable-manifold and inverse-function theorems provide a local graph
   selecting consumption and the shadow price from the given stocks.
   The normalized vector field is independent of A0 and N0; the explicit BGP
   levels depend smoothly on them. The open neighborhood therefore extends
   to all four initial values in the main statement.
6. The existing exponential-convergence argument verifies both transversality
   conditions and finite objectives. The existing concavity verification
   establishes global agent optimality at the resulting price paths. The
   constructed trajectories are equilibria, not just solutions of FOCs.

Appendix C now describes the spectral and projection properties as proved
conclusions. Its calibration-specific eigenvalues remain as an illustration,
not as evidence sufficient to establish the general result. The proof remains
under the single Proof of Proposition 4 heading in Appendix A.

## Reproducible checks

Run from the repository root with NumPy available:

```powershell
python -B -X utf8 -c "import sys,unittest; sys.path[:0]=['.python-packages','tests']; r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_rewrite_uncapped_unit','test_uncapped_unit_local_stability'])); sys.exit(not r.wasSuccessful())"
```

All 14 focused tests pass. The new module checks:

- Exact rational determinant expansion over all 24 permutations, the
  polynomial factorization, coefficient signs, and two key identities in
  198 admissible parameter configurations, including zero depreciation.
- Similarity to the existing implemented equilibrium Jacobian in six
  configurations, including research elasticities above one half; stable
  root ordering and eigenvector projection formulas.
- Invariance of the nonlinear normalized vector field to A0 and N0.

These tests check the algebra and implementation correspondence. The written
sign argument establishes the general result; the finite grid is not used
as a proof of existence. No transition simulations were run. No model code,
calibration, numerical results, title, abstract, introduction, other proposition,
or literature-review text was changed.

The broader eleven-module suite runs 89 tests: 86 pass, with the same three
pre-existing source-wording failures documented in the previous audit.
Running those three tests with TeX sources from `ccfe608` substituted in
memory reproduces all three failures. They expect author-deleted text after
Proposition 3, the phrase `technological frontier`, and older abstract wording;
none concerns the new proof. Those unrelated texts and tests remain unchanged.

Tectonic compiles successfully, with no unresolved references/citations,
duplicate labels, or overfull/underfull boxes in the final log. Proposition 4
and its proof link fit on printed page 20. Its proof is on pages 60--65,
with the new analytic stability argument on pages 62--65; Appendix C describes
the proved local properties on pages 71--72. Visual inspection of the revised
statement, local proof, and Appendix C found no layout defects. The local PDF
and public PDF retain their existing filenames and are byte-identical.
