# Davidson bibliography: targeted follow-up, 16 September 2026

## Scope and result

I screened the 31 entries in the bibliography of the user-supplied
`davidsonetal2026.pdf` (printed pp. 44-46; PDF pp. 45-47). The supplied file
matches the previously cached Davidson PDF, SHA-256
`a9faa0e31ca48f3d8778d7ac053a312c39b25c1cd61d05c02ca6121ca4d01938`.

Ten works were already represented in the literature catalogue, sometimes
under a different version year. Eight candidates have been added with original
passage locations, proposed uses and limits. Thirteen entries are deferred;
deferral is not a judgment that they are unimportant.

The manuscript, bibliography used by LaTeX, figures and simulations are
unchanged. These are candidates for the agreed paragraph-by-paragraph review,
not instructions to insert every citation.

## Reading standard

This is a targeted reading of the original passages needed to assess each
connection, not an audit of every proof, estimate or version of every paper.
The catalogue gives specific page/equation references. Downloading a source is
not evidence that its claims have been verified: `source_manifest.json`
deliberately retains the downloader's `downloaded_not_yet_audited` status;
the editorial review and its limits are recorded here and in
`literature/manual_entries.json`.

| New candidate | Passages checked | Possible location, subject to approval |
|---|---|---|
| Besiroglu, Emery-Xu and Thompson (2024) | Published pp. 2-4; Section 2.2, equations (1)-(4), Proposition 1 | AI-assisted research; capital intensity versus autonomous research |
| Erdil, Besiroglu and Ho (2024) | arXiv v1 pp. 2, 5-6, 22 | RSI specification and parameter-identification cautions |
| Ekerdt and Wu | November 2024 text, pp. 1-2, 5 | Interpretation of declining research productivity; cautions around the Bloom et al. connection |
| Ngai and Samaniego (2011) | Published pp. 476-478, equations (2), (4) | Endogenous research expenditure and appropriability |
| Liu and Ma (2024) | June 2024 text, pp. 1-8, Section 2.1, equations (1)-(6) | Research allocation and an optional multisector extension |
| Zeira (1998) | Scanned published pp. 1093-1095 read visually; Section II, equations (1)-(2) | Adoption of labor-saving technology versus improvements in AI efficiency |
| Cottier et al. | arXiv v2 pp. 1-4, especially Section 2.5 | Research/training compute and measurement limitations |
| Mirhoseini et al. (2021) | Published p. 208; publisher correction/addendum history | Optional narrow example of AI-assisted chip development |

### Version and attribution cautions

- Ekerdt and Wu is listed as forthcoming by AER, DOI
  `10.1257/aer.20241592`. The full text reviewed is the November 2024 working
  paper, not an asserted final published version. The catalogue year identifies
  that text. No sample periods or estimates are mixed across versions.
- Liu and Ma's author webpage reports AER acceptance. The June 2024 author PDF
  was read through web PDF access; direct download returned 403. The local
  fallback is NBER w29607, revised January 2023, and is explicitly not the same
  version. The catalogue does not invent a final AER DOI or publication date.
- Cottier et al.'s reviewed version is v2, February 2025, with six authors.
  Model-development costs cannot be treated as an observed aggregate annual
  research-compute share of GDP.
- Nature reports a code-availability correction and a September 2024 addendum
  for Mirhoseini et al. The 2023 editorial concern was removed after review.
  The catalogue uses only the narrow chip-placement application, not disputed
  quantitative superiority claims or a claim that autonomous RSI exists.
- The explosive-growth note hosted by Chad Jones is a technical lead, not one
  of the eight ordinary research-paper additions. Its title page credits
  **ChatGPT 5.2 Pro via Chad Jones**, dated 2 January 2026. Only its provenance
  and introductory explanation were inspected; its proof was not verified.
  It must not be presented as a peer-reviewed Jones theorem or as an existence
  or nonexistence proof for this paper's decentralized equilibrium.

## Complete bibliography disposition

| Davidson entry | Disposition |
|---|---|
| Aghion, Jones and Jones (2019) | Already represented |
| Altman (2025), The Gentle Singularity | Defer: statement/blog, not a research result |
| Besiroglu, Emery-Xu and Thompson (2024) | Added candidate |
| Bloom et al. (2020) | Already represented |
| Cottier et al. (2024) | Added candidate; v2 read |
| Ekerdt and Wu | Added candidate; version/status distinguished |
| Epoch AI (2026), Trends | Defer: data resource; consult for a specific empirical question |
| Erdil et al. (2025), GATE | Already represented |
| Erdil, Besiroglu and Ho (2024) | Added candidate |
| Goldie and Mirhoseini (2024), AlphaChip | Defer blog; original chip-placement paper added instead |
| Good (1966) | Already represented under the catalogue's 1965 version; do not duplicate |
| Hanson (2000) | Defer historical forecasting connection |
| Ho and Whitfill (2025) | Defer software-intelligence-explosion blog |
| Ho et al. (2024), algorithmic progress | Already represented |
| Benjamin Jones (2025), AI and R&D | Already represented |
| Charles Jones (1995) | Already represented |
| Explosive-growth note hosted by Charles Jones (2026) | Cached technical lead; AI authorship disclosed; proof not audited |
| Jones and Tonetti (2025) | Already represented by updated 2026 version |
| Korinek and Vipra (2025) | Already represented |
| Krugman (1998), Two Cheers for Formalism | Defer methodological essay |
| Liu and Ma (2024) | Added candidate |
| Mirhoseini et al. (2021) | Added candidate with editorial-history caution |
| Nesov (2025) | Defer LessWrong contribution |
| Ngai and Samaniego (2011) | Added candidate |
| OpenAI (2025), livestream | Defer announcement, not an academic demonstration |
| Roodman (2020) | Defer historical growth-forecasting comparison |
| Sandberg and Manheim (2021) | Defer physical/value upper-limit discussion |
| Trammell and Korinek (2025) | Already represented under an earlier version key |
| Whitfill, Snodin and Becker (2025) | Defer forecast-horizon connection |
| Yudkowsky (2013) | Defer conceptual intelligence-explosion discussion |
| Zeira (1998) | Added candidate |

## Reproduction

Public originals are cached outside tracked files by:

```text
python scripts/cache_davidson_references.py
python scripts/build_literature_database.py --publish
python -m unittest discover -s scripts -p test_literature_database.py
```

`download_urls.json` preserves the requested sources and fallback;
`source_manifest.json` preserves retrieval information and hashes. Local PDFs
and extracts are in the ignored `tmp/davidson_references_2026-09-16` directory.
The public catalogue publishes links and editorial summaries, not copies of
the source PDFs.
