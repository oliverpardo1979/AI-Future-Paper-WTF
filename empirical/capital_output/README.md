# Initial capital-output ratios

This is an additional calibration check for *The Future of Growth and Human
Labor under Recursive AI Self-Improvement* (`main_rewrite.tex`), not a new
calibration or a change to the saved equilibrium trajectories.

## Reproduce

From the repository root, with the replication dependencies installed:

```text
python scripts/audit_rewrite_capital_output.py
python -m unittest discover -s tests -p test_rewrite_parameter_tables.py
```

The script reads the saved paths, recomputes their initial static production
and monopoly block, and checks `K/Y = alpha/(r + delta)` independently of the
stored ratio. It never runs a dynamic boundary-value solver. Results are in
`numerical_rewrite/initial_capital_output_audit.json`. The four entries in each
paper table are ordered by sigma: 0.90, 1.00, 1.10, 1.50. The financing
comparison instead reports its main and distant-stock configurations at 1.50.

To regenerate the empirical extract, download the official
[PWT 11.0 Stata file](https://dataverse.nl/api/access/datafile/554030) and run:

```text
python scripts/audit_rewrite_capital_output.py --pwt path/to/pwt110.dta
```

`source.json` records the download URL, source-variable definitions, retrieval
date and SHA256. The frozen extract keeps all 185 country rows in 2019, 2021
and 2023, including missing capital observations; missing is never set to zero.
There are no duplicate country-year keys. Five economies lack capital data
(Curacao, Guyana, Somalia, South Sudan and Sint Maarten). The 180-economy
comparison covers 99.95% of available PWT PPP output in 2023, not literally
every country in the world. Totals use the same valid countries in numerator
and denominator; ratios are ratios of sums, not unweighted country averages.

## Definitions and interpretation

- Model `K0/Y0` is the initial physical stock divided by the instantaneous
  output flow at an annual rate, hence measured in years. It is not a free
  structural parameter, an incremental capital-output ratio, or `K/(AL)`.
- The no-AI steady state implies `alpha/(rho + gamma + delta) = 3.30`.
  Its capital stock can be inherited by an AI economy without inheriting
  this ratio: output changes at the technology switch. The reported AI
  ratios use output **after** the switch, not the old Ramsey output.
- PWT `cn` is the capital stock at current PPPs; `cgdpo` is output-side GDP
  at current PPPs. Both are in millions of 2021 US dollars. `ck` is a
  capital-services index, not a stock, and is not used.
- PWT price levels `pl_n` and `pl_gdpo` convert these measures to current
  market-exchange-rate dollars. Thus the sample's current-price ratio is
  `sum(cn*pl_n)/sum(cgdpo*pl_gdpo)`. The PPP quantity comparison is
  `sum(cn)/sum(cgdpo)`. These answer different valuation questions.
- In 2023, the current-price sample ratio is 3.61 and the US ratio is 3.42;
  at current PPPs they are 4.72 and 3.24, respectively. In 2019 the sample
  ratios were 3.45 and 4.42. These are descriptive checks, not an acceptance
  interval or a claim that every country should have the same ratio.
- The Ramsey value is about 9% below the 2023 current-price sample ratio,
  but 30% below its PPP counterpart. The main illustrative AI ratios
  (2.29--3.14) are lower still. The low-efficiency Ramsey-start ratios
  (4.35--5.66) exceed the current-price benchmark because output initially
  falls when the production weights change. No parameters have been changed.
- PWT's heterogeneous produced assets, their relative prices and national
  accounts treatment of R&D/inference expenditure do not map exactly onto
  the one-good model. PWT does not measure the model's AI efficiency stock B.
  The model's instantaneous initial flow also differs from measured output
  averaged over a full calendar year, particularly during a rapid transition.
  These limitations prevent claiming an exact empirical calibration.
- Cooley and Prescott (1995, p. 21) use 3.32 annually, but their capital
  concept is broad, including land, inventories and consumer durables and
  imputed service flows in output. This is a literature reference, not an
  identical definition to PWT or the present model.

## Sources

- [Penn World Table 11.0](https://doi.org/10.34894/FABVLR), downloaded
  September 14, 2026; CC BY 4.0. Attribution: Feenstra, Inklaar and Timmer
  (2015), *The Next Generation of the Penn World Table*, AER 105(10),
  3150--3182, [DOI](https://doi.org/10.1257/aer.20130954). Appendix C explains
  the capital-stock price conversion; the Stata file supplies current labels.
- Cooley and Prescott (1995), *Economic Growth and Business Cycles*, in
  *Frontiers of Business Cycle Research*, pp. 1--38;
  [chapter](https://faculty.econ.ucdavis.edu/faculty/kdsalyer/LECTURES/Ecn200e/cooley_prescott.pdf).

The public paper is available through the repository's stable
[PDF](https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/the-future-of-growth-and-human-labor-under-recursive-ai-self-improvement.pdf).
