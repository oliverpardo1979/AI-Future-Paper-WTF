# Replicating the equilibrium simulations

This guide accompanies the paper [*The Future of Growth and Human Labor Under
Recursive AI Self-Improvement*](main_rewrite.tex) and reproduces its numerical
results. It is written for readers who want to run the published comparison
without first learning the internal structure of every solver module.

## What the computation does

The principal exercise now activates RSI in an economy with existing AI.
Before date zero, `B=B0` is fixed and research is unavailable (`chi=0`,
`M=0`). At date zero RSI unexpectedly becomes available. Production weights
remain unchanged, so the event does not mechanically change output, AI
production services, inference, wages, interest, or the service price.
The experiment is not the first appearance of AI and not an anticipated
event under pre-event perfect foresight.

For each `sigma=0.90,1.00,1.10,1.50`, initial capital is calculated from
the fixed-B BGP, with `K0/Y0=3.30` and `r0=0.05`. The four stocks are
`3.433644797858547`, `4.649320432676148`, `5.036956080779938`, and
`5.5046668887702594`, respectively. The common inputs are `omega_X=0.10`,
`eta=0.20`, `Bbar=1360.9921392415592`, and `B0=13.609921392415593`.
The refitted `chi=36.83070200718361` matches the unit-elastic price target,
then stays fixed across the other elasticities. Pre-event consumption is
reported for comparison but is NOT a boundary condition after activation.
The post-event BVP independently selects consumption and the shadow value.

```text
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation
python -m unittest discover -s tests -p test_rewrite_rsi_activation.py -v
```

For a staged run, append `--calibrate-only`, then run `--sigma 0.9`,
`--sigma 1`, `--sigma 1.1`, and `--sigma 1.5` separately, and finally
`--finish`. Finishing repeats the original equilibrium checks, adds the
event-continuity audit, verifies the final price match, and only then
exports all four paths. See `numerical_rewrite/rsi_activation/README.md`.

The default `python scripts/reproduce_rewrite_results.py` reproduces this
exercise. Add `--include-legacy` to regenerate the earlier comparisons as
well. All old data, figures, and texts remain intact. In `main_rewrite.tex`,
`\showlegacysimulationsfalse` displays RSI activation; changing it to
`\showlegacysimulationstrue` restores the earlier quantitative section and
numerical appendix. This is an editorial switch, not a simulation setting.

## Preserved earlier comparisons

The earlier principal configuration is still available with
`python scripts/calibrate_rewrite_ai_price.py --variant low_ai`, using
common no-AI Ramsey capital and `chi=36.03184470863892`. Its files were
not overwritten. The remaining instructions below describe these preserved
designs where their names are specified.

All common-stock comparisons use four values of the elasticity of substitution between
effective labor and effective AI production services: 0.90, 1.00, 1.10, and
1.50. All other parameters, the AI-efficiency frontier, and the predetermined
initial stocks are held fixed.

The earlier illustrative comparison sets `K0=4`, `B0/Bbar=0.10`, and `chi=1.4378`. These
intermediate predetermined stocks keep the four elasticities comparable while
preventing the financing needs of an extremely distant initial economy from
dominating the main figures. The last value makes the 1.50 labor share complete
half of its decline after about 50 model years. The separate financing
sensitivity deliberately uses the earlier distant stocks and `chi=1.4223` to
preserve the same midpoint. It isolates the effect of initial technological
distance on date-zero financing and is not a fifth line in those figures.
The legacy design name `main` in the solver and the full-replication workflow
still identifies this earlier timing exercise, not the newly designated
principal calibration. Code names and saved outputs are preserved.

The slower-transition comparison recovers the paper's earlier design and asks
how long the same terminal regimes can remain hidden when research is slower
and the initial economy is farther from its frontier:
`K0=2.027733653970002`, `B0=0.44367093160980464`, and `chi=0.01`. It repeats
the same four elasticities and the same three-figure layout over 4,000 model
years. It is a separately solved and admitted comparison, not a rescaling of
the main paths. Because both the initial stocks and `chi` change, it should
not be read as a one-parameter estimate of the effect of research productivity.

The near-terminal diagnostic uses all four elasticities and sets
`B0/Bbar=0.9999`. This value is close enough to display the analytical limits
while remaining inside the positive-research problem. For the three
labor-bottleneck regimes, it sets
`K0/(A0*N0)` equal to the analytical terminal capital ratio. The AI-dominated
regime has no finite terminal value of that ratio, so it instead sets
`(Bbar-B0)*K0` equal to the analytical terminal gap scale. Consumption and the
shadow value are still solved by the BVP. This comparison isolates terminal
behavior; it does not hold every initial stock fixed.

The Ramsey-start experiment fixes `K0/(A0*N0)=5.94157252710329`, the exact
no-AI steady-state capital ratio under the paper's macro parameters, and sets
`B0/Bbar=0.01`. The low latent AI-efficiency value is illustrative and leaves
room for a visible transition; it is not identified by the no-AI economy,
where AI efficiency is irrelevant. Before date zero, `omega_X=0`; from date
zero onward all four paths use `omega_X=0.20`. Only the predetermined stocks
carry across the technology switch. Consumption and the developer's shadow value are solved
anew by the positive-AI BVP.

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
4. Move the local solution gradually to the prescribed date-zero stocks by
   continuation. The preceding solution supplies the next numerical guess.
5. Extend the horizon twice and tighten tolerances to check that the initial
   jump variables and the displayed path are stable.
6. Admit a trajectory only if it passes the independent equation, feasibility,
   optimality, transversality, horizon, and provenance checks described below.

The last step matters. Successful convergence of SciPy's boundary-value solver
creates a candidate path; it does not by itself establish that the path is an
equilibrium.

## Quick start from a fresh clone

### Initial capital-output audit

The [capital-output comparison](empirical/capital_output/README.md) documents
the initial ratio in every quantitative exercise and checks it against
PWT 11.0 and the calibration literature. Run
`python scripts/audit_rewrite_capital_output.py` to reproduce the comparison
from the included data extract and saved equilibrium paths, without solving
any new trajectories. The no-AI steady-state ratio is 3.30; the ratio after
the introduction of AI generally differs because output can change while
capital is inherited. None of the existing simulations has been refitted to
this additional moment.

### Separate joint-calibration audit

The [joint-calibration workstream](empirical/joint_calibration/README.md)
examines sector size, prices and research expenditure using documented source
snapshots. It fits sector size and the price decline conditionally at unit
elasticity, screens the other elasticities for compatibility, and keeps
research expenditure as an external check. Its provisional US reference is
not a measured worldwide sector total. This workstream does not replace any
paper simulation or figure.

### Additional price-calibrated comparison

The price-calibrated exercise is separate from all preceding designs. It keeps
the no-AI Ramsey capital stock `K0=5.94157252710329`, sets `B0/Bbar=0.10`, and
retains `eta=0.20`, `omega_X=0.20`, and the common `Bbar=170.12401740519473`.
It chooses `chi` at `sigma=1` to match `p_X(2.25)/p_X(0)=0.20`, then uses the
same `chi` at all four elasticities. The target is a rounded approximation to
the [OECD price-index decline from January 2024 to April 2026](https://www.oecd.org/en/publications/artificial-intelligence-markets_d531d73f-en/full-report.html).
It is a cumulative decline over 27 months, not an annual rate. The exercise
holds the general final-good price constant when mapping this dollar-price
index into the model's relative price. It is not an exactly deflated estimate
of RSI productivity or a calibration of the current industry's revenue share.

Run only this additional exercise with:

```text
python scripts/calibrate_rewrite_ai_price.py
```

To refit `chi`, run the same script with `--calibrate-only`. To resume one
elasticity, use `--sigma 1.5` (or another of the four values); `--finish` runs
the second horizon extensions, final audits, and exports. Checkpoints live in
`tmp/rewrite_bvp_price_calibrated/`; published data and the source/target record
live in `numerical_rewrite/price_calibrated/`. Calibration trials are explicitly
marked as candidates and are not plotted. The final fit is checked again on
the longest-horizon unit-elastic path before export.

The established admission checks are supplemented with dense tests over the
first ten years: independent five-point differences at steps 0.0003 and
0.0001 years, counterfactual concavity, and, when needed, Hamiltonian support
at two resolutions. These checks use the existing tolerances. They prevent
a uniform multi-millennial audit grid from overlooking a fast initial
transition. Additional export dates resolve this same early window.

### Principal calibration: lower AI weight and higher efficiency bound

The principal lower-weight comparison uses the same price target, macro
parameters, and no-AI Ramsey capital stock. It changes `omega_X` to `0.10`,
`B0/Bbar` to `0.01`, and sets `Bbar=1360.9921392415592`: ten percent above
the new `sigma=1.5` threshold. This bound is eight times the preceding bound;
it keeps `sigma=1.5` in the AI-dominated regime. The same target does not imply
the same `chi`: this design refits it at unit elasticity.

```text
python scripts/calibrate_rewrite_ai_price.py --variant low_ai
```

Use `--variant low_ai --calibrate-only` to refit, `--variant low_ai --sigma 1.5`
to resume one elasticity, or `--variant low_ai --finish` to finish the admission
and exports. Its files are isolated in
`numerical_rewrite/price_calibrated_low_ai_high_cap/` and
`tmp/rewrite_bvp_price_calibrated_low_ai_high_cap/`. The variant name is a code
identifier, not a claim that the resulting revenue share matches today's AI
industry. The baseline price-calibrated comparison is unchanged.

### Full replication

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
solves and refines the four main, four Ramsey-start, four slow-transition, and
four near-terminal boundary-value problems, performs the global
Hamiltonian-support checks required for the main, Ramsey-start, and slow 1.50
cases, applies the final equilibrium-admission gates, reproduces the
distant-initial-stock financing sensitivity, exports the data, and regenerates
the figures. It
stops at the first failure and therefore cannot knowingly create a partial
published comparison.

The calculation stores resumable spline checkpoints in `tmp/rewrite_bvp/`,
`tmp/rewrite_bvp_ramsey_start/`, `tmp/rewrite_bvp_slow/`, and
`tmp/rewrite_bvp_near_terminal/`.
They are generated files and are not committed. Rerunning the command reuses
valid existing stages. To recompute every boundary-value checkpoint from
scratch, use:

```text
python scripts/reproduce_rewrite_results.py --fresh
```

`--fresh` removes only the generated `base`, `refined`, and `long`
checkpoint files belonging to the four main scenarios, the four slow
scenarios, the four near-terminal scenarios, the four Ramsey-start scenarios,
and the financing sensitivity.
The committed numerical
reports and figures are then overwritten only as their corresponding stages
successfully complete.

## What counts as a replicated equilibrium

The final admission script, `scripts/audit_rewrite_equilibria.py`, requires all
of the following:

- positive and feasible allocations along the path;
- small residuals in the four original dynamic equations, reconstructed from
  saved spline values independently of the solver's derivative routine;
- small residuals in the static monopoly and research first-order conditions;
- stability of the initial jump variables and the entire display window
  (0--500 in the main, Ramsey-start, and near-terminal designs and 0--4,000 in the slow design) after a longer
  horizon and tighter tolerances;
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
- `numerical_rewrite/initial_financing_sensitivity.json`: the separately
  admitted distant-initial-stock financing exercise;
- `numerical_rewrite/equilibrium_paths.csv`: the 4,804 plotted observations;
- `numerical_rewrite/paths_manifest.json`: links the exported data to the
  audited checkpoint hashes;
- `numerical_rewrite/figure_manifest.json`: links the figures to the exported
  data and records the plotted fields;
- `figures_rewrite/equilibrium_accumulation_growth.{pdf,png}`;
- `figures_rewrite/equilibrium_growth_returns.{pdf,png}`;
- `figures_rewrite/equilibrium_ai_distribution.{pdf,png}`;
- `numerical_rewrite/ramsey_start/`: the four Ramsey-start audits, two
  Hamiltonian-support checks, plotted CSV, and provenance manifests;
- `figures_rewrite/equilibrium_ramsey_start_accumulation_growth.{pdf,png}`;
- `figures_rewrite/equilibrium_ramsey_start_growth_returns.{pdf,png}`;
- `figures_rewrite/equilibrium_ramsey_start_ai_distribution.{pdf,png}`;
- `numerical_rewrite/slow_transition/`: the four slow-transition audits,
  two Hamiltonian-support checks, plotted CSV, and provenance manifests;
- `figures_rewrite/equilibrium_slow_accumulation_growth.{pdf,png}`;
- `figures_rewrite/equilibrium_slow_growth_returns.{pdf,png}`;
- `figures_rewrite/equilibrium_slow_ai_distribution.{pdf,png}`;
- `numerical_rewrite/near_terminal/`: the four near-terminal audits,
  plotted CSV, and provenance manifests;
- `figures_rewrite/equilibrium_near_terminal_growth_returns.{pdf,png}`.

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

- `scripts/simulate_rewrite_finite_frontier.py` defines the published
  elasticities, the main, Ramsey-start, slow, and near-terminal designs,
  checkpoint handling, and the plot-data export.
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
- `scripts/audit_initial_financing_sensitivity.py` reproduces the initial
  loss that arises when the economy starts much farther from the terminal
  regime while preserving the same 50-year transition midpoint.
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
