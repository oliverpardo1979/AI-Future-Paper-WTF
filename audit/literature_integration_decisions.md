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
