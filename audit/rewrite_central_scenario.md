# Central illustrative scenario — September 14, 2026

## Approved editorial change

This update supersedes the ordering in `rewrite_simulation_selection.md`:

- 6.1: common experimental design and initial conditions.
- 6.2: central illustrative scenario, formerly 6.3, chi=7.616304576019883.
- 6.3: slow-transition sensitivity, formerly 6.2, chi=1.4378.
- 6.4: interpretation and limitations.

Both use the same four elasticities, initial stocks and other parameters.
No solver, calibration target, trajectory, admission tolerance, CSV or figure
was changed. The six existing figures, parameter tables, numerical-accuracy
tables, appendix instructions and default replication commands follow the
new order. The full-price and legacy switches remain available.

The central scenario is described on its own before the slow sensitivity
compares its initial reallocation and transition dates with that benchmark.
The title, abstract, introduction, model equations and analytical results
are preserved. Only the proof's calibration-table cross-reference changes.

## Empirical interpretation

Chi remains fitted to the 40% price decline over 27 months at sigma=1,
not to research spending. The first-year ratio of the integral of M to
the integral of Y is 0.1829159408% at sigma=1. The US 2024 estimate is
45.23/29298.013 = 0.1543790700%, a difference of 2.8536871 basis points.
The US 2025 estimate is 109.58/30762.099 = 0.3562175650%.

These are comparisons with different dated estimates, not confidence
bounds or a second fitted target. Compute values are from Korinek and
McKelvey (2026), Table 3 (technical appendix Table 13); nominal GDP is
BEA GDPA, accessed September 14, 2026. The paper explains the assumed 50%
training/research allocation and rental-equivalent costs, as well as the
US/global and human-directed/autonomous research distinctions.

The central sigma=1.50 path instead has first-year M/Y=3.0091094586%,
well above these estimates. This limitation is explicit. All four model
shares fall between the first and second years, unlike the US estimates.
No claim of a joint empirical fit or identified takeoff dates is added.

## Verification

Executed without solving new equilibrium paths:

- `test_rewrite_simulation_selection.py`: 7 passing tests for subsection
  and figure order, appendix and replication order, empirical comparison,
  unchanged saved inputs/CSV hashes, and mocked default/legacy commands.
- `test_rewrite_rsi_half_decline.py`: 9 passing tests, including saved
  admission records, checkpoint hashes, initial continuity, the price
  target, parameters, analytical limits and figure provenance.
- `test_rewrite_research_share_low.py`: 8 passing tests, including the
  unchanged expenditure target, all four saved admission records, initial
  stocks, annual moments, feasibility and accounting.
- Tectonic compiles `main_rewrite.tex`; the contents and equation/figure/
  table references update automatically. Rendered review checks subsection
  starts, the empirical qualification, parameter tables and the contents.
- No tracked changes under `numerical_rewrite/` or `figures_rewrite/`;
  the two calibration scripts are unchanged. The replication driver only
  changes the order of its existing commands.

The stable public PDF path and all numerical filenames remain unchanged.
