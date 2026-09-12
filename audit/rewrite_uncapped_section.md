# Separate uncapped section -- 2026-09-12

## Scope and preservation

The user requested a separate section studying all three substitution regimes
without an AI-efficiency frontier. Origin/main was fetched before editing;
HEAD and origin/main both pointed to b563d12 and the working tree was clean.

Section 4 now covers only finite-frontier equilibria, retaining its unified
proposition, table, figure, and the user's opening paragraph. New Section 5,
sections_rewrite/05_uncapped_equilibria.tex, introduces the uncapped law once
and states how Definition 1 applies with psi=1 and psi'=0.
The old law/equilibrium labels are preserved even where a label's historical
name contains "unit". Section 6 contains the unchanged quantitative results;
Section 7 concludes.

The title, abstract, and argumentative introduction are unchanged. Only the
introduction's roadmap is updated from six to seven sections. The conclusion
adds the uncapped-complementarity production bound without calling it an
existence result. The model, parameter meanings, timing, simulation code,
calibration, numerical data, figures, references, and companion source/PDF
are unchanged. No new transition simulations were run.

## Mathematical content and scope

### Complementarity (Section 5.1)

- Proposition 2 proves a CES production bound independent of B. The aggregate
  resource constraint then bounds K/(AL) and Y/(AL). The upper long-run
  time-average growth rate of Y/N cannot exceed gamma.
- B cannot diverge at a finite date: the integrated resource constraint bounds
  total M, and Holder's inequality bounds the integral of M^eta for 0<eta<1.
  This is not a regularity theorem for every instantaneous control.
- The appendix also bounds the developer's fixed-horizon supremum at given
  K,A,L,r independently of B. Neither this nor the feasibility result proves
  that an infinite-horizon equilibrium exists.
- Conditional result 1 assumes an equilibrium with B tending to infinity,
  positive finite limits of K/(AL) and C/(AL), and finite limiting growth
  rates of C,Y,w. It derives g_(Y/N)=g_w=gamma, r=rho+gamma, and
  s_X=(1-sigma)/(1-alpha*sigma).
- The limiting labor share is sigma(1-alpha)^2/(1-alpha*sigma), not 1-alpha.
  AI revenue retains a positive share because the monopolist approaches its
  revenue-maximizing finite X/(AL) when marginal cost goes to zero.
- Additional assumptions that g_B, g_M, and M/U have positive finite limits
  imply g_B=eta(n+gamma), g_M=(1-eta)(n+gamma), and U/Y,M/Y tending to zero.
  The appendix checks the costate-implied M/U ratio, both TVC implications,
  and finite objective integrals. These are conditional consistency checks,
  not a construction or a global-optimality proof.

### Unit elasticity (Section 5.2)

The existing BGP theorem is moved intact and automatically becomes
Proposition 3. All its substantive parameter restrictions, growth formulas,
allocation identities, initial-stock quantifiers, and global-optimality/TVC
proof are retained. The local off-BGP result remains in Appendix C and becomes
Proposition 5. The separate companion remains in place and is cited here.

### Substitution (Section 5.3)

The existing uncapped discussion is relocated. Divergence of R(Bbar) as
Bbar grows is not turned into a nonexistence or finite-time-singularity proof.
For eta>alpha the existing profitable-deviation proof excludes finite-valued
developer optima (now Proposition 4 in Appendix A). For eta<alpha the
fixed-horizon value bound does not establish infinite-horizon existence.
The eta=alpha boundary is explicitly distinguished and remains unresolved in
general. No unverified transition is inserted into the quantitative section.

## Proof and reference organization

New proofs are included through appendix_uncapped_complements_proofs.tex
inside the existing single Appendix A proof section, without new subsections.
Headings are "Proof of Proposition ..." and "Proof of Conditional result ...",
with automatic labels. New and unit-elastic proof links have explicit anchors.
The unit-elastic verification now points to Definition 1 and the uncapped law,
rather than to the subsection where the general specification no longer sits.

## Reproducible checks

Run from the repository root with the existing Python dependencies:

    python -m unittest discover -s tests -p test_rewrite_uncapped_complements.py -v

The full targeted run comprises 44 tests in these modules:

- test_companion
- test_rewrite_proposition_structure
- test_rewrite_uncapped_unit
- test_rewrite_uncapped_complements
- test_positive_ai_branch
- test_rewrite_finite_frontier

The new tests check the CES and capital bounds, limiting income accounting,
static monopoly convergence at sigma=0.5,0.9,0.99, conditional research/costate
identities, TVC decay rates, and explicit source scope. Additional algebra
grids cover sigma=0.1,0.25, eta up to 0.8, and several production weights.
Numerical tolerances concern floating-point arithmetic only. No test is a
substitute for an equilibrium-existence proof.

All 44 tests passed. Tectonic 0.16.9 compiled the 68-page main_rewrite.pdf,
with no undefined/multiply-defined references or overfull/underfull boxes.
The environmental Fontconfig warning did not affect compilation.
The new section occupies pages 18--21: complementarity 18--19, unit elasticity
19--20, and substitution 21. The new complementarity proofs start on pages
53 and 54; the unit-elastic BGP proof starts on page 55.

The PDF is visually checked after compilation, including the new section,
proofs, section transitions, roadmap, and affected conclusion/appendix pages.
No hard section page breaks were introduced. The stable public PDF path is
unchanged. Local compilation and remote Pages deployment are verified separately.

## Next mathematical step

Construct an uncapped complementary-input equilibrium from an appropriate
nonempty set of initial states, then verify global developer and household
optimality and both TVCs. The conditional growth/share formulas provide a
candidate asymptotic regime; they must not be promoted to existence without
that argument. General uncapped substitution with eta<=alpha is also open.
