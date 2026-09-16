# Jones (2026): connection to the current manuscript

Date: 2026-09-15. Initial manuscript baseline: `b7aef75`.
Before publication, the unrelated Overleaf edits in `6e0515d` were incorporated
by fast-forward; their changes to Section 6.1 were preserved without modification.

**Source:** Charles I. Jones, "AI and Our Economic Future," *Journal of
Economic Perspectives* 40(3), Summer 2026, pp. 3--22.
DOI: [10.1257/jep.20261505](https://www.aeaweb.org/articles?id=10.1257/jep.20261505).
The user supplied the published 20-page PDF. All 20 pages, including the
references, were read. The printed pp. 10--11 and 14 were also inspected
visually to verify the formula, Figure 2 and distributional discussion.
PDF SHA-256: `ca7887c25c89ada3b4c066eb2a44a01d2a1ee8797a84721335cb97766ff32576`.
The publisher's landing page independently confirms the bibliographic metadata.
The third-party PDF is not redistributed in this public repository.

## Full reread and paragraph-by-paragraph editing map (2026-09-16)

I reread all 20 pages of the user-supplied published PDF, including all nine
footnotes and the bibliography on printed pp. 20--22. The SHA-256 above is
unchanged. I also inspected Figures 1 and 2 and the CES expressions visually
(printed pp. 7, 9--11), together with the distribution discussion on p. 14.
This records reading of Jones's essay, not independent verification of every
empirical statement or reading of every work in its bibliography. Confidence
in the passage attributions below: High. No manuscript text was changed in
this rereading pass.

### Connections to use when their paragraph comes up

| Passage in Jones (printed pages) | Useful connection | Boundary to preserve |
| --- | --- | --- |
| Opening and two scenarios, pp. 3--8 | Frame uncertainty about the scale of AI's growth effects. Continued historical growth need not mean a technology is economically unimportant. | His counterfactual without further innovation can involve slowing growth. Our exogenous labor-augmenting trend is a different counterfactual. Do not equate the two benchmarks. |
| Effective compute and RSI, p. 5 | Relate raw compute and algorithmic efficiency to BM; describe better AI helping develop better AI. | Training-run measures are not the whole research-compute flow. Reported improvements do not identify chi, establish autonomous RSI today, or validate a common efficiency index in both activities. |
| Harder-to-find ideas and diffusion, pp. 7--8 | Distinguish diminishing research productivity from delays due to complementary organizational investment. | Neither discussion establishes a finite upper bound on AI efficiency. Our simulated delays do not include organizational adoption costs unless the model is extended. |
| Weak links, pp. 8--11 | Explain why enormous gains in selected inputs can coexist with limited aggregate gains while other tasks remain scarce. | His elasticity is across tasks. Ours is between aggregate labor and AI services. His competitive task-cost-share formula cannot be imported into a monopoly pricing model. |
| Innovation-automation feedback and delayed acceleration, p. 12; synthesis p. 19 | Recognize a direct antecedent for moderate early growth followed by acceleration. Trace the underlying dynamic model to Jones and Tonetti. | His task set expands. Our task structure is fixed and research and capital allocations are endogenous. Similar trajectories do not establish identical mechanisms or validate calendar dates. |
| Jobs as bundles of tasks, p. 13 | Motivate the distinction between workers, jobs, and tasks, and the limits of an aggregate wage. | Our model does not derive occupational reallocation, heterogeneous wages, or creation of new human tasks. |
| Wages and labor shares, p. 14 | Explicit antecedent for labor incomes rising even while their GDP share vanishes. | This coexistence is not a novelty claim. Nor does his example establish our model's parameter restrictions or a universal necessity of substitution for wage acceleration. |
| Ownership and redistribution, p. 14 | Explain why aggregate prosperity does not determine who receives it. | Functional income shares are not personal income inequality. Our representative household does not establish distribution across households or political power. |
| Meaningful work, pp. 14--15; risk, pp. 15--19 | Delimit the economic questions left outside the model. | Do not insert a safety, strategic race, or welfare conclusion into a model without those mechanisms. Use only if the limitations paragraph needs it. |

### Two calculations that require particular care

On pp. 9--11, Jones starts with a harmonic-mean example and then gives the
CES level gain `(1/(1-s))^(sigma/(1-sigma))`, where s is the initial spending
share of tasks made infinitely productive under competitive markets. For
sigma = 0.2, automating half the initial cost share raises the output level
by about 19%; the example does not predict an annual growth rate. Figure 2
uses a logarithmic vertical scale. On p. 12, its time interpretation adds
the illustrative assumption that s rises by 0.01 each year. The resulting
finite-date divergence is not a solved infinite-horizon equilibrium with
optimal saving and research, and is not a proof for our uncapped economy.

The wage/share discussion on p. 14 separates task prices, workers' incomes
when changing occupations, and total labor income. Preserve those distinctions
when moving to our homogeneous labor supply. In our own manuscript, any
necessity claim tying permanently faster wages to vanishing labor shares must
retain its intended regime coverage: the uncapped unit-elasticity case is not
the same as the finite-bound classification.

### Reference trails, not automatic additional citations

- Production constraints and automation: Jones and Tonetti (2026), Aghion,
  Jones, and Jones (2019), Kremer (1993), and Jones (2011).
- Research constraints and measurement: Bloom et al. (2020), Benjamin Jones
  (2025), Ho et al. (2024), and the specific Epoch AI dataset cited by Jones.
- Wages, tasks, and comparative advantage: Caselli and Manning (2019),
  Restrepo (2025), Autor and Thompson (2025), Acemoglu and Restrepo (2022),
  Althoff and Reichardt (2026), and Freund and Mann (2026).
- Diffusion and complementary organizational investment: David (1990) and
  Brynjolfsson and Hitt (2000).

Use Jones for the synthesis. Where a proposed sentence needs a theorem or
empirical finding, check the relevant original source and its assumptions
before proposing that attribution. Reading Jones's reference list does not
upgrade those other sources to full-text-read status. Bibliographic details
should also be checked against the original publication, not copied blindly.

For upcoming edits, show one minimal paragraph-level connection at a time
and wait for the author's approval. Preserve approved wording and notation.
Do not add every connection above or move literature-review filler into the
rest of the paper. The manuscript's title, abstract, introduction, equations,
figures, parameters, and simulations were left untouched in this pass.

## Verified connections

1. **RSI (p. 5).** The essay explicitly describes AI models creating better
   AI models without human involvement. This is a direct conceptual connection
   to the autonomous research benchmark, not a proof that RSI has already
   occurred or an estimate of research productivity. Confidence: High.
2. **Production bottlenecks (pp. 9--11).** With complementary tasks, making
   some inputs arbitrarily abundant does not remove constraints imposed by
   remaining scarce tasks. In the competitive CES illustration, the gain
   from infinitely automating tasks with initial cost share s is
   `(1/(1-s))^(sigma/(1-sigma))`. This is a conditional level comparison,
   not a calibrated prediction for our monopoly model. Confidence: High.
3. **Delayed takeoff (p. 12; conclusion p. 19).** A gradual expansion of the
   automated task set can leave early growth moderate before a large later
   acceleration. The essay explicitly draws on the richer Jones--Tonetti
   model. Our low-chi paths have a related qualitative pattern, but fixed
   production structure and endogenous research/capital accumulation rather
   than an expanding task set. The essay does not validate our dates or chi.
   Confidence: High for the attribution; the connection is an interpretation.
4. **Wages versus labor share (pp. 13--14).** Jones explicitly distinguishes
   falling labor shares from falling wages and illustrates how labor income
   can keep growing while its share tends to zero. This reinforces the
   existing disclaimer that coexistence is not our novel result. The sharper
   claim in our manuscript is its conditional equilibrium classification,
   efficiency threshold and wage-growth/share-decline relationship.
   Confidence: High.
5. **Distribution and risk (pp. 14--19).** Greater output does not settle
   ownership or redistribution, and weak links can delay benefits while
   leaving catastrophic vulnerabilities. These are important limits to our
   representative-household model, not results it derives. No new risk
   mechanism or welfare claim was inserted. Confidence: High.

## Essential non-equivalence

Jones's elasticity is between tasks. Our sigma governs substitution between
effective labor and AI production services in an aggregate CES. In his
framework, progressively automating remaining complementary tasks can
eventually remove bottlenecks even with a low task elasticity. Our fixed
aggregate structure instead requires substitution above one and a sufficiently
high efficiency bound for the characterized AI-dominated regime. This is not
a contradiction. His illustrative sigma=0.2 should not be imported as a direct
calibration of ours. Neither the static infinite-productivity example nor its
stylized time interpretation proves existence or nonexistence of equilibrium
in our uncapped model.

## Edits

- Related Literature: cite the weak-link/delayed-acceleration synthesis beside
  Jones and Tonetti; distinguish the elasticities; cite the explicit
  wage-versus-labor-share discussion on p. 14.
- Section 6.4: connect delayed acceleration without equating the mechanisms
  or treating the essay as an empirical validation of transition dates.
- Add the published bibliographic entry `jones2026future` and an explicitly
  editorial, structured literature-browser summary.
- No changes to title, abstract, introduction, model, propositions,
  calibration or simulation data.

## Validation scope

The September 13 audit validator already failed its exact-coverage check on
the unmodified baseline, before this citation was added. That historical audit
is not represented as a complete audit of the current literature section.
This memo records a complete source reading for this added reference only.
The database rebuild exposed an existing duplicate of Acemoglu and Restrepo
(2018): the same key appeared in both the bibliography and manual additions.
Its manual record was moved to metadata overrides, preserving its content
and leaving one bibliographic record. No claim about that source was re-audited.
The offline literature-database builder checks citation coverage, duplicate
keys/DOIs and completeness of structured review fields. Compilation checks
the new citation and bibliography, and the changed pages are rendered for QA.
The rebuild passes: 103 records, no duplicate citation keys or DOIs, no missing
cited keys and no incomplete structured reviews. A targeted check confirms
the new citation resolves in the compiled bibliography and retains its
full-text-reading provenance. The first PDF build has no undefined references
or overfull boxes; literature pp. 5--6, limitations p. 33 and bibliography p. 66
were inspected visually. The final build also incorporates the Overleaf update.

The preserved Overleaf paragraph in Section 6.1 reintroduces the former
calibration values (7.616305 and 1.4378), whereas the active exercises use
illustrative values (7.5 and 1.5). This inconsistency is flagged to the author;
resolving it is outside the Jones-citation edit and no simulation was rerun.
