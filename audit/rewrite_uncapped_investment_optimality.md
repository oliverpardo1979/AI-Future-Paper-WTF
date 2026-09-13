# Optimal investment and the uncapped nonexistence question

2026-09-12. Starting commit: d962063. This note records the extension of
Proposition 5 prompted by the argument that high returns should prevent
vanishing investment shares. It changes neither the model nor its calibration.
No transition simulation is computed or presented as an equilibrium.

## What is proved

For sigma > 1, no finite upper bound on B, and the paper's primitives
(in particular 0 < eta < 1, rho > n, gamma > 0 and n >= 0):

1. The exclusion of persistent positive lower bounds on both
   gross capital-investment and research shares remains part (i).
2. Part (ii) now excludes an equilibrium in which BOTH investment shares
   converge to finite limits. These limits may be zero; the capital-investment
   limit is not assumed nonnegative.
3. Whenever Y/K -> infinity along a proposed global equilibrium,
   limsup[(dot K+delta K)/Y] >= alpha. Thus B -> infinity implies this
   limsup bound via Section 4's dated return lower bound.

Neither B -> infinity, s_X -> 1, convergence of growth rates, nor convergence
of share derivatives is assumed for part (ii). Both a bounded and an
unbounded increasing B are considered and excluded under convergent shares.
Convergent expenditure shares are not the same as balanced growth.

This is still NOT general nonexistence for eta <= alpha. Any remaining
equilibrium would have shares that do not both converge and cannot both stay
bounded below by positive constants. The result does not establish the
existence of such an equilibrium. It does not establish that every solution
of the dated equations reaches a finite-time singularity.

## The argument

Proof variables: i=(dot K+delta K)/Y, m=M/Y, u=U/Y, c=C/Y,
z=Y/K and k=K/(AL). These are ratios of existing variables, not new saving
rules or a change in the state/control definitions.
The full proof is Part (ii), Steps 5-9, in
sections_rewrite/appendix_uncapped_substitutes_proof.tex.

### Capital investment when returns diverge

The household Euler equation and capital accumulation give exactly

\[
 \frac{d}{dt}\log(C/K)=(\alpha-i)z-(\rho-n).
\]

If z -> infinity and eventually i <= epsilon < alpha, then C/K grows without
bound. Feasibility gives C/K <= (1-i)z, including negative gross investment.
Writing v=C/K therefore gives the Riccati inequality

\[
 \dot v\geq v\left[
 \frac{\alpha-\epsilon}{1-\epsilon}v-(\rho-n)\right].
\]

This contradicts a globally finite v. The implication is a limsup bound,
not a liminf bound; recurrent low-investment episodes are not excluded.

### Static monotonicity in the bounded-efficiency case

The monopoly conditions imply a reduced output-capital ratio z(k,B).
It is strictly decreasing in k and increasing in B. At fixed B it tends to
infinity as k -> 0 and to [R(B)+delta]/alpha as k -> infinity.
These signs are proved from monopoly pricing, not imported from a
competitive reduced production function. The key identity is

\[
 {\cal D}(s)-\alpha s[1-e(s)]
 =-\frac{1-s}{\sigma^2}
 \{(\sigma-2)(1-\alpha\sigma)s-(\sigma-1)\}>0.
\]

If B has a finite limit and i converges to a nonpositive limit, normalized
capital tends to zero. Then z -> infinity, contradicting the capital
limsup bound. A positive limiting i bounds k away from zero and makes it
converge to a positive value or grow without bound. This follows from
the signs of the scalar normalized-capital field, including the boundary
where its stationary value lies at infinity. Thus u has a positive limit
and Y grows without bound.

### Research incentives and transversality

The uncapped FOC gives M=eta qB g_B. The costate equation then gives

\[
 \frac{d(qB)}{dt}=r qB-U+\frac{1-\eta}{\eta}M.
\]

Suppose m -> 0 and u -> u_infinity > 0, with i convergent.
If c -> 0, then i -> 1-u_infinity > alpha. But for h=qB/K and
T(t)=integral_0^t z_s ds,

\[
 \frac{dh}{dT}=(\alpha-i)h+\frac{1-\eta}{\eta}m-u
\]

is eventually bounded above by a negative constant. Since T -> infinity,
h must cross zero, contradicting q>0. Therefore c has a positive limit.
The developer TVC and the household Euler equation then give

\[
 \frac{q_tB_t}{C_t}=
 \int_t^\infty e^{-(\rho-n)(s-t)}
 \frac{u_s-\frac{1-\eta}{\eta}m_s}{c_s}\,ds.
\]

This is a shadow-stock identity, not an identification of qB with the
developer's firm value. Dominated convergence is justified by the positive
limiting c and rho > n. Hence

\[
 \frac{qB}{Y}\longrightarrow\frac{u_\infty}{\rho-n}>0,
 \qquad g_B=\frac{m}{\eta(qB/Y)}\longrightarrow0.
\]

But the same FOC requires exactly

\[
 m=\left[\chi\eta(qB/Y)\right]^{1/(1-\eta)}
        \frac{Y^{\eta/(1-\eta)}}{B}.
\]

Vanishing m therefore requires Y^(eta/(1-eta))/B -> 0.

### Both alternatives for B fail under convergent shares

- B bounded: Y -> infinity and integral M^eta < infinity rule out a
  positive limiting research share. With m -> 0, the shadow-stock identity
  contradicts Y -> infinity and bounded B.
- B unbounded: Section 4 gives z -> infinity, so limiting i >= alpha.
  Capital grows faster than any fixed exponential; K/(AL) -> infinity
  implies s_X -> 1 and u -> (1-alpha)^2. Part (i) excludes positive limiting
  m. With m -> 0, the developer identity gives g_B -> 0, so B is
  subexponential. Yet Y grows faster than any fixed exponential, contradicting
  Y^(eta/(1-eta))/B -> 0.

No derivative of a converging ratio is assumed to converge. The PV step
explicitly uses the developer TVC; the household Euler equation eliminates
the endogenous discount rate from that integral.

## Consistency with the other regimes

- At sigma=1 the power-law return lower bound does not apply. The preserved
  uncapped BGP has bounded Y/K and positive convergent shares. It independently
  verifies the shadow-stock PV identity.
- With a finite upper bound the costate equation includes
  -dot B psi'(B)/psi(B). The shadow-stock equation therefore has an additional
  term. The AI-dominated capped limit has qB/Y -> u/r, rather than the
  uncapped vanishing-research implication u/(rho-n). Copying either formula
  to the other research law would be an error.
- The proof uses the paper's positively growing effective labor when
  handling bounded B. It adds no new population or technology restriction
  and does not claim to cover gamma=n=delta=0.

## Scope and verification

The open question is now nonconvergent investment shares. A proof of general
nonexistence must exclude that class using optimality/transversality or an
explosion condition permitting sufficiently intermittent investment. Naming
such paths irregular is not a reason to exclude them.
The title, abstract, introduction, simulations and calibrated parameters
are unchanged.

All 70 tests in the nine-module targeted suite passed on 2026-09-12,
including eight new tests in tests/test_rewrite_investment_optimality.py.
The new checks cover exact identities, static monotonicity near sigma=1
and at high sigma, the shadow-value transformation, capped/uncapped
costate differences, and the PV identity against the preserved unit-elastic
equilibrium. They supplement, not replace, the written proof.
