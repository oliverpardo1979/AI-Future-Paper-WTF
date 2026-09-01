# Rewrite plan: autonomous-AI benchmark

## Editorial anchor

**Central question.** How does the elasticity of substitution between AI
services and human labor shape economic growth, wages, interest rates, and the
functional distribution of income when frontier AI research is autonomous?

Every section, proposition, calibration, and figure must contribute directly to
this question. Material that does not help answer it belongs in the appendix, a
separate extension, or the current archival manuscript.

## Model scope

- The benchmark has autonomous AI research: \(\omega_H=0\).
- The benchmark formulation does not introduce \(H\), \(\omega_H\), or
  \(\sigma_{HM}\). These objects are not set to zero after being defined; they
  are absent from the benchmark.
- Human research is a possible later extension. It will enter this paper only
  if it changes or establishes the robustness of a central result.
- The notation, timing, and parameter meanings inherited from the current
  benchmark remain unchanged.
- A finite capability frontier is an equilibrium regularization and an
  analytical device, not a robustness exercise. The uncapped economy is studied
  only through an explicitly stated limiting argument.

## Logical order

1. Define population, labor productivity, preferences, and predetermined
   stocks.
2. Present final production and solve the competitive final-good firm.
3. Derive the static relationship between AI services and labor.
4. Present the integrated AI developer and explain the market structure.
5. Define AI production services, AI research services, and capability
   accumulation.
6. Solve the developer's pointwise service decision before deriving its dynamic
   conditions.
7. State the resource constraint, initial conditions, transversality
   conditions, and a self-contained equilibrium definition.
8. Derive results for \(\sigma_{XL}<1\), \(\sigma_{XL}=1\), and
   \(\sigma_{XL}>1\), in that order.
9. Present only numerical trajectories that satisfy the equilibrium-admission
   rule.

No condition from a later agent problem may be used to solve an earlier problem.
No balanced-growth restriction may be inserted into the definition of an
equilibrium trajectory.

## Proposed main-text results

| Order | Result | Current source | Status | Proposed location |
|---|---|---|---|---|
| 1 | Static effect of AI services on production labor and the wage | `prop:axm-ai-labor-comparative-static` | Proven | Model |
| 2 | Existence and uniqueness of the pointwise monopoly service choice | `prop:axm-monopoly-existence` | Proven under stated curvature conditions | Model; technical proof in appendix |
| 3 | Invariance of the finite capability domain and finite-horizon developer existence | `prop:axm-finite-cap-invariance` | Proven | Model |
| 4 | Checkable sufficient condition for global developer optimality with a finite frontier | `prop:axm-capped-developer-sufficiency` | Proven | Model; proof in appendix |
| 5 | Labor bottleneck when \(\sigma_{XL}<1\) | `prop:axm-complements` | Proven under regular limiting conditions | Equilibrium regimes |
| 6 | Local equilibrium existence near the complementary-input limit | `prop:axm-complement-local-existence` | Proven | Equilibrium regimes |
| 7 | Existence and analytical characterization of a positive-AI balanced-growth equilibrium when \(\sigma_{XL}=1\) | `prop:axm-benchmark-equilibrium-existence` | Proven for the autonomous benchmark | Equilibrium regimes |
| 8 | Local equilibrium trajectories around the unit-elastic balanced-growth path | `prop:axm-unit-saddle-path` | Proven | Equilibrium regimes |
| 9 | Two finite-frontier terminal regimes separated by \(\overline B_c\) when \(\sigma_{XL}>1\) | `prop:axm-capped-terminal-regimes` | Proven conditional on a regular frontier approach | Equilibrium regimes; central proposition |
| 10 | Local finite-cap equilibrium paths on both sides of \(\overline B_c\) | `prop:axm-capped-local-equilibrium` | Proven | Equilibrium regimes |
| 11 | No finite-rate balanced-growth path with unbounded capability when \(\sigma_{XL}>1\) | `prop:axm-no-bgp` | Proven conditional on \(B\to\infty\) | Equilibrium regimes |
| 12 | Finite-window limit as \(\overline B\to\infty\) and noncommuting long-run limit | `prop:axm-infinite-frontier-limit` | Proven; does not establish uncapped equilibrium | Equilibrium regimes |
| 13 | Global finite-cap equilibrium from the common initial stocks for a moderate frontier | `global_finite_cap_bvp_analysis.json` | Numerically admitted under the documented equilibrium rule | Quantitative equilibria |

## Results reserved for the appendix

- Interior research at every finite date.
- Research-curvature and coercivity arguments supporting \(\eta<\alpha\).
- The costate derivations and sufficiency proofs.
- Necessary restrictions on irregular gross-substitutes continuations.
- Finite-window continuation around \(\sigma_{XL}=1\).
- The complete BVP algorithm, residual reconstruction, horizon tests, and
  trajectory-admission audit.
- The conditional AI-dominated singular scaling, clearly labeled as a
  conditional result rather than an equilibrium trajectory.

## Material excluded from the new benchmark paper

- The human-research production function and all propositions whose assumptions
  require \(H\), \(\omega_H>0\), or \(\sigma_{HM}\).
- Numerical paths that solve canonical equations but fail developer optimality,
  transversality, admissibility, or an infinite-horizon continuation requirement.
- The large-frontier rejected candidate as a quantitative transition. Its
  failure may be mentioned only to delimit what has not been established.
- Any claim that the uncapped gross-substitutes economy has an equilibrium
  singularity. The existing result characterizes a conditional branch; it does
  not prove that an equilibrium reaches that branch.

## Planned figures and tables

The main text should contain at most the following items, subject to the
equilibrium-admission rule:

1. A diagram of the benchmark model and the feedback from capability to AI
   research services.
2. A figure illustrating the static substitution mechanism governed by
   \(\sigma_{XL}\).
3. A table of parameters, interpretations, values, and sources.
4. One figure comparing admitted equilibrium paths around unit elasticity.
5. One figure for the admitted finite-frontier gross-substitutes equilibrium,
   only if its trajectories add information beyond the propositions.
6. One compact table summarizing the three analytical regimes and their labor
   income-share implications.

## Writing sequence

1. Write and audit the benchmark model and the equilibrium definition.
2. Rewrite the analytical propositions in their logical order.
3. Decide which admitted numerical results materially clarify those
   propositions.
4. Write the quantitative section and algorithm appendix.
5. Write the introduction, literature review, abstract, and conclusion last.
