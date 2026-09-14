# Lower research-expenditure calibration

This folder reproduces subsection 6.3 of [The Future of Growth and Human Labor
Under Recursive AI Self-Improvement](https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/the-future-of-growth-and-human-labor-under-recursive-ai-self-improvement.pdf),
compiled from `main_rewrite.tex`. It replaces the displayed 2025-proxy exercise;
the old results remain in `../rsi_research_share_2025/` and their text in
`sections_rewrite/preserved/`. Other subsections are unchanged.

## Target and interpretation

The lowest of the three dated proxies discussed is US 2023:
18.46 / 27811.517 = 0.0006637537967, or **0.0663754% of GDP**.
The numerator is training/research compute expenditure in billions of current
USD in [Korinek and McKelvey (2026), Table 3](https://www.piie.com/sites/default/files/2026-05/wp26-9.pdf).
The denominator is 2023 BEA nominal annual GDP via [FRED GDPA](https://fred.stlouisfed.org/data/GDPA),
accessed September 14, 2026. Their [methodological appendix](https://www.piie.com/sites/default/files/2026-05/wp26-9-appendix.pdf)
explains rental-equivalent costs and the assumed 50% research/training share.
This is neither directly observed autonomous RSI spending, a global total,
nor a lower confidence bound. It is a historical proxy, not a current estimate.

The model moment is the ratio of integrals over the first year, not
instantaneous M0/Y0 or the average of instantaneous shares. Chi=1.4378 is
the archived low-chi-branch candidate closest to the target. It yields
**0.0637427%**, a **0.2633-basis-point** shortfall (3.97% relative).
The author allowed a few basis points; the publication gate is stricter,
at one basis point. This is an empirical-fit allowance, not solver tolerance.
No exact parameter identification or global monotonicity is claimed.

## Unchanged economic design

Only chi changes relative to the formerly displayed research calibration.
Sigma=1, omega_X=0.10, eta=0.20, alpha=0.33, delta=0.05, rho=0.04,
n=0.003, gamma=0.01, A0=N0=1; Bbar=1360.9921392415592;
B0=13.609921392415593 and K0=4.649320432676148.
The initial economy is the existing-AI fixed-B BGP with K0/Y0=3.30.
Research is unavailable before unexpected RSI activation. Stocks and
production prices/quantities remain continuous; C0, q0 and M0 are re-solved.
No other elasticity is exported for this calibration.

## Reproduction

Follow the environment setup in the root [replication guide](../../REPLICATION.md), then run:

```text
python scripts/calibrate_rewrite_research_share_low.py
python -m unittest discover -s tests -p test_rewrite_research_share_low.py -v
```

The script selects from the preserved high-target diagnostic, verifies the
candidate hash when its cache exists, or solves it again when absent. It
reuses the original positive-AI BVP, extends the horizon twice by 500 years,
checks original equations independently at two difference steps on both
the full and early windows, verifies developer optimality and terminal/TVC
continuation, and checks event continuity. The empirical target never
replaces any of these gates. Quadrature uses 64/128 nodes with a 1e-8 log
agreement threshold; the moment must remain stable to 2e-5 in logs across
the horizon refinements. Export is refused if any admission gate fails.

Final horizon: 5579.8 years, 888 mesh points. The maximum independent
dynamic residual is below 1.06e-9, the final common-window coordinate
change below 3.74e-8, and the annual-moment log change below 3.44e-8.
The first-year share is 0.0637427%, second-year share 0.0620367%, and
the untargeted 27-month price decline is 8.96%. Initial output-per-person
and wage growth are 1.2250% (instantaneous annual rates). At year 500,
B/Bbar is only 0.4599; the displayed window is not the terminal boundary.

`calibration.json` records sources, approximate fit, settings and hashes.
`sigma_1_00_audit.json` and `activation_audit.json` record numerical checks.
`equilibrium_paths.csv` supplies the three displayed figure groups, with
analytical limits and SHA-256 bindings in the manifests. The figures use
the previous variables and two windows (-2 to 10; 10 to 500 years).

## Regression checks (September 14, 2026)

All six new low-target tests passed. Combined with the preserved high-target
tests, 20 passed and the unfinished exact-fit four-regime test was skipped.
The full `test_rewrite*.py` suite ran 148 tests: 142 passed, one was skipped,
and the same five pre-existing manuscript-wording/parser assertions failed.
Those baseline failures are documented in the preserved high-target folder;
no approved analytical text was changed to satisfy them.
