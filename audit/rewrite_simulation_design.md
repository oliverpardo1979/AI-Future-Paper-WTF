# Agreed simulation design for the finite-frontier rewrite

Status: design and interior initial-state reference confirmed on 2026-09-03.
All four BVPs have now passed the final numerical equilibrium audit. See
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
| chi | 0.01 | Illustrative research productivity, not estimated |

The UN source does not project a constant population-growth rate forever.
Likewise, with the other annual rates fixed, chi is not merely a free time-unit
normalization: changing it changes research speed relative to the other
processes. None of the AI-specific values is an empirical estimate.

## Initial condition: confirmed interior reference

The user suggested starting at the stationary state for sigma=1. In the
finite-frontier model, an exact stationary normalized macro allocation with
constant capability requires B at its frontier. Setting B_0=Bbar makes
psi(B_0)=0 and prevents subsequent capability accumulation. A developer gains
nothing from research expenditure at that boundary, so the research choice
would be M=0. This is a boundary problem, not an interior path satisfying the
current research first-order condition and the maintained B_0<Bbar domain.
Do not put B_0=Bbar into the current interior BVP or approximate it by clipping.

The historical uncapped unit-elastic BGP instead supplied

\[
 A_0=N_0=1,\qquad K_0=2.027733653970002,\qquad
 B_0=0.44367093160980464.
\]

These are the confirmed common initial stocks for the finite-frontier
comparison, but they are not an exact BGP of the new capped model. The old
consumption and shadow-value choices must not be imported: C_0 and q_0 must be
selected anew by the equilibrium BVP for each sigma. Using terminal normalized
capital with B_0<Bbar would be another initialization, also not an exact
stationary state; no arbitrary frontier gap has been selected.

The user approved the recommended interior reference after the distinction
was explained. Every final BVP uses exactly these stocks; none was moved to
obtain convergence. Initial consumption and the shadow price are endogenous.

## Two figures, six panels each

Use one economic variable per panel and one line per admitted scenario.
Preserve the following row-major order, notation, denominators, and scales.
The comparison uses line charts, not stacked bars or stacked areas.

### Figure 1: growth, wages, and the distribution of final output

| Panel | Variable | Vertical scale |
|---|---|---|
| A | Y/(AL) | Logarithmic |
| B | g_Y-n | Linear, percent per year |
| C | g_w | Linear, percent per year |
| D | r | Linear, percent per year |
| E | wL/Y | Linear, percent |
| F | p_X X/Y | Linear, percent |

The last panel shows AI-industry sales relative to final output. Do not
replace it by Pi/Y or label sales as industry value added.

### Figure 2: technology, accumulation, and AI-revenue composition

| Panel | Variable | Vertical scale |
|---|---|---|
| A | B/Bbar | Linear, fraction between zero and one |
| B | C/(AL) | Logarithmic |
| C | K/(AL) | Logarithmic |
| D | U/(p_X X) | Linear, percent |
| E | M/(p_X X) | Linear, percent |
| F | Pi/(p_X X) | Linear, percent, allowing negative values |

The second-row denominator is deliberately AI revenue, not final output:
U/(p_X X)+M/(p_X X)+Pi/(p_X X)=1. This is a display normalization, not a
redefinition of any model variable. Preserve negative profits where they
occur instead of truncating the axis or applying a logarithmic scale.

Use identical scenario colors and distinguishable line styles in both figures,
linear time axes, and common plotted horizons. Use the same physical unit and
normalization across scenarios. Do not divide each scenario by its own
initial or terminal value, which would conceal impact differences. A constant
The vertical distance between g_Y-n and g_w is the growth wedge that governs
the decline of labor's income share. Y/(AL) need not converge in the AI-dominated
regime. Growth and interest limits can be shown as analytical reference lines,
not imposed observations or fabricated extensions of a finite numerical path.

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
