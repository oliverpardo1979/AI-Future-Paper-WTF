# Research expenditure calibration diagnostic (2025 US proxy)

Companion data for [The Future of Growth and Human Labor Under Recursive AI
Self-Improvement](https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/the-future-of-growth-and-human-labor-under-recursive-ai-self-improvement.pdf),
compiled from `main_rewrite.tex`, subsection "An approximate calibration to
research expenditure". The author accepted the discrepancy and requested
publication of the already-verified **sigma=1** simulation. Its CSV, figure
metadata and approximate-calibration record are in `published_unit/`.
The two existing RSI comparisons and the original search are preserved.
The high target was not matched exactly; no four-elasticity comparison is claimed.

## Result (September 14, 2026)

Keeping all non-chi parameters and initial stocks fixed, the numerical branch
examined at sigma=1 has a local maximum of first-year research expenditure
near chi=81.08480943. The annual ratio is **0.321497%**, versus the empirical
proxy of **0.356218%**: a shortfall of 0.034720 percentage points, or 9.7469%
relative to the target. It is not a successful exact calibration.

The local-peak path passed the original equilibrium checks, two 500-year
horizon extensions, independent original-equation residual checks, the
developer's global concavity check, terminal/TVC continuation checks and dense
early-window checks. The annual moment changed by 4.44e-10 in log terms after
refinement; its 64/128-node quadrature discrepancy was 5.44e-15. These errors
cannot account for the target shortfall. This is numerical verification, not
a new theorem about global existence or uniqueness.

| Unit-elastic case | chi | First-year M/Y | Second-year M/Y | Price fall over 27 months |
|---|---:|---:|---:|---:|
| Existing half-price-decline calibration | 7.6163 | 0.1829% | 0.1635% | 40.0% |
| Existing full-price-decline calibration | 36.8307 | 0.3015% | 0.2250% | 80.0% |
| Verified local peak of the annual research moment | 81.0848 | 0.3215% | 0.2114% | 90.6% |

Every annual entry is a ratio of integrals over its own year. The old two
paths are unchanged; `published_comparison.json` measures their research
shares and records their admitted checkpoint hashes. At the new local peak,
instantaneous M0/Y0 is 0.4521%, which must not be substituted for annual M/Y.

The broad candidate search used chi from 0.179725 to 368.0768. It found a
turning point and declining annual expenditure beyond the peak. The BVP
failed at 368.0768 (singular collocation Jacobian); that point is recorded as
missing numerical evidence, not zero expenditure or proof of nonexistence.
The result is local to the examined branch and initial conditions. There is
no proof that a disconnected branch or different initial stocks could not
match the target. Full four-regime export is deliberately withheld.

Economically, higher research productivity need not raise expenditure over
a fixed year monotonically. Faster efficiency improvement changes the
amount and timing of raw compute needed, the value of future improvements,
and output in the denominator. The numerical paths show substantial
front-loading of research. A high expenditure target therefore does not by
itself give a smoother or slower transition. A nearby 0.30% target would
largely reproduce the already-published fast price-calibrated case; it would
not establish a match to the growth of observed research expenditure.

## Target and interpretation

At sigma=1, fit constant post-activation chi to
`integral_0^1 M(t) dt / integral_0^1 Y(t) dt = 109.58 / 30762.099`.
The numerator is the 2025 US training/research compute expenditure estimate
in Korinek and McKelvey (2026), Table 3, in billions of current dollars;
the denominator is BEA nominal annual GDP (FRED series GDPA), same units/year.
This is approximately **0.356%**, not 35.6%, not instantaneous M0/Y0,
and not the arithmetic mean of the expenditure share. It is the higher
dated estimate, not an upper confidence bound or a directly observed RSI total.
Sources: [Korinek and McKelvey, Table 3](https://www.piie.com/sites/default/files/2026-05/wp26-9.pdf),
[methodological appendix](https://www.piie.com/sites/default/files/2026-05/wp26-9-appendix.pdf),
and [BEA nominal GDP via FRED](https://fred.stlouisfed.org/data/GDPA), accessed
September 14, 2026. Metadata and qualifications are in `feasibility_diagnostic.json`.

All other parameters and initial stocks are identical to `../rsi_activation/`.
The published path uses sigma=1, omega_X=0.10, eta=0.20, B0=0.01*Bbar,
Bbar=1.10 times the sigma=1.50 threshold, and a fixed-efficiency pre-RSI BGP
with K0/Y0=3.30. RSI activates unexpectedly. Only K0 and B0 are inherited;
C0, q0 and M0 are solved endogenously. The selected chi is 81.08480942910101.
The other three elasticities have not been simulated at this chi. There is no price target.

## Run

Install the root `requirements-rewrite.txt`, then from the repository root:

```text
python scripts/calibrate_rewrite_research_share.py --publish-unit
python -m unittest discover -s tests -p test_rewrite_research_share.py -v
```

`--publish-unit` recreates the selected candidate if needed, repeats both
horizon extensions, equilibrium verification and activation checks, then
exports only sigma=1 using the paper's existing figures. Dotted lines are
the **unit-elastic** analytical limits, not sigma=1.50 reference lines.
The separate `published_unit/calibration.json` records author acceptance,
the empirical shortfall and the unchanged numerical tolerances, binding
the checkpoint, CSV and displayed figures with SHA-256 hashes.

To reproduce the original search or compare the old price calibrations:

```text
python scripts/calibrate_rewrite_research_share.py --diagnose
python scripts/calibrate_rewrite_research_share.py --verify-peak
python scripts/calibrate_rewrite_research_share.py --compare-published
python -m unittest discover -s tests -p test_rewrite_research_share.py -v
```

The comparison command requires the existing published-price checkpoints;
reproduce those first using the root `REPLICATION.md` if they are absent.
All BVP checkpoints are reproducible, ignored cache files, not pickled objects.
`--diagnose` records candidate points and solver failures, then uses a bounded
local maximization between the best grid point's neighbors. The log-chi peak
tolerance is 0.002 (about 0.2% in chi), sufficient to resolve the broad peak;
it does not loosen the fit or equilibrium tolerances. Search metadata and all
trial hashes are saved, and failed solves are never assigned an objective value.

`--calibrate-only` searches the increasing low-chi branch and stops with an
explicit error when it turns below the target. It does not silently substitute
a lower target. The optional fitted workflow (`--sigma`, then `--finish`)
remains gated on a matching `calibration.json`; it has not been completed for
this target. It reuses the existing positive-AI BVP, without claiming global
monotonicity or parameter identification. Trial
checkpoints are candidates, not admitted equilibrium trajectories.
Gauss-Legendre quadrature with 64 and 128 nodes checks the ratio of integrals;
the log discrepancy must be below 1e-8. The root tolerance in log chi is 2e-6,
and the final log moment error must be below 2e-5 after horizon refinement.
These numerical errors are much smaller than the empirical proxy's precision.

The original `run` and shared `finish` functions retain both horizon extensions,
original-equation residuals, developer optimality/support, TVC continuation,
early-window checks and event audit. The **exact-fit four-regime workflow**
does not export unless all four scenarios pass and the refined annual target
matches. The author-approved approximate publication is a separate command
with one verified path, not a bypass of equilibrium gates. None of the older
simulation folders is overwritten. A completed fit would produce
`annual_moments.json` and four-regime figures, but these files are intentionally
absent. `peak_verification.json` records the separate, admitted diagnostic
path used in the new subsection; it must not be described as matching the target exactly.

## Test status

After adding the subsection, the publication, research-moment, existing RSI,
price-calibration, finite-frontier and simulation-design suites ran 59 tests:
58 passed, none failed and the exact four-regime-fit test was skipped.
The full `test_rewrite*.py` suite ran 142 tests: 136 passed, the same five
pre-existing editorial assertions failed, and one test was skipped. Four new
publication tests verify the declared one-regime scope, explicit empirical
discrepancy, unchanged admission checks, correct unit-elastic limits and
SHA-256 bindings between verification, CSV data and the displayed figures.

Before publication, the full `test_rewrite*.py` suite ran 138 tests: 132 passed, five failed and
one was skipped. All ten executed research-share tests passed. The skipped
test requires a completed four-regime target fit, which does not exist.
All 17 existing RSI activation/half-decline tests passed.

The five failures concern manuscript wording and a source parser that counts
both branches of the legacy LaTeX switch. Re-running those tests against
manuscript sources at the pre-edit commit `f7ec991` reproduced the same five
failures. No manuscript wording was restored or changed to satisfy obsolete
text assertions. `test_results.json` records the tests and baseline recheck.
