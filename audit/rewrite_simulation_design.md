# Agreed simulation design for the finite-frontier rewrite

Status: revised design and interior initial-state reference confirmed on 2026-09-07;
slow-transition and near-terminal diagnostics added on 2026-09-08, and the
Ramsey-start transition added on 2026-09-09. All
reported BVPs have passed the final numerical equilibrium audit. See
`audit/rewrite_equilibrium_simulations.md` and `numerical_rewrite/*_audit.json`
for execution evidence and remaining publication steps. The original design
and the distinction between a capped stationary boundary and the historical
uncapped BGP are preserved below.

## Economic question and comparison

Compare growth, wages, returns, and the distribution of final output when
autonomous AI research operates under different elasticities of substitution
between effective labor and AI production services. All four scenarios have
positive AI weight. Do not reintroduce human research or a no-AI scenario into
this comparison.

The agreed scenario elasticities are 0.90, 1.00, 1.10, and 1.50. Hold every
other parameter, including the capability frontier, fixed. The proposed common
frontier is

\[
 \overline B=1.10\,\overline B_c(1.50)=170.12401740519488.
\]

This is an illustrative scenario choice, not an empirical estimate. The
factor 1.10 puts the last case ten percent above its analytical threshold;
it does not represent a numerical tolerance. The threshold at sigma=1.10
is 60,413,358.45354841, whereas at sigma=1.50 it is 154.65819764108625.
Thus the comparison includes two distinct substitute-input regimes.

| sigma | Intended terminal regime | Per-person growth limit | Net interest limit |
|---|---|---|---|
| 0.90 | Positive labor income share | 0.01 | 0.05 |
| 1.00 | Unit-elastic reference; constant labor income share | 0.01 | 0.05 |
| 1.10 | Positive labor income share, frontier below threshold | 0.01 | 0.05 |
| 1.50 | AI-dominated, frontier above threshold | 0.0313499758138466 | 0.0713499758138466 |

These numbers evaluate the Section 4 formulas. The transition calculations
are separately documented and audited; these formulas alone do not establish
equilibrium from common initial stocks.

## Inherited parameters

The controlling historical references are Table 2 in
`sections_axm/04_growth_regimes.tex` and
`PositiveAIBenchmarkParameters` in `scripts/define_positive_ai_branch.py`.
They agree on the following values. Do not import the obsolete n=0.012 and
gamma_A=0 values still present in older simulation artifacts.

| Current paper notation | Value | Interpretation / inherited rationale |
|---|---|---|
| alpha | 0.33 | Final-output capital elasticity; agreed macro benchmark |
| delta | 0.05 | Annual capital depreciation; historical table references PWT |
| rho | 0.04 | Annual household discount rate; agreed preference benchmark |
| n | 0.003 | Constant-rate approximation adopted from UN 2024-2100 projections |
| gamma | 0.01 | Annual exogenous labor-productivity growth, formerly gamma_A |
| omega_X | 0.20 | Illustrative AI-services CES weight, not an estimated share |
| omega_L | 0.80 | One minus omega_X |
| eta | 0.20 | Research exponent, satisfying eta<alpha and 2 eta<=1 |
| chi | 1.4378 | Research speed calibrated to a 50-year transition midpoint in the sigma=1.50 path |

The UN source does not project a constant population-growth rate forever.
Likewise, with the other annual rates fixed, chi is not merely a free time-unit
normalization: changing it changes research speed relative to the other
processes. The midpoint is the first date at which the sigma=1.50 labor share
has completed half of the decline from its date-zero value to its analytical
limit. The calibration is illustrative, not an empirical estimate.

## Initial condition: confirmed interior reference

The user suggested starting at the stationary state for sigma=1. In the
finite-frontier model, an exact stationary normalized macro allocation with
constant capability requires B at its frontier. Setting B_0=Bbar makes
psi(B_0)=0 and prevents subsequent capability accumulation. A developer gains
nothing from research expenditure at that boundary, so the research choice
would be M=0. This is a boundary problem, not an interior path satisfying the
current research first-order condition and the maintained B_0<Bbar domain.
Do not put B_0=Bbar into the current interior BVP or approximate it by clipping.

The published comparison instead uses

\[
 A_0=N_0=1,\qquad K_0=4,\qquad
 B_0=0.10\overline B=17.012401740519476.
\]

These common stocks are closer to the capped sigma=1 terminal regime: initial
AI efficiency is 10 percent of its frontier and initial capital per unit of
effective labor is about 44 percent of its terminal sigma=1 value. They are
still not an exact BGP of the capped model. Consumption and the shadow value
must be selected anew by the equilibrium BVP for each sigma.

Every main BVP uses exactly these stocks; none was moved to obtain convergence.
Initial consumption and the shadow price are endogenous. A separately audited
financing sensitivity retains the earlier distant stocks
K_0=2.027733653970002 and B_0=0.44367093160980464 and uses chi=1.4223 to keep
the same 50-year midpoint. It is not one of the four main plotted paths.

## Slow-transition sensitivity

The earlier comparison is retained as a separate sensitivity rather than
replacing the main design. It uses K_0=2.027733653970002,
B_0=0.44367093160980464, and chi=0.01, while holding the frontier, all other
parameters, and the four sigma values fixed. Its display window is 4,000 years.
The same BVP, horizon extensions, independent equation checks, TVCs, and
developer-optimality gates are rerun for all four paths. The figures preserve
the main comparison's variables, normalizations, scenario order, and scale
types. Because both the initial stocks and chi differ from the main design,
this is a joint timing sensitivity rather than a one-parameter derivative.

## Near-terminal diagnostic

To distinguish long-run behavior from adjustment to the common main stocks,
the diagnostic uses all four elasticities and sets B0/Bbar=0.9999. For
sigma=0.90, 1.00, and 1.10, it sets K0/(A0 N0) equal to the corresponding
analytical terminal capital ratios: 6.557094, 9.098967, and 12.265203. The
AI-dominated regime has no finite terminal value of K/(AN). For sigma=1.50,
the design therefore initializes its convergent predetermined state at
(Bbar-B0)K0=dbar, which implies K0=4101704.227532. The BVP selects consumption
and the shadow value anew. Because B0 is strictly below the frontier, the
paths remain interior and are not exact finite-date steady states. Because
the initial capital rule differs across terminal regimes, the diagnostic
illustrates each regime near its own terminal allocation; it is not a
common-stock comparative experiment. The sole figure reports
output-per-person growth, real-wage growth, and the net interest rate over 500
years against the regime-specific analytical limits.

## Transition from the no-AI steady state

The additional common-stock experiment starts from the exact no-AI Ramsey
steady-state capital ratio implied by the maintained macro parameters,

\[
 K_0/(A_0N_0)=[\alpha/(\rho+\delta+\gamma)]^{1/(1-\alpha)}
 =5.94157252710329,
 \qquad B_0/\overline B=0.01.
\]

Before date zero, omega_X=0 and AI efficiency is irrelevant. At date zero,
omega_X changes to 0.20 and omega_L to 0.80. The positive-AI BVP is then
solved independently for all four elasticities. Consumption and the shadow
value are not imported from the Ramsey allocation. This is a technology-switch
experiment from Ramsey predetermined stocks, not continuation through the
degenerate omega_X=0 branch and not a welfare comparison that preserves the
old production technology as an outside option. The display window is 500
years and uses the same three figure families as the main comparison.

## Published figure layout

Use one economic variable per panel and one line per admitted scenario.
Preserve the following row-major order, notation, denominators, and scales.
The comparison uses line charts, not stacked bars or stacked areas.

### Quantities and accumulation

| Panel | Variable | Vertical scale |
|---|---|---|
| A | g_Y-(n+gamma) | Linear, percent per year |
| B | g_X-(n+gamma) | Linear, percent per year; separate range |
| C | g_K-(n+gamma) | Linear, percent per year |

Panels A and C use the same vertical scale. Panel B uses a separate range
because the initial growth of X/(AL) is much larger.

### Prices and returns

| Panel | Variable | Vertical scale |
|---|---|---|
| A | g_w | Linear, percent per year |
| B | r | Linear, percent per year |
| C | p_X | Logarithmic level |

The AI-service price remains strictly positive, declines, and converges to a
finite level in all four terminal regimes. Its level is therefore more
informative than its growth rate; the logarithmic scale keeps all four paths
visible.

### Distribution of noncapital output

| Panel | Variable | Vertical scale |
|---|---|---|
| A | wL/Y | Linear, percent |
| B | Pi/Y | Linear, percent |
| C | U/Y | Linear, percent |
| D | M/Y | Linear, percent |

The four shares sum to 1-alpha. The omitted gross capital-income share is the
constant alpha. Keep the separate financing sensitivity in the text because
its negative initial profit is not part of the four main plotted paths.

Use identical scenario colors and distinguishable line styles in all figures,
linear time axes, and common plotted horizons. Use the same physical unit and
normalization across scenarios. Do not divide each scenario by its own
initial or terminal value, which would conceal impact differences. The
difference between g_Y-n and g_w remains the growth wedge governing the
decline of labor's income share, even though the two rates now appear in
different parts of the quantitative presentation. Y/(AL) need not converge in
the AI-dominated regime. Growth, price, and interest limits can be shown as
analytical reference lines, not imposed observations or fabricated extensions
of a finite numerical path.

## Implementation and admission requirements

Preserve the existing finite-cap architecture: exact static monopoly solution,
four-dimensional dated BVP, two initial stock conditions, and two terminal
stable-manifold projection conditions. The terminal regime, not the
unit-elastic BGP of the uncapped model, determines the long-run closure.

The production terminal dispatcher now also implements the rewrite's
sigma<=1 formulas. All four cases retain the existing static block,
four-dimensional BVP, initial-state continuation, and terminal projections.
The exact unit limit and near-unit evaluations have separate tests.

Before exporting any figure, require dated equation residuals, feasibility,
stability to horizon and tolerance changes, a justified infinite-horizon
continuation, both TVCs, and sufficient global developer optimality over the
reachable counterfactual capability domain. The local existence propositions
alone do not establish the common-initial-state comparison. Keep failed
candidates out of plot-ready files, the paper, and summaries of equilibrium
results; do not quietly omit a requested scenario from a figure.

The archived global audit at a different frontier is not evidence for this
comparison. Each new scenario has its own solved checkpoints, two horizon
extensions, independent equation residuals, and optimality audit. For sigma
1.50, global profit concavity fails; the new appendix proves a weaker
sufficient global-Hamiltonian-support criterion, which passes the numerical
transition audit and has an analytical eventual bound. The old failed
curvature verdict remains in the report rather than being overwritten.

## Historical preparation check

Executed the existing five tests in `tests/test_rewrite_finite_frontier.py`:
all passed. These check terminal algebra, linearizations, consumption,
near-unit static continuity, and interest comparative statics. They are not
four transition simulations. The default sandbox could not read the local
NumPy installation; the same test command passed with approved access to the
existing project dependencies. No dependency, parameter, trajectory, figure,
or manuscript file was changed by that preparation-stage verification.
Subsequent simulation execution is recorded in the separate implementation
report, not retroactively attributed to this initial algebra check.
