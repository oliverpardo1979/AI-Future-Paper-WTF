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
productivity is refitted at unit elasticity, then shared across all four
scenarios. Data and audits are in `numerical_rewrite/rsi_activation/`.

A second subsection keeps the same initial economies and all other parameters,
but fits chi to a 40% price decline over 27 months instead of 80%.
Its separate results are in `numerical_rewrite/rsi_activation_half_decline/`.
Use `--variant rsi_activation_half_decline` for that exercise, or
`python scripts/reproduce_rewrite_results.py` for all active comparisons.

A third subsection selects chi=1.4378 using the lower historical US
research-expenditure proxy (2023), then holds it fixed across the same four
elasticities. Run `python scripts/calibrate_rewrite_research_share_low.py`.
Its data, source qualifications and admission checks are in
`numerical_rewrite/rsi_research_share_2023/`. The manuscript explains the
unfitted industry size, expenditure-growth mismatch and adjustment assumptions;
these are conditional scenarios, not forecasts of current-world growth.

To reproduce the principal calibration from a fresh clone with Python 3.12:

```text
python -m pip install -r requirements-rewrite.txt
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation
```

The command exports only paths that pass the numerical equilibrium-admission
checks. The earlier timing, slow-transition, and near-terminal comparisons
remain available through `python scripts/reproduce_rewrite_results.py --include-legacy`.
Nothing was deleted: `\showlegacysimulationsfalse` in `main_rewrite.tex`
selects the three RSI exercises; change it to `\showlegacysimulationstrue` to
restore the earlier quantitative section and numerical appendix. See
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
