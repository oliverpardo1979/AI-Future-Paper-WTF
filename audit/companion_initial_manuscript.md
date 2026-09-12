# Initial companion manuscript audit -- 2026-09-12

## Authorized scope

Create an independent paper in the same repository with the approved title
**How Much Can Recursive AI Self-Improvement Raise Economic Growth?** Import
useful documented parameters, prepare sensitivity analysis, and cite it in
Section 4.3 of the original paper. Preserve the original Appendix C, protected
title/abstract/introduction, and existing simulation code and results.

## Delivered source

- `main_companion.tex` and six files under `sections_companion/`: independent
  11-page first draft, with a model, equilibrium definition, BGP construction
  and global-optimality proof, parameter provenance, analytical derivatives,
  and explicit remaining empirical work.
- `COMPANION.md` and README entries: compiling, provenance, replication checks,
  and research plan. No new transition simulations or empirical estimates.
- `references.bib`: reciprocal working-paper citations with clickable permanent
  PDF links. The original's citation is on page 18 (Section 4.3); its
  bibliography entry is on page 63.
- Pages workflow: compiles both entry points and copies both PDFs to separate
  stable paths. The original URL is unchanged.

## Mathematical and editorial checks

The construction is adapted from the original Appendix C, not a new model.
The household and firm problems precede the developer and equilibrium block.
No BGP restrictions enter the definition of an equilibrium trajectory.
The proof constructs BGP initial stocks; it does not assert existence from
arbitrary fixed stocks. Both TVCs and both agents' global optimality are proved.
The eta<alpha condition is retained for comparability and explicitly identified
as unnecessary for this particular unit-elastic proof.

The initial parameter table is taken from the current rewrite, not the obsolete
`numerical/calibration.csv`. The AI parameters are illustrative, n and gamma
are long-run approximations, and rho is a preference calibration. The capped
chi timing target is not treated as an estimate for the uncapped model.

The editorial review separated demonstrated results, illustrative calculations,
and planned empirical work. It removed no material from the original appendix.
The new document makes no claim to have identified the causal effect of recursion
or calibrated the world economy from data.

## Executed verification

The following test suites passed together: 29 tests.

```text
test_companion
test_rewrite_proposition_structure
test_rewrite_uncapped_unit
test_positive_ai_branch
```

They check local labels and references, calibration provenance, dated analytical
equilibrium residuals, baseline calculations, analytic derivatives versus finite
differences, chi invariance of rates and ratios, proof structure, and publication
paths. Finite differences are numerical derivative checks, not sensitivity
scenarios or additional equilibrium-existence assumptions.

Both manuscripts compiled with Tectonic 0.16.9. Final logs have no undefined
references, duplicate labels, overfull boxes, or underfull boxes. The existing
Fontconfig environment warning does not affect rendering.

All 11 companion pages were rendered with Poppler and visually inspected.
Original pages 18--19 and 63--64 were inspected after the citation update.
The parameter-column width was corrected after the first compile. PDF annotation
inspection verified reciprocal external links to the intended permanent URLs.

`git diff --exit-code` confirmed no changes to `main_rewrite.tex`, its
introduction, literature or model sections, the original uncapped appendix and
proof file, or `scripts/define_positive_ai_branch.py`.

## Remaining work

Empirical identification/mapping, defensible AI-parameter ranges, numerical
sensitivity tables and figures, and a separately solved no-recursion
counterfactual remain pending. The first draft contains an illustrative
closed-form calculation, not a completed empirical paper or new transition paths.
Remote publication is verified separately from these local build checks.
