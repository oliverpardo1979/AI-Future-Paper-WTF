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
