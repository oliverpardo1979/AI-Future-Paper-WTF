# Uncapped benchmark in the main text -- 2026-09-12

## Scope and preservation

The user approved bringing the uncapped unit-elastic benchmark into Section 4
while retaining the separate companion paper. Before editing, origin/main was
fetched and user commit `3ff718b` (the shortened opening of Section 4) was
fast-forwarded. That opening remains unchanged.

No edits were made to the companion source or its tracked PDF, the original
title/abstract/introduction/model, numerical code, data, or figures. No new
simulations were run. The companion remains a separate active manuscript.

## Organization

- Section 4.3, pages 18--19: the uncapped research law, the unit-elastic output
  elasticities, the two BGP growth restrictions, and Proposition 2 with growth,
  wages, interest, and labor share. Initial stocks are constructed with the BGP;
  no existence claim from arbitrary stocks is introduced.
- Section 4.4, pages 19--20: the existing open gross-substitutes problem,
  preserving the distinctions between nonexistence, unbounded value, and a
  finite-time singularity. The research-scale result is now Proposition 3.
- Appendix A: the BGP and local-trajectory proofs remain in the existing single
  proof section. Their mathematics is unchanged; one cross-reference now points
  to the equilibrium specification in Section 4.3. The proof of Proposition 2
  begins on page 52. A conditional spacing guard keeps the Proofs heading with
  its first lemma, without inserting unconditional section page breaks.
- Appendix C, pages 59--62: detailed rate/ratio derivations, the role of each
  sufficient restriction, and the existing local-trajectory Proposition 4.
  The BGP proposition is not duplicated; moved equation labels are preserved.
- Related literature and conclusions: explicitly scope the wage-growth/labor-share
  equivalence to characterized finite-frontier equilibria. The conclusion notes
  the uncapped unit-elastic exception and narrows the outstanding existence agenda.

The companion citation remains in Section 4.3. No new theorem, parameter
convention, initial-condition rule, or numerical trajectory is introduced.

## Verification

Thirty tests passed across `test_companion`,
`test_rewrite_proposition_structure`, `test_rewrite_uncapped_unit`, and
`test_positive_ai_branch`. Organization tests now check the four subsections,
the unique main-text BGP statement, definitions before use, both TVCs, global
optimality, and the appendix-only local theorem. Existing analytical tests still
check dated equations, the Jacobian, and the reference BGP.

Tectonic 0.16.9 compiled the 65-page `main_rewrite.pdf`. Final logs contain no
undefined or duplicate references, overfull boxes, or underfull boxes. Poppler
rendering and visual inspection covered the affected literature, main-text,
conclusion, proof, and Appendix C pages. The compact BGP statement fits on page
18; its proof pointer follows on page 19. Proof and proposition numbers use
labels, not manually entered numbers.

`git diff --check` passed. Diff checks verified that protected manuscript and
companion files, all scripts, numerical data, and figures are unchanged from
the synchronized base. Remote publication status is checked separately from
the local PDF and mathematical checks.
