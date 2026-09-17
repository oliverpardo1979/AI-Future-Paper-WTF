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
The two displayed exercises use `chi=7.5` and `chi=1.5`, author-selected
illustrative values rather than estimates or fitted targets. Each value stays
fixed across the four elasticities. Pre-event consumption is
reported for comparison but is NOT a boundary condition after activation.
The post-event BVP independently selects consumption and the shadow value.

Section 6.1 gives the common design, Section 6.2 higher research productivity,
and Section 6.3 lower research productivity. Limitations are discussed in the
conclusion. The former Section 6.4 is preserved in
`sections_rewrite/11_rsi_limitations.tex` but its input in `main_rewrite.tex`
is commented out; uncomment that input to restore it. Run
`python scripts/reproduce_rewrite_results.py` for both displayed comparisons
in this order. Add `--include-legacy` to regenerate the preserved comparisons
as well. These commands re-solve and audit the model; they do not rescale a
saved trajectory in time. Both illustrative comparisons were newly solved
for all four elasticities; the former calibrated paths are not relabeled.

In `main_rewrite.tex`, both `\showlegacysimulationsfalse` and
`\showfullpricebenchmarkfalse` are the defaults. A third switch,
`\showcalibratedrsiscenariosfalse`, selects the new illustrative comparisons;
set it to `\showcalibratedrsiscenariostrue` to restore the previous
chi=7.616304576019883 and chi=1.4378 text, table values and appendix.
Change `\showfullpricebenchmarkfalse` to
`\showfullpricebenchmarktrue` to add back the full 80%-price-decline
experiment, including its parameter table, figures and accuracy table.
Change the former to `\showlegacysimulationstrue` to restore the older
quantitative section and numerical appendix instead. These are editorial
switches, not simulation settings; all underlying files remain available.

## Current comparison: chi=7.5 and chi=1.5

```text
python -m pip install -r requirements-rewrite.txt
python scripts/simulate_rewrite_illustrative_rsi.py
python -m unittest discover -s tests -p test_rewrite_illustrative_rsi.py -v
```

Use `--chi 7.5` or `--chi 1.5` for one four-elasticity comparison.
`--sigma 1.5 --solve-only` solves one elasticity without publishing an
incomplete comparison. After all four have been solved, `--chi 7.5 --finish`
repeats the longer-horizon, optimality, transversality and early-window checks
before exporting. Omit `--finish` to run all stages. There is no outer
calibration loop. Checkpoints in `tmp/rewrite_bvp_rsi_chi_*/` are reusable;
their parameters and initial stocks are checked before use.

The two output folders are `numerical_rewrite/rsi_chi_7_5/` and
`numerical_rewrite/rsi_chi_1_5/`. Each contains the parameter specification,
three-horizon annual research moments, equation and optimality audits,
event-continuity checks, CSV, snapshots and plot manifests. Annual research
expenditure is `integral(M,0,1)/integral(Y,0,1)`, not M0/Y0; these are
**outcomes, not targets**. The figures retain the paper's three groups:
normalized accumulation growth, wages/interest/prices, and income shares,
with years -2 to 10 and 10 to 500 shown separately. Earlier exports are
untouched. Research productivity affects the transition but not the
characterized finite-bound limiting growth rates. The dates are not forecasts.

The following two sections document **archived target-based exercises**;
their numbers and calibration descriptions do not describe the default PDF.

## Central illustrative scenario: first-year research share of 0.183% (archived)

The former Section 6.2 uses `integral(M,0,1)/integral(Y,0,1)=0.00183` as an
illustrative target at sigma=1, not as an exact observed estimate. It is
neither M0/Y0 nor the time average of the instantaneous ratio. The retained
chi gives 0.1829159408%, a discrepancy of -0.0084059 basis points. The
rounding half-width is 0.05 basis points (three decimal places in percent),
so no numerical retuning is needed. Equilibrium tolerances are unchanged.

```text
python scripts/calibrate_rewrite_research_share_central.py
python -m unittest discover -s tests -p test_rewrite_research_share_central.py -v
python -m unittest discover -s tests -p test_rewrite_rsi_half_decline.py -v
```

The default command solves all four cases using the retained chi, repeats
the equilibrium and event-continuity audits, and verifies the research
target before publication. With existing admitted checkpoints, append
`--verify-existing` to recompute annual moments at 64/128 quadrature nodes
on the base, refined and long horizons without solving again. It checks
checkpoint and CSV hashes, existing admission, and annual-moment stability.
This mode does not claim to rerun every equilibrium audit. It writes
`research_share_target.json` in `numerical_rewrite/rsi_activation_half_decline/`.

For provenance, the retained chi was originally chosen to match a 40%
price decline over 27 months, half the rounded observed percentage fall.
The original `calibration.json`, price-search script and trials remain
unchanged. The price decline is now an implied outcome, not a second
target; the diamond in the price panel illustrates that outcome. The new
target was selected after examining the earlier simulations, not estimated
independently. Initial stocks, other parameters and trajectories are unchanged.

The unit-elastic first-year research share is 0.1829159%, compared with the
US 2024 proxy of 0.1543791% (45.23/29298.013) and the US 2025 proxy of
0.3562176% (109.58/30762.099). Compute estimates are from Korinek and
McKelvey (2026), Table 3; nominal GDP is the BEA GDPA series. This is a
check on magnitude, not an exact empirical or joint fit. The
estimates assume a 50% training/research allocation of rental-equivalent
AI compute spending and do not directly measure global autonomous RSI.
At sigma=1.50, first-year M/Y is 3.0091%, well above these proxies.
All annual ratios use the integral of M divided by the integral of Y,
not an initial instantaneous ratio. All four model ratios fall between
the first and second years, unlike the US estimates over 2023-2025.

At sigma=1.50, labor's share reaches half its initial value around year 47.
The limiting output-per-person growth, wage growth and net interest rate
are 3.13%, 2.42% and 7.13%. Industry size and recent expenditure growth
remain unfitted; the reported dates are not forecasts.

## Slow-transition sensitivity: approximate research-expenditure calibration (archived)

The former Section 6.3 uses the lowest previously discussed dated proxy, US 2023:
training/research compute of $18.46 billion divided by nominal GDP of
$27,811.517 billion, or 0.0663754%. At chi=1.4378 the unit-elastic path gives
0.0637427%, a shortfall of 0.2633 basis points. The author requested an
approximate match; no equilibrium tolerance was relaxed. All other parameters
and initial stocks are unchanged. The three figure groups retain their format.
Chi is selected at sigma=1 and held fixed at 0.90, 1.10 and 1.50; no second
target is imposed in those cases. Each economy retains its own fixed-B
pre-RSI BGP with common K0/Y0=3.30. Data, checks and source qualifications
are in `numerical_rewrite/rsi_research_share_2023/README.md`.

```text
python scripts/calibrate_rewrite_research_share_low.py
python -m unittest discover -s tests -p test_rewrite_research_share_low.py -v
```

For a staged run, add `--sigma 0.9`, `--sigma 1`, `--sigma 1.1`, or
`--sigma 1.5` to solve one case, then run without arguments to audit and
publish the complete comparison. The existing two horizon extensions,
early-window residual tests, terminal/TVC and Hamiltonian-support gates
are unchanged. `annual_moments.json` reports first- and second-year
expenditure shares and untargeted price changes for every elasticity.

The default full-replication driver includes the low-target publication.
The higher 2025-target exercise is no longer displayed but remains intact in
`numerical_rewrite/rsi_research_share_2025/` and can be reproduced with
`python scripts/calibrate_rewrite_research_share.py --publish-unit`.
Its former text and tables are in `sections_rewrite/preserved/`.
The original high-target search remains available through `--diagnose`, while
`--compare-published` measures the earlier price-calibrated paths. These
commands retain the distinction between verified equilibria and exact fits.

At sigma=1.50, labor's share reaches half its initial value around year 221,
versus 47 in the central scenario. The limiting output-per-person
growth, wage growth and net interest rate remain 3.13%, 2.42% and 7.13%.
In the finite-bound limits characterized in the paper, positive chi affects
the transition, not those limits. This does not identify sigma or Bbar,
and the dates are not forecasts. Industry size and recent expenditure
growth remain unfitted; the two empirical moments are not matched jointly.

## Preserved full-price-decline benchmark

The former Section 6.1 fitted chi=36.83070200718361 to the full rounded
80% price decline. Its large initial research outlay, developer loss and
negative gross investment at sigma=1.50 motivate removing its figures from
the main presentation, not rejecting its numerical equilibrium checks.
Its original source is `sections_rewrite/08_rsi_activation.tex`, with
tables/results beside it, figures in `figures_rewrite/`, and data/audits in
`numerical_rewrite/rsi_activation/`. Nothing was deleted.

```text
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation
python -m unittest discover -s tests -p test_rewrite_rsi_activation.py -v
```

The original price driver supports `--calibrate-only`, `--sigma` and `--finish`. See
`numerical_rewrite/rsi_activation/README.md`. Use the editorial switch above
to restore the figures without rerunning any simulation.

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
