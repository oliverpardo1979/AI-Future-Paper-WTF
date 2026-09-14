# Selection of displayed simulations — September 14, 2026

## Decision and scope

Section 6 now has four subsections: common design, principal M/Y calibration,
half-price-decline sensitivity, and interpretation/limitations. The six
displayed figures use the existing four-sigma CSVs and figure files without
modification. No new equilibrium path, numerical approximation, parameter,
initial condition, tolerance, or model equation was introduced.

The full 80%-price-decline benchmark is hidden by
`\showfullpricebenchmarkfalse`, not deleted or numerically rejected. Its
original `08_rsi_activation.tex`, results, parameter/accuracy tables, code,
CSV, audits and figures remain intact. The separate older-presentation
switch is also preserved. The default reproduction driver now runs only
the two displayed calibrations; `--include-legacy` retains the full-price
command as well. The introductory loss example is identified in a footnote
as belonging to the archived exercise. The approved title, abstract, main
introductory text, analytical statements and proofs are unchanged, except
that an appendix cross-reference now points to the principal parameter table.

## What the comparison establishes

- Principal chi: 1.4378. Faster sensitivity: 7.616304576019883.
- All other parameter fields, Bbar, B0 and sigma-specific K0 match exactly
  between the saved manifests. Common K0/Y0 remains 3.30.
- For sigma=1.50, saved T50 is 220.54970420158583 versus
  46.79608906261537 years; T90 is 424.0296289432169 versus
  137.02405771748656 years. These dates concern the decline in labor's share,
  not a separately defined output takeoff event.
- The limiting rates and shares characterized with finite Bbar and positive
  chi are independent of chi. Timing and the allocation along the path are
  not. This is conditional on the characterized limits, not an identification
  claim for sigma/Bbar, a theorem for the uncapped economy, or a world forecast.
- Industry size, recent expenditure growth and simultaneous expenditure/price
  matching remain limitations. The aggressive benchmark's initial losses
  and capital liquidation are discussed, not attributed to the displayed cases.

## Reproducible checks executed

- `test_rewrite_simulation_selection.py`: 5 tests pass. They verify section
  order, six active figures, reversible restoration of the nine-figure
  presentation, unchanged data hashes/other inputs, saved transition dates,
  and default/legacy driver command selection (mocked; no solver run).
- Research-share-low, RSI-half-decline, RSI-activation, no-AI BVP, finite-cap
  BVP, global finite-cap BVP, and near-unit BVP suites: 47 tests pass.
  These use the existing admission records and regression problems; no
  calibration or export pipeline was rerun.
- `git diff --check`: passes. No changes under `numerical_rewrite/` or
  `figures_rewrite/`, or to the two calibration scripts.
- Tectonic compilation of `main_rewrite.tex`: 73 pages, no unresolved
  references/citations or overfull/underfull boxes. Fontconfig emits the
  pre-existing local configuration warning, but TeX completes successfully.
- Visual review covers the contents, section transitions, parameter table,
  retained charts, limitations/conclusion and numerical-accuracy tables.
- The fetched remote merge b31b55e had the same tree as 25c9a8d and was
  fast-forwarded before publication, preserving Overleaf history.

The README, replication guide and numerical appendix document the new order
and both reversible switches. The stable public PDF filename is unchanged.
