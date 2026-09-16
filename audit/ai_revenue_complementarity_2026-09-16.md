# AI revenue, complementarity, and measurement: attribution check

Base: `1c62563` (author's 6.3 edits). Scope: additions to Related literature
and the conclusion; no changes to model equations, simulations, figures,
section 6.2, or the author's revised section 6.3.

The four new academic PDFs were downloaded from public author/university
sources. They and extracted page text are cached in the ignored directory
`tmp/related_literature_audit_2026-09-13/`. The earlier Acemoglu--Restrepo PDF
was reused. This is a targeted attribution review of the passages below, not
an independent verification of every proof, regression, or table in these papers.
The September 13 full-literature audit remains a historical record.

## Sources and supported claims

- `bresnahantrajtenberg1995`: published Journal of Econometrics article,
  pp. 83--88 (PDF pp. 1--6). General-purpose technologies enable downstream
  applications and complementary innovation. Their analysis is partial
  equilibrium; it does not establish a growing aggregate AI-revenue/GDP ratio.
  [Author PDF](https://tbres.su.domains/wp-content/uploads/2023/11/Bresnahan-and-Trajtenberg-1995-General-purpose-technologies-%E2%80%98Engines-of-growth.pdf).
  SHA-256: `97264530e0c2779c44e36805e6b7a7ad999832da9957c184c008fc8e05e5000c`.
  Confidence: High for the stated attribution.
- `bresnahanbrynjolfssonhitt2002`: published QJE article, pp. 339--342 and
  370--371 (PDF pp. 1--4 and 32--33). Firm-level evidence supports a cluster
  of complementarities involving IT, organization, products/services, and
  skills. This is not an estimate of an aggregate AI--labor CES elasticity.
  [Stanford PDF](https://cpi.stanford.edu/_media/pdf/Reference%20Media/Bresnahan_Brynjolfsson_Hitt_2002_Organizations.pdf).
  SHA-256: `fe8ff4aa25d758bb0bc89d54ff650c396d75f88fbbb14f1a554dd02e68d3b805`.
  Confidence: High for the stated attribution.
- `brynjolfssonliraymond2025`: published QJE article, pp. 889--893 (PDF
  pp. 1--5). The assistant improves issues resolved per hour by 15% on
  average; agents retain responsibility for conversations. The paper
  explicitly does not identify aggregate employment or wage effects and
  cannot establish the aggregate AI-sector revenue share. The manuscript
  uses the qualitative result without adding a numerical calibration target.
  [Author PDF](https://danielle.li/assets/docs/GenerativeAIatWork.pdf).
  SHA-256: `b59b45b650ad75640735e4a44bc58dae8aa1133f7886c820fb4e815f08a4df9f`.
  Confidence: High for the stated attribution.
- `ngaipissarides2007`: published AER article, pp. 429--431 (PDF pp. 1--3),
  especially equation (10). With CES preferences and fixed weights,
  relative expenditure responds to relative prices with exponent one
  minus the substitution elasticity. The paper concerns substitution
  across final goods, not AI versus labor. The manuscript explicitly calls
  this an analogy, not an empirical estimate or identical production model.
  [Author PDF](https://personal.lse.ac.uk/ngai/np.pdf).
  SHA-256: `b0242825343abdd79a3baa8109d5a36e17c12821c90e01ff62f2adfd43ad5b71`.
  Confidence: High for the stated attribution.
- `acemoglurestrepo2019` (already cited): published JEP article, pp. 8--9
  (cached PDF pp. 6--7), and p. 14 (PDF p. 12). Changing the allocation of
  tasks can reduce labor's share independently of whether the elasticity
  is above one. This is task displacement, not evidence that automation
  involves no replacement of human tasks. Their task-derived CES weights
  change with automation; ours are fixed.
  [Published article](https://www.aeaweb.org/articles?id=10.1257/jep.33.2.3).
  Confidence: High for the stated attribution.
- `bea2018grossoutput`: BEA FAQ 1197, published February 12, 2018,
  accessed September 16, 2026. Read the complete definition and kayak
  example. Gross output includes intermediate inputs; value added excludes
  them and includes employee compensation. Industry revenue/GDP is neither
  a value-added share nor the owners' income share. No claim is made about
  the national-accounts classification of every expenditure in our model.
  [Official source](https://www.bea.gov/help/faq/1197).
  Confidence: High for the accounting distinction.

## Limits of the inference added to the paper

Diffusion and new applications can expand demand for technology that helps
workers. The possibility of AI revenue growing faster than GDP through those
channels is our economic inference, not an aggregate finding in the cited
microeconomic studies. Neither a helpful AI application nor a growing AI
industry by itself identifies a CES elasticity below or above one.

For the fixed-technology comparison, the two-input CES first-order conditions
give spending on AI relative to labor proportional to their effective-price
ratio raised to `1 - sigma`, with fixed weights. Thus a falling effective
AI/labor price ratio reduces that spending ratio for `sigma < 1`. This is a
relative-expenditure statement, not an unconditional prediction for industry
revenue divided by economy-wide GDP. Growing quantities, growing revenue,
and a growing revenue/GDP ratio are different claims.

The new conclusion concerns actual suppliers that employ labor, not a new
human-research input in the benchmark model. No parameter or mechanism has
been added to the simulations.

## Build and preservation checks

- Tectonic compiled `main_rewrite.tex` successfully, including BibTeX and
  cross-reference reruns. The final log has no undefined references,
  undefined citations, or overfull boxes; BibTeX reports no errors.
- Visually inspected PDF pages 6--8 (literature), 37 (conclusion), and
  67 and 70 (new bibliography entries). Text and citations render correctly.
- The compiled PDF has 70 pages. Source diffs are confined to the literature,
  conclusion, bibliography, and this audit note; the author's section 6.3,
  other simulations, parameters, initial conditions, and figures are unchanged.
