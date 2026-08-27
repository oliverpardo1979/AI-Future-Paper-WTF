# Architecture of the strictly positive-AI equilibrium solver

## Purpose

The no-AI Ramsey--Cass--Koopmans economy and the positive-AI economy are two
different boundary-value problems. The numerical architecture must compare
their solutions, not manufacture one from the other by mechanically continuing
through \(\omega_X=0\).

At \(\omega_X=0\), \(B\), \(q\), \(U\), and \(M\) cease to affect final
production. The developer's static and dynamic conditions disappear, so the
equilibrium system falls from four dynamic variables to two. The rank and
dimension change at zero. An implicit-function or homotopy argument that starts
from the no-AI solution is therefore unavailable.

The positive-AI branch instead starts at the paper's target value
\(\omega_X=0.20\), with \(\sigma_{XL}=1\), where an exact interior
balanced-growth equilibrium is available. The old numerical code remains
untouched and can serve as an independent comparison once the corresponding
calibration is aligned.

### Calibration-consistency finding

The numerical balanced-growth values and roots currently printed in the
Appendix cannot be reused with Table 2. They correspond to the earlier
calibration \(n=0.012\) and \(\gamma_A=0\). With the current values
\(n=0.003\) and \(\gamma_A=0.01\), the analytic definitions instead give

\[
 g_Y^*=0.0138667,\qquad g_B^*=0.0034667,\qquad r^*=0.0508667,
\]

and the roots of the recomputed Jacobian are approximately

\[
 -0.098971,\qquad -0.003194,\qquad 0.040391,\qquad 0.149290.
\]

This is an algebraic calibration check, not a simulated result. The paper's
old numerical paragraph should be updated only after the complete positive-AI
solver and its independent audit have been accepted.

## Exact positive-AI seed

For the automated-research benchmark, define

\[
 \beta=(1-\alpha)\omega_X,\qquad
 \lambda=(1-\alpha)\omega_L,\qquad
 \Delta=\lambda(1-\eta)-\beta\eta.
\]

Under the restrictions already stated in the paper, the exact unit-elastic
balanced-growth seed is

\[
 g_Y^*=\frac{\lambda(1-\eta)}{\Delta}(n+\gamma_A),
 \qquad
 g_B^*=\frac{\eta}{1-\eta}g_Y^*,
 \qquad
 r^*=\rho+g_Y^*-n,
\]

\[
 u^*=\beta^2,\qquad
 k^*=\frac{\alpha}{r^*+\delta},\qquad
 i^*=(g_Y^*+\delta)k^*,
\]

\[
 m^*=\frac{\beta^2\eta g_B^*}{\rho-n+\eta g_Y^*},
 \qquad
 c^*=1-u^*-i^*-m^*.
\]

The seed is admissible only if all existence restrictions hold and \(c^*>0\).
Its levels are constructed from the production and capability laws, rather
than assigned independently. For the current calibration, the construction
gives \(B_0^*\simeq0.444\). This differs from the paper's normalization
\(B_0=1\), which is why the seed cannot itself be reported as the target
initial equilibrium.

## Stationary four-dimensional system

Keep the paper's state and jump variables and write

\[
 \xi=(\xi_K,\xi_B,\xi_C,\xi_q)'
 =\left(\log\frac K{K^*},\log\frac B{B^*},
 \log\frac C{C^*},\log\frac q{q^*}\right)'.
\]

At \(\sigma_{XL}=1\), the monopoly condition implies \(U/Y=\beta^2\)
at every date. The dated static equations can therefore be eliminated exactly:

\[
 \widehat Y=\frac{\alpha}{1-\beta}\xi_K
 +\frac{\beta}{1-\beta}\xi_B,
 \qquad
 \widehat M=\frac{\xi_q+\eta\xi_B}{1-\eta},
\]

\[
 \log\frac{g_B}{g_B^*}
 =\frac{(2\eta-1)\xi_B+\eta\xi_q}{1-\eta}.
\]

Substituting these identities in the resource constraint, household Euler
equation, capability law, and developer costate equation yields an exact
autonomous system \(\dot\xi=f(\xi)\). No simulation equation is added and no
equilibrium condition is dropped.

The Jacobian \(J^*=D f(0)\) must be recomputed with the parameters currently in
Table 2. The positive-AI branch is locally usable only if it has exactly two
stable and two unstable roots and the projection of the stable eigenspace onto
the predetermined variables \((\xi_K,\xi_B)\) is nonsingular.

## Initial stocks and finite-horizon boundary conditions

The level-normalized off-BGP validation fixes \(B_0=1\) but leaves \(K_0\)
scenario-specific. A transparent initialization rule is to choose \(K_0\) so
that the initial \(K/Y\) ratio
equals \(k^*\), after solving the date-zero production equation at \(B_0=1\).
This is a calibration rule for the initial stock. It is not an equilibrium
condition, a theorem, or a claim that \((K_0,B_0)\) lies on the balanced-growth
path.

For a finite horizon \(T\), the boundary-value problem imposes

\[
 \xi_K(0)=\log(K_0/K_0^*),\qquad
 \xi_B(0)=\log(B_0/B_0^*).
\]

Let \(V_S\) span the two-dimensional stable eigenspace of \(J^*\), and let
\(P_\perp\) be two independent rows satisfying \(P_\perp V_S=0\). The terminal
conditions are

\[
 P_\perp\xi(T)=0.
\]

These conditions do not force the terminal point to equal the steady point.
They remove the two unstable components. Since the true stable manifold is
nonlinear, terminal-horizon convergence remains an acceptance requirement.

## Continuation order

1. Start from the exact zero-deviation solution at
   \((\omega_X,\sigma_{XL})=(0.20,1)\).
2. At fixed positive \(\omega_X\), move the two initial log-stock deviations
   from zero to their target values. Warm-start each collocation problem from
   the preceding accepted solution.
3. Increase the terminal horizon and mesh until initial jump variables and all
   reported finite-window paths are stable.
4. Only after the unit-elastic target path is accepted, vary
   \(\sigma_{XL}\) locally above or below one. This continuation is valid on a
   fixed finite window; it does not transfer the unit-elastic asymptotic result
   to \(\sigma_{XL}\ne1\).
5. If \(\omega_X\) is later varied, continue only between two strictly
   positive values, preferably in logit coordinates. Recompute the moving
   balanced-growth seed, detrending, Jacobian, and terminal projector at every
   accepted weight. Never include zero in that schedule.

The no-AI and positive-AI results will therefore meet only in tables and
figures as economic counterfactuals. They do not belong to one numerical
homotopy.

## Acceptance gates and failure interpretation

A positive-AI transition is reportable only if it passes all of the following:

- the dated static equations, four differential equations, initial conditions,
  and terminal projection have small independently reconstructed residuals;
- \(K,B,C,q,U,M,X,Y\) remain strictly positive and all feasibility and
  monopoly second-order restrictions hold;
- the household and developer transversality expressions decline toward zero;
- the solution is stable to tighter tolerances, denser meshes, more stock
  continuation stages, and longer terminal horizons;
- forward and backward reconstructions agree with the collocation path; and
- an independent implementation or the preserved older solver reproduces the
  accepted path within stated tolerances.

A failed continuation stage is not evidence of nonexistence. It may indicate a
poor initial guess, insufficient mesh resolution, departure from the local
stable-manifold neighborhood, a genuine loss of saddle-path structure, or an
economically inadmissible path. These possibilities must be diagnosed
separately.

## Implemented off-BGP validation

`scripts/define_positive_ai_branch.py` constructs and audits the seed,
normalized system, Jacobian, stable terminal projector, and legal continuation
schedules. `scripts/solve_positive_ai_bvp.py` then implements the agreed
positive-AI collocation problem. It starts from the exact zero-deviation path,
moves \((K_0,B_0)\) to the target in log-stock space at fixed
`omega_x = 0.20`, and repeats the accepted solve at horizons 100, 150, 200,
and 250. The no-AI solution is never used as a homotopy point.

That validation's target initialization sets \(B_0=1\) and chooses \(K_0\) by the explicit
date-zero rule described above. This target is materially off the reference
BGP: \(B_0^*=0.4436709\), so
\(\log(B_0/B_0^*)=0.8126721\). The 12-stage stock continuation reaches this
target and the subsequent horizon continuation is accepted. At the refined
solve, the maximum resource residual is \(3.0\times10^{-9}\), the maximum
boundary residual is \(2.8\times10^{-17}\), and all reconstructed equilibrium
residuals are below \(3.0\times10^{-9}\). The two finite-date transversality
expressions decline over the solved interval.

The independent dynamic check reconstructs the four right-hand sides without
calling the solver function and reintegrates the accepted path backward in
ten-year segments with a different integrator. Segmentation is necessary
because a single centuries-long backward integration magnifies roundoff along
the fast stable mode. Its maximum disagreement with the collocation path is
\(2.0\times10^{-10}\) in the refined solve. Tightening the collocation
tolerance from \(10^{-8}\) to \(10^{-9}\), increasing the initial mesh from 121
to 181 nodes, and increasing stock-continuation stages from 12 to 16 changes
the two initial jump variables by at most \(5.1\times10^{-13}\) and the first
50 years of the log path by at most \(7.7\times10^{-10}\).

These checks show that the numerical branch reaches the paper's off-BGP target
and is stable under the stated refinements. They do not show that \(B_0=1\)
belongs to the local neighborhood in the stable-manifold theorem, prove global
existence or uniqueness, or verify the transversality limits at infinity. The
calculation solves and audits a finite-horizon approximation to the equilibrium
trajectory.
