# Finite-frontier equilibrium simulations: execution record

Originally completed on 2026-09-03 and revalidated through the public entry
point on 2026-09-04. All four requested trajectories passed the final numerical
equilibrium admission gate. The public reproduction workflow and installation
instructions are in `REPLICATION.md`; this file records the execution
underlying the paper's reported numerical results.

## Publication status

Complete. The final 4,804-row CSV, its provenance manifest, and the three
published figures were regenerated on 2026-09-04. All 32 relevant regression
tests passed. The PDF was compiled and visually inspected after the numerical
outputs were incorporated.

## Scope and initial conditions

The design is recorded in `audit/rewrite_simulation_design.md`. The parameters
are alpha=0.33, delta=0.05, rho=0.04, n=0.003, gamma=0.01, omega_X=0.20,
omega_L=0.80, eta=0.20, chi=0.01. There is no human research input.
Only sigma varies: 0.90, 1.00, 1.10, 1.50. The common frontier is
170.12401740519473, 1.10 times the threshold for sigma=1.50.

Every scenario fixes A0=N0=1, K0=2.027733653970002 and
B0=0.44367093160980464. These are stocks from the historical **uncapped**
unit-elastic BGP, not a BGP of the capped model. Each capped BVP selects its
own C0 and q0. No initial stock was changed to obtain convergence.

The Section 3 no-AI remark is a separate boundary reduction to
Ramsey--Cass--Koopmans. It is not a fifth simulation or an intermediate
continuation step through omega_X=0.

## Existing architecture preserved

- `scripts/analyze_axm_finite_cap_bvp.py`: extend the production terminal
  dispatcher to sigma<=1, preserving the existing finite-frontier systems
  and terminal projection. Evaluate frontier thresholds in logarithms and
  solve the labor terminal static condition directly for log[X/(AL)].
- `scripts/solve_near_unit_ai_bvp.py`: allow a negative-marginal-revenue
  trial to bracket the monopoly root for sigma<1. A negative margin is not
  an accepted optimum and does not change an equilibrium equation.
- `scripts/simulate_rewrite_finite_frontier.py`: run the existing local BVP,
  initial-state continuation, and two horizon extensions; save non-pickled
  spline checkpoints and export all four scenarios only after admission.
- `scripts/audit_rewrite_equilibria.py`: independently reconstruct the
  original dynamics, first-order conditions, full-window horizon sensitivity,
  terminal coordinates, and the final admission decision.
- `scripts/audit_rewrite_hamiltonian_support.py`: check the alternative
  sufficient optimality condition proved in the appendix. The stronger failed
  concavity verdict remains visible in the sigma=1.50 JSON report.
- `scripts/plot_rewrite_equilibria.py`: render the three published figures,
  with checkpoint/data provenance checks. Real-wage growth is
  recovered from the exact static share identity rather than by numerical
  differentiation. Both figures passed inspection as standalone PNGs and in
  the compiled paper.

The saved vector spline must retain `PPoly.axis=1`. An independent residual
check exposed an incorrect reload orientation during development; the loader
now uses `PPoly.construct_fast` with the saved axis. The final audits below
were rerun after this correction.

## Completed numerical evidence

| sigma | Terminal regime | Solved horizon | Final mesh | Independent ODE residual | Full-window horizon change |
|---|---|---:|---:|---:|---:|
| 0.90 | Positive labor share | 6857.067 | 809 | 8.5255e-10 | 2.4326e-8 |
| 1.00 | Unit elastic / positive labor share | 6731.921 | 607 | 8.8756e-10 | 5.7274e-9 |
| 1.10 | Positive labor share | 6647.850 | 831 | 9.3605e-10 | 1.6715e-8 |
| 1.50 | AI dominated | 4919.361 | 1255 | 1.0548e-9 | 2.7249e-8 |

Independent residuals use five-point differences of spline values, not its
derivative method or the solver's right-hand side, at 1,001 dates and steps
0.003 and 0.001. First-order residuals are below 2.3e-13. The final horizon
comparison covers every plotted year, 0--4,000; initial jumps change by less
than 2.4e-11 in logs. Both TVCs have negative asymptotic log growth n-rho=-0.037.

The original global concavity diagnostic passes for the first three cases.
For sigma=1.50 its minimum counterfactual margin is -1.0250, so it fails.
The new appendix proves that a global upper tangent to the maximized
research-depth Hamiltonian is an alternative sufficient condition for the
same developer problem. The diagnostic checks all sampled local minima,
covers the unbounded counterfactual depth domain by an analytical derivative
bound, and repeats at 81x101 and 321x241 date/state resolutions. The minimum
gap divided by output is -2.571e-14, within floating-point error of zero.
The analytical eventual-support margin using B*=0.75 Bbar is 0.097810739674;
the final dated margin differs by less than 4e-13.

These are numerically verified equilibrium approximations with analytical
continuations and sufficient optimality tests, **not interval-arithmetic
existence certificates**. The general local-existence theorem alone is not
being used to establish existence from arbitrary initial stocks. No failed
canonical path is presented as a substitute for an equilibrium.

## Tests and data checks

Completed before the execution-service failure:

- Six existing finite-cap tests, five global finite-cap tests, and five
  rewrite terminal tests passed (16 total).
- The first four new design tests passed: agreed parameters/terminal regimes,
  exact unit limit, bilateral terminal continuity, and nonlinear local BVPs
  below and at one. The continuity test uses distances 1e-2, 1e-3, 1e-4,
  1e-6, and 1e-8 from one on both sides.
- Four complete final BVP audits passed as documented above.
- All seven changed/new Python modules passed syntax compilation.
- A separate PowerShell check of all 4,804 CSV rows confirmed positive
  plotted levels and wL/Y+p_X X/Y=0.67. The maximum error in
  U/(p_X X)+M/(p_X X)+Pi/(p_X X)=1 was 1.111e-16.

The eight tests in `test_rewrite_simulation_design.py` all pass, including
saved vector-spline orientation, the maximized-Hamiltonian identity and
slope, the exact real-wage growth calculation, and the uniform
service-capability elasticity bound. The eight-test
near-unit regression suite also passes after the change to its shared static
bracketing function. Together with the sixteen finite-frontier and global-BVP
tests listed above, the final regression count is 32.

## Reproduction commands

For a new user, the supported entry point is:

```text
python scripts/reproduce_rewrite_results.py
```

It executes the following underlying commands in fail-fast order. The
expanded list is retained here as an auditable execution record.

From the repository root, using a Python environment with the existing
NumPy, SciPy, and Matplotlib dependencies:

```powershell
foreach ($sigma in @(0.9, 1.0, 1.1, 1.5)) {
    python scripts/simulate_rewrite_finite_frontier.py --sigma $sigma
    if ($LASTEXITCODE -ne 0) { throw "BVP failed for sigma=$sigma" }
}
python scripts/simulate_rewrite_finite_frontier.py --verify-long-horizon
python scripts/audit_rewrite_hamiltonian_support.py --sigma 1.5 --time-points 81 --capability-points 101
python scripts/audit_rewrite_hamiltonian_support.py --sigma 1.5 --time-points 321 --capability-points 241
python scripts/audit_rewrite_equilibria.py
python scripts/simulate_rewrite_finite_frontier.py --export-horizon 4000
python scripts/plot_rewrite_equilibria.py
python -m unittest discover -s tests -p test_finite_cap_bvp.py -v
python -m unittest discover -s tests -p test_global_finite_cap_bvp.py -v
python -m unittest discover -s tests -p test_rewrite_finite_frontier.py -v
python -m unittest discover -s tests -p test_rewrite_simulation_design.py -v
python -m unittest discover -s tests -p test_near_unit_ai_bvp.py -v
```

Stop on an error; do not bypass the exporter or chart admission guards.
Checkpoints in `tmp/rewrite_bvp` are local, reproducible calculation caches.
The final JSON audits record their SHA-256 hashes. Plot-ready CSV provenance
is generated by the final export command; the renderer requires that manifest.

## Results to explain in the paper

The first three cases tend to 1% annual per-person growth and 5% net interest,
but different labor shares: about 54.2%, 53.6%, and 50.2%. The last case tends
to 3.135% growth, 7.135% interest, and a vanishing labor share; real wages grow
asymptotically at 2.423%. Its AI revenue share tends to 67% of output and its
net distribution to 22.11% of output.

The sigma=1.50 transition initially adjusts sharply, then remains near
moderate growth for a long period. At year 500, per-person growth is 1.062%
and labor's share is 60.5%; at year 1,500 the corresponding values are 2.797%
and 14.5%. Growth and interest overshoot their eventual limits before
converging. The speed is calibration dependent; model years are not calendar
forecasts. These statements are based on the exported computed data, not on
an extrapolation of the analytical limiting rates.

## Final delivery

The stable output is `output/pdf/main_rewrite.pdf`. The Section 3 no-AI
boundary case remains separate from the positive-AI four-scenario comparison.
The numerical admission evidence supports the four displayed trajectories;
it is not presented as a formal existence proof for arbitrary initial stocks.
