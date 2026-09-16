# Figure-by-figure exposition of the illustrative RSI simulations

Baseline: `76b3062`, including the author's latest Section 6.2 edit.
Scope: prose only; no new simulations, calibration changes or figure edits.

## Organization

Each figure is now introduced and interpreted before the next one:

- Section 6.2: Figure 4 quantities, Figure 5 wages/returns/prices,
  Figure 6 income and expenditure shares.
- Section 6.3: Figures 7--9 in the same order, emphasizing what lower
  research productivity changes and what it leaves unchanged.
- Each discussion identifies panels, normalization, units, line styles,
  initial versus extended horizons, short-run mechanisms and long-run limits.
- Distribution figures have two rows per horizon, not one. Their layout
  and captions are preserved exactly.

The editorial narrative is in `12_rsi_high_productivity.tex` and
`13_rsi_low_productivity.tex`, beside the unchanged figure environments.
The generated `rsi_chi_*_results.tex` digests are preserved but no longer
input in these sections. This prevents the reporting script from overwriting
the new prose; neither that script nor the solver was edited.

## Sources and checks

The existing `summary.json`, `annual_moments.json`, `figure_manifest.json`,
scenario files, admission audits and path hashes in the two
`numerical_rewrite/rsi_chi_*` folders were inspected. All six figure images
were inspected, and the revised PDF pages were rendered and checked.

Reproducible, read-only check:

```text
python scripts/check_rewrite_rsi_exposition.py
```

This checks 24 rounded snapshot values, the two first-year research shares,
27-month price changes, labor-share halving dates, analytical limits,
existing admission records and data hashes, unchanged figure environments,
and unchanged parameters, initial states, figure files and simulation data.
It also checks positive net profit on the stored higher-productivity paths.
It does not rerun the equilibrium solver or replace its original audit.

The final Tectonic build completes without undefined references or
overfull/underfull-box warnings. The 69-page PDF places Section 6.2 on
pp. 24--29 (Figures 4--6 on pp. 26, 27 and 29) and Section 6.3 on
pp. 30--34 (Figures 7--9 on pp. 31, 32 and 34). The public PDF copy
has the same SHA-256 as the local compiled PDF.

Important distinctions retained in the text:

- The plotted quantity growth rates subtract `n + gamma`; output-per-person
  growth subtracts only `n`. The zero line is not zero aggregate growth.
- Rates are instantaneous, while initial stocks and current production
  remain continuous. Consumption and research can jump, reducing investment.
- At sigma=1.5, the limiting normalized quantity growth rate is 2.13%,
  output-per-person growth 3.13%, wage growth 2.42% and the interest rate 7.13%.
- At year 500, normalized output growth is still 2.24% with chi=7.5
  and 3.21% with chi=1.5. Endpoints are not reported as exact limits.
- The later scenario's faster growth at year 500 is a difference in stage
  of transition, not a higher asymptotic growth rate.
- Annual expenditure shares are expenditure/output integrals over year one,
  not date-zero ratios and not empirical calibration targets.
- AI revenue is not net profit: inference and research costs are separated.

## Minimal compilation repairs

Two pre-existing editorial breakages were repaired without restoring
deleted prose or changing economic content:

1. Remove the orphan `\fi` in `rsi_parameters.tex`; every table value and
   other table line is unchanged.
2. In the active numerical appendix, replace a reference to the author's
   commented-out pre-event consumption equation with the existing resource
   constraint, evaluated at zero research and BGP capital growth.

Title, abstract, introduction, Section 6.1 prose, model, propositions,
simulation routines, generated numerical digests and all figures remain
unchanged relative to the baseline.
