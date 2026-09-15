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
productivity takes two illustrative values, 7.5 and 1.5, each shared across
all four elasticities. Neither value is fitted to a price or expenditure
target. Section 6.1 explains the common design and initial conditions.

Section 6.2 uses **chi=7.5 (higher research productivity)**; Section 6.3
uses **chi=1.5 (lower research productivity)**. All eight paths are solved
and audited independently; no trajectory is rescaled in time. Results are
in `numerical_rewrite/rsi_chi_7_5/` and `numerical_rewrite/rsi_chi_1_5/`.
The annual research shares and price changes are model outcomes, not targets.
Section 6.4 discusses unfitted industry size, measurement limitations and
adjustment assumptions. Within the characterized finite-bound limits,
chi affects transitions, not limiting growth and distribution. The reported
dates are conditional model outcomes, not forecasts.

To reproduce both illustrative scenarios from a fresh clone with Python 3.12:

```text
python -m pip install -r requirements-rewrite.txt
python scripts/simulate_rewrite_illustrative_rsi.py
```

Each output directory contains `scenario.json`, `annual_moments.json`,
audits, a CSV and figure manifests. The command exports only paths that
pass the numerical equilibrium-admission
checks. Run `python scripts/reproduce_rewrite_results.py` for both displayed
comparisons; add `--include-legacy` for the earlier comparisons as well.
The full 80%-price-decline experiment is preserved, but hidden because of
its implausibly large initial reallocations, not a failure of its numerical
checks. Its original text is `sections_rewrite/08_rsi_activation.tex` and
its outputs are in `numerical_rewrite/rsi_activation/`.
Set `\showfullpricebenchmarktrue` in `main_rewrite.tex` to display it again.
The former chi=7.616304576019883 and chi=1.4378 comparisons remain intact;
set `\showcalibratedrsiscenariostrue` to restore their text, figures and
parameter-table row. The default is `\showcalibratedrsiscenariosfalse`.
Separately, `\showlegacysimulationstrue` restores the older quantitative
section and numerical appendix. All three switches are false by default. See
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
