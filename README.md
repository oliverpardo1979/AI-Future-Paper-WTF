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

The principal calibration is in Section 6.6, "Principal calibration: AI
prices and common initial stocks". It uses the existing
`price_calibrated_low_ai_high_cap` results: common Ramsey capital,
`omega_X=0.10`, `eta=0.20`, `B0/Bbar=0.01`, and `chi=36.03184470863892`
fitted at unit elasticity and held fixed across the four elasticities.
The upper bound is ten percent above the `sigma=1.50` threshold.

To reproduce the principal calibration from a fresh clone with Python 3.12:

```text
python -m pip install -r requirements-rewrite.txt
python scripts/calibrate_rewrite_ai_price.py --variant low_ai
```

The command exports only paths that pass the numerical equilibrium-admission
checks. The earlier timing, slow-transition, and near-terminal comparisons
remain available through `python scripts/reproduce_rewrite_results.py`. See
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
