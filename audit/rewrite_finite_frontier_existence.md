# Finite-frontier existence and long-run comparative statics

Date: 2026-09-03. Source: Section 4 and Appendix A.6 of `main_rewrite.tex`.

## Scope

The results construct infinite-horizon equilibrium trajectories for an open
set of nearby predetermined normalized stocks. They are local in initial
conditions, not finite-horizon simulations and not merely BGP calculations.
The two jump variables are selected by a stable-manifold graph. Both TVCs,
finite objectives, market clearing, and global developer optimality are
verified in the proof. The developer's curvature test holds over every
alternative reachable capability at every date, not only on the candidate.

The common assumptions are a fixed positive finite frontier, positive AI
weights and chi, rho > n, n + gamma > 0, 0 < eta < alpha < 1, and 2 eta <= 1,
together with the stock neighborhoods stated in each proposition.

- Complementarity: the positive labor-share construction requires Bbar > Bbar_c.
- Unit elasticity: every positive finite Bbar supports the local construction.
- Substitution: Bbar < Bbar_c gives a positive labor share; Bbar > Bbar_c gives
  the AI-dominated construction.
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
For sigma > 1 above the threshold, rbar = alpha*z_A(Bbar;sigma)-delta and
d rbar/d Bbar = (1-alpha)*z_A/Bbar > 0. The limiting interest rate is unbounded
as the finite frontier tends to infinity across economies. This is not an
explosion in time for a fixed frontier and does not prove uncapped existence.
The initial-state neighborhoods need not be uniform across frontiers.

## Reproducible checks

Run with the project's NumPy/SciPy dependencies:

```text
python -m unittest discover -s tests -p test_rewrite_finite_frontier.py -v
```

The five tests cover:

1. Static and dynamic terminal identities, frontier-inequality orientation,
   analytic Jacobians versus central differences at steps 1e-4 and 1e-5,
   three stable/two unstable roots, and nonsingular state projection for
   sigma = 0.25, 0.5, 0.9, 0.99, 0.9999, 1, 1.0001, 1.01, 1.5, 2, 5.
2. The unit-elastic capital formula and convergence of the static allocation
   at fixed capital and frontier, for sigma = 1 +/- {0.01, 0.001, 0.0001}.
3. Consumption positivity at alpha = 0.2, 0.33, 0.8, 0.95, including high
   substitution elasticities. These are algebraic stress tests, not calibration.
4. Regression checks against the existing AI-dominated equations and Jacobians
   at sigma = 1.1, 1.5, 2, 5, each with Bbar = 2*Bbar_c.
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
