# How Much Can Recursive AI Self-Improvement Raise Economic Growth?

Oliver Pardo, September 2026. Initial companion working paper.

## Files and scope

Compile `main_companion.tex` **from the repository root**. Do not change the
main file of the original paper: it remains `main_rewrite.tex`.

```text
tectonic --keep-logs --keep-intermediates --outdir output/pdf main_companion.tex
```

Both manuscripts use `references.bib`; neither includes the other's source
sections. The original Appendix C is preserved. The mathematical source is
`sections_rewrite/appendix_uncapped_unit.tex` and its proof file, at repository
commit `2e25ff25c4524e89931dff7e37666d9b55259591`. The companion restates the
BGP construction with its own equation and proposition labels. It refers to
the existing local-trajectory theorem without claiming global existence from
arbitrary initial stocks.

## Parameter provenance

The source for inherited values is the **current** table in
`sections_rewrite/05_quantitative_equilibria.tex`, not legacy
`numerical/calibration.csv` (which contains obsolete population and research
parameters from a different model).

| Parameter | Reference | Status |
|---|---:|---|
| alpha | 0.33 | One-third benchmark |
| delta | 0.05 | Annual depreciation benchmark; PWT comparison |
| rho | 0.04 | Preference calibration |
| n | 0.003 | Constant approximation based on UN 2024--2100 projection, not an infinite-horizon demographic forecast |
| gamma | 0.01 | Illustrative labor-augmenting trend, not a direct OECD estimate of this model's A |
| omega_X | 0.20 | Illustrative AI production weight, not revenue share |
| omega_L | 0.80 | Defined as 1 - omega_X |
| eta | 0.20 | Illustrative research elasticity, not estimated |
| sigma | 1 | Maintained scope, not an empirical calibration |
| chi | Any positive value | BGP rates and shares are independent of it; levels are not |

The finite-frontier value chi=1.4378 was chosen for transition timing. It is
not imported as an empirical research-productivity estimate. The preserved
analytical code defaults to chi=0.01; tests may use either value to verify
rate/ratio invariance, not to claim level calibration.

## Reproducibility and current limitations

No new transition solver, empirical estimates, or sensitivity grid is produced
by this initial draft. `scripts/define_positive_ai_branch.py` remains unchanged.
It computes the analytical BGP and dated canonical residuals; the global
optimality proof, rather than a residual tolerance, establishes equilibrium.

Run the new companion checks and the existing analytical checks from the root:

```text
python -m unittest discover -s tests -p test_companion.py
python -m unittest discover -s tests -p test_rewrite_uncapped_unit.py
python -m unittest discover -s tests -p test_positive_ai_branch.py
python -m unittest discover -s tests -p test_rewrite_proposition_structure.py
```

Install the existing `requirements-rewrite.txt` in a suitable environment if
needed. Tests check references, parameter provenance, the reference growth
calculation, analytic sensitivity, and sufficient-condition boundaries.
Finite-difference tolerances are arithmetic checks, not new economic assumptions.

The illustrative annual growth rate is 0.0108666666667 and the net return is
0.0508666666667. The growth premium over gamma is 0.0866666667 percentage points.

## Next substantive work

1. Map evidence on algorithmic efficiency and research compute to B, dot B,
   and M. Separate human research, data, hardware, and AI research contributions.
2. Identify defensible ranges for eta and omega_X rather than choose them to
   deliver a desired growth forecast. The historical research equation is not
   automatically causally identified because M is endogenous.
3. Evaluate joint AI-parameter sensitivity only under the proposition's
   sufficient conditions. Report growth, wages, interest, and research shares.
4. Vary n and gamma separately; assess their long-horizon interpretation.
5. To isolate recursion, specify and solve a counterfactual retaining AI in
   production but removing B from research productivity. This is not yet done.
6. Before off-BGP figures, select explicit initial stocks and verify the entire
   equilibrium trajectory, both TVCs, and global optimality. A BGP comparison
   is not a transition or evidence of equilibrium from arbitrary initial stocks.

## Publication

The shared Pages workflow builds both entry points, leaving the original
public paper URL unchanged. The companion has a separate permanent PDF path:

https://oliverpardo1979.github.io/AI-Future-Paper-WTF/paper/how-much-can-recursive-ai-self-improvement-raise-economic-growth.pdf
