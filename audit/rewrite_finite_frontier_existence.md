# Finite-frontier existence and long-run comparative statics

Updated: 2026-09-10. Source: Section 4 and the common existence argument in
Appendix A (Proofs) of `main_rewrite.tex`.

## Scope

The results construct infinite-horizon equilibrium trajectories for an open
set of nearby predetermined normalized stocks. They are local in initial
conditions, not finite-horizon simulations and not merely BGP calculations.
The two jump variables are selected by a stable-manifold graph. Both TVCs,
finite objectives, market clearing, and global developer optimality are
verified in the proof. The developer's curvature test holds over every
alternative reachable capability at every date, not only on the candidate.

The finite-frontier constructions use a fixed positive finite frontier,
positive AI weights and chi, 0 < eta < 1, rho > n, n >= 0, gamma > 0,
and the stock neighborhoods stated in each proposition. Neither
Assumption 1 (eta < alpha) nor Assumption 2 (eta <= 1/2) is required for
these local capped constructions. They remain available for uncapped
research bounds and simpler global concavity checks, respectively, and the
simulation calibration is unchanged. The separate former Assumption 3
(n + gamma > 0) was redundant given Section 3's n >= 0 and gamma > 0 and has
been removed. The zero-effective-labor-growth case is not covered here.

- Complementarity: the positive labor-share construction requires
  $\overline B>\mathcal B(\sigma)$.
- Unit elasticity: every positive finite Bbar supports the local construction.
- Substitution: $\overline B<\mathcal B(\sigma)$ gives a positive labor share;
  $\overline B>\mathcal B(\sigma)$ gives the AI-dominated construction.
- Threshold equality, other complementary-input regimes, arbitrary common
  initial stocks, and the uncapped limit are not established by these proofs.

The normalized consumption equation is r - rho - gamma, without subtracting
n again. Positive terminal consumption follows from inference/output < 1-alpha
and investment/output < alpha. No stronger general bound on inference/output
is required. Repeated stable eigenvalues do not invalidate the triangular
stable-graph selection argument.

## Analytical growth and interest

Convergent growth rates and a positive limiting C/Y imply limiting per-capita
output growth rbar-rho. This equals gamma in the positive labor-share family.
For sigma > 1 above the threshold, with
$\overline{\zeta}\equiv\zeta(\overline B)$,
$\overline r=\alpha\overline{\zeta}-\delta$ and
$\partial\overline r/\partial\overline B
=(1-\alpha)\overline{\zeta}/\overline B>0$. The limiting interest rate is unbounded
as the finite frontier tends to infinity across economies. This is not an
explosion in time for a fixed frontier and does not prove uncapped existence.
The initial-state neighborhoods need not be uniform across frontiers.

## Reproducible checks

Run with the project's NumPy/SciPy dependencies:

```text
python -m unittest discover -s tests -p test_rewrite_finite_frontier.py -v
```

The original five tests cover:

1. Static and dynamic terminal identities, frontier-inequality orientation,
   analytic Jacobians versus central differences at steps 1e-4 and 1e-5,
   three stable/two unstable roots, and nonsingular state projection for
   sigma = 0.25, 0.5, 0.9, 0.99, 0.9999, 1, 1.0001, 1.01, 1.5, 2, 5.
2. The unit-elastic capital formula and convergence of the static allocation
   at fixed capital and frontier, for sigma = 1 +/- {0.01, 0.001, 0.0001}.
3. Consumption positivity at alpha = 0.2, 0.33, 0.8, 0.95, including high
   substitution elasticities. These are algebraic stress tests, not calibration.
4. Regression checks against the existing AI-dominated equations and Jacobians
   at sigma = 1.1, 1.5, 2, 5, each with
   $\overline B=2\mathcal B(\sigma)$.
5. The frontier derivative, threshold boundary value, and Euler/TVC accounting.

On 2026-09-03 all five tests passed. Across the positive labor-share checks,
the maximum terminal residual was 1.73e-15, the maximum Jacobian error at
step 1e-5 was 6.53e-11, and the smallest singular value of the stable-state
projection exceeded 0.2615. Diagnostic tolerances cover finite-difference
truncation and floating-point roundoff; they are not equilibrium-admission
rules. These checks support the algebra but do not substitute for the proof.

No transition simulation was run, and no production simulation code or
existing numerical output was changed. Simulations remain useful for the
duration and shape of transitions, not for deriving the analytical limits.

## Proposition and verification audit, 2026-09-10

The refinements preserve the equilibrium equations and all long-run formulas.

1. All three propositions now quantify their initial-state neighborhoods and
   identify the constants by equation labels. Local uniqueness refers only to
   trajectories remaining near and converging to the specified normalized
   fixed point. There is no assertion of global equilibrium uniqueness.
2. Lemma 1 supplies the smooth unique static choice needed by the implicit
   equations and the normalized vector fields. Lemma 2 remains a global
   verification theorem, not an existence theorem for arbitrary exogenous
   paths. Both statements and proofs remain in Appendix A.
3. After maximizing over research, the research-depth Hamiltonian contains a
   positive multiple of B(R)^mu, mu = eta/(1-eta). Its second derivative is
   mu B^(mu-2) psi(B) [(mu-1)psi(B)-B/Bbar]. It is concave on the whole
   reachable interval if B0/Bbar >= max(0,(2 eta-1)/eta). This bound is below
   one for every fixed eta < 1. Combined with the uniform operating-profit
   curvature bound, it verifies global optimality after shrinking the
   initial-stock neighborhood. No extra curvature assumption is imposed on
   a presumed candidate. The neighborhoods need not be uniform as eta -> 1.
4. The stable-subspace projection is proved injective by the triangular
   homogeneous system, including repeated eigenvalues. The AI-dominated
   vector field's C1 extension is made explicit; Feldman's stable-manifold
   statement covers that regularity. Dyatlov's existing reference remains
   for the smooth positive-share construction.
5. Ratio convergence alone does not imply growth-rate convergence. The proof
   now uses convergence of the normalized vector field to zero. Both TVCs
   have limiting logarithmic growth n-rho < 0. Household optimality is
   verified by an explicit concavity/budget inequality. Discounted operating
   profit is uniformly bounded over all alternative developer policies,
   rather than assumed finite along only the candidate.
6. Necessary domain information was restored in the equilibrium definition:
   exogenous paths, initial stocks, continuous CES limit at sigma=1, and agent
   optimality. Household capital is nonnegative and research expenditure is
   locally finite. The erroneous equation equating the flow Pi to a lifetime
   maximized present value was corrected by removing that left-hand side;
   Pi retains its original net-distribution meaning everywhere.

Three additional tests verify the relaxed eta range, including eta = 0.5,
0.7, 0.9 and a repeated-stable-root configuration; the exact research-depth
curvature up to eta = 0.99; and global upper tangents at near-frontier test
states for sigma = 0.5, 1, 1.5, 4. The expanded suite runs eight tests, all
passing on 2026-09-10. It includes 35 positive-share and 15 AI-dominated
linearization cases in the relaxed-eta test. These are algebraic regression
checks, not new transition simulations or a substitute for the proof.

The production simulation parameter class still enforces its narrower
benchmark/seed assumptions. Algebra-only test fixtures do not modify it or
claim that the production algorithm is validated outside its previous range.
Initial states far from the normalized limits, threshold equality, and the
uncapped economy remain outside these existence results.
