# Rewrite plan: autonomous-AI benchmark

## Editorial anchor

**Central question.** How does the elasticity of substitution between AI
services and human labor shape economic growth, wages, interest rates, and the
functional distribution of income when frontier AI research is autonomous?

Every section, proposition, calibration, and figure must contribute directly to
this question. Material that does not help answer it belongs in the appendix, a
separate extension, or the current archival manuscript.

## Accepted editorial decisions (September 13, 2026)

### Restore AI efficiency (September 14, 2026; superseding wording decision)

- The author prefers "AI efficiency" for B after reconsidering
  "AI productivity". Restore this term throughout the manuscript, including
  diagrams, tables, and appendices. Keep the original services-per-compute
  definition and its connection to algorithmic efficiency.
- This supersedes the AI productivity terminology decision below. Preserve
  all subsequent abstract edits, especially the approved closing sentence
  beginning "Numerical simulations show that early growth alone may".
- Keep A as labor-augmenting technology, chi as the research-productivity
  parameter, and all equations, calibration records, solver code and results.

### AI productivity terminology (September 14, 2026; latest wording decision)

- Call B "AI productivity" throughout main_rewrite and its sections, tables,
  figure labels and appendices. At its introduction in Section 3, retain
  "AI efficiency" as an alternative description of services per unit of
  compute and connect it to the cited computer-science literature on
  algorithmic efficiency. This supersedes earlier terminology choices.
- Preserve B, BU, BM, every equation and reference label, all parameters,
  calibration records and numerical paths. Keep chi's distinct meaning as
  the research-productivity parameter and preserve "efficiency units" for A.
- Do not rename internal solver functions or stored data fields as part of
  this editorial change.

### Simulation terminology (September 14, 2026; latest wording decision)

- Use "numerical simulations" rather than "numerical equilibrium paths"
  or "numerical equilibrium trajectories" to name the numerical exercises
  throughout the current manuscript, including headings and captions.
- Retain "equilibrium" in mathematical definitions, existence results and
  numerical admission checks. This is a wording change, not a relaxation of
  any equilibrium condition or a change to the solver, data or figures.

### Central research-share target (September 14, 2026; latest decision)

- Set the central illustrative target to first-year M/Y=0.183% at sigma=1.
  The annual ratio is integral(M)/integral(Y), not M0/Y0. Retain chi
  7.616304576019883 because it produces 0.1829159408%, which rounds to the
  target; other sigmas use the same chi. Do not claim an exact empirical fit.
- This supersedes the central price-target designation below. Preserve the
  original price-search record and acknowledge the target was selected
  after examining those simulations. The 40% price decline is now an outcome.
- Keep the slow sensitivity, all stocks, trajectories, figure curves,
  analytical results, title, abstract and introduction unchanged.
- The new central replication driver validates the research target and
  retains the existing equilibrium solver and numerical tolerances.

### Central illustrative scenario and slow sensitivity (September 14, 2026)

- The author selected the former Section 6.3 as the central illustrative
  scenario. It now appears as Section 6.2, chi=7.616304576019883, with
  the same 40% price-decline target at sigma=1. The former Section 6.2
  becomes the slow-transition sensitivity in 6.3, chi=1.4378.
- Supersede the ordering and principal/sensitivity designations below,
  not any saved calibration or trajectory. Keep all four sigmas, stocks,
  equations, numerical gates and figure files unchanged.
- State that the central unit-elastic annual M/Y of 0.1829% is close in
  magnitude to the US 2024 proxy of 0.1544%, not a second fitted target.
  Disclose that sigma=1.50 gives 3.0091% and does not match these data;
  the proxy is US rental-equivalent training/research, not global RSI.
- Reorder the figure/parameter/accuracy tables and replication instructions
  consistently. Keep title, abstract and introduction unchanged.

### Restore the low-eta research-value case (September 14, 2026)

- Proposition 5 now states both uncapped, fixed-horizon cases for sigma>1:
  finite value/coercivity when eta<alpha and unbounded value when eta>alpha.
  Keep its existing label and automatic numbering; its proof was already
  present and is now explicitly organized into parts (i) and (ii).
- Link eta=0.20<alpha=0.33 in the simulation design and parameter tables to
  part (i). This is a conservative modeling restriction, not an empirical
  estimate, not necessary for finite-horizon bounded value with a finite
  Bbar, and not a proof of uncapped infinite-horizon equilibrium existence.
- Preserve the eta>alpha continuation/nonexistence result, the unsettled
  equality case, all commented research, and every simulation input/output.

### Select two displayed calibrations (September 14, 2026)

- This decision supersedes the presentation choices below, not the saved
  simulations. All four sigmas have now passed the original equilibrium
  checks in the lower research-expenditure calibration.
- Section 6.1 contains common design and initial conditions. Section 6.2
  presents the principal US 2023 M/Y proxy calibration (chi=1.4378).
  Section 6.3 presents the faster sensitivity fitted to half the observed
  percentage price decline (chi=7.616304576019883). Section 6.4 discusses
  interpretation and limitations.
- Keep the full 80%-price-decline text, data, code and figures intact.
  `\showfullpricebenchmarkfalse` hides its displayed results; changing it
  to true restores them. Its large initial reallocations are explained
  briefly in limitations. Clarify the introductory loss example with a
  footnote, leaving the approved paragraph itself unchanged.
- State in limitations and conclusions that, within the characterized
  finite-bound limits and for positive chi, chi changes the transition but
  not limiting growth, interest or income shares. These conditional results
  are firmer than takeoff dates; sigma, Bbar and other parameters still
  matter. Do not claim Bbar alone determines outcomes or that these are
  forecasts. No new simulations, parameter changes or tolerance changes.
- Keep title, abstract and analytical results unchanged. Preserve the
  legacy presentation switch and document both options in the replication guide.

### Lower research-expenditure target replaces subsection 6.3 (September 14, 2026)

- The author requested the lowest previously discussed M/Y datum and allowed
  a few basis points of empirical mismatch. Use US 2023, 18.46/27811.517,
  or 0.0663754%, not the 2024 or 2025 datum.
- Select the nearest previously explored increasing-branch candidate:
  chi=1.4378, annual M/Y=0.0637427%, shortfall 0.2633 bp. All non-chi
  parameters and initial stocks stay fixed; only sigma=1 is presented.
- Original equilibrium, optimality, two-horizon-extension, early-window and
  event checks pass. Numerical tolerances are unchanged.
- Active results: numerical_rewrite/rsi_research_share_2023/;
  script: scripts/calibrate_rewrite_research_share_low.py.
  The former high-target results and figures remain intact; the old text
  and tables are under sections_rewrite/preserved/.
- Leave title, abstract, introduction, analytical model and subsections 6.1/6.2 untouched.

### Approximate research-expenditure calibration accepted (September 14, 2026)

The author accepted 0.3215% first-year M/Y against the 0.3562% US 2025 proxy
and requested that the already-verified simulation become a new subsection.
Publish only the existing sigma=1 path, chi=81.08480942910101, with unchanged
initial stocks, other parameters and equilibrium gates. This is an approximate
empirical fit, not an exact fit or an excuse to relax numerical tolerances.
Retain all prior simulations and the diagnostic search. Use the same three
figure groups, a parameter/initial-stock table, and explicit source caveats.
The new source is `sections_rewrite/10_rsi_research_share.tex`; its separate
outputs are `numerical_rewrite/rsi_research_share_2025/published_unit/`.
Do not label it a four-elasticity comparison: the other three paths at this
chi have not been constructed or admitted. Do not change the title, abstract,
introduction, or analytical model.

### Additional half-price-decline target (September 14, 2026)

Add a second active subsection with `p_X(2.25)/p_X(0)=0.60`: half the
rounded observed 80% percentage decline. Refit chi at sigma=1 and solve
all four elasticities again with the existing BVP and unchanged audits.
Keep the same fixed-B pre-RSI BGP stocks and all other parameters.
Preserve the 80%-decline exercise and the silenced legacy comparisons.
Do not interpret the sensitivity as an empirical monopoly/competition wedge.

### RSI activation replaces the displayed calibration (September 14, 2026)

The user approved a pre-event BGP with AI already present and fixed B0,
followed by an unanticipated activation of previously unavailable RSI.
Keep omega_X=0.10 before and after the event. Choose K0 separately for
each sigma to match K0/Y0=3.30 and r0=0.05; do not impose pre-event C0
on the new equilibrium. Keep eta, the four sigmas, B0/Bbar=0.01, and
Bbar=1.10 times the sigma=1.50 threshold. Refit chi at sigma=1, then hold
it fixed. The new variant is `rsi_activation`; source and results use
separate files. Preserve the post-event equations, BVP logic, and admission
thresholds. Add checks of the pre-event BGP and event continuity.

The LaTeX switch `\showlegacysimulationsfalse` selects the new section and
numerical appendix; `\showlegacysimulationstrue` restores all earlier
simulations. No old trajectory, figure, or numerical data is deleted.
The title, abstract, introduction, and analytical model remain untouched.

### Previous principal calibration (preserved, September 14, 2026)

The existing lower-weight price-calibrated comparison in
`sections_rewrite/07_low_ai_price_calibration.tex` was the principal
calibration. Preserve its four sigmas 0.90, 1.00, 1.10, 1.50; common no-AI Ramsey
initial capital; eta=0.20; omega_X=0.10; Bbar=1.10 times the sigma=1.50
threshold; B0/Bbar=0.01; and chi=36.03184470863892, fitted to the price decline
at sigma=1 and then held fixed across sigmas. Numerical files remain in
`numerical_rewrite/price_calibrated_low_ai_high_cap/`; do not rename code
identifiers or overwrite earlier simulations merely to change their editorial
status. Ramsey supplies the capital reference; the principal comparison does
not assume that adding AI preserves the old production set. Matching the same
price decline does not make different B0 values economically equivalent.
The omega_X=0.20 and B0/Bbar=0.10 price exercise remains a joint sensitivity,
not a one-parameter B0 comparison. A B0/Bbar=0.10 exercise at omega_X=0.10 has
not yet been solved and must not be claimed as completed.

### Preserved model edits

Do not restore the household sentence "Admissible choices satisfy $C_t>0$,
$K_t\geq0$, and $K(0)=K_0$", or reintroduce it in paraphrase. Oliver has
deliberately removed this redundant prose. This editorial deletion does not
change the equilibrium conditions or simulation constraints stated elsewhere.

When introducing the CES weights, explain that $\omega_L$ weights effective
labor and $\omega_X$ weights effective AI production services. Do not restore
the sentence that the weights "are strictly positive and sum to one" in this
paragraph; Oliver has repeatedly removed that redundant prose.

Do not restore the paragraph beginning "The exogenous paths are" after the
equilibrium equation block, in whole or in paraphrase. Oliver explicitly
removed all of its statements: the repeated exogenous paths and initial stock
conditions, the unit-elastic CES limits, the feasibility and agent-optimality
restatement, and the finite-date upper-bound restatement. Do not reactivate the
older commented versions of this material. This is an editorial deletion, not
authorization to change the agents' problems, equations, or simulation rules.

Call $\Pi$ the developer's "net profit", not "net distributions". References
to verification results must identify the lemma and appendix with automatic
LaTeX references, not refer vaguely to "the verification lemma in the appendix".

Keep the remark "The economy without AI" to one sentence identifying the
Ramsey--Cass--Koopmans case; do not restore its redundant equation block or
the accompanying explanation of the no-AI specialization.

## Model scope

- The benchmark has autonomous AI research: \(\omega_H=0\).
- The benchmark formulation does not introduce \(H\), \(\omega_H\), or
  \(\sigma_{HM}\). These objects are not set to zero after being defined; they
  are absent from the benchmark.
- Human research is a possible later extension. It will enter this paper only
  if it changes or establishes the robustness of a central result.
- The notation, timing, and parameter meanings inherited from the current
  benchmark remain unchanged.
- A finite AI-efficiency frontier is an equilibrium regularization and an
  analytical device, not a robustness exercise. Section 5 studies all three
  uncapped regimes separately: complementarity bounds and conditional limits,
  a proved unit-elastic BGP, and nonexistence/open cases under substitution.
  Detailed proofs and the local unit-elastic trajectory result remain in the
  appendices. None is obtained by taking the long-run limit of finite-frontier
  equilibria. The companion paper remains separate and unchanged.

## Logical order

1. Define population, labor-augmenting technology, preferences, and predetermined
   stocks.
2. Present final production and solve the competitive final-good firm.
3. Derive the static relationship between AI services and labor.
4. Present the integrated AI developer and explain the market structure.
5. Define effective AI production services, effective AI research services, and AI efficiency
   accumulation.
6. Solve the developer's pointwise service decision before deriving its dynamic
   conditions.
7. State the resource constraint, initial conditions, transversality
   conditions, and a self-contained equilibrium definition.
8. Derive results for \(\sigma<1\), \(\sigma=1\), and
   \(\sigma>1\), in that order.
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
| 3 | Invariance of the finite AI-efficiency domain and finite-horizon developer existence | `prop:axm-finite-cap-invariance` | Proven | Model |
| 4 | Checkable sufficient condition for global developer optimality with a finite frontier | `prop:axm-capped-developer-sufficiency` | Proven | Model; proof in appendix |
| 5 | Labor bottleneck when \(\sigma<1\) | `prop:axm-complements` | Proven under regular limiting conditions | Equilibrium regimes |
| 6 | Local equilibrium existence near the complementary-input limit | `prop:axm-complement-local-existence` | Proven | Equilibrium regimes |
| 7 | Existence and analytical characterization of a positive-AI balanced-growth equilibrium when \(\sigma=1\) | `prop:axm-benchmark-equilibrium-existence` | Proven for the autonomous benchmark | Equilibrium regimes |
| 8 | Local equilibrium trajectories around the unit-elastic balanced-growth path | `prop:axm-unit-saddle-path` | Proven | Equilibrium regimes |
| 9 | Two finite-frontier terminal regimes separated by \(\overline B_c\) when \(\sigma>1\) | `prop:axm-capped-terminal-regimes` | Proven conditional on a regular frontier approach | Equilibrium regimes; central proposition |
| 10 | Local finite-cap equilibrium paths on both sides of \(\overline B_c\) | `prop:axm-capped-local-equilibrium` | Proven | Equilibrium regimes |
| 11 | No finite-rate balanced-growth path with unbounded AI efficiency when \(\sigma>1\) | `prop:axm-no-bgp` | Proven conditional on \(B\to\infty\) | Equilibrium regimes |
| 12 | Finite-window limit as \(\overline B\to\infty\) and noncommuting long-run limit | `prop:axm-infinite-frontier-limit` | Proven; does not establish uncapped equilibrium | Equilibrium regimes |
| 13 | Global finite-cap equilibrium from the common initial stocks for a moderate frontier | `global_finite_cap_bvp_analysis.json` | Numerically admitted under the documented equilibrium rule | Quantitative equilibria |

## Results reserved for the appendix

- Interior research at every finite date.
- Research-curvature and coercivity arguments supporting \(\eta<\alpha\).
- The costate derivations and sufficiency proofs.
- Necessary restrictions on irregular gross-substitutes continuations.
- Finite-window continuation around \(\sigma=1\).
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

1. A diagram of the benchmark model and the feedback from AI efficiency to
   effective AI research services.
2. A figure illustrating the static substitution mechanism governed by
   \(\sigma\).
3. A table of parameters, interpretations, values, and sources.
4. One three-panel figure: `g_Y-n`, `g_w`, and `r`, with a common vertical
   scale for the two growth rates and all four scenarios shown together.
5. One three-panel figure: `B/Bbar`, `wL/Y`, and `p_X X/Y`, again with all four
   scenarios shown together.
6. One five-panel figure: `C/(AL)`, `K/(AL)`, `U/(p_X X)`, `M/(p_X X)`,
   and `Pi/(p_X X)`.
7. One compact table reporting initial and long-run values of the central
   simulated outcomes, in addition to the analytical-regime summary.

The four agreed elasticities are 0.90, 1.00, 1.10, and 1.50, with common
parameters, frontier, and initial stocks. All four now pass the numerical
equilibrium audit. The confirmed initial stocks come from the historical
uncapped unit-elastic BGP, not the finite-frontier stationary boundary;
consumption and the shadow price are selected anew for every case. See
`audit/rewrite_simulation_design.md` for the design and
`audit/rewrite_equilibrium_simulations.md` for execution evidence,
optimality checks, and publication status. Numerical admission is not a
formal existence certificate for arbitrary initial stocks.

## Writing sequence

1. Write and audit the benchmark model and the equilibrium definition.
2. Rewrite the analytical propositions in their logical order.
3. Decide which admitted numerical results materially clarify those
   propositions.
4. Write the quantitative section and algorithm appendix.
5. Write the introduction, literature review, abstract, and conclusion last.
