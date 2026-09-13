# Uncapped unit-elastic appendix: recovery and validation

Date: 2026-09-12.

Subsequent update (2026-09-13): the historical restriction eta <= 1/2
was removed from the current unit-elastic proposition and seed guard.
The new proof uses eta<alpha in its transformed-concavity branch.
See `audit/rewrite_ramsey_proof_extensions.md` for the current scope and tests;
the record below describes the original recovery.

## Scope and sources

The added Appendix C studies the autonomous-research economy with sigma=1
and no finite efficiency frontier. It replaces psi(B) by 1 only for this
appendix. The finite-frontier model, simulations, parameters, and figures
are unchanged. The title, abstract, and introduction are unchanged.

Recovered sources:

- `sections_axm/03_model.tex`: `prop:axm-benchmark-equilibrium-existence`,
  its constructive proof and comparative statics, and `prop:axm-unit-saddle-path`.
- `sections_axm/appendix.tex`: the proof of `prop:axm-unit-saddle-path`.
- `scripts/define_positive_ai_branch.py`: the preserved exact BGP and
  normalized equilibrium system. This implementation was not modified.

The new text uses the current gamma, sigma, and psi notation, with no human
research variables. It distinguishes the BGP from nearby off-BGP equilibrium
trajectories and does not assert existence from arbitrary initial stocks.
The feedback restriction eta+omega_X<1 is necessary for the constructed
positive finite-rate BGP. The separate curvature conditions are sufficient
for global optimality, not claimed to be necessary for equilibrium existence.
The historical eta<alpha restriction is retained but explicitly not used
separately in the construction.

## Placement

- Results: `sections_rewrite/appendix_uncapped_unit.tex`, included after the
  existing appendices by `main_rewrite.tex`.
- Proofs: `sections_rewrite/appendix_uncapped_unit_proofs.tex`, included within
  the existing single Proofs section. Each proof names its proposition through
  an automatic reference; there are no additional proof subsections.
- A fourth paragraph at the end of Section 4.3 refers to Appendix C and states
  the contrast with the finite-frontier regimes.

## Reproducible checks

From the repository root, with the replication Python dependencies installed:

```powershell
python -B -c "import sys,unittest; sys.path[:0]=['.python-packages','tests']; names=['test_rewrite_proposition_structure','test_rewrite_uncapped_unit','test_positive_ai_branch']; result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(names)); sys.exit(not result.wasSuccessful())"
```

Result: 23 tests passed. No transition solver was run and no simulation data
were exported. The new tests independently reconstruct the appendix's initial
levels, growth rates, dated equilibrium conditions, objective values, both
TVC decay rates, and Jacobian. They use four positive AI weights, both the
historical and current research productivities, and one configuration on the
eta=1/2 concavity boundary. All dated checks use the original equations and
are evaluated at years 0, 25, and 200. Algebraic relative tolerances of
5e-11 or tighter account for floating-point arithmetic; they do not replace
the analytical proof or alter an equilibrium condition.

The calibrated Jacobian has two negative and two positive eigenvalues,
approximately (-0.098971, -0.003194, 0.040391, 0.149290). The absolute state
projection determinant is 0.6036533882 for unit-length eigenvectors, which
rounds to the manuscript's 0.6037. The preserved solver orthonormalizes the
stable basis and obtains 0.6037895017 instead. A first test incorrectly
compared these two basis conventions; the final test compares like with like
and verifies nonsingularity for both. No model or solver change was needed.

## PDF validation

Compiled `main_rewrite.tex` with Tectonic, keeping logs and intermediates.
The final log contains no overfull/underfull boxes or unresolved/duplicate
references. Visual inspection covered page 18 (Section 4.3), pages 50--53
(new proofs and transition to the existing algorithm appendix), and pages
57--61 (Appendix C and transition to the bibliography). The PDF has 64 pages;
Appendix C occupies pages 57--60 and its proofs pages 50--52.

This validation checks the published expressions against the preserved code.
The local existence conclusion rests on the stated stable-manifold and global
optimality argument, not on numerical eigenvalues alone. Nothing here proves
uncapped equilibrium existence or nonexistence for sigma>1.
