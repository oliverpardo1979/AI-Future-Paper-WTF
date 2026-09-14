# Joint calibration: sector size, prices, and research expenditure

This is a separate calibration workstream for `main_rewrite.tex`, **The Future
of Growth and Human Labor under Recursive AI Self-Improvement**. None of the
existing paper sections, figures, parameters, or simulation exports is replaced.
The paper and its replication entry point remain linked in the repository's
[main replication guide](../../REPLICATION.md).

## Current decision

Keep eta = 0.20. Treat sigma and the finite upper bound on B as scenarios, not
estimated parameters. Start with a conditional calibration at sigma = 1 using
two references: AI-service revenue relative to output and the decline in the
quality-adjusted price of services. B0/Bbar = 0.01 remains an assumption, not an
estimate. The household's initial consumption and developer's shadow value are
selected by the existing BVP.

The first reference is **US sector intensity**, not a measured world total.
The macro parameters retain the global paper's values; this is not a full US
calibration either. This reference is preferable to combining a selective list
of worldwide company revenues with world GDP and treating it as industry
coverage. A worldwide calibration remains the intended scope, subject to a
comparable revenue series.

## Sources and comparability

1. **AI-service revenue.** Table 13 of the [technical appendix to Measuring the
   AI Economy](https://www.piie.com/sites/default/files/2026-05/wp26-9-appendix.pdf)
   reports US estimates of USD 27.69, 67.84 and 164.38 billion for 2023, 2024 and
   2025. These are imputed, not audited consolidated industry sales. Section 7.3
   assumes inference uses half of compute spending and revenue is 1.5 times
   inference spending. The global chip-based growth estimates elsewhere in the
   appendix must not be confused with these US revenue levels.
2. **GDP denominator.** [World Bank indicator NY.GDP.MKTP.CD](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations=US), same country and
   year, current US dollars. The downloaded response includes both USA and WLD
   so the code can explicitly select USA; it never divides US revenue by world
   GDP. The source vintage is preserved in the JSON response.
3. **Prices.** [OECD Figure 2](https://www.oecd.org/en/publications/artificial-intelligence-markets_d531d73f-en/full-report.html)
   reports a nearly 80% decline from January 2024 to April 2026. The fit rounds
   this to p(2.25)/p(0) = 0.20, as in the existing exercise. It is a broad cloud
   API index, not a US-only fixed-task price. Holding the final-good price
   constant is an approximate numeraire mapping. Competition, hardware, human
   research and changing task intensity are not separated. Matching this moment
   does not estimate pure monopoly RSI productivity or establish how rapidly a
   real monopoly would reduce prices.
4. **Company revenues and compute.** [Epoch AI's dataset](https://epoch.ai/data/ai-companies)
   helps examine reporting definitions and spending composition. Coverage is
   selective; full-company and product revenues, annual revenue and annualized
   run rates cannot be added indiscriminately. Many underlying financial sources
   are media reports rather than public audited accounts. In particular, the
   2024 OpenAI research-cost observation is a projection that combines training
   with amortized research expense. It is not an independently verified current
   expenditure flow M. Report-before-period-end dates are flagged automatically.

The snapshots in `sources/` were downloaded on 14 September 2026. Epoch data
are credited to Josh You, John Croxton, Venkat Somala and Yafah Edelman and are
distributed under the source's CC BY license. Do not interpret the source's
`Confident` label as our verification of an audited amount. The original sources
and source notes remain in the snapshots; hashes are in `source_audit.json`.

The revenue moment concerns a year, whereas the model starts with instantaneous
flows. At sigma=1, the revenue/output ratio is constant, so it also equals the
ratio of integrated annual flows. That shortcut does **not** extend to other
sigma values: a later conditional fit must use the correctly dated integrated
revenue/output moment, rather than silently treating an annual value as a
date-zero observation. Model time zero is a stylized technology-switch date,
not a claim that the United States had no AI in January 2024.

Y is final-good-sector output in the model. Using GDP is an external calibration
convention; exact national-account treatment of intermediate inference and
capitalized research requires a separate reconciliation before claiming a
literal measured industry share.

## What the data currently imply

The US reference is about 0.232% in 2024. At sigma=1, the model implies

    pX X / Y = (1-alpha) omega_X.

Consequently omega_X is about 0.003456, rather than 0.10 or 0.20. This is a
conditional mapping from an estimated US reference, not an identified global
technology weight. The comparison across 2023--2025 describes changing US
sector intensity; it does not license choosing three different years as a
statistical confidence interval. Constant weights at sigma=1 cannot reproduce
the whole rising revenue-share series.
The year 2024 aligns the size reference with the beginning of the price
window; it is not selected to improve the numerical fit.

Positive monopoly marginal revenue requires e_X < 1. For sigma < 1 this gives

    pX X / Y > (1-alpha)(1-sigma)/(1-alpha sigma).

Thus sigma=0.90 and sigma=0.99 cannot reproduce the 2024 reference in this
model, whatever chi, B0 or omega_X. Passing this necessary test at sigma=0.999
or above does not prove that a joint dynamic calibration exists. Existing
illustrative paths remain unchanged and valid within their stated scope.

At sigma=1 the model also implies

    U / (pX X) = (1-alpha) omega_X = pX X / Y.

The source's assumed inference/revenue ratio (two thirds) cannot simultaneously
match the model's small revenue/output share. This is a structural/proxy
incompatibility, not something an optimizer can repair by changing chi or B0.

## Executed conditional fits

All three fits below passed the existing equilibrium-admission checks on
14 September 2026. They keep sigma=1, eta=0.20, the paper's macro parameters,
and no-AI Ramsey initial capital. Each matches the revenue/output reference
of 0.23155% and the cumulative price ratio of 0.20; omega_X=0.00345599312
in every row. Research expenditure is a prediction, not a fitted target.

| Upper bound on B | B0 / upper bound | Fitted chi | Initial M / AI revenue | Record |
|:--|--:|--:|--:|:--|
| 170.124 | 1% | 26.1443 | 0.17842% | [Baseline](../../numerical_rewrite/joint_us_proxy/1351533afdbe/calibration.json) |
| 1360.992 | 1% | 137.8757 | 0.17826% | [Higher bound](../../numerical_rewrite/joint_us_proxy/4e46d39c591e/calibration.json) |
| 170.124 | 10% | 269.7145 | 0.12083% | [Initial-efficiency check](../../numerical_rewrite/joint_us_proxy/db484dc0d890/calibration.json) |

The first and third rows show that the two references do not distinguish B0
from chi, even at the same upper bound. The third row is a separate
identification diagnostic; it does not replace the assumed 1% starting point.
The two upper bounds likewise remain alternative scenarios, not estimates.
Full values, search trials and admission reports are stored beside each
record. Raw solution checkpoints remain in the ignored cache and are
regenerated by the commands below.

The final horizons extend to about 4,592 model years to check the long-run
conditions; they are not forecasts of a transition date. Across the three
fits, independent early-window ODE residuals are below 3.1e-9, the maximum
change on the common 500-year window after the second extension is below
3.7e-8, and terminal coordinate gaps are below 3.5e-6. The developer's
concavity checks pass and both asymptotic transversality growth rates are
-0.037. The eight new tests and nine existing price-calibration tests pass.
These are numerical checks of the existing equilibrium construction, not
a claim that matching two moments establishes empirical validity.

In particular, every fit predicts inference spending of only 0.23155% of
AI revenue, and very small initial research spending. This warrants resolving
the model-to-data cost comparison before presenting the fits as a realistic
calibration of the current industry. Confidence in the empirical mapping is
**Medium**: the revenue estimate is imputed, the price index is not US-only,
and the cost definitions do not coincide exactly with the model. The present
paper text, PDF and earlier simulations are unchanged.

## Research expenditure and identification

Do not fit B0 to the two-thirds training/revenue ratio in the PIIE construction:
that ratio follows from its assumed inference/training split and markup. It is
not independent evidence. Do not substitute total data-center capex for M or
treat training performance scaling exponents as eta without an economic mapping.

At sigma=1, size fixes omega_X. Conditional on eta, Bbar and B0, a root search
fits chi to the price change. If B0 is also free, two moments cannot generally
identify all three parameters. The executed B0 check above illustrates this
directly. A wider profile can examine how research expenditure changes along
the equally well-fitting candidates. An independently measured research
moment may discriminate among them.
An annual expenditure observation must be compared with the integrated model
flow over the same year, not with the initial instantaneous M/Y reported in
the diagnostic files.

Before claiming even local identification, evaluate the log-moment Jacobian
with respect to log(omega_X), log(chi), and log(B0) using independently admitted
equilibria at every perturbed point. `local_log_sensitivity` reports singular
values at three finite-difference steps. Stable non-negligible singular values
are needed; the number of moments and the floating-point rank alone are not
evidence of economic identification. Also search for multiple parameter fits.

## Reproduction and safeguards

From the repository root:

```text
python scripts/calibrate_rewrite_joint_moments.py
python scripts/calibrate_rewrite_joint_moments.py --fit
python scripts/calibrate_rewrite_joint_moments.py --fit --frontier 1360.9921392415592
python scripts/calibrate_rewrite_joint_moments.py --fit --initial-fraction 0.1
python -m unittest discover -s tests -p test_rewrite_joint_moments.py
```

The first command only rebuilds the source and structural audit. The fits use
the original finite-cap BVP, two horizon extensions, independent equation and
FOC residuals, developer optimality and transversality checks. Root and
admission tolerances match the prior price-calibration implementation. Fitting
trials are **candidates**, not equilibrium trajectories. No trial is plotted.
Only an admitted final solution contributes numerical moments to a calibration
record. Outputs use new fingerprinted directories in
`numerical_rewrite/joint_us_proxy/`; caches are separate and ignored by Git.

No elasticity other than one is dynamically fitted by this first-stage script.
The source audit screens all proposed elasticities before any such extension.
The upper bounds are kept at the two existing scenario levels, not raised to
force AI domination after reducing omega_X.

For a later comparison at other elasticities, distinguish two questions.
Holding the unit-calibrated omega_X and chi fixed isolates a change in sigma,
but no longer holds the empirical sector-size and price targets fixed.
Refitting omega_X and chi separately for each sigma compares differently
calibrated economies. Neither exercise should be described as the other.

The source audit also records stress tests of the existing static solver.
Very small weights with sigma below one can place marginal revenue so close
to zero that floating-point evaluation either raises an error or returns a
large FOC residual. In the recorded grid, this affects omega_X=0.001 at
sigma=0.90, 0.99 and 0.999, and the unit-fit weight at 0.90 and 0.99. These
points are not accepted solutions. The first two elasticities already fail
the analytical sector-size screen. The issue must nevertheless be resolved
before any dynamic fit uses an affected point; this workstream does not
change the existing solver or loosen its residual gates. The sigma=1 fits
do not use this near-boundary root calculation.
