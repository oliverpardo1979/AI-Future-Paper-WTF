# Finite-frontier equilibrium simulations: execution record

Originally completed on 2026-09-03, revalidated under the revised initial
conditions and transition calibration on 2026-09-07, and extended with the
slow-transition, near-terminal, and Ramsey-start comparisons on
2026-09-08--09. All sixteen displayed trajectories passed the final numerical
equilibrium admission gate.
The public reproduction workflow and installation
instructions are in `REPLICATION.md`; this file records the execution
underlying the paper's reported numerical results.

## Publication status

Complete. The main, Ramsey-start, slow-transition, and near-terminal
4,804-row CSV files, their provenance manifests, ten published figures, and
the separate financing-sensitivity audit
were regenerated. All 36
relevant regression tests passed. The PDF was compiled and visually inspected
after the numerical outputs were incorporated.

## Scope and initial conditions

The design is recorded in `audit/rewrite_simulation_design.md`. The parameters
are alpha=0.33, delta=0.05, rho=0.04, n=0.003, gamma=0.01, omega_X=0.20,
omega_L=0.80, eta=0.20, chi=1.4378. There is no human research input.
Only sigma varies: 0.90, 1.00, 1.10, 1.50. The common frontier is
170.12401740519473, 1.10 times the threshold for sigma=1.50.

Every main scenario fixes A0=N0=1, K0=4 and
B0=0.10 Bbar=17.012401740519476. These stocks are closer to the capped
sigma=1 terminal regime but are not a BGP of the capped model. Each capped BVP
selects its own C0 and q0. Chi is calibrated so that the sigma=1.50 labor share
completes half of its decline after 50.014 model years.

The Section 3 no-AI remark is a separate boundary reduction to
Ramsey--Cass--Koopmans. It is not a fifth simulation or an intermediate
continuation step through omega_X=0.

The Ramsey-start comparison uses the exact no-AI steady-state capital ratio
K0/(A0 N0)=5.94157252710329 and B0/Bbar=0.01. At date zero, omega_X changes
from zero to 0.20. Only the predetermined stocks are imported: each
positive-AI BVP selects C0 and q0 anew.

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
  differentiation. The growth of X/(AL) is likewise recovered from the exact
  gradient of the dated static block. The AI-service price and the four
  noncapital output shares are exact transformations of the same dated static
  allocation. All figures passed inspection as
  standalone PNGs and in the compiled paper.

The saved vector spline must retain `PPoly.axis=1`. An independent residual
check exposed an incorrect reload orientation during development; the loader
now uses `PPoly.construct_fast` with the saved axis. The final audits below
were rerun after this correction.

## Completed numerical evidence

| sigma | Terminal regime | Solved horizon | Final mesh | Independent ODE residual | Full-window horizon change |
|---|---|---:|---:|---:|---:|
| 0.90 | Positive labor share | 4946.189 | 874 | 9.168e-10 | 3.255e-8 |
| 1.00 | Unit elastic / positive labor share | 4821.043 | 872 | 1.044e-9 | 3.725e-8 |
| 1.10 | Positive labor share | 4736.972 | 909 | 9.111e-10 | 3.364e-8 |
| 1.50 | AI dominated | 3008.482 | 1092 | 8.182e-10 | 1.560e-8 |

Independent residuals use five-point differences of spline values, not its
derivative method or the solver's right-hand side, at 1,001 dates and steps
0.003 and 0.001. First-order residuals are below 2.3e-13. The final horizon
comparison covers every plotted year, 0--500; initial jumps change by less
than 1.8e-10 in logs. Both TVCs have negative asymptotic log growth n-rho=-0.037.

The recovered slow-transition comparison uses the earlier stocks
K0=2.027733653970002 and B0=0.44367093160980464 with chi=0.01. Its final
horizons and diagnostics are:

| sigma | Terminal regime | Solved horizon | Final mesh | Independent ODE residual | Full-window horizon change |
|---|---|---:|---:|---:|---:|
| 0.90 | Positive labor share | 6857.067 | 809 | 8.525e-10 | 2.433e-8 |
| 1.00 | Unit elastic / positive labor share | 6731.921 | 607 | 8.876e-10 | 5.727e-9 |
| 1.10 | Positive labor share | 6647.850 | 831 | 9.360e-10 | 1.671e-8 |
| 1.50 | AI dominated | 4919.361 | 1255 | 1.055e-9 | 2.725e-8 |

The horizon comparison covers the full 0--4,000 plotted window. The dense
Hamiltonian-support grid for sigma=1.50 has a minimum normalized gap of
-2.57e-14, within the 1e-10 floating-point diagnostic tolerance. Both TVCs
again have asymptotic log growth -0.037.

The near-terminal diagnostic sets B0/Bbar=0.9999. It initializes K0/(A0 N0)
at each labor-bottleneck regime's analytical terminal ratio. Because the
AI-dominated regime has no finite terminal value for that ratio, its initial
capital instead satisfies (Bbar-B0)K0=dbar. The final admission results are:

| sigma | Initial K0 | Solved horizon | Final mesh | Independent ODE residual | Full-window horizon change |
|---|---:|---:|---:|---:|---:|
| 0.90 | 6.557094 | 4946.189 | 603 | 7.603e-10 | 9.524e-9 |
| 1.00 | 9.098967 | 4821.043 | 604 | 9.734e-10 | 1.327e-8 |
| 1.10 | 12.265203 | 4736.972 | 605 | 8.458e-10 | 1.700e-8 |
| 1.50 | 4101704.227532 | 3008.482 | 628 | 1.003e-9 | 1.433e-8 |

These paths start close to, but not at, the terminal regime because B0 remains
strictly below the frontier and research is positive. All four pass the
global-concavity sufficiency test and both transversality conditions.

The Ramsey-start comparison has the following final admission results:

| sigma | Initial K0 | Solved horizon | Final mesh | Independent ODE residual | Full-window horizon change |
|---|---:|---:|---:|---:|---:|
| 0.90 | 5.941573 | 4946.189 | 1394 | 1.066e-9 | 3.355e-8 |
| 1.00 | 5.941573 | 4821.043 | 1402 | 1.013e-9 | 3.747e-8 |
| 1.10 | 5.941573 | 4736.972 | 1413 | 1.059e-9 | 3.257e-8 |
| 1.50 | 5.941573 | 3008.482 | 1576 | 9.282e-10 | 1.582e-8 |

The first three paths pass the global-concavity condition. The sigma=1.50
path passes both Hamiltonian-support grids; the dense grid's minimum
normalized gap is -1.921e-14, within the 1e-10 floating-point tolerance.
Both transversality conditions pass in all four cases.

In the main, Ramsey-start, and slow comparisons, the global concavity diagnostic passes for
the first three cases. For sigma=1.50 its minimum counterfactual margin is
-1.0250, so it fails. The near-terminal sigma=1.50 path is different: its
reachable counterfactual domain begins sufficiently close to the frontier for
the stronger global-concavity test to pass.
The new appendix proves that a global upper tangent to the maximized
research-depth Hamiltonian is an alternative sufficient condition for the
same developer problem. The diagnostic checks all sampled local minima,
covers the unbounded counterfactual depth domain by an analytical derivative
bound, and repeats at 81x101 and 321x241 date/state resolutions. The minimum
gap divided by output is -1.932e-14, within floating-point error of zero.
The analytical eventual-support margin using B*=0.75 Bbar is 0.097810739674;
the final dated margin differs by less than 4e-13.

These are numerically verified equilibrium approximations with analytical
continuations and sufficient optimality tests, **not interval-arithmetic
existence certificates**. The general local-existence theorem alone is not
being used to establish existence from arbitrary initial stocks. No failed
canonical path is presented as a substitute for an equilibrium.

## Tests and data checks

Completed in the final reproduction run:

- Six existing finite-cap tests, five global finite-cap tests, and five
  rewrite terminal tests passed (16 total).
- The three no-AI Ramsey tests passed, including the exact detrended steady
  state used to initialize the Ramsey-start experiment.
- The first four new design tests passed: agreed parameters/terminal regimes,
  exact unit limit, bilateral terminal continuity, and nonlinear local BVPs
  below and at one. The continuity test uses distances 1e-2, 1e-3, 1e-4,
  1e-6, and 1e-8 from one on both sides.
- All sixteen displayed BVP audits passed as documented above.
- All seven changed/new Python modules passed syntax compilation.
- Separate checks of each 4,804-row CSV confirmed positive
  plotted levels and wL/Y+p_X X/Y=0.67. The maximum error in
  U/(p_X X)+M/(p_X X)+Pi/(p_X X)=1 was 1.111e-16.

The nine tests in `test_rewrite_simulation_design.py` all pass, including
saved vector-spline orientation, the maximized-Hamiltonian identity and
slope, the exact real-wage and AI-services growth calculations, and the
uniform service-capability elasticity bound. The eight-test
near-unit regression suite also passes after the change to its shared static
bracketing function. Together with the sixteen finite-frontier and global-BVP
tests and the three Ramsey tests listed above, the final regression count is 36.

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
$horizons = @{ main = 500; ramsey_start = 500; slow = 4000; near_terminal = 500 }
$designSigmas = @{ main = @(0.9, 1.0, 1.1, 1.5); ramsey_start = @(0.9, 1.0, 1.1, 1.5); slow = @(0.9, 1.0, 1.1, 1.5); near_terminal = @(0.9, 1.0, 1.1, 1.5) }
foreach ($design in @('main', 'ramsey_start', 'slow', 'near_terminal')) {
    foreach ($sigma in $designSigmas[$design]) {
        python scripts/simulate_rewrite_finite_frontier.py --design $design --sigma $sigma
        if ($LASTEXITCODE -ne 0) { throw "BVP failed for $design, sigma=$sigma" }
    }
    python scripts/simulate_rewrite_finite_frontier.py --design $design --verify-long-horizon
    if ($design -ne 'near_terminal') {
        python scripts/audit_rewrite_hamiltonian_support.py --design $design --sigma 1.5 --time-points 81 --capability-points 101
        python scripts/audit_rewrite_hamiltonian_support.py --design $design --sigma 1.5 --time-points 321 --capability-points 241
    }
    python scripts/audit_rewrite_equilibria.py --design $design
    python scripts/simulate_rewrite_finite_frontier.py --design $design --export-horizon $horizons[$design]
    python scripts/plot_rewrite_equilibria.py --design $design
}
python scripts/audit_initial_financing_sensitivity.py
python -m unittest discover -s tests -p test_rck_no_ai_bvp.py -v
python -m unittest discover -s tests -p test_finite_cap_bvp.py -v
python -m unittest discover -s tests -p test_global_finite_cap_bvp.py -v
python -m unittest discover -s tests -p test_rewrite_finite_frontier.py -v
python -m unittest discover -s tests -p test_rewrite_simulation_design.py -v
python -m unittest discover -s tests -p test_near_unit_ai_bvp.py -v
```

Stop on an error; do not bypass the exporter or chart admission guards.
Checkpoints in `tmp/rewrite_bvp`, `tmp/rewrite_bvp_ramsey_start`,
`tmp/rewrite_bvp_slow`, and `tmp/rewrite_bvp_near_terminal` are local,
reproducible calculation caches.
The final JSON audits record their SHA-256 hashes. Plot-ready CSV provenance
is generated by the final export command; the renderer requires that manifest.

## Results to explain in the paper

The first three cases tend to 1% annual per-person growth and 5% net interest,
but different labor shares: about 54.2%, 53.6%, and 50.2%. The last case tends
to 3.135% growth, 7.135% interest, and a vanishing labor share; real wages grow
asymptotically at 2.423%. Its AI revenue share tends to 67% of output and its
net distribution to 22.11% of output.

For sigma=1.50, the labor share completes 10%, 50%, and 90% of its decline at
8.267, 50.014, and 145.199 years. At year 50, per-person growth is 5.616% and
labor's share is 25.5%; at year 100 the corresponding values are 6.290% and
10.9%. At year 500, growth is 3.239% and the labor share is 0.19%, close to
their analytical limits. The speed is calibration dependent; model years are
not calendar forecasts.

The separate distant-stock sensitivity uses K0=2.027733653970002,
B0/Bbar=0.2608%, and chi=1.4223. It independently passes the same equilibrium
admission logic and preserves a 50.001-year midpoint. At date zero, inference
uses 34.52% of AI revenue, research uses 105.98%, and profit is -40.50%.
`numerical_rewrite/initial_financing_sensitivity.json` records its diagnostics.

In the slow sigma=1.50 equilibrium, the labor share completes 10%, 50%, and
90% of its decline after 656.914, 1294.886, and 1605.167 model years. At year
500, per-person growth is 1.062% and the labor share is 60.53%; at year 1,500,
the corresponding values are 2.797% and 14.49%.

In the near-terminal diagnostic, the three labor-bottleneck paths begin within
0.001 percentage points of their growth and interest limits. In the
AI-dominated path, date-zero output-per-person growth, wage growth, and net
interest are 3.443%, 2.632%, and 7.437%; by year 500 they are 3.143%, 2.429%,
and 7.143%, close to their analytical limits. The comparison isolates the
transitional origin of the higher initial rates in the common-stock
labor-bottleneck paths while retaining the AI-dominated benchmark.

In the Ramsey-start comparison, initial X/(AL) growth ranges from 30.5% to
79.0% while K/(AL) initially contracts between 5.7% and 8.1%. For sigma=1.50,
the labor share starts at 61.48%, reaches the transition midpoint after 49.97
years, and falls to 0.20% by year 500. Output-per-person growth peaks at 6.38%
near year 107; real-wage growth peaks at 4.58% near year 109; and the net
interest rate peaks at 9.98% near year 116.

## Final delivery

The stable output is `output/pdf/main_rewrite.pdf`. The Section 3 no-AI
boundary case remains separate from the positive-AI four-scenario comparison.
The numerical admission evidence supports the displayed trajectories;
it is not presented as a formal existence proof for arbitrary initial stocks.
