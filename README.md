# The Future of Growth and Human Labor Under Recursive AI Self-Improvement

This repository contains the paper, analytical appendices, numerical
equilibrium solver, admission audits, and published figures.

## Current manuscript

- `main_rewrite.tex`: current manuscript entry point.
- `sections_rewrite/`: introduction, literature review, model, equilibrium
  regimes with a finite frontier, the uncapped economy, quantitative results,
  conclusion, and appendices.
- `sections_rewrite/05_uncapped_equilibria.tex`: Section 5 compares all three
  substitution regimes without a frontier, distinguishing production bounds,
  conditional limits, proved equilibrium existence, and the remaining open case.
- `output/pdf/main_rewrite.pdf`: local compiled PDF (generated, not tracked).
- `REPLICATION.md`: user-oriented instructions for reproducing every reported
  numerical equilibrium and figure.

The principal exercise activates RSI in an economy already using AI.
Each elasticity starts from its own fixed-efficiency BGP, with common
`K0/Y0=3.30` and `r0=0.05`. Production weights do not jump: `omega_X=0.10`
before and after activation. The exercise keeps `eta=0.20`, `B0/Bbar=0.01`,
and an upper bound ten percent above the `sigma=1.50` threshold. Research
productivity is calibrated at unit elasticity, then shared across all four
scenarios. Section 6.1 explains this common design and the initial conditions.

Section 6.2 is the central illustrative scenario: a first-year M/Y target
of **0.183% at sigma=1**. The retained chi=7.616304576019883 produces
0.18291594%, matching the target at its quoted precision. This target is
illustrative, not an exact observed datum. Chi was originally obtained from
a 40% price decline over 27 months; that decline is now an implied outcome,
not a second target. At sigma=1.50, the first-year
share is 3.0091%, well above the empirical estimates. Results are in
`numerical_rewrite/rsi_activation_half_decline/`.
Section 6.3 is the slow-transition sensitivity: chi=1.4378 approximately
matches the historical US 2023 training-compute/GDP proxy. Other parameters
and initial stocks are unchanged. Data, sources and checks are in
`numerical_rewrite/rsi_research_share_2023/`.
Section 6.4 discusses the unfitted industry size, expenditure-growth mismatch
and adjustment assumptions. Within the characterized finite-bound limits,
chi affects transitions, not limiting growth and distribution. The reported
dates are conditional model outcomes, not forecasts.

To reproduce the central scenario from a fresh clone with Python 3.12:

```text
python -m pip install -r requirements-rewrite.txt
python scripts/calibrate_rewrite_research_share_central.py
```

The current target and achieved moment are recorded in
`numerical_rewrite/rsi_activation_half_decline/research_share_target.json`;
`calibration.json` preserves the historical price calibration. The command
exports only paths that pass the numerical equilibrium-admission
checks. Run `python scripts/reproduce_rewrite_results.py` for both displayed
comparisons; add `--include-legacy` for the earlier comparisons as well.
The full 80%-price-decline experiment is preserved, but hidden because of
its implausibly large initial reallocations, not a failure of its numerical
checks. Its original text is `sections_rewrite/08_rsi_activation.tex` and
its outputs are in `numerical_rewrite/rsi_activation/`.
Set `\showfullpricebenchmarktrue` in `main_rewrite.tex` to display it again.
Separately, `\showlegacysimulationstrue` restores the older quantitative
section and numerical appendix. Both switches are false by default. See
`REPLICATION.md` for the economic intuition, platform-specific setup, output
map, and interpretation of the diagnostics.

## Companion paper

**How Much Can Recursive AI Self-Improvement Raise Economic Growth?**

- `main_companion.tex`: independent entry point, compiled from the repository root.
- `sections_companion/`: self-contained unit-elastic uncapped model, analytical
  balanced-growth equilibrium and proof, inherited calibration, and sensitivity framework.
- `COMPANION.md`: scope, parameter provenance, checks, and remaining empirical work.
- `output/pdf/main_companion.pdf`: local compiled PDF (generated, not tracked).
- [Latest companion PDF](https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/how-much-can-recursive-ai-self-improvement-raise-economic-growth.pdf).

The companion is an initial working paper, not a completed empirical assessment.
The original manuscript and its Appendix C remain in place. Their numerical
solvers and reported transition paths are unchanged.

## Repository map

- `scripts/`: analytical, boundary-value, auditing, export, and plotting code.
- `tests/`: algebraic and numerical regression tests.
- `numerical_rewrite/`: committed audit reports, plot-ready data, provenance
  manifests, and a README linking the numerical files back to the paper.
- `figures_rewrite/`: figures generated from admitted paths.
- `audit/rewrite_equilibrium_simulations.md`: execution record for the
  published numerical results.
- `literature/literature_browser.html`: searchable literature database with
  abstracts or explicitly labeled editorial summaries and document links.

The earlier specification remains in `main.tex`, `sections/`, `numerical/`,
and the legacy solver scripts. Its proportional-allocation exercises should
not be interpreted as the equilibrium paths reported in the current paper.
