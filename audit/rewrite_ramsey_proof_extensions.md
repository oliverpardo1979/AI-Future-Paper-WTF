# Ramsey-based extensions of the uncapped proofs

Date: 2026-09-13. Baseline: commit 5857ea9.

## Authorized scope

Implement recommendations 2 and 3 from the preceding Ramsey literature
review: broaden the unit-elastic existence proof and try to remove the
assumed consumption-growth limit under complementarity. The no-AI remark,
finite-cap propositions, title, abstract, introduction, simulations, and
calibrations are unchanged.

## Proposition 4: broader sufficient conditions

The condition eta <= 1/2 has been removed; the other restrictions remain.
The original concavity proof applies for eta <= 1/2. Above 1/2 the proof
uses S=B^(1-eta), with costate p=q*B^eta/(1-eta). This is an invertible
coordinate change on the same feasible set, confined to the proof.

- Research becomes Sdot=(1-eta)*chi*M^eta.
- Optimized operating profit is a positive coefficient times S to the
  power (1-alpha)*omega_X/((1-(1-alpha)*omega_X)*(1-eta)).
- eta<alpha and eta+omega_X<1 imply that this exponent is less than one
  when eta>1/2. The transformed Hamiltonian is jointly concave.
- The developer TVC is unchanged up to a positive constant because
  p*S=q*B/(1-eta).
- The original first-order equations, levels, growth rates and resource
  accounting are unchanged. The global verification extends to nearby
  off-BGP candidates if the appendix's separate spectral conditions hold.

Only the obsolete eta <= 1/2 rejection was removed from
`PositiveAIBenchmarkParameters.__post_init__`. Remaining seed restrictions
are preserved. The proposition still constructs the initial K and B for
its BGP; it does not establish existence from arbitrary initial stocks.

## Proposition 3: convergence is now a conclusion

The assumed finite limit of aggregate consumption growth was removed.
The proof still assumes an equilibrium exists and B tends to infinity.
Its logical order is:

1. Static monopoly optimality bounds X/(AL) by a finite revenue-maximizing
   value and identifies the limiting Cobb-Douglas production coefficient.
   At fixed B, Y/K decreases in K/(AL).
2. Feasibility and Euler give an upper bound on normalized consumption.
   The integrated household budget, household TVC, and developer
   continuation optimality give C >= (rho-n)*K and a bound on the present
   value of wage income. The auxiliary continuation value is derived,
   finite and nonnegative; no new asset or financing condition is imposed.
3. At small normalized capital the return is high; elsewhere normalized
   wages have a positive lower bound. These two regions give a uniform
   present-value bound for effective labor without assuming convergence
   of the return. The costate identity and developer TVC then bound future
   research expenditure by a constant times AL/B.
4. A crossing argument rules out repeated late descents of normalized
   capital from epsilon to epsilon/2. On this interval consumption grows,
   the duration is bounded, and the required research spending would
   contradict the present-value bound. Capital and, hence, consumption
   are eventually bounded away from zero.
5. The research-growth inequality converts the integral research bound
   into M/(AL) -> 0. The normalized two-dimensional dynamics converge
   uniformly on the resulting compact positive region to a Ramsey system.
6. Time translations have complete limiting Ramsey orbits. The limiting
   system has a unique saddle and positive Bendixson-Dulac divergence
   (rho-n)/c^2. Periodic and homoclinic orbits are excluded; its only
   complete orbit confined to a compact positive region is its stationary
   point. This establishes convergence, rather than assuming it.
7. The static derivative and research-growth bounds verify the output and
   wage growth limits separately. Convergent levels alone would not suffice.

This proof uses only the maintained 0<eta<1 in the complementarity case.
It does not use eta<alpha or eta<=1/2. It does not prove existence from any
initial state, uniqueness of the IA equilibrium, or that B necessarily
diverges along every equilibrium.

The Ramsey phase-portrait reference is Groth (2013), Chapter 10, especially
Appendices A and E. The new bibliography entry is cited only in the proof.
The persistence and research bounds are our model-specific arguments, not
results attributed to Groth. No unverified asymptotically autonomous
convergence theorem is invoked in place of the explicit compact-orbit proof.

## Reproducible validation

From the repository root with the replication dependencies installed:

```powershell
python -B -X utf8 -c "import sys,unittest; sys.path[:0]=['.python-packages','tests']; names=['test_rewrite_uncapped_complements','test_rewrite_uncapped_unit','test_positive_ai_branch','test_rewrite_proposition_structure','test_rewrite_finite_frontier','test_rewrite_uncapped_substitutes','test_rewrite_investment_optimality','test_rewrite_short_substitution','test_rewrite_davidson_route','test_companion']; result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(names)); sys.exit(not result.wasSuccessful())"
```

Result: 84 tests passed. The first run identified a source assertion sensitive
to a line break; it was changed to normalize whitespace, without weakening
the substantive scope assertions.

Added checks cover exact rational static elasticities, the Dulac identity,
the limiting saddle determinant, transformed concavity, transformed FOCs
and TVC, and original dated equilibrium equations. New unit-elastic cases
include (eta,alpha,omega_X)=(0.6,0.7,0.2) and (0.75,0.85,0.1), checked at
dates 0,25,200. Exact inequality checks also cover eta=0.500001,0.51,0.8,0.99.
These are algebraic tests and evaluations of explicit BGP solutions, not
new numerical transition simulations or a substitute for the proof.

An in-memory import of the module from commit 5857ea9, compared with the
working module, confirmed bit-for-bit equality of every default BGP field.

Compiled `main_rewrite.tex` using Tectonic with logs and intermediates.
The 72-page PDF has no overfull/underfull boxes, undefined citations,
undefined references or duplicate labels in the final log. Visually checked
pages 19-20 (statements), 54-60 (proofs), and 66-67 (appendix conditions).
The public PDF is a byte-identical copy of the local compiled artifact.
