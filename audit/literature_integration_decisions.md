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

## Section 6.2: consumption growth and real returns (approved, 2026-09-17)

- Replaced only the approved sentence in the paragraph introducing Figure 5,
  `12_rsi_high_productivity.tex`, with the Euler-condition explanation and
  the Chow--Halperin--Mazlish citation.
- Verified the original June 2026 working paper, Section 3.1, printed p. 8
  (PDF p. 9), Equations (1)--(2), and Section 3.2, pp. 9--10:
  https://www.basilhalperin.com/papers/agi_emh.pdf.
- Higher returns accompany faster consumption growth under the manuscript's
  Euler condition; they do not moderate that growth rate. The comparison
  concerns intertemporal optimality, not an equivalence of long-maturity
  market rates and our instantaneous net return on physical capital.
- Updated the bibliography tool's placement and verification notes. No other
  manuscript text, equation, simulation, figure, or notation was changed.

## Section 6.3: initially similar paths and later divergence (approved, 2026-09-17)

- Added only the approved final sentence citing Jones--Tonetti Figure 5 to
  the paragraph discussing the lower row of Figure 7 in
  `13_rsi_low_productivity.tex`. Completed the existing 2.1% reference with
  `long-run limit`; neither number nor simulation was changed.
- Verified the May 2026 v0.5 original, Figure 5 on printed p. 40 and its
  explanation on pp. 39--41. The connection recognizes initially similar
  growth paths followed by divergent long-run outcomes, not an equivalence
  of automation technology, substitution elasticities, thresholds, or dates.
- Checked the stored slow-exercise output growth at year 500 (3.2136%) and
  its analytical normalized limit (2.1350%); both retain one decimal in prose.
- Updated the collected reference's placement note. No other manuscript
  paragraph, equation, simulation, figure, parameter, or notation changed.

## Conclusion: wealth concentration and heterogeneous ownership (approved, 2026-09-17)

- Added only the approved Moll--Rachel--Restrepo sentence after the existing
  Jones reference in the last substantive paragraph of `06_conclusion.tex`.
- Verified the published Econometrica article, Section 2.1, p. 2650;
  Lemma 1 and Proposition 1, pp. 2653--2654; and Section 2.3,
  Proposition 3 and discussion, pp. 2659--2661, including Equation (12):
  https://benjaminmoll.com/wp-content/uploads/2019/07/UG.pdf.
- Their heterogeneous wealth accumulation mechanism motivates an extension;
  our representative-household interest-rate result does not itself imply
  increasing personal income or wealth inequality.
- Added the published article to `references.bib` and migrated its existing
  collected record from additions to overrides, preserving its metadata
  and editorial summary without creating a duplicate. Updated placement notes.
- This completes the current paragraph-by-paragraph pass through the main
  text. The closing sentence needs no citation. Related Literature remains
  unchanged for a separately approved shortening pass; no new equation,
  simulation, figure, parameter, or notation changes were made.

## Commented comparison with Davidson and Jones--Tonetti (requested, 2026-09-17)

- Fast-forwarded to the author's GitHub commit `3cba833` before editing;
  preserved the author's new introductory paragraphs verbatim.
- Added a percent-commented draft to `02_literature.tex` distinguishing
  endogenous technological progress from optimized research and saving.
- Verified Davidson et al. (May 2026), Section 3.2, printed pp. 19--21,
  especially Equation (26) and the fixed sectoral allocation shares:
  https://thomas-houlden.com/assets/DHHK_May2026.pdf.
- Verified Jones and Tonetti (May 2026, v0.5), Section 5.3, Table 9 on
  printed p. 36: research and investment are fixed shares of output,
  despite endogenous innovation and task automation:
  https://web.stanford.edu/~chadj/JonesTonetti_Automation.pdf.
- The latest synchronized manuscript still includes Related Literature
  actively. Only the new draft is commented; the existing section and its
  inclusion in `main_rewrite.tex` are unchanged.
- Discussed the author's feedback-loop paragraph in chat only. In particular,
  unbounded discounted net profit does not mean profit is monotone in every
  research increase; the uncapped result requires the stated substitution and
  research-return restrictions. No introduction, model, or simulation edits.

## Introduction: approved feedback-loop and upper-bound paragraph (2026-09-17)

- Replaced only the active feedback-loop paragraph in `01_introduction.tex`
  with the exact wording approved in the conversation (using the existing
  straight-apostrophe TeX convention).
- Retained both citations, distinguished potentially unbounded discounted
  net profit from monotonic profit gains, and stated the substitution,
  research-return, and unrestricted-efficiency qualifications.
- Preserved the author's first paragraph, neighboring paragraphs, and the
  commented comparison; no model, simulation, figure, or notation changes.

## Related literature: shorter active section and preserved prior text (2026-09-17)

- Fast-forwarded to the author's `aafbb5b` commit before editing; the completed
  introduction is untouched.
- Replaced the active review with four paragraphs focused on seven references:
  Davidson et al.; Jones--Tonetti; Romer; Hemous--Olsen; Liu--Wan;
  Aghion--Jones--Jones; and Ray--Mookherjee. The entire prior source, including
  the earlier commented comparison, is preserved below with one additional
  percent-and-space prefix per line. No bibliographic entry or citation
  elsewhere in the manuscript was removed.
- Kept the comparison between endogenous technological progress and optimized
  resource allocation explicit. Davidson's aggregate growth application fixes
  saving and sectoral shares; Jones--Tonetti's Table 9 fixes investment and
  research shares. Neither is described as imposing all technological progress.
- Distinguished physical-capital compensation from developer net profit, not
  separate household ownership groups. Romer and Hemous--Olsen are retained as
  precedents for privately financed innovation; Liu--Wan provides the direct
  AI-market-structure comparison. Stored originals and the source passages
  checked in the preceding review support these comparisons.
- Connected Aghion--Jones--Jones to production bottlenecks and Ray--Mookherjee
  to rising wages with a vanishing labor share. Own growth-regime statements
  retain the finite-bound qualification and concern the characterized regimes.
- Checked the current high/low research-productivity text: the active examples
  have initial profit reductions, not the temporary losses of older exercises.
  The new review therefore says reductions in developer net profit.
- No changes to the introduction, abstract, model, results, numerical code,
  figures, parameters, initial conditions, or notation.
- Validation: recovered the commented archive and compared it with the
  pre-edit source; it is identical apart from line-ending normalization.
  Tectonic compiled `main_rewrite.tex` successfully with no unresolved
  citations/references or overfull boxes in the final log. Visually checked
  the new review on PDF pages 4--5. The shorter section has about 410 words
  (TeX citation commands counted as single tokens).

## Direct antecedents integrated after the author's approval (2026-09-17)

- Fetched origin and verified that local `1260120` already matched the latest
  main branch before editing. Title, abstract, introduction, equations,
  simulations, figures, parameters, and initial conditions remain untouched.
- Kept Related Literature in four paragraphs. Added GATE to the feedback and
  resource-allocation comparison, Acemoglu--Restrepo (2018) to profit-driven
  innovation, and Caselli--Manning (2019) to wages and capital adjustment.
  The previously silenced full literature review is preserved verbatim.
- GATE: checked arXiv:2503.04941v2, Sections 5.1, 6.1 and 8. Its planner already
  optimizes investment and compute allocation, with adjustment costs and an
  optional research-externality wedge. Our distinction is private monopoly
  incentives and equilibrium prices, not endogenous investment in general.
- Acemoglu--Restrepo: published AER 2018, Section III, pp. 1511--1513,
  equations (22)--(26) and footnote 25. Their profit-driven research chooses
  between automation and new human tasks; our research improves AI efficiency.
  The existing conclusion already cites their 2019 reinstatement mechanism as
  a missing force. Preserved that paragraph instead of adding a duplicate.
- Zeira (1998): added a brief paragraph after the final-good zero-profit
  identity in Section 3.3. The published pp. 1094--1095, Section II and
  equations (1)--(2), support the distinction between technical availability
  and profitable adoption. Did not equate discrete technique choice to our
  continuous AI-input demand.
- Caselli--Manning (2019): added the contrast after the wage/revenue remark
  in Section 4.2, with a reference to the existing wage-growth equation.
  Checked the LSE author manuscript, benchmark assumptions and Results 1--2,
  pp. 3--6, and the discussion of rising interest rates/non-steady states,
  pp. 12--13. Their steady-state wage-level comparison at a fixed interest
  rate is not our growth-rate result with an endogenous interest rate.
- Aghion--Jones--Jones already appears in Related Literature, Section 3.3
  (weak links and the distinct elasticities), and Section 4.2 (bottlenecks).
  Ho et al. already appears in Section 3.4.1 on effective compute, with the
  scope difference between measured model training and broader research.
  Preserved those connections rather than repeating them.
- Added Zeira and Caselli--Manning to BibTeX and migrated their existing
  bibliography-tool records from additions to overrides, retaining their
  reviewed metadata without duplicate keys. Updated placement notes for
  the new connections and rebuilt the local/public bibliography browser.
- Validation: Tectonic compiled the 66-page `main_rewrite.pdf`; the final log
  contains no unresolved citations/references or overfull/underfull boxes.
  The seven bibliography tests passed, with no duplicate keys/DOIs or missing
  cited records in the rebuilt 153-record database.
- Visually checked the amended text on PDF pages 4--5, 7--8, and 17;
  citations resolve correctly and the paragraphs render legibly.

## Paragraph-level focus of the short review (2026-09-17)

- Fast-forwarded to the author's `1a09951` introduction edits before the
  review and preserved them. Changed only active Related Literature prose.
- Paragraph 1: resource allocation to AI research (fixed shares, planner
  optimization, and decentralized private decisions). Preserved unchanged.
- Paragraph 2: monopoly rents as a research incentive and an income source
  distinct from physical-capital remuneration. Shortened the comparison and
  removed the detour into automation versus new-task research. Retained every
  citation and the contrast with Liu--Wan. The model and conclusion continue
  to explain the absence of new human tasks.
- Paragraph 3: production bottlenecks and the conditions for temporary versus
  permanent growth gains. Preserved unchanged.
- Paragraph 4: faster real-wage growth can coexist with a declining labor
  share. Removed the closing detour into AI revenues, compute costs, and
  transitional profits; those topics remain in paragraph 2 and the numerical
  results, respectively. No paragraph needed deletion or division.
- The previously silenced review remains untouched. No title, abstract,
  equation, result, simulation, figure, parameter, or initial-condition edits.

## Wage-growth and labor-share antecedents (2026-09-17)

- Fast-forwarded to the author's `8400dd2` (Rel Lit edits) before editing.
  Preserved that commit's first paragraph, the other active paragraphs, and
  the commented archive. Replaced only the wage/labor-share paragraph with
  the paragraph approved in the conversation.
- Acemoglu--Restrepo (2019): productivity, displacement, and new human tasks.
  The original JEP discussion, pp. 5 and 9--12, distinguishes those forces.
  Our fixed-weight CES does not create new tasks. The existing conclusion
  already cites this missing mechanism; no duplicate limitation was added.
- Autor--Kausik (2026): automation can raise wages while lowering labor's
  share. Ray--Mookherjee (2022): the share can vanish while wages rise
  indefinitely. These are precedents, not claims that the cited papers
  establish our particular growth rates or monopoly-profit decomposition.
- Caselli--Manning (2019), Robot Arithmetic: New Technology and Wages:
  reviewed all 21 pages of the public LSE accepted manuscript, including
  its appendix. Benchmark assumptions and Results 1--2 (pp. 3--6) concern
  wage comparisons between steady states. Page 9 distinguishes wages from
  the labor share. The Rising Interest Rate discussion (p. 12) explicitly
  leaves open wage dynamics when technology raises both growth and the
  interest rate. Replaced the ambiguous "once capital adjusts" comparison
  with this more direct connection. Our private-RSI model characterizes
  that combination under its own assumptions; no equivalence is claimed.
  Source: https://eprints.lse.ac.uk/87371/1/Manning__robot-arithmatic--author-merged.pdf
  Local copy: tmp/caselli_manning_review_2026-09-17/caselli_manning_2019_accepted.pdf
- Section 4.2: refined the existing paragraph after the wage/AI-revenue
  remark, linking these antecedents to the limiting-return and wage-growth
  equations by label. Section 6.2: added one sentence citing Autor--Kausik
  and Ray--Mookherjee beside the Figure 6 distributional results. Section
  6.3 does not repeat the same citation for the lower-productivity exercise.
- Validation: Tectonic compiled the 66-page PDF without unresolved citations,
  unresolved references, or overfull/underfull boxes. Visually checked the
  amended paragraphs on pages 5, 17, and 28; equation references resolve to
  (40)--(41). No simulations were rerun or numerical claims changed.

## Jones (2026): approved bottleneck and transition connections (2026-09-17)

- Verified that `3cedf75` matched origin/main before editing. Added only the
  two passages approved after the complete rereading of Jones's published
  JEP article (20 PDF pages, printed pp. 3--22, including the references).
- Related Literature, paragraph 3: added Jones's explanation of modest
  aggregate growth despite rapid AI progress, after the Aghion--Jones--Jones
  bottleneck antecedent. All other paragraphs and the archived review remain
  unchanged.
- Section 6.3, Figure 7 discussion: replaced the sentence citing only
  Jones--Tonetti with the approved comparison to Jones (pp. 11--12), retaining
  Jones--Tonetti as the underlying source. Explicitly distinguished private
  RSI investment and capital accumulation from progressive automation of
  additional tasks. Similar trajectories do not imply identical mechanisms.
- Preserved the existing Jones citations on effective compute and in the
  conclusions. Did not reactivate Section 6.4, alter the bibliography, or
  change equations, numerical claims, simulations, figures, or parameters.

## Acemoglu--Restrepo (2018): labor-share result and omitted new tasks (2026-09-19)

- The author rejected placement in the conclusion and in the developer's
  research problem, approving a connection beside the falling-labor-share
  results instead. Updated Section 4.2 after the wages/AI-revenue remark.
- Read the complete published AER article (pp. 1488--1542, including its
  printed appendix). Proposition 5 and pp. 1509--1510 establish that, in the
  relevant interior BGP comparison, greater automation can raise wages
  while lowering labor's share. This is an antecedent, not their proof of
  our limiting growth rates or a vanishing labor share.
- Added the omitted adjustment margin: new human tasks can counteract
  automation. Section III, especially Proposition 6 and pp. 1515--1518,
  establishes conditions for stable interior growth with a positive labor
  share; it also permits full automation under other conditions. The text
  therefore says "can" and leaves the effect of adding task creation to
  our model open.
- Preserved the author's latest conclusion correction in e13bec7. No
  title, abstract, Related Literature, model equation, simulation, figure,
  parameter, or initial-condition changes.
- Source: https://ide.mit.edu/sites/default/files/publications/aer.20160696.pdf
  Local copy: tmp/related_literature_audit_2026-09-13/acemoglurestrepo2018.pdf
- Validation: Tectonic compiled the 65-page PDF without unresolved citations,
  unresolved references, or overfull/underfull boxes. Visually checked the
  two updated paragraphs on page 17; the citation resolves correctly and
  the surrounding Figure 3 remains legible. No simulations were rerun.

### Author's follow-up: retain only the result citation (2026-09-19)

- Removed the proposition-specific citation locator and the entire added
  paragraph about omitted new human tasks, as explicitly requested.
- Retained Acemoglu--Restrepo (2018) beside the rising-wage/falling-labor-share
  antecedents in Section 4.2. No other manuscript passage was changed.
- The next paper, Hemous--Olsen (2022), is being reviewed for a separate
  proposal; no new placement is approved or implemented yet.
- Validation: rebuilt the 65-page PDF, checked the absence of unresolved
  references/citations and overfull/underfull boxes, and visually inspected
  page 17. The removed paragraph is absent from the extracted PDF text.

## Hemous--Olsen (2022): reviewed, placement pending approval (2026-09-19)

- Read the complete published article, all 45 PDF pages (printed pp. 179--223),
  including its printed Appendix A and references, from the existing local
  copy. Verified the published version against the author's UZH download.
  Did not read or claim verification of the separate online Appendix B.
- Source: https://www.econ.uzh.ch/dam/jcr:45914647-fc05-419a-94b8-210ac86dc9aa/The%20Rise%20of%20the%20Machines.pdf
  Local source: tmp/related_literature_audit_2026-09-13/hemousolsen2022.pdf
- Relevant result: pp. 188--190, equations (10)--(11), and pp. 195--196.
  Low-skill wages grow at a positive rate below output growth in the
  characterized interior long-run regime; high-skill wages grow with output.
  Equation (9), p. 186, and equation (A6), p. 210, explain why aggregate
  labor income retains a positive share. The quantitative extension on
  pp. 198 and 202--203 preserves the distinction across skill groups.
- Proposed one-sentence comparison in the existing Section 4.2 antecedents
  paragraph, after Ray--Mookherjee: low-skill wage growth lags output, but
  high-skill wages preserve a positive aggregate labor share. This recognizes
  the wage-growth-gap antecedent without attributing a vanishing total labor
  share, private RSI, or our specific elasticity formula to their model.
- No manuscript citation to this paper has been added outside Related
  Literature. Await the author's approval before implementation.

### Approved placement implemented (2026-09-19)

- Added exactly the approved sentence in Section 4.2, after Ray--Mookherjee
  and before Caselli--Manning. The citation names the paper without a
  proposition-specific locator. Preserved the surrounding text.
- No changes to Related Literature, the title, abstract, model, simulations,
  or the author's deletion of the separate Acemoglu--Restrepo limitation.
- Validation: Tectonic rebuilt the 65-page PDF successfully. No unresolved
  references/citations or overfull/underfull boxes were reported. Inspected
  page 17 visually and verified the added sentence in extracted PDF text.

## Liu--Wan (2026): full reading, proposal pending approval (2026-09-19)

- Read all 107 PDF pages of the existing complete paper, including references
  and Appendices A--D. The PDF is dated May 16, 2026, also confirmed by its
  creation metadata. SSRN lists May 10 as Date Written and May 22 as posting
  date; these are not treated as a different verified revision.
- Title: AGI, ANI and Economic Growth. Authors: Taoxiong Liu and Ruidong Wan.
  Source: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6776339
  Local source: tmp/related_literature_audit_2026-09-13/liuwan2026.pdf
- Proposed connection: pricing by a supplier of general-purpose AI affects
  both its own innovation incentives and the research costs of specialized
  AI developers. The manuscript's integrated developer abstracts from this
  conflict between distinct AI firms.
- Evidence: printed pp. 30--32, equations (39)--(44), especially Section 4.3.3;
  Section 3.3, pp. 24--25, equations (28)--(30), and Appendix C.1, pp. 53--54,
  examine vertical integration. Visually inspected printed pp. 31--32 to
  check the formulas and stated incentive conflict.
- Limits: their research technology distinguishes general-purpose models,
  specialized applications and data. It is not our one-state RSI technology.
  The proposed citation does not assert that our integrated monopoly is
  efficient or that their growth comparisons carry over to our model.
- Placement proposed: the final paragraph of Section 3.4.3, beginning
  'That being said, monopoly is an institutional assumption', in
  sections_rewrite/03_model.tex. Add two sentences explaining the omitted
  conflict. No Liu--Wan manuscript edit has been made; await approval.

### Approved Liu--Wan placement implemented (2026-09-19)

- Added exactly the two approved sentences to the final paragraph of
  Section 3.4.3, in sections_rewrite/03_model.tex. The existing paragraph
  and references remain intact. The citation names the paper without
  a proposition-specific locator.
- No changes to Related Literature, the title, abstract, model equations,
  simulations, or silenced material.
- Validation: Tectonic rebuilt the 65-page PDF successfully. No unresolved
  references/citations or overfull/underfull boxes were reported. Verified
  the added text on page 11 and visually inspected pages 11 and 12.

## Erdil et al. (2025): full reading, proposal pending approval (2026-09-19)

- Read all 85 pages of the existing PDF, including references and Appendices
  A--D. Verified its version, arXiv:2503.04941v2 (March 12, 2025), against
  the arXiv version history. No newer arXiv revision was listed.
- Title: GATE: An Integrated Assessment Model for AI Automation.
  Authors: Ege Erdil, Andrei Potlogea, Tamay Besiroglu, Edu Roldan, Anson Ho,
  Jaime Sevilla, Matthew Barnett, Matej Vrzla, and Robert Sandler.
  Source: https://arxiv.org/pdf/2503.04941v2
  Local source: tmp/related_literature_audit_2026-09-13/erdiletal2025gate.pdf
- Direct connection: Section 3.5, pp. 19--20, equations (5)--(6), multiplies
  hardware and software efficiency growth by factors that vanish at their
  respective upper bounds. Visually inspected these pages and equations.
  Proposed placement: Section 3.4.2, immediately after the sentence explaining
  psi(B), in sections_rewrite/03_model.tex.
- Proposed addition: 'A related approach appears in \\citet{erdiletal2025gate},
  who also reduce research productivity as hardware and software efficiency
  approach their respective upper bounds.'
- Limits: their factors depend on normalized logarithmic distances to the
  bounds, unlike our linear factor 1-B/Bbar. Their two separate efficiency
  indices are not identical to our single AI-efficiency state. Their
  specification is a modeling antecedent, not empirical validation of a
  finite AI-efficiency bound or a proof of our equilibrium results.
- Appendix D, pp. 75--76, explicitly describes considerable uncertainty
  about the maximum algorithmic efficiency. Do not treat this paper as
  identifying our upper-bound parameter.
- No Erdil manuscript edit has been made. Previously silenced references
  remain silenced. Await approval of this one connection.
