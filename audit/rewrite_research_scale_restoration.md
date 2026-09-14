# Restore the low-eta case in Proposition 5

September 14, 2026. The author requested restoring eta<alpha to motivate
Section 6. The result and proof were already present: before commit 5273da8,
both cases were stated in the appendix; the low-eta argument remained in
the current proof after only the high-eta case was moved into Section 5.3.

Proposition `prop:rewrite-research-scale` now states two cases, with unchanged
automatic numbering and proof link. For sigma>1, uncapped B, a fixed finite
horizon, positive continuous K/A/L and integrable r, eta<alpha implies a finite
supremum and coercivity in total research expenditure. Eta>alpha permits
unbounded discounted net profit and excludes the existing finite-valued
developer equilibrium candidate by the preserved continuation argument.

The underlying calculation is unchanged. If S is total research expenditure,
the bound is C0+C1*S**p-Dmin*S with
p=eta*(1-alpha)/(alpha*(1-eta)). Exactly,
p-1=(eta-alpha)/(alpha*(1-eta)). For eta=0.20 and alpha=0.33, p=0.5075757576.
Thus the linear cost dominates the upper bound on benefits when eta<alpha.
The high-eta conclusion still uses a constructed profitable deviation,
not an inference from a diverging upper bound.

The design and shared parameter tables reference part (i). The text explicitly
distinguishes motivating eta<alpha from estimating eta=0.20. It does not assert
attainment in the uncapped low-eta case or infinite-horizon equilibrium
existence. The condition is not necessary for finite-horizon bounded value
with finite Bbar. The equality case and commented research remain intact.

Verification: four new algebra/source/calibration tests, three focused existing
proposition/preservation tests, and five simulation-selection tests pass (12
total). The source-length check also passes without relaxing its threshold.
No simulation, calibration script, figure, numerical input or numerical output
changed. Tectonic compiles the 73-page PDF without unresolved references or
layout warnings. The proposition remains number 5, on page 23; its proof
starts on page 51. Title, abstract and introduction are unchanged.
