# Jones (2026) and top-five literature review

Review date: 16 September 2026. This is a candidate-selection report, not a
claim that every relevant article or proof has been exhaustively audited.

## What changed

- Added 24 candidate records to `literature/manual_entries.json`: 17 articles in
  the conventional top five and seven other references identified through Jones.
- Each record separates the source's method and result from a possible use in
  this paper and the limits of that comparison. Search `Jones-top5-2026` in the
  literature browser; `priority-high` identifies the more direct connections.
- Downloaded 23 public full texts and read the passages identified in
  `selected_review.json`. This was a targeted reading of introductions and
  mechanism/measurement passages, not a full proof or replication audit.
- Braxton and Taska (2023) remains a clearly marked abstract-only candidate:
  the official AEA PDF endpoint was inaccessible. Do not insert a substantive
  attribution to it before obtaining and checking the body of the article.
- Corrected Ide and Talamas's page range in the tool to 3762-3800, as recorded
  in publisher-deposited Crossref metadata. No change to the manuscript BibTeX.
- In the manuscript, implemented only the already approved introduction
  paragraph citing Davidson et al. The title, abstract, Related Literature,
  model and simulations were not changed by this survey.

## Coverage and selection

The starting source was Charles I. Jones, *AI and Our Economic Future*,
Journal of Economic Perspectives 40(3), Summer 2026, pp. 3-22,
DOI 10.1257/jep.20261505. The user-supplied 20-page PDF, including its reference
list, was read. JEP is not one of the conventional top five.

The journal screen covers American Economic Review, Quarterly Journal of
Economics, Journal of Political Economy, Econometrica and Review of Economic
Studies. Crossref queries retrieved 2,488 journal-article metadata records:

| Journal | Records returned |
| --- | ---: |
| AER | 597 |
| QJE | 246 |
| JPE | 624 |
| Econometrica | 490 |
| ReStud | 531 |

These are records screened by title, not 2,488 articles read. The queries,
publication dates and title matches are saved in `crossref_screen.json`.
They were supplemented with publisher and author-site searches. Publication
status and final issue details were checked separately from the downloaded
working-paper versions. Online and print dates can differ: notably Guerreiro,
Rebelo and Teles appeared online in 2021 but in the January 2022 issue and is
therefore included. Danieli is a published 2026 advance-access article; Freund
and Mann is a working paper with an AER revise-and-resubmit, not an AER article.

The screen targets AI, automation, task allocation, endogenous innovation,
growth, wages and transition mechanisms. It is not a census of every use of
machine learning in econometrics or every paper on innovation. Pure estimation
methods, algorithmic pricing without a direct connection to this model, and
unrelated sectoral innovations were not added merely because their titles
matched. Broad knowledge and policy papers were retained at medium priority
only when they motivate a concrete extension or limitation.

Three particularly relevant top-five works were already in the tool and were
not duplicated: Moll, Rachel and Restrepo (Econometrica 2022); Brynjolfsson, Li
and Raymond (QJE 2025); Ide and Talamas (JPE 2025). Several other Jones references
were also already present, including Davidson et al., Jones and Tonetti,
Acemoglu, Aghion-Jones-Jones, Restrepo, and Korinek-Suh.

## Which connections to consider first

1. **Jones and Liu, AER 2024:** improvements in already automated inputs are
   different from automating more tasks. This is essential when comparing
   substitution results across models. Their task margin is absent from ours.
2. **Hemous, Olsen, Zanella and Dechezlepretre, JPE 2025:** evidence that labor
   costs induce automation innovation. A strong motivation for endogenous
   technological investment, without claiming their estimates identify RSI.
3. **Autor, Chin, Salomons and Seegmiller, QJE 2024:** the emergence of new human
   work. This is an important omitted margin when interpreting a vanishing
   labor share, not a result already represented by our model.
4. **Acemoglu and Restrepo, QJE 2026:** automation can dissipate worker rents.
   Labor income and bargaining-related rents must not be confused with
   developer monopoly profit.
5. **Beraja and Zorzi, ReStud 2025:** slow reallocation and borrowing constraints
   can change the welfare ranking of transition speeds. Our representative
   household cannot establish their policy conclusion.
6. **De Ridder, AER 2024:** scalable intangibles affect market power, entry and
   innovation. Useful for discussing what permanent monopoly excludes.
7. **Kalyani et al., QJE 2025:** invention and diffusion need not coincide.
   Useful for transition interpretation, not a direct calibration of chi.
8. **Autor and Thompson, JEEA 2025; Althoff-Reichardt and Freund-Mann, working
   papers 2026:** occupations bundle tasks and workers differ in skills. These
   refine the representative-worker limitation rather than replicate our
   aggregate substitution mechanism.

Caselli and Manning (AER: Insights 2019), Jones (AEJ: Macro 2011), and Ho et al.
(2024) provide focused antecedents on wages with capital adjustment, weak links,
and algorithmic efficiency respectively. Neither AER: Insights nor AEJ: Macro
is counted as AER in the top-five screen.

## Implications for positioning this paper

Jones explicitly discusses rising wages alongside a vanishing labor share
(printed p. 14) and delayed growth acceleration due to weak links (pp. 8-12).
These possibilities alone should not be described as new. The next
paragraph-by-paragraph review should focus on what our decentralized RSI model
adds through endogenous developer investment, its equilibrium characterization,
and its joint growth-distribution-transition results. This is a proposed
positioning, not a certified priority claim over the entire literature.

Theoretical similarity does not establish equivalence. In particular:

- Elasticities across tasks and between aggregate AI and labor are different
  objects unless a mapping is demonstrated.
- Functional income shares do not identify personal inequality, welfare or
  political power without ownership, heterogeneity and institutional structure.
- Evidence on AI assistance, patent innovation or algorithmic benchmarks does
  not establish autonomous RSI, an upper bound, or a numerical value of chi.
- Slow adoption, labor reallocation, and endogenous research investment can all
  delay observed gains but are distinct mechanisms.

## Evidence and reproducibility

- `selected_review.json`: all 24 records, candidate priorities, original passage
  locations, version notes and limits.
- `source_manifest.json`: download attempts, URLs, timestamps, page counts and
  SHA256 hashes. The status `downloaded_not_yet_audited` describes the automatic
  downloader only; manual reading status is in `selected_review.json` and the
  literature records.
- `download_urls.json`: public source locations used by the downloader.
- `../../scripts/survey_top5_ai_2026.py`: reproducible metadata screen.
- `../../scripts/cache_jones_top5_sources.py`: public-original-text cache helper.

Downloaded PDFs and extracted text remain under ignored `tmp/`; they are not
republished with the site. Where a prepublication text was read, its date is
explicitly recorded. Specific estimates or propositions should be rechecked in
the final published version before being inserted in the manuscript.

After additions, rebuild and test with:

```text
python scripts/build_literature_database.py --publish
python -m unittest discover -s scripts -p test_literature_database.py
```
