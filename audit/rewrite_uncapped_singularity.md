# Conditional uncapped explosion, both sides of eta = alpha

Date: 2026-09-12. Starting commit: aabeff7 (author's latest Section 5.2 edits).

## Result and scope

Section 5.3 now contains an automatically numbered proposition. Its proof is
in the existing Appendix A, headed "Proof of Proposition" with a label-based
link. No new appendix section, model, parameterization, algorithm, or numerical
trajectory is introduced.

For sigma > 1 and 0 < eta < 1, consider a differentiable solution of the dated
intratemporal and dynamic equations on [0,T), where T is not assumed finite.
The conditions are:

- Positive K, B, C and M (no positivity requirement on developer profits).
- B tends to infinity and s_X tends to one at the maximal endpoint.
- C/Y and M/Y tend to positive finite constants.
- The log derivatives of C/Y and M/Y, divided by Y/K, tend to zero.

The last condition is explicit: convergence of a differentiable ratio alone
does not imply convergence of its derivative. These are asymptotic conditions,
not assumptions of constant expenditure shares along the whole trajectory.

The proof derives

    dot(Y/K)/(Y/K)^2 -> eta*alpha*(1-alpha)/(1-alpha*eta) > 0.

Consequently T is finite, and B, K, Y, C and r diverge at T. This excludes an
infinite-horizon equilibrium with those asymptotics. It does not construct a
solution satisfying the conditions or prove that every initial stock pair
enters the excluded regime. Global agent optimality is not inferred from the
dated equations. An exploding solution is not presented as an equilibrium.

For eta > alpha, the existing fixed-price profitable-deviation theorem already
rules out a finite-valued developer optimum without the new convergence
conditions. For eta <= alpha, general existence/nonexistence outside the
excluded class is still open. The threshold eta = alpha in the former theorem
is not a boundary for the new conditional explosion coefficient.

## Proof audit

1. Derive an EXACT static identity for z = Y/K as a function of B and s_X from
   CES production and the monopoly condition. Only then differentiate it.
   Differentiating a limiting approximation without derivative control would
   be invalid.
2. Euler plus consumption-share regularity gives g_Y/z -> alpha. Research-share
   regularity gives g_M/z -> alpha. The derivative of s_X is eliminated using
   its exact CES identity; no extra assumption on that derivative is needed.
3. Set h = g_B/z and rescale time by the integral of z. Show this rescaled time
   tends to infinity even if the physical endpoint is finite. The exact h
   equation is logistic with converging positive coefficients, which proves
   h -> eta*alpha^2/(1-alpha*eta). This convergence is derived, not assumed.
4. The resulting positive quadratic growth of z implies a finite endpoint by
   reciprocal integration. The positive limit of g_K/z and the divergent
   integral of z then imply K -> infinity, not just Y/K -> infinity.

Compared with the archived singular-limit argument, no assumptions on the
limits of g_B/z, qB/K, or the investment share are used. The proof is valid
throughout 0 < eta < 1, rather than only eta < alpha. It is not uniform as
sigma approaches one: the AI-dominance limit is taken for each fixed sigma > 1.
There is no conflict with the separate unit-elastic BGP theorem.

## Literature used and its limits

- Davidson, Halperin, Houlden and Korinek (2026), July author version,
  https://basilhalperin.com/papers/singularities.pdf, Section 3.2, equations
  (23)-(28), Proposition 1.*. Technological and economic feedback can jointly
  overcome diminishing returns. That analysis fixes saving and factor shares;
  its theorem is not imported as an equilibrium theorem for this paper.
- Ceballos-Lira, Macias-Diaz and Villa (2011),
  https://ejde.math.txstate.edu/Volumes/2011/05/ceballos.pdf,
  Lemma 2.2 and Theorem 3.1. The scalar Osgood/comparison criterion supplies
  the finite-time step; the elementary reciprocal calculation is also shown.
- The existing Nordhaus (2021) citation is retained for the economic role of
  substitution in singular growth, not for the developer-optimality proof.

## Preservation and checks

The author's latest unstarred explicit BGP formulas and commented-out repeated
claims in Section 5.2 are preserved. Two literal source tests were updated to
match those edits; finiteness, global-optimality and TVC checks still inspect
the proof. Title, abstract, introduction, calibration, simulation code, stored
trajectories, figures and companion paper are unchanged. The Section 5 overview's
unqualified substitution/singularity sentence is qualified to match the new
result. Author-requested provisional wording in the abstract is not rewritten.

New test module: tests/test_rewrite_uncapped_substitutes.py. It checks exact
rational derivative identities and the logistic reduction; signs below, at
and above eta = alpha; the log-level static identity near sigma = 1; and proof
links/scope/citations. Alpha values: 0.2, 0.33, 0.6. Eta values for the sign
check: alpha/2, alpha, (1+alpha)/2. Sigma values for the level check:
1.0001, 1.001, 1.01, 1.5, 4. The log-level roundoff bound includes the large
intermediate terms that cancel near one; it is not a simulation tolerance.

Reproduce from the repository root with the existing Python dependencies:

```powershell
python -B -X utf8 -c "import sys,unittest; sys.path[:0]=['.python-packages','tests']; r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(['test_companion','test_rewrite_proposition_structure','test_rewrite_uncapped_unit','test_rewrite_uncapped_complements','test_positive_ai_branch','test_rewrite_finite_frontier','test_rewrite_uncapped_substitutes'])); sys.exit(not r.wasSuccessful())"
tectonic --keep-logs --keep-intermediates --outdir output/pdf main_rewrite.tex
```

These tests audit algebra and implementation consistency. They do not replace
the analytical proof or certify existence of new economic trajectories.

Executed result: all 52 tests passed. Tectonic compiled without undefined
references/citations or overfull/underfull boxes. The proposition is on page 21;
its proof is on pages 58-60. The affected main-text and proof pages were
rendered and visually inspected. The stable public PDF is updated from this
same build; no fresh equilibrium transitions were computed.

Next mathematical step: determine whether the dated equations force the
assumed positive limiting shares and AI dominance, or permit alternatives
(vanishing research/consumption shares, bounded efficiency, or nonconvergent
ratios). Until then, eta <= alpha does not have a general nonexistence theorem.
