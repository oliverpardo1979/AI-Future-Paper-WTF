# RSI activation: implementation and verification

Date: September 14, 2026. Current manuscript: `main_rewrite.tex`.

## Agreed change

Replace the displayed no-AI-to-AI technology switch with an unanticipated
activation of RSI in an economy already using AI. Hide earlier simulations
with a reversible LaTeX switch, without deleting or overwriting them.
The title, abstract, introduction, analytical model, and equilibrium
definition are unchanged.

Before the event research is unavailable, B is fixed, and omega_X=0.10.
Each sigma has its own fixed-B BGP capital with K/Y=3.30 and r=0.05.
The post-event positive-chi BVP inherits only states, not pre-event C or q.
This is not a zero-M solution of the positive-chi problem, and numerical
continuation does not pass through chi=0 or omega_X=0.

## Implementation

- `scripts/simulate_rewrite_finite_frontier.py`: new `fixed_efficiency_bgp`
  helper and initial-capital rule; existing rules/equations unchanged.
- `scripts/calibrate_rewrite_ai_price.py`: separate `rsi_activation`
  variant, regime-specific initial stocks in calibration, full inherited
  admission pipeline, event/reference checks, and analytical pre-event
  segments in the existing three figure groups.
- `scripts/reproduce_rewrite_results.py`: default to the new comparison;
  `--include-legacy` also regenerates the preserved older designs. A default
  fresh run does not remove older-design checkpoints.
- `tests/test_rewrite_rsi_activation.py`: references, homogeneity,
  parameters, invalid-reference rejection, event continuity and resource
  accounting, admission, price match, and plot provenance.
- `sections_rewrite/08_rsi_activation.tex` and its parameter/result includes:
  new quantitative section. `appendix_rsi_activation.tex` and its accuracy
  include document the current algorithm and audits.
- `main_rewrite.tex` / `appendix.tex`: false selects the new presentation;
  `\showlegacysimulationstrue` restores the earlier section and numerical
  appendix. The conclusion's old simulation paragraph follows the same switch.

## Reproducible run

```text
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation --calibrate-only
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation --sigma 0.9
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation --sigma 1
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation --sigma 1.1
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation --sigma 1.5
python scripts/calibrate_rewrite_ai_price.py --variant rsi_activation --finish
python -m unittest discover -s tests -p test_rewrite_rsi_activation.py -v
python -m unittest discover -s tests -p test_rewrite_price_calibration.py -v
python -m unittest discover -s tests -p test_rewrite_parameter_tables.py -v
python -m unittest discover -s tests -p test_rewrite_simulation_design.py -v
```

Python used: bundled Python with repository `.python-packages` first in the
import path, matching the existing workflow. The four initial solves ran
independently. The complete calibration, final extensions, optimality and
early-window audits, export and figure rendering were executed successfully.

## Verified numerical results

The fit is chi=36.83070200718361. After both horizon extensions,
p_X(2.25)/p_X(0)=0.2000000011758617. All four cases pass the unchanged
post-event equilibrium admission rule and the added event audit.

| sigma | K0 | final horizon | nodes | largest independent dynamic residual | final-horizon change, years 0--500 |
|---|---:|---:|---:|---:|---:|
| 0.90 | 3.433644797858547 | 4815.8911 | 1740 | 1.626e-9 | 2.886e-8 |
| 1.00 | 4.649320432676148 | 4591.9184 | 1868 | 2.835e-9 | 3.756e-8 |
| 1.10 | 5.036956080779938 | 4591.9184 | 1959 | 3.180e-9 | 2.854e-8 |
| 1.50 | 5.504666888770259 | 2545.6692 | 2294 | 3.642e-9 | 1.517e-8 |

The dynamic maximum includes the dense first decade. First-order residuals
are below 1.5e-11. Terminal-coordinate gaps are below 2.5e-6. Both TVCs have
asymptotic log growth n-rho=-0.037. The high-substitution case passes both
Hamiltonian-support grids and the analytical continuation bound, despite
failing the stronger global-concavity test. Initial production/price log
gaps across activation are below 1.4e-15. Pre-event equations and the
event's real-resource reallocation identity are checked separately.

## Economic qualifications

No jump in output levels does not imply a smooth growth rate. Initial
output-per-person growth is 4.60%, 11.51%, 13.48%, 23.97%, respectively.
The price target still implies a rapid RSI response. The industry is already
large in the reference, and neither its size nor B0 is empirically fitted.

At sigma=1.50, consumption jumps 22.71%, M/Y is initially 9.32%, and
Pi/Y is -6.02%. Gross investment Y-C-U-M is -6.09% of output. The
model permits reversible one-good capital, so this requires disinvestment,
not only a financial transfer to the developer. A nonnegative-gross-investment
constraint would be a different equilibrium problem and was not added.

The data are numerical equilibrium approximations with analytical terminal
and optimality support, not interval-arithmetic proofs for arbitrary stocks.
The older paths remain intact in their own folders. The legacy switch was
compiled separately and restores the 99-page presentation without unresolved
references or overfull boxes.

## Document and regression checks

All 33 tests in the four suites listed above pass with the regenerated
checkpoints (no skips). On a fresh clone, the checkpoint-dependent test is
explicitly skipped until the untracked BVP files have been regenerated; the
replication driver reruns that test after solving.
The active PDF has 65 pages, with Section 6.1 starting on page 23. Both
editorial switch positions compile without unresolved references or overfull
boxes. The contents, parameter table, new figure pages, and numerical
appendix were rendered and inspected. The old data and figure files were
not modified.

The new JSON/CSV artifacts have Git line-ending conversion disabled in
`.gitattributes`: their byte-level provenance hashes must survive checkouts
on both Windows and Linux. This rule does not touch legacy artifacts.
