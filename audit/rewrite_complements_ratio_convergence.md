# Section 5: derived allocation ratios and lighter notation

Date: 2026-09-13. Source baseline: e2118e2 (including the author's latest
abstract change). This note supersedes the conditional-characterization
assumptions recorded in the historical uncapped-section audit.

## Proposition 3: what changes

The old statement assumed positive finite limits of K/(AL) and C/(AL), and
finite limits of the growth rates of C, Y, and w. The revised statement
assumes only an equilibrium with B tending to infinity and a finite limit
of aggregate consumption growth. The model's original primitives apply:
0 < sigma < 1, 0 < alpha < 1, 0 < eta < 1, rho > n, gamma > 0,
n >= 0, delta >= 0, positive CES weights, and chi > 0.

It now derives

- K/Y -> alpha/(rho + gamma + delta) > 0;
- C/Y -> 1 - alpha(delta + n + gamma)/(rho + gamma + delta) > 0;
- U/Y, M/Y -> 0;
- positive finite limits of K/(AL), C/(AL), and Y/(AL);
- the previously stated output, wage, return, and income-share limits.

This is a conditional characterization, not an existence theorem. It does
not prove that B diverges or that consumption growth converges along every
equilibrium. It does not impose a BGP or fixed saving/research shares.

## Proof audit

1. Feasibility bounds capital per effective worker. A finite limit of g_C,
   Euler, and the capital-return equation bound Y/K. Static monopoly pricing
   then forces e_X -> 1 and s_X -> (1-sigma)/(1-alpha sigma) as B -> infinity.
   The CES identities yield positive limits of X/(AL), K/(AL), and Y/(AL),
   and U/(AL) -> 0. No allocation-ratio convergence is assumed.
2. Consumption cannot grow permanently faster than effective labor without
   violating resources. To exclude slower growth, use the exact identity

   d[D(K + eta/(1-eta) qB)]/dt
   = D[(1-alpha)Y - C - U/(1-eta)].

   The research FOC and costate imply
   d(qB)/dt = r qB - U + (1-eta)M/eta. Thus the positive weighted combination
   cancels M. Both TVCs require its discounted value to tend to zero;
   C/Y -> 0 would instead make it eventually strictly increasing.
   The combination is a proof device, not a new definition of firm value.
   This step works for all 0 < eta < 1: no eta <= 1/2 or eta < alpha is added.
3. With r -> rho+gamma > n+gamma, the developer TVC bounds discounted future
   research by eta/(1-eta) times discounted future inference expenditure.
   Dividing by current AL makes this bound vanish. The dated FOC/costate
   also gives (1-eta)g_M = r-U/(qB) <= r. This one-sided growth bound excludes
   arbitrarily narrow upward spikes and turns the integral result into the
   pointwise limit M/(AL) -> 0. It is not an assumed research-rate limit.
4. Integrating normalized resources over [t,t+1], using convergence of k and
   g_C-n-gamma -> 0, proves convergence of c to its positive resource residual.
   The residual numerator is rho-n+(1-alpha)(n+gamma+delta), hence positive.
5. Integrating the research law with the same one-sided bound controls g_B.
   The static marginal-revenue function has a simple zero at the limiting x.
   Implicit differentiation then gives dot x -> 0, and hence the output/wage
   growth limits. Convergence of levels alone is not used to infer convergence
   of derivatives.

Both transversality conditions and all relevant dated model equations are
referenced by automatic labels in the proof. No new proof subsection or lemma
is introduced. The proof remains in the existing Appendix A proof section.

## Section 5.2 and the associated unit-elastic appendix

The derived aliases beta=(1-alpha)omega_X and lambda=(1-alpha)omega_L are
removed from Section 5.2, Appendix C, and its two proofs. Expressions now
use the original primitives, or the already defined u*=U/Y where useful.
The production-growth coefficient becomes omega_X/omega_L. The existing
equation labels and the appendix's reference-BGP notation are preserved.

The simulation implementation and its internal aliases are unchanged.
Tests compare the expanded initial-stock and profit formulas with the
preserved implementation/previous expressions. No primitive parameter,
state, control, price, timing convention, or normalization is redefined.
Unrelated locally defined aliases elsewhere in the manuscript are untouched.
Title, abstract, introduction, Section 5.3 (including its commented archive),
calibration, transition data, figures, and companion paper are preserved.

## Reproduction and limits of the checks

From the repository root, using Python with the existing dependencies:

```powershell
python -B -X utf8 -c "import sys,unittest; sys.path[:0]=['.python-packages','tests']; result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(['test_companion','test_rewrite_proposition_structure','test_rewrite_uncapped_unit','test_rewrite_uncapped_complements','test_positive_ai_branch','test_rewrite_finite_frontier','test_rewrite_uncapped_substitutes','test_rewrite_davidson_route','test_rewrite_investment_optimality','test_rewrite_short_substitution'])); sys.exit(not result.wasSuccessful())"
```

The checks cover exact-rational TVC cancellation on both sides of eta=1/2,
positivity of allocation ratios, the dated CES/monopoly identity, the simple
marginal-revenue zero, formula equivalence, BGP dated conditions, Jacobian
agreement, and source scope/labels. They check algebra and regressions, not
equilibrium existence or the analytic convergence proof by numerical examples.
No transition simulations are run by these tests.

The manuscript is compiled from main_rewrite.tex. Changed main-text and
appendix pages are rendered and visually inspected before updating the public
PDF at its existing stable filename.

Verification completed: all 80 tests passed. Tectonic compiled successfully
without undefined references, duplicate labels, or overfull/underfull boxes.
Visual checks covered pages 19-20, 54-58, and 64-66; page 54 was re-rendered
after the final wording clarification. The revised Proposition 3 is on page
19, its proof on pages 54-56, and Section 5.2 on pages 19-20.
