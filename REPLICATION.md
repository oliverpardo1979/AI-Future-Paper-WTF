# Replicating the equilibrium simulations

This guide reproduces the numerical results in *The Future of Growth and
Human Labor Under Recursive AI Self-Improvement*. It is written for readers
who want to run the published comparison without first learning the internal
structure of every solver module.

## What the computation does

The simulations compare four values of the elasticity of substitution between
effective labor and effective AI production services: 0.90, 1.00, 1.10, and
1.50. All other parameters, the AI-efficiency frontier, and the predetermined
initial stocks are held fixed.

Capital and AI efficiency are predetermined at date zero. Consumption and the
developer's shadow value can jump. The algorithm chooses those two initial
jump variables so that the path beginning at the prescribed stocks approaches
the stable terminal regime derived in the paper. It does this as a
four-dimensional boundary-value problem, rather than by guessing all four
initial values and integrating forward.

The workflow has six conceptual steps:

1. Determine the analytical terminal regime for the requested elasticity and
   common AI-efficiency frontier.
2. Solve a local boundary-value problem near that terminal point. Two terminal
   projection conditions remove the unstable directions.
3. At each trial point, solve the static monopoly condition and recover
   research expenditure from the developer's first-order condition.
4. Move the local solution gradually to the common date-zero stocks by
   continuation. The preceding solution supplies the next numerical guess.
5. Extend the horizon twice and tighten tolerances to check that the initial
   jump variables and the displayed path are stable.
6. Admit a trajectory only if it passes the independent equation, feasibility,
   optimality, transversality, horizon, and provenance checks described below.

The last step matters. Successful convergence of SciPy's boundary-value solver
creates a candidate path; it does not by itself establish that the path is an
equilibrium.

## Quick start from a fresh clone

Python 3.12 is recommended. From the repository root, create an isolated
environment and install the pinned numerical dependencies.

PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-rewrite.txt
.\.venv\Scripts\python.exe scripts\reproduce_rewrite_results.py
```

macOS or Linux:

```bash
python3.12 -m venv .venv
./.venv/bin/python -m pip install -r requirements-rewrite.txt
./.venv/bin/python scripts/reproduce_rewrite_results.py
```

The last command is the public entry point. It runs the regression tests,
solves and refines all four boundary-value problems, performs the two global
Hamiltonian-support checks required for the 1.50 case, applies the final
equilibrium-admission gate, exports the data, and regenerates the figures. It
stops at the first failure and therefore cannot knowingly create a partial
published comparison.

The calculation stores resumable spline checkpoints in `tmp/rewrite_bvp/`.
They are generated files and are not committed. Rerunning the command reuses
valid existing stages. To recompute every boundary-value checkpoint from
scratch, use:

```text
python scripts/reproduce_rewrite_results.py --fresh
```

`--fresh` removes only the twelve generated `base`, `refined`, and `long`
checkpoint files belonging to these four scenarios. The committed numerical
reports and figures are then overwritten only as their corresponding stages
successfully complete.

## What counts as a replicated equilibrium

The final admission script, `scripts/audit_rewrite_equilibria.py`, requires all
of the following:

- positive and feasible allocations along the path;
- small residuals in the four original dynamic equations, reconstructed from
  saved spline values independently of the solver's derivative routine;
- small residuals in the static monopoly and research first-order conditions;
- stability of the initial jump variables and the entire 0--4,000 display
  window after a longer horizon and tighter tolerances;
- convergence toward the regime-specific analytical terminal coordinates;
- both infinite-horizon transversality conditions;
- a sufficient global optimality check for the AI developer.

For elasticities 0.90, 1.00, and 1.10, the developer check uses global
concavity over the counterfactual AI-efficiency domain. That stronger
condition fails in the 1.50 scenario. The code therefore applies the distinct
Hamiltonian upper-support condition proved in the appendix, at two grid
resolutions, together with its analytical terminal bound. This is not a
relaxation of the developer's first-order conditions.

An admitted numerical path is a verified equilibrium approximation supported
by the paper's analytical terminal and optimality results. The calculation is
not an interval-arithmetic existence certificate for arbitrary initial stocks
or arbitrary parameter values.

## Outputs

The full command regenerates:

- `numerical_rewrite/sigma_*_audit.json`: one final admission report per
  elasticity;
- `numerical_rewrite/sigma_1_50_support_*.json`: the two global
  Hamiltonian-support audits;
- `numerical_rewrite/equilibrium_paths.csv`: the 4,804 plotted observations;
- `numerical_rewrite/paths_manifest.json`: links the exported data to the
  audited checkpoint hashes;
- `numerical_rewrite/figure_manifest.json`: links the figures to the exported
  data and records the plotted fields;
- `figures_rewrite/equilibrium_growth_returns.{pdf,png}`;
- `figures_rewrite/equilibrium_ai_distribution.{pdf,png}`;
- `figures_rewrite/equilibrium_technology_revenue.{pdf,png}`.

The renderer checks the manifests before plotting. A changed or stale
checkpoint, audit, or CSV therefore prevents figure generation instead of
silently mixing outputs from different runs.

To compile the paper after reproducing the figures, run a LaTeX engine on
`main_rewrite.tex`. With Tectonic installed:

```text
tectonic --keep-logs --outdir output/pdf main_rewrite.tex
```

The paper PDF is written to `output/pdf/main_rewrite.pdf`.

## Where to inspect or change the computation

- `scripts/simulate_rewrite_finite_frontier.py` defines the four published
  elasticities, the common frontier, the common initial stocks, checkpoint
  handling, and the plot-data export.
- `scripts/define_positive_ai_branch.py` contains the benchmark parameter
  object.
- `scripts/solve_near_unit_ai_bvp.py` solves the static monopoly block with an
  exact unit-elastic limit and numerically stable evaluation near one.
- `scripts/analyze_axm_finite_cap_bvp.py` characterizes the terminal regimes
  and their local stable manifolds.
- `scripts/solve_axm_global_finite_cap_bvp.py` implements continuation, horizon
  refinement, reconstruction of model variables, and the main diagnostics.
- `scripts/audit_rewrite_hamiltonian_support.py` implements the alternative
  sufficient optimality check used for the 1.50 scenario.
- `scripts/plot_rewrite_equilibria.py` defines the displayed variables,
  normalizations, scales, and figure styles.
- `tests/` contains the algebra, unit-limit, near-unit, spline-orientation, and
  global boundary-value regression tests.

When changing a parameter or scenario, change its economic definition at the
source rather than altering an exported CSV. Then run the public entry point
with `--fresh`. A new scenario should not enter the paper merely because its
BVP converges: its terminal regime and optimality test must also be justified,
implemented, and admitted.

## Numerical tolerances and current execution record

The precise continuation stages, mesh sizes, solver tolerances, acceptance
thresholds, final residuals, and horizon comparisons are reported in
`sections_rewrite/appendix.tex` and
`audit/rewrite_equilibrium_simulations.md`. The JSON audit files provide the
machine-readable record for each trajectory. These tolerances diagnose the
approximation error; they do not replace any equation or economic condition.
