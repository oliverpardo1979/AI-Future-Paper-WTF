# Paragraph-by-paragraph literature integration

Related Literature remains unchanged during this review. Implement only
paragraphs explicitly approved by the author.

## Introduction, paragraph 1 (approved)

- File: `sections_rewrite/01_introduction.tex`.
- Incorporated the exact wording approved in the conversation, beginning
  "Advances in artificial intelligence raise both hopes and fears" and ending
  "output per worker grows even faster than wages".
- No external reference added: the paragraph introduces the motivation and the
  paper's own result. No literature discussion has been relocated here.
- The author chose to leave technical scope qualifications for later paragraphs;
  do not silently reinsert them into this opening paragraph.

## Introduction, paragraph 2 (approved)

- File: `sections_rewrite/01_introduction.tex`.
- Applied the author's choice of the second proposed version: distinguish
  supplying AI services from using AI research services to improve efficiency.
- Added one sentence linking expected monopoly profits and research incentives
  to Romer (1990), `romer1990`.
- Verified against the published original, *Endogenous Technological Change*,
  *Journal of Political Economy* 98(5, Part 2), pp. S73 and S81--S82:
  https://web.stanford.edu/~klenow/Romer_1990.pdf.
- The connection is the incentive for innovation, not identical market
  structure: Romer models patented varieties and multiple producers, not a
  single recursively self-improving AI developer.
- Related Literature remains unchanged. The next paragraph has not been edited.

## Introduction, paragraph 3 (approved)

- Applied the minimally revised paragraph approved by the author, with
  `davidsonetal2026` attached to the distinction between the technological and
  economic feedback loops.
- Checked the May 2026 author PDF, printed pp. 2--3 (mechanisms), 21 and 38
  (fixed savings and research allocations in their application).
- The comparison acknowledges the feedback architecture, not identical
  optimization problems or equilibrium results. No additional prose added.
- Review paused before paragraph 4 to inspect Jones (2026) and recent top-five
  journal publications. New candidates go into the literature tool, not the paper.

### Jones and Tonetti addition (approved, 2026-09-16)

- Added one sentence to paragraph 3 linking automation, research resources and
  further innovation to `jonestonetti2026`; retained the Davidson attribution
  for the technological/economic-loop distinction and all other wording.
- Checked the May 2026 version 0.5 original, Section 5.3, Table 9 (printed
  p. 36), and the summary on p. 45:
  https://christophertonetti.com/files/papers/JonesTonetti_Automation.pdf.
- Their research input uses final goods and research expenditure is a fixed
  fraction of output; ideas raise task productivity and support automation.
  This is a related feedback, not an identical RSI technology or the same
  optimal research-allocation problem. Their task elasticity is not equated
  with this paper's aggregate AI-labor elasticity.
- Related Literature and all other manuscript paragraphs remain unchanged.

## Section 5.3: hyperbolic growth and finite-time singularities (approved, 2026-09-16)

- File: `sections_rewrite/05_uncapped_equilibria.tex`.
- Added `davidsonetal2026` immediately before the research-expenditure
  proposition. Verified the May 2026 original, Proposition 1 (printed p. 16),
  the economic-feedback extension (pp. 19--20), and the discussion of fixed
  saving and factor-allocation shares (pp. 19 and 21):
  https://thomas-houlden.com/assets/DHHK_May2026.pdf.
- Recognized the antecedent for hyperbolic growth and a finite-time
  singularity when feedback overcomes diminishing returns. The benchmark's
  fixed allocation rules are not equated with our optimal allocations.
- Distinguished finite-date divergence from indefinitely increasing growth
  rates and from an unbounded developer objective over a fixed horizon.
  The dated return bound does not establish the time to divergence.
- Replaced the blanket statement that singularities are not studied with
  the precise exclusion under the paper's infinite-horizon equilibrium
  definition. No new existence or nonexistence claim, equation, or proposition.
- Preserved all commented earlier derivations. Related Literature, the
  introduction, abstract, model, and simulations remain unchanged.

## Section 3.4.1: economic uses of compute (approved, 2026-09-16)

- Added the author's sentence immediately after the definitions of U and M in
  `sections_rewrite/03_model.tex`, preserving the original terminology and equations.
- The production/research distinction concerns economic uses, not disjoint
  inference/training operations: executing AI researchers also uses inference.
- Cited `davidsonetal2026`; rechecked the May 2026 original, Section 4.2,
  printed p. 23, Equation (33), which describes inference compute for AI labor
  across sectors, including research. No equation or result is equated to ours.
- No other manuscript paragraph was changed.

## Section 3.4.1: effective compute and BM (approved, 2026-09-16)

- Added a short connection after the definition of B, BU, and BM in
  `sections_rewrite/03_model.tex`, citing `hoetal2024algorithms` and
  `jones2026future`.
- Verified Jones, JEP 40(3), printed p. 5, including his attribution to
  Ho et al. (2024) and Epoch AI (2026), in the author's published PDF:
  https://web.stanford.edu/~chadj/AIandEconomicFuture.pdf.
- Rechecked Ho et al., arXiv:2403.05812v1, pp. 1-3, especially the definition
  of algorithmic progress through compute savings and its pretraining scope:
  https://arxiv.org/pdf/2403.05812.
- Distinguished rival compute M from the nonrival algorithmic knowledge
  represented by B. This is the model's economic interpretation, not an
  empirical finding about nonrivalry attributed to Ho et al.
- The effective-compute analogy does not equate the paper's broad research
  flow with a training-run measure or identify B or chi from those estimates.
  No reported growth factor is imported into the calibration.
- Preserved all equations, notation, simulations, and other manuscript text.

## Introduction and conclusion: results, limitations, and extensions (2026-09-16)

- Implemented the author's approved introduction passages on temporary versus
  permanent growth, the wage-growth premium, and research productivity's effect
  on resource allocation. Preserved the opening, framework, feedback loops,
  uncapped paragraph, and roadmap. Corrected the distinction between the
  interest-rate level and the growth rates of output and wages.
- Used the approved first conclusion paragraph. Did not insert the two rejected
  proposed result-recap paragraphs. Replaced repeated result summaries with
  limitations tied to specific possible extensions; kept the finite-bound scope,
  the uncapped unit-elastic exception, and the legacy-simulation branch.
- Verified original sources (not just abstracts) for these connections:
  - Davidson et al. (May 2026), Sections 4.1 and 6.2, printed pp. 22 and 40--43:
    human/AI research tasks and bottlenecks. These mechanisms motivate extensions;
    their explosive-growth conditions do not prove our equilibrium existence.
    https://thomas-houlden.com/assets/DHHK_May2026.pdf
  - Korinek and McKelvey (2026), printed pp. 6--9: incomplete information on
    compute allocation and assumptions used for measurement, not identified
    structural parameters for this manuscript.
    https://www.bankofcanada.ca/wp-content/uploads/2026/06/swp2026-20.pdf
  - Erdil et al., GATE, arXiv:2503.04941v2, Section 3.6, pp. 20--21, and
    Equation (29), p. 37: compute and conventional-capital adjustment costs.
    Their planner framework is not identified with our decentralized equilibrium.
    https://arxiv.org/pdf/2503.04941
  - Korinek and Vipra, INET WP 228 (2024 version of the 2025 publication),
    printed pp. 6--7 and 14--16: competing developers, compute costs, and
    concentration forces. Not a claim that permanent monopoly is established.
    https://www.ineteconomics.org/uploads/papers/WP_228-Korinek-and-Vipra.pdf
  - Acemoglu and Restrepo (2019), JEP, printed pp. 8--10: changing task content,
    displacement and reinstatement, distinct from fixed CES weights.
    https://economics.mit.edu/sites/default/files/publications/Automation%20and%20New%20Tasks%20-%20How%20Technology%20Displace.pdf
  - Jones (2026), JEP, printed pp. 13--14: occupational heterogeneity, ownership,
    distribution and redistribution. Read in the supplied published PDF.
    https://web.stanford.edu/~chadj/AIandEconomicFuture.pdf
- No title, abstract, Related Literature, model, simulation, figure, parameter,
  initial-condition, or notation changes. Updated bibliographic placement data.

## Aghion, Jones, and Jones: weak links and equilibrium regimes (2026-09-16)

- Added a short paragraph in Section 3.3 connecting the CES complementarity
  case to their weak-link mechanism. No new equation or parameter is introduced.
  The reference distinguishes replacement within tasks from complementarity
  across tasks and does not identify their elasticity with our aggregate sigma.
- Added a paragraph after Proposition 1 recognizing the antecedent of stable
  growth and a positive labor share despite near-complete automation. Our
  autonomous RSI and return threshold do not make that qualitative mechanism new.
- Verified the published chapter, Section 9.2.2, pp. 242--246, Equations
  (5)--(16), Figure 9.1, and footnote 8, plus the fixed-saving closure on p. 240:
  https://web.stanford.edu/~chadj/AJJ-AIandGrowth.pdf.
- Their footnote 8 permits an AK limit under sufficiently rapid automation
  despite complementarity between tasks. Consequently our aggregate sigma>1
  condition must not be presented as a condition for all task-based models.
- Updated the bibliographic-tool record to the published PDF and recorded
  these passages and limits. Related Literature, the introduction, abstract,
  conclusions, equations, notation, and all simulations remain unchanged.

## Silence Section 6.4 and refine conclusions (2026-09-16)

- Commented only the input of `11_rsi_limitations.tex` in `main_rewrite.tex`.
  The subsection's file, label, text, and references remain intact; uncommenting
  the input restores it. Updated README and REPLICATION to avoid stale directions.
- Preserved the approved opening of the conclusion and its final question.
  Distinguished the existing weak-link and wage/share antecedents from the
  efficiency threshold and exact wage-growth premium characterized here.
- Rechecked Sections 3--6: the finite-bound regimes, the complementarity
  feasibility bound, the uncapped unit-elastic BGP/local existence result,
  and the fixed-horizon unbounded-profit result under strong research returns.
  Did not claim global existence, general nonexistence, or a finite-time singularity.
- Restated the main simulations' distinction between transition and limits.
  Retained the essential calibration, adjustment, monopoly, homogeneous-labor,
  and ownership limitations despite silencing 6.4. No discarded numerical
  exercise was reintroduced into the active conclusion.
- Retained source-verified connections documented above: Aghion--Jones--Jones
  on weak links; Jones on wages, shares, and ownership; GATE on investment
  frictions; Korinek--McKelvey on measurement; Korinek--Vipra on market structure;
  Acemoglu--Restrepo on tasks; Davidson et al. on research networks and bottlenecks.
- Title, abstract, introduction, Related Literature, substantive Sections 3--6,
  equations, figures, simulations, parameters, and initial conditions unchanged.

## Introduction, paragraph 4: labor bottleneck (approved, 2026-09-16)

- Added only the approved final sentence recognizing the related human-task
  bottleneck in Aghion, Jones, and Jones (2019), `aghionjonesjones2019`.
- Verified the published original, Section 9.2.2, pp. 242--246, especially
  Equations (5)--(16), Figure 9.1, and footnote 8. The antecedent is the
  bottleneck mechanism, not our aggregate substitution or efficiency threshold.
- Updated the bibliographic tool's placement note. No other manuscript
  paragraph, equation, simulation, figure, or notation changed.
- The author rejected adding Jones (2026) to paragraph 1; leave it intact.
  Paragraphs 2 and 3 retain their previously approved references without additions.

## Introduction, paragraph 5: capital accumulation (approved, 2026-09-16)

- Added the approved sentence citing `jonesmanuelli1990` after the statement
  that an AI-dominated long-run regime becomes possible.
- Verified NBER Working Paper 3241 (January 1990), Condition G and Theorem 1
  on p. 8, and the characterization on pp. 11--12. The connection concerns
  sustained growth with a sufficiently high limiting return on capital,
  not our AI-efficiency threshold or private RSI-investment problem.
- Updated the bibliographic placement and passage-verification notes.
- Added a local Needspace instruction to avoid leaving the following paragraph's
  first line alone at the foot of the page; its wording is unchanged.
- All other manuscript paragraphs remain unchanged. Title, abstract,
  Related Literature, model, equations, figures, simulations, parameters,
  and initial conditions remain untouched.

## Model, opening paragraph: research versus production automation (approved, 2026-09-16)

- Added only the approved sentence citing `trammellkorinek2023` to distinguish
  autonomous research from the removal of labor from final-good production.
- Verified the April 2026 revision of NBER Working Paper 31815, Section 3,
  printed pp. 15--16 (PDF pp. 17--18), particularly Section 3.1 and Equations
  (9)--(10). The connection is the distinction between the two automation
  margins, not an equivalence of research technologies or a factual claim
  that research has already been fully automated.
- Updated the bibliographic tool's placement and verification notes.
- No other manuscript paragraph, equation, simulation, figure, parameter,
  initial condition, title, abstract, or Related Literature text changed.

## Section 4.1: substitution and the limiting return (approved, 2026-09-16)

- Added the approved final sentence citing `duffypapageorgiou2000` to the
  paragraph immediately after Equation `eq:rewrite-critical-frontier`.
- Verified the authors' March 2000 final draft, Section 2.2, printed pp. 7--8
  (PDF pp. 8--9). The antecedent is the joint role of substitution and a
  sufficiently high limiting return on capital in CES growth models, not
  our AI-efficiency threshold or decentralized AI-developer equilibrium.
- Updated the bibliographic tool's placement and passage-verification notes.
- The author rejected the proposed Hemous--Olsen addition in Section 3.4.4;
  that paragraph remains unchanged. No other manuscript text changed.

## Section 4.2: rising wages and a vanishing labor share (approved, 2026-09-16)

- Added the approved sentence citing `raymookherjee2022` immediately after
  `rem:rewrite-ai-revenue-share`, outside the remark; the remark is unchanged.
- Verified the publisher-formatted article hosted by Mookherjee at
  `https://people.bu.edu/dilipm/publications/AutREDpub.pdf`, Sections 3.3--3.4,
  Theorem 1 on p. 9 and Proposition 2(b) on p. 11. The antecedent concerns
  rising wages and a vanishing labor share from capital-driven automation,
  not our AI-efficiency threshold, limiting wage-growth rate, or AI revenues.
- Updated the bibliographic placement, original-document link, and passage
  notes. No other manuscript text, equation, figure, or simulation changed.

## Section 5.2: research resources and long-run growth (approved, 2026-09-16)

- Added only the two approved sentences citing `jones1995` to the paragraph
  following Proposition `prop:rewrite-uncapped-unit-bgp`.
- Verified the original JPE article hosted at
  `https://web.stanford.edu/~chadj/JonesJPE95.pdf`, printed pp. 765--768,
  especially Equations (7)--(8) on p. 767 and their explanation on p. 768.
- The comparison distinguishes Jones's expanding human research workforce
  from effective labor's indirect contribution through production in our
  autonomous RSI model. It does not claim equivalent research technologies.
- Updated the collected reference's placement and verified-passage notes.
  Related Literature and all other manuscript text remain unchanged.

## Section 6.1: unanticipated activation (approved, 2026-09-17)

- Added the approved Beaudry--Portier sentence at the end of the opening
  paragraph in `08_rsi_design.tex`. The previously commented discussion
  remains commented. No simulation or initial condition was changed.
- Verified the published JEL article, Section 4.1, pp. 1044--1045; the
  connection concerns advance responses to news, not their direction in
  our model or simultaneous increases in consumption and investment.

## Abstract and Jones--Tonetti comparison (requested, 2026-09-17)

- Specified `output-per-worker growth` in the last abstract sentence;
  per-worker normalization preserves the comparison with gamma.
- Read the Jones--Tonetti May 2026 v0.5 main text, pp. 1--46, and relevant
  appendices B--C. Proposition 1 (p. 10) and B.3, Equations (33)--(35),
  support a CES representation conditional on task assignment, not an
  unconditional equivalence with our fixed-weight Z for every sigma.
- In the existing introduction feedback paragraph, clarified that their
  innovation is endogenous but research and capital investment use fixed
  output shares (Table 9, p. 36). Our developer chooses research spending
  to maximize discounted net profit, jointly with household saving and
  capital accumulation. This is a comparison with their allocation rule,
  not a claim that private endogenous innovation is new to the literature.
- Documented both connections and their limits in the bibliography tool.
  Related Literature, model equations, notation, figures, and simulations
  remain untouched.
