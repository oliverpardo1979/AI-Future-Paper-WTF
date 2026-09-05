# The Future of Growth and Human Labor Under Recursive AI Self-Improvement

This repository contains the paper, analytical appendices, numerical
equilibrium solver, admission audits, and published figures.

## Current manuscript

- `main_rewrite.tex`: current manuscript entry point.
- `sections_rewrite/`: introduction, literature review, model, equilibrium
  regimes, quantitative results, conclusion, and appendices.
- `output/pdf/main_rewrite.pdf`: local compiled PDF (generated, not tracked).
- `REPLICATION.md`: user-oriented instructions for reproducing every reported
  numerical equilibrium and figure.

To reproduce the simulations from a fresh clone with Python 3.12:

```text
python -m pip install -r requirements-rewrite.txt
python scripts/reproduce_rewrite_results.py
```

The reproduction command is fail-fast. It exports the four-scenario comparison
only after every path passes the numerical equilibrium-admission checks. See
`REPLICATION.md` for the economic intuition, platform-specific setup, output
map, and interpretation of the diagnostics.

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
