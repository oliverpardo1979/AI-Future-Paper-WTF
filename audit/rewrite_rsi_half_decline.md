# Half-price-decline RSI sensitivity

September 14, 2026. Requested additional subsection in `main_rewrite.tex`.

## Experiment

The user requested half the observed percentage decline in p_X as the target
for chi. The announced interpretation is an 80% -> 40% decline over 2.25
years: a final/initial ratio of 0.60. This does not halve the log change or
chi. The price target is a sensitivity assumption, not another observation.

All other parameters and the four initial stocks are identical to the
existing-AI pre-RSI BGP exercise. Only chi is refitted. The old 80%-target
data and figures, all silenced earlier designs, title, abstract, introduction,
and analytical equilibrium equations are preserved.

## Execution

Executed the public command with variant `rsi_activation_half_decline`:
first `--calibrate-only`, then each of `--sigma 0.9`, `--sigma 1`,
`--sigma 1.1`, and `--sigma 1.5`, then `--finish`.
The unchanged four-dimensional BVP uses 32 initial-stock continuation stages,
two 500-year horizon extensions, independent equation checks, both TVCs,
global developer optimality, and dense first-decade checks. No tolerance
or economic condition was relaxed.

The fitted chi is 7.616304576019883 (20.679% of the original). The final
refined unit-elastic price ratio is 0.6000000059127867.
All four cases pass admission. The high-substitution case fails the stronger
global-concavity test but passes both existing 81/101 and 321/241 Hamiltonian
support grids and the analytical continuation bound. Its dense early-window
concavity check also passes; no alternative early support grid is required.

| sigma | final horizon | nodes | maximum independent dynamic residual | final-horizon change |
|---|---:|---:|---:|---:|
| 0.90 | 5422.060570 | 1199 | 1.1922e-9 | 3.0852e-8 |
| 1.00 | 4938.575563 | 1295 | 1.3741e-9 | 3.4952e-8 |
| 1.10 | 4822.839545 | 1336 | 1.4491e-9 | 3.7395e-8 |
| 1.50 | 3007.088683 | 1589 | 1.8011e-9 | 1.4947e-8 |

Residual bounds include the independent first-decade checks. The largest
monopoly FOC residual is below 1.46e-11; terminal coordinate gaps are below
3.22e-6. Both TVCs have asymptotic log growth n-rho=-0.037. Initial
production/price continuity log gaps are below 1.4e-15.

## Main comparison

The hash-bound `comparison_to_full_decline.json` verifies that only chi
changes, and records both sets of initial values and transition dates.

At sigma=1.50, initial output-per-person growth falls from 23.970% to
4.536%; the consumption jump falls from 22.708% to 5.045%; M/Y falls
from 9.317% to 3.098%; Pi/Y rises from -6.020% to +0.199%; and gross
investment/Y rises from -6.094% to +13.789%. These are initial values,
not new financing or investment constraints. Gross investment is still
below depreciation: K initially falls at an annualized 0.8215% rate.
The long-run rates and
shares are unchanged. The labor-share midpoint shifts from 11.744 to
46.796 years, and the 90% decline from 60.020 to 137.024 years.

No claim is made that the assumed initial sector size is fitted to data,
or that half the observed price decline identifies a monopoly effect.
This remains a model-conditional timing calibration.

## Replication and preservation

`scripts/calibrate_rewrite_ai_price.py` now selects the target by variant
without changing the original 0.20 constant or existing variants. The
new comparison has separate caches, outputs, figures, tests, and paper
includes. The default reproduction driver covers both active exercises.
The existing LaTeX switch still restores all older comparisons. JSON/CSV
line-ending preservation is scoped to the two active designs so SHA-256
provenance survives platform changes.

## Verification and PDF

All 42 tests in `test_rewrite_price_calibration.py`,
`test_rewrite_parameter_tables.py`, `test_rewrite_simulation_design.py`,
`test_rewrite_rsi_activation.py`, and `test_rewrite_rsi_half_decline.py`
pass with no skips after regeneration. The last suite checks the arithmetic
target, unchanged parameters and stocks, limiting rates, parameter table,
four admissions, final price match, plot hashes, and both-source comparison.

The PDF has 71 pages. Subsection 6.2 begins on page 29, its parameter
table is on page 30, and Figures 7--9 are on pages 32--34. Both sets of
accuracy checks appear in the numerical appendix. The contents, subsection,
table, figures, and appendix were rendered and visually inspected; there
are no unresolved references or overfull boxes. Window-figure font settings
are now explicit so a full run and a standalone redraw match visually.

Git comparisons confirm that the original RSI data, original window
figures, and original subsection/results text are unchanged.
